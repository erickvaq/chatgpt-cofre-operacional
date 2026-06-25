# -*- coding: utf-8 -*-
"""Indexacao local de clientes/lotes para a interface dinamica."""

import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook

from app import config


LOTE_RE = re.compile(r"\b([A-H]\s*[-.]?\s*\d{1,3}[A-Z]?)\b", re.IGNORECASE)
QUADRA_RE = re.compile(r"\bquadra\s*([A-H])\b", re.IGNORECASE)
REMOVE_WORDS_RE = re.compile(
    r"\b(contrato|copia|final|corrigido|previa|carne\d*|apart\d*|agua|viva|leandro|meirelles|leo|docx|pdf|txt|html|md)\b",
    re.IGNORECASE,
)


def normalizar(texto):
    texto = texto or ""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()


def slug_busca(texto):
    return re.sub(r"[^a-z0-9]+", " ", normalizar(texto).lower()).strip()


def extrair_lote(nome):
    match = LOTE_RE.search(nome or "")
    if not match:
        return "-"
    return re.sub(r"\s+", "", match.group(1).upper().replace(".", "").replace("-", ""))


def extrair_quadra(nome, lote):
    match = QUADRA_RE.search(nome or "")
    if match:
        return match.group(1).upper()
    if lote and lote != "-":
        return lote[0].upper()
    return "-"


def limpar_nome_cliente(nome):
    sem_ext = re.sub(r"\.[a-z0-9]{2,5}$", "", nome or "", flags=re.IGNORECASE)
    sem_lote = LOTE_RE.sub(" ", sem_ext)
    sem_ruido = REMOVE_WORDS_RE.sub(" ", sem_lote)
    sem_ruido = sem_ruido.replace("_", " ").replace("-", " ")
    sem_ruido = re.sub(r"\s+", " ", sem_ruido).strip(" ._-")
    return normalizar(sem_ruido).title() if sem_ruido else normalizar(nome).title()


def detectar_contrato(pasta):
    arquivos = []
    for path in Path(pasta).glob("*"):
        if not path.is_file():
            continue
        nome = path.name.lower()
        if path.suffix.lower() not in (".docx", ".pdf", ".txt"):
            continue
        if any(skip in nome for skip in ("carne", "recibo", "wp-pdf", "boleto")):
            continue
        arquivos.append(path)
    if not arquivos:
        return "Nao encontrado", ""
    principal = sorted(arquivos, key=lambda p: p.stat().st_size if p.exists() else 0, reverse=True)[0]
    return "Encontrado", str(principal)


def iterar_pastas_cliente():
    base = config.CONTRATOS_DIR
    if not base.exists():
        return []
    candidatos = []
    for path in base.rglob("*"):
        if not path.is_dir():
            continue
        nome = path.name.strip()
        if not nome or nome.lower().startswith(("_", ".")):
            continue
        lote = extrair_lote(nome)
        contrato_status, contrato_path = detectar_contrato(path)
        if lote != "-" or contrato_status == "Encontrado":
            candidatos.append((path, lote, contrato_status, contrato_path))
    return candidatos


def indexar_clientes(validar_widepay=False, log_callback=None):
    config.ensure_dirs()
    agora = datetime.now()
    log_path = config.LOG_DIR / f"atualizacao_clientes_{agora.strftime('%Y%m%d_%H%M%S')}.log"

    def log(msg):
        if log_callback:
            log_callback(msg)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")

    log("Indexacao iniciada")
    widepay_status = "Nao validado nesta atualizacao"
    if validar_widepay:
        try:
            from app.login_navegador import garantir_navegador_conectado

            garantir_navegador_conectado()
            widepay_status = "CDP WidePay acessivel"
            log("WidePay/CDP validado")
        except Exception as exc:
            widepay_status = f"WidePay indisponivel: {exc}"
            log(widepay_status)

    registros = []
    vistos = set()
    for pasta, lote, contrato_status, contrato_path in iterar_pastas_cliente():
        cliente = limpar_nome_cliente(pasta.name)
        quadra = extrair_quadra(pasta.name, lote)
        chave = (slug_busca(cliente), lote, str(pasta).lower())
        if chave in vistos:
            continue
        vistos.add(chave)
        origem = "Contrato local"
        status = "Pendente validacao WidePay"
        if contrato_status != "Encontrado":
            status = "Sem contrato confirmado"
        registro = {
            "selecionado": False,
            "cliente": cliente,
            "lote": lote,
            "quadra": quadra,
            "status": status,
            "contrato": contrato_status,
            "contrato_arquivo": contrato_path,
            "origem": origem,
            "parcelas_pagas_identificadas": "",
            "ultima_parcela_paga": "",
            "ultimo_vencimento_pago": "",
            "valor_ultimo_pagamento": "",
            "data_atualizacao": agora.isoformat(timespec="seconds"),
            "observacoes": widepay_status,
            "divergencias": "",
            "pasta_local": str(pasta),
        }
        registros.append(registro)

    registros.sort(key=lambda r: (slug_busca(r["cliente"]), r["lote"]))
    salvar_cache(registros)
    log(f"Indexacao concluida: {len(registros)} cliente/lote")
    return {"registros": registros, "log": str(log_path), "widepay_status": widepay_status}


def salvar_cache(registros):
    config.ensure_dirs()
    payload = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "quantidade": len(registros),
        "registros": registros,
    }
    with open(config.CLIENTES_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    salvar_xlsx(registros)


def salvar_xlsx(registros):
    wb = Workbook()
    ws = wb.active
    ws.title = "Clientes indexados"
    headers = [
        "cliente",
        "lote",
        "quadra",
        "status",
        "contrato",
        "origem",
        "parcelas_pagas_identificadas",
        "ultima_parcela_paga",
        "ultimo_vencimento_pago",
        "valor_ultimo_pagamento",
        "data_atualizacao",
        "observacoes",
        "divergencias",
        "pasta_local",
    ]
    ws.append(headers)
    for item in registros:
        ws.append([item.get(h, "") for h in headers])
    for col in ws.columns:
        width = min(max(len(str(cell.value or "")) for cell in col) + 2, 60)
        ws.column_dimensions[col[0].column_letter].width = width
    wb.save(config.CLIENTES_XLSX)


def carregar_cache():
    if not config.CLIENTES_JSON.exists():
        return []
    with open(config.CLIENTES_JSON, "r", encoding="utf-8") as f:
        payload = json.load(f)
    return payload.get("registros", [])
