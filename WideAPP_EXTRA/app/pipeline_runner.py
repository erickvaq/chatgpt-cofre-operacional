# -*- coding: utf-8 -*-
"""Execucao do pipeline financeiro completo a partir da interface."""

import re
import subprocess
import threading
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


class ExecucaoCanceladaError(RuntimeError):
    """Sinaliza cancelamento solicitado pelo usuario."""


_EXECUCAO_LOCK = threading.Lock()
_EXECUCAO_CANCELAR = threading.Event()
_PROCESSO_ATUAL = None


def limpar_cancelamento():
    _EXECUCAO_CANCELAR.clear()


def cancelamento_solicitado():
    return _EXECUCAO_CANCELAR.is_set()


def _definir_processo_atual(proc):
    global _PROCESSO_ATUAL
    with _EXECUCAO_LOCK:
        _PROCESSO_ATUAL = proc


def _obter_processo_atual():
    with _EXECUCAO_LOCK:
        return _PROCESSO_ATUAL


def _limpar_processo_atual(proc=None):
    global _PROCESSO_ATUAL
    with _EXECUCAO_LOCK:
        if proc is None or _PROCESSO_ATUAL is proc:
            _PROCESSO_ATUAL = None


def solicitar_cancelamento(log_callback=None):
    _EXECUCAO_CANCELAR.set()
    proc = _obter_processo_atual()
    if log_callback:
        emitir_log(log_callback, "CANCELAMENTO: solicitacao registrada.")
    if not proc or proc.poll() is not None:
        return False
    try:
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        else:
            proc.terminate()
    except Exception:
        try:
            proc.kill()
        except Exception:
            return False
    return True


def emitir_log(log_callback, msg):
    if not log_callback:
        return
    try:
        log_callback(msg)
    except UnicodeError:
        log_callback(str(msg).encode("ascii", "replace").decode("ascii"))
    except Exception:
        pass


def slug(texto):
    base = slug_busca(texto).upper().replace(" ", "_")
    return re.sub(r"_+", "_", base).strip("_") or "CLIENTE"


def tokens_cliente(texto):
    return [
        token for token in slug(texto).split("_")
        if len(token) >= 3 and token not in {"DOS", "DAS", "DE", "DA", "DO", "E"}
    ]


def arquivo_pertence_cliente(path, cliente, lote):
    texto = slug(str(path))
    lote_slug = slug(lote)
    cliente_tokens = tokens_cliente(cliente)
    if lote_slug and lote_slug != "-" and lote_slug not in texto:
        return False
    if not cliente_tokens:
        return False
    tokens_presentes = sum(1 for token in cliente_tokens if token in texto)
    if len(cliente_tokens) <= 2:
        return tokens_presentes == len(cliente_tokens)
    return tokens_presentes >= max(2, len(cliente_tokens) - 1)


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
                # Para arquivos na pasta final de relatórios gerados (OUTPUT_DIR),
                # aceitamos independente de timestamp para evitar problemas com modelos de arquivo antigos.
                if base == config.OUTPUT_DIR:
                    encontrados.append(path)
                elif path.stat().st_mtime >= (inicio - 120):
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
    if cancelamento_solicitado():
        raise ExecucaoCanceladaError("Execucao cancelada antes de iniciar novo cliente.")
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
        emitir_log(log_callback, msg)
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
    _definir_processo_atual(proc)
    with open(log_path, "a", encoding="utf-8") as f:
        for line in proc.stdout or []:
            f.write(line)
            stripped = line.rstrip()
            emitir_log(log_callback, stripped)
            if progress_callback:
                for text, percent, rem_sec in PROGRESS_STEPS:
                    if text in stripped:
                        pct = ((cliente_index - 1) + (percent / 100.0)) / total_clientes * 100.0
                        tot_rem = rem_sec + (total_clientes - cliente_index) * 25
                        progress_callback(pct, tot_rem)
    code = proc.wait()
    _limpar_processo_atual(proc)
    log(f"CODIGO_SAIDA: {code}")
    if cancelamento_solicitado():
        raise ExecucaoCanceladaError(f"Execucao cancelada pelo usuario para {cliente} lote {lote}. Veja {log_path}")
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


