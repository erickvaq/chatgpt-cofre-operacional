# -*- coding: utf-8 -*-
"""Execucao do pipeline financeiro completo a partir da interface."""

import re
import subprocess
from datetime import datetime
from pathlib import Path

from app import config
from app import drive_uploader
from app import gerador_xlsx_consolidado
from app.indexador_clientes import slug_busca


TIPOS = {
    ".xlsx": "xlsx",
    ".pdf": "pdf",
    ".html": "html",
    ".md": "md",
    ".json": "json",
    ".log": "log",
}


def slug(texto):
    base = slug_busca(texto).upper().replace(" ", "_")
    return re.sub(r"_+", "_", base).strip("_") or "CLIENTE"


def arquivos_relevantes_desde(inicio):
    encontrados = []
    for base in (config.OUTPUT_DIR, config.TEMP_DIR, config.LOG_DIR):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in TIPOS:
                continue
            try:
                if path.stat().st_mtime >= inicio:
                    encontrados.append(path)
            except OSError:
                continue
    return encontrados


def classificar_arquivos(paths):
    result = {"xlsx": [], "pdf": [], "html": [], "md": [], "json": [], "log": []}
    for path in paths:
        tipo = TIPOS.get(path.suffix.lower())
        if tipo:
            result[tipo].append(path)
    for lista in result.values():
        lista.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    return result


