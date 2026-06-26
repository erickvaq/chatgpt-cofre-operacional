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


PROGRESS_STEPS = [
    ("Verificando se o WidePay requer login", 10, 22),
    ("WidePay ja esta logado", 15, 20),
    ("Pesquisando Carnes para", 30, 17),
    ("Navegando para a pagina de cobrancas", 55, 11),
    ("Pesquisando Cobranças/Boletos", 70, 7),
    ("Dados brutos extraidos", 85, 4),
    ("Status da Auditoria", 95, 2),
]


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


def executar_cliente(registro, log_callback=None, progress_callback=None, cliente_index=1, total_clientes=1):
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
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
    )
    with open(log_path, "a", encoding="utf-8") as f:
        for line in proc.stdout or []:
            f.write(line)
            stripped = line.rstrip()
            if log_callback:
                log_callback(stripped)
            if progress_callback:
                for text, percent, rem_sec in PROGRESS_STEPS:
                    if text in stripped:
                        pct = ((cliente_index - 1) + (percent / 100.0)) / total_clientes * 100.0
                        tot_rem = rem_sec + (total_clientes - cliente_index) * 25
                        progress_callback(pct, tot_rem)
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


def executar_lote(registros, grupo="SELECIONADOS", log_callback=None, progress_callback=None):
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

    falhas = []
    if total >= 1:
        for idx, registro in enumerate(confirmados, start=1):
            log(f"[{idx}/{total}] Processando {registro.get('cliente')} lote {registro.get('lote')}...")
            if progress_callback:
                pct_inicio = ((idx - 1) / total) * 100.0
                progress_callback(pct_inicio, (total - idx + 1) * 25)
            try:
                res = executar_cliente(
                    registro,
                    log_callback=log_callback,
                    progress_callback=progress_callback,
                    cliente_index=idx,
                    total_clientes=total,
                )
            except Exception as exc:
                falhas.append({
                    "cliente": registro.get("cliente", ""),
                    "lote": registro.get("lote", ""),
                    "erro": str(exc),
                })
                log(f"ERRO_CLIENTE: {registro.get('cliente')} lote {registro.get('lote')}: {exc}")
                continue
            resultados.append(res)
            if progress_callback:
                pct_fim = (idx / total) * 100.0
                progress_callback(pct_fim, (total - idx) * 25)
            for path in res["todos_arquivos"]:
                arquivos_upload.append({
                    "cliente": res["cliente"],
                    "lote":    res["lote"],
                    "arquivo": path.name,
                    "caminho_local": str(path),
                })

    if not resultados:
        detalhe = "; ".join(f"{f['cliente']} lote {f['lote']}: {f['erro']}" for f in falhas)
        raise RuntimeError(f"Nenhum cliente foi concluido com sucesso. Falhas: {detalhe}")

    consolidado = None
    if len(confirmados) > 1:
        consolidado = gerador_xlsx_consolidado.gerar(confirmados, grupo)
        arquivos_upload.append({
            "cliente": "CONSOLIDADO",
            "lote":    grupo,
            "arquivo": consolidado.name,
            "caminho_local": str(consolidado),
        })

    if progress_callback:
        progress_callback(100.0, 0)
    drive = drive_uploader.enviar_arquivos(arquivos_upload, grupo)
    return {
        "resultados":      resultados,
        "ignorados":       ignorados,
        "falhas":          falhas,
        "consolidado":     consolidado,
        "drive":           drive,
        "arquivos_upload": arquivos_upload,
    }