def executar_bloco_clientes(bloco_registros, log_callback=None, progress_callback=None, bloco_index=1, total_blocos=1, total_clientes=1):
    if cancelamento_solicitado():
        raise ExecucaoCanceladaError("Execucao cancelada antes de iniciar novo bloco.")
        
    config.ensure_dirs()
    inicio = datetime.now().timestamp()
    
    # Gerar log_path baseado no primeiro cliente do bloco para evitar caminhos muito longos
    primeiro_cli_slug = slug(bloco_registros[0].get("cliente", "bloco"))
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_path = config.LOG_DIR / f"pipeline_bloco_{primeiro_cli_slug}_{timestamp_str}.log"
    
    # Parâmetros de clientes e lotes casados
    clientes_csv = ",".join(r.get("cliente", "").strip() for r in bloco_registros)
    lotes_csv = ",".join(r.get("lote", "").strip() or "-" for r in bloco_registros)
    
    args = [str(config.VENV_PYTHON), str(config.EXECUTOR), "--clientes", clientes_csv, "--lotes", lotes_csv]

    def log(msg):
        emitir_log(log_callback, msg)
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
    _definir_processo_atual(proc)
    
    clientes_concluidos = 0
    
    with open(log_path, "a", encoding="utf-8") as f:
        for line in proc.stdout or []:
            f.write(line)
            stripped = line.rstrip()
            emitir_log(log_callback, stripped)
                
            if "AUDITORIA_CONCLUIDA" in stripped or "FALHA_AUDITORIA" in stripped:
                clientes_concluidos += 1
                
            if progress_callback:
                pct_base = ((bloco_index - 1) / total_blocos) * 100.0
                progresso_bloco = (clientes_concluidos / len(bloco_registros)) * (1.0 / total_blocos) * 100.0
                
                extra_pct = 0.0
                if clientes_concluidos == 0:
                    if "Pesquisando Carnes para" in stripped or "Extração em Bloco" in stripped:
                        extra_pct = 0.1 / total_blocos * 100.0
                    elif "Navegando para a pagina de cobrancas" in stripped:
                        extra_pct = 0.2 / total_blocos * 100.0
                        
                pct = pct_base + progresso_bloco + extra_pct
                tot_rem = max(10, (total_blocos - bloco_index) * 100 + (len(bloco_registros) - clientes_concluidos) * 35)
                progress_callback(pct, tot_rem)
                
    code = proc.wait()
    _limpar_processo_atual(proc)
    log(f"CODIGO_SAIDA: {code}")
    
    if cancelamento_solicitado():
        raise ExecucaoCanceladaError(f"Execucao cancelada pelo usuario para o bloco. Veja {log_path}")
    if code != 0:
        raise RuntimeError(f"Pipeline falhou para o bloco de clientes; veja {log_path}")

    # Coletar todos os arquivos modificados
    todos_arquivos = arquivos_relevantes_desde(inicio)
    todos_arquivos.append(log_path)
    
    # Classificar e separar arquivos por cliente
    from app.rastreabilidade import re_slug
    
    resultados_bloco = []
    for registro in bloco_registros:
        cli_nome = registro.get("cliente", "").strip()
        cli_lote = registro.get("lote", "").strip() or "-"
        
        nome_limpo = re_slug(cli_nome)
        lote_slug = re_slug(cli_lote)
        pasta_entrega_nome = f"{nome_limpo}_LOTE_{lote_slug}_FINAL"
        
        arquivos_do_cliente = []
        for path in todos_arquivos:
            if pasta_entrega_nome in str(path) or pasta_entrega_nome in path.parts:
                arquivos_do_cliente.append(path)
            elif f"WIDEPAY_{nome_limpo}.json" in path.name:
                arquivos_do_cliente.append(path)
            elif arquivo_pertence_cliente(path, cli_nome, cli_lote):
                arquivos_do_cliente.append(path)
            elif path == log_path:
                arquivos_do_cliente.append(path)
                
        classificados = classificar_arquivos(arquivos_do_cliente)
        classificados["log"] = [log_path]
        
        obrigatorios = ("xlsx", "pdf", "html", "md", "json", "log")
        faltando = [tipo for tipo in obrigatorios if not classificados.get(tipo)]
        if faltando:
            raise RuntimeError(
                f"Pipeline sem artefatos obrigatorios para {cli_nome} lote {cli_lote}: "
                f"{', '.join(faltando)}. Veja {log_path}"
            )
            
        resultados_bloco.append({
            "cliente": cli_nome,
            "lote": cli_lote,
            "log": log_path,
            "arquivos": classificados,
            "todos_arquivos": sorted(set(arquivos_do_cliente), key=lambda p: str(p)),
        })
        
    return resultados_bloco