def executar_cliente(registro, log_callback=None):
    cliente = registro.get("cliente", "").strip()
    lote    = registro.get("lote", "").strip()
    if registro.get("contrato") != "Encontrado":
        raise RuntimeError(f"Contrato nao confirmado para {cliente} lote {lote}")
    if not cliente:
        raise RuntimeError("Cliente vazio")

    config.ensure_dirs()
    inicio   = datetime.now().timestamp()
    log_path = config.LOG_DIR / f"pipeline_{slug(cliente)}_{slug(lote)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    args     = [str(config.VENV_PYTHON), str(config.EXECUTOR), "--cliente", cliente]
    if lote and lote != "-":
        args += ["--lote", lote]

    def log(msg):
        if log_callback:
            log_callback(msg)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    log("EXECUCAO_PIPELINE: " + " ".join(args))
    proc = subprocess.Popen(
        args,
        cwd=str(config.ROOT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    with open(log_path, "a", encoding="utf-8") as f:
        for line in proc.stdout or []:
            f.write(line)
            if log_callback:
                log_callback(line.rstrip())
    code = proc.wait()
    log(f"CODIGO_SAIDA: {code}")
    if code != 0:
        raise RuntimeError(f"Pipeline falhou para {cliente} lote {lote}; veja {log_path}")

    arquivos    = arquivos_relevantes_desde(inicio)
    arquivos.append(log_path)
    classificados = classificar_arquivos(arquivos)
    obrigatorios  = ("xlsx", "pdf", "html", "md", "json", "log")
    faltando = [tipo for tipo in obrigatorios if not classificados.get(tipo)]
    if faltando:
        raise RuntimeError(
            f"Pipeline sem artefatos obrigatorios para {cliente} lote {lote}: "
            f"{', '.join(faltando)}. Veja {log_path}"
        )
    return {
        "cliente": cliente,
        "lote": lote,
        "log": log_path,
        "arquivos": classificados,
        "todos_arquivos": sorted(set(arquivos), key=lambda p: str(p)),
    }


def executar_lote(registros, grupo="SELECIONADOS", log_callback=None):
    """Processa N clientes selecionados.

    Quando ha mais de um cliente confirmado usa --clientes CSV num unico
    subprocesso (abre o Chrome uma unica vez). Quando ha so um, usa --cliente
    para manter retrocompatibilidade.
    """
    confirmados = [r for r in registros if r.get("contrato") == "Encontrado"]
    ignorados   = [r for r in registros if r.get("contrato") != "Encontrado"]
    if not confirmados:
        raise RuntimeError("Nenhum cliente/lote com contrato confirmado para executar")

    def log(msg):
        if log_callback:
            log_callback(msg)

    total = len(confirmados)
    log(f"LOTE: {total} cliente(s) confirmado(s) para processar.")

    resultados     = []
    arquivos_upload = []

    if total == 1:
        # Caminho simples: um unico cliente via --cliente
        log(f"[1/1] Processando {confirmados[0].get('cliente')}...")
        res = executar_cliente(confirmados[0], log_callback=log_callback)
        resultados.append(res)
        for path in res["todos_arquivos"]:
            arquivos_upload.append({
                "cliente": res["cliente"],
                "lote":    res["lote"],
                "arquivo": path.name,
                "caminho_local": str(path),
            })
    else:
        # Multiplos clientes: passa --clientes CSV num unico subprocesso
        # para aproveitar a mesma sessao CDP/Chrome ja aberta.
        nomes_csv = ",".join(r.get("cliente", "").strip() for r in confirmados)
        inicio    = datetime.now().timestamp()
        log_path  = config.LOG_DIR / f"pipeline_LOTE_{grupo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        args      = [str(config.VENV_PYTHON), str(config.EXECUTOR), "--clientes", nomes_csv]

        log(f"EXECUCAO_LOTE: {' '.join(args)}")
        proc = subprocess.Popen(
            args,
            cwd=str(config.ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        with open(log_path, "a", encoding="utf-8") as f:
            for i, line in enumerate(proc.stdout or []):
                f.write(line)
                stripped = line.rstrip()
                # Detectar inicio de auditoria individual para log de progresso
                if "AUDITANDO CLIENTE:" in stripped:
                    nome_atual = stripped.split("AUDITANDO CLIENTE:")[-1].strip().strip("=").strip()
                    idx = next(
                        (j + 1 for j, r in enumerate(confirmados)
                         if nome_atual.lower() in r.get("cliente", "").lower()),
                        "?"
                    )
                    log(f"[{idx}/{total}] {nome_atual}")
                elif stripped:
                    log(stripped)

        code = proc.wait()
        log(f"CODIGO_SAIDA_LOTE: {code}")
        if code != 0:
            raise RuntimeError(f"Pipeline em lote falhou; veja {log_path}")

        # Coletar artefatos gerados desde o inicio
        arquivos_todos = arquivos_relevantes_desde(inicio)
        arquivos_todos.append(log_path)
        classificados  = classificar_arquivos(arquivos_todos)

        # Montar resultados por cliente (melhor esforco via nome no caminho)
        for registro in confirmados:
            cliente = registro.get("cliente", "").strip()
            lote    = registro.get("lote", "").strip()
            slug_c  = slug(cliente)
            arqs_cliente = [p for p in arquivos_todos if slug_c in p.stem.upper()]
            class_c = classificar_arquivos(arqs_cliente) if arqs_cliente else classificados
            resultados.append({
                "cliente": cliente,
                "lote":    lote,
                "log":     log_path,
                "arquivos": class_c,
                "todos_arquivos": arqs_cliente,
            })
            for path in arqs_cliente:
                arquivos_upload.append({
                    "cliente": cliente,
                    "lote":    lote,
                    "arquivo": path.name,
                    "caminho_local": str(path),
                })

    consolidado = None
    if len(confirmados) > 1:
        consolidado = gerador_xlsx_consolidado.gerar(confirmados, grupo)
        arquivos_upload.append({
            "cliente": "CONSOLIDADO",
            "lote":    grupo,
            "arquivo": consolidado.name,
            "caminho_local": str(consolidado),
        })

    drive = drive_uploader.enviar_arquivos(arquivos_upload, grupo)
    return {
        "resultados":      resultados,
        "ignorados":       ignorados,
        "consolidado":     consolidado,
        "drive":           drive,
        "arquivos_upload": arquivos_upload,
    }