def executar_lote(registros, grupo="SELECIONADOS", log_callback=None, progress_callback=None):
    """Processa N clientes selecionados em blocos de até 3 clientes simultaneamente."""
    limpar_cancelamento()
    confirmados = [r for r in registros if r.get("contrato") == "Encontrado"]
    ignorados   = [r for r in registros if r.get("contrato") != "Encontrado"]
    if not confirmados:
        raise RuntimeError("Nenhum cliente/lote com contrato confirmado para executar")

    def log(msg):
        emitir_log(log_callback, msg)

    total = len(confirmados)
    log(f"LOTE: {total} cliente(s) confirmado(s) para processar.")

    resultados     = []
    arquivos_upload = []

    falhas = []
    cancelado = False
    
    # Agrupar clientes em blocos de até 3
    tamanho_bloco = 3
    blocos = [confirmados[i:i + tamanho_bloco] for i in range(0, len(confirmados), tamanho_bloco)]
    total_blocos = len(blocos)
    
    if total >= 1:
        for bloco_idx, bloco in enumerate(blocos, start=1):
            if cancelamento_solicitado():
                cancelado = True
                log("CANCELAMENTO: execucao interrompida antes do proximo bloco.")
                break
                
            clientes_nomes = [r.get("cliente") for r in bloco]
            log(f"\n[{bloco_idx}/{total_blocos}] Processando bloco de clientes: {', '.join(clientes_nomes)}...")
            
            if progress_callback:
                pct_inicio = ((bloco_idx - 1) / total_blocos) * 100.0
                progress_callback(pct_inicio, (total_blocos - bloco_idx + 1) * 100)
                
            try:
                res_bloco = executar_bloco_clientes(
                    bloco,
                    log_callback=log_callback,
                    progress_callback=progress_callback,
                    bloco_index=bloco_idx,
                    total_blocos=total_blocos,
                    total_clientes=total,
                )
                for res in res_bloco:
                    resultados.append(res)
                    for path in res["todos_arquivos"]:
                        arquivos_upload.append({
                            "cliente": res["cliente"],
                            "lote":    res["lote"],
                            "arquivo": path.name,
                            "caminho_local": str(path),
                        })
            except ExecucaoCanceladaError as exc:
                cancelado = True
                log(f"CANCELAMENTO: {exc}")
                break
            except Exception as exc:
                for reg in bloco:
                    falhas.append({
                        "cliente": reg.get("cliente", ""),
                        "lote": reg.get("lote", ""),
                        "erro": str(exc),
                    })
                    log(f"ERRO_CLIENTE: {reg.get('cliente')} lote {reg.get('lote')}: {exc}")
                continue

    if cancelado and not resultados:
        limpar_cancelamento()
        return {
            "resultados": [],
            "ignorados": ignorados,
            "falhas": falhas,
            "consolidado": None,
            "drive": [],
            "arquivos_upload": [],
            "cancelado": True,
        }

    if not resultados:
        detalhe = "; ".join(f"{f['cliente']} lote {f['lote']}: {f['erro']}" for f in falhas)
        raise RuntimeError(f"Nenhum cliente foi concluido com sucesso. Falhas: {detalhe}")

    consolidado = None
    if len(resultados) > 1 and not cancelado:
        consolidado = gerador_xlsx_consolidado.gerar(confirmados, grupo)
        arquivos_upload.append({
            "cliente": "CONSOLIDADO",
            "lote":    grupo,
            "arquivo": consolidado.name,
            "caminho_local": str(consolidado),
        })

    if progress_callback and not cancelado:
        progress_callback(100.0, 0)
    drive = [] if cancelado else drive_uploader.enviar_arquivos(arquivos_upload, grupo)
    limpar_cancelamento()
    return {
        "resultados":      resultados,
        "ignorados":       ignorados,
        "falhas":          falhas,
        "consolidado":     consolidado,
        "drive":           drive,
        "arquivos_upload": arquivos_upload,
        "cancelado":       cancelado,
    }
