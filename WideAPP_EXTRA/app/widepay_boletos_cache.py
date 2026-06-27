# -*- coding: utf-8 -*-
"""Cache global de boletos/carnes coletados do WidePay."""

import json
import re
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path

from openpyxl import Workbook

from app import config


QUADRA_LETRAS = "ABCDEFGH"


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFD", str(texto or ""))
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()


def slug_busca(texto):
    return re.sub(r"[^a-z0-9]+", " ", normalizar_texto(texto).lower()).strip()


def normalizar_lote_quadra(lote="", quadra="", referencia="", pasta_local=""):
    """Converte variacoes como G14, 14/G e Quadra G Lote 14 para G14."""
    partes = " ".join(str(v or "") for v in (lote, quadra, referencia, Path(str(pasta_local or "")).name))
    texto = normalizar_texto(partes).upper()
    texto_compacto = re.sub(r"[^A-Z0-9]+", "", texto)

    candidatos = []
    q = re.search(r"\bQUADRA\s*([A-H])\b", texto)
    l = re.search(r"\bLOTE\s*0*(\d{1,3}[A-Z]?)\b", texto)
    if q and l:
        candidatos.append((q.group(1), l.group(1)))

    for match in re.finditer(r"\b([A-H])\s*[-/]?\s*0*(\d{1,3}[A-Z]?)\b", texto):
        candidatos.append((match.group(1), match.group(2)))

    for match in re.finditer(r"\b0*(\d{1,3}[A-Z]?)\s*[/ -]\s*([A-H])\b", texto):
        candidatos.append((match.group(2), match.group(1)))

    compact_match = re.search(r"([A-H])0*(\d{1,3}[A-Z]?)", texto_compacto)
    if compact_match:
        candidatos.append((compact_match.group(1), compact_match.group(2)))

    quadra_limpa = normalizar_texto(quadra).upper()
    lote_limpo = normalizar_texto(lote).upper()
    if quadra_limpa in QUADRA_LETRAS:
        numero = re.search(r"0*(\d{1,3}[A-Z]?)", lote_limpo)
        if numero:
            candidatos.insert(0, (quadra_limpa, numero.group(1)))

    for quadra_can, lote_can in candidatos:
        numero = re.match(r"0*(\d+)([A-Z]?)$", lote_can)
        if not numero:
            continue
        numero_sem_zero = str(int(numero.group(1)))
        sufixo = numero.group(2) or ""
        return f"{quadra_can}{numero_sem_zero}{sufixo}"

    return ""


def chave_lote_canonica(registro):
    return registro.get("chave_lote_canonica") or normalizar_lote_quadra(
        registro.get("lote") or registro.get("lote_original"),
        registro.get("quadra"),
        registro.get("referencia") or registro.get("descricao"),
        registro.get("pasta_local"),
    )


def _decimal(valor):
    if valor in (None, ""):
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)
    bruto = str(valor).replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(bruto)
    except ValueError:
        return 0.0


def _registro_base(item, origem, cliente_fallback="", coletado_em="", pagina_origem=""):
    referencia = item.get("referencia") or item.get("descricao") or ""
    lote_original = item.get("lote") or item.get("lote_original") or ""
    quadra = item.get("quadra") or ""
    chave = normalizar_lote_quadra(lote_original, quadra, referencia, item.get("pasta_local"))
    cliente_original = item.get("cliente") or item.get("cliente_original_widepay") or cliente_fallback
    return {
        "cliente_original_widepay": cliente_original,
        "cliente_normalizado": slug_busca(cliente_original),
        "lote_original": lote_original or chave,
        "lote_canonico": chave,
        "chave_lote_canonica": chave,
        "quadra": quadra or (chave[:1] if chave else ""),
        "referencia": referencia,
        "forma": item.get("forma") or "",
        "origem": origem,
        "status": item.get("status") or "",
        "vencimento": item.get("vencimento") or item.get("proximo_vencimento") or "",
        "data_pagamento": item.get("pagamento") or item.get("data_pagamento") or "",
        "valor_original": _decimal(item.get("valor_original", item.get("valor_parcela", item.get("valor")))),
        "valor_recebido": _decimal(item.get("valor_recebido", item.get("total_recebido"))),
        "id_boleto": item.get("id") or item.get("carne") or item.get("id_boleto") or "",
        "pagina_origem": pagina_origem,
        "coletado_em": coletado_em,
        "fonte": "carne" if origem.lower().startswith("carne") else "cobranca",
    }


def registros_de_resultado_bloco(resultado_bloco, coletado_em=None):
    coletado_em = coletado_em or datetime.now().isoformat(timespec="seconds")
    registros = []
    for cliente, dados in (resultado_bloco or {}).items():
        for item in dados.get("carnes") or []:
            registros.append(_registro_base(item, "Carne", cliente, coletado_em))
        for item in dados.get("cobrancas") or []:
            registros.append(_registro_base(item, "Cobranca", cliente, coletado_em))
    return deduplicar_boletos(registros)


def chave_boleto(registro):
    return "|".join(
        str(registro.get(campo) or "").strip().lower()
        for campo in (
            "fonte",
            "id_boleto",
            "cliente_normalizado",
            "lote_canonico",
            "referencia",
            "vencimento",
            "valor_original",
            "valor_recebido",
            "status",
        )
    )


def deduplicar_boletos(registros):
    unicos = {}
    ordem = []
    for registro in registros:
        item = dict(registro)
        item["lote_canonico"] = item.get("lote_canonico") or chave_lote_canonica(item)
        item["chave_lote_canonica"] = item["lote_canonico"]
        chave = chave_boleto(item)
        if chave not in unicos:
            ordem.append(chave)
        unicos[chave] = item
    return [unicos[chave] for chave in ordem]


def salvar_cache(registros, metadados=None):
    config.ensure_dirs()
    registros = deduplicar_boletos(registros)
    metadados = dict(metadados or {})
    metadados.setdefault("fim_coleta", datetime.now().isoformat(timespec="seconds"))
    metadados.setdefault("ultima_atualizacao", metadados["fim_coleta"])
    metadados.setdefault("total_registros", len(registros))
    metadados.setdefault("total_carnes", sum(1 for r in registros if r.get("fonte") == "carne"))
    metadados.setdefault("total_cobrancas", sum(1 for r in registros if r.get("fonte") == "cobranca"))
    metadados.setdefault("total_clientes_reconhecidos", len({r.get("cliente_normalizado") for r in registros if r.get("cliente_normalizado")}))
    payload = {"metadados": metadados, "registros": registros}
    config.WIDEPAY_BOLETOS_CACHE_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    salvar_xlsx(registros, metadados)
    return payload


def mesclar_cache(registros_novos, metadados=None):
    atual = carregar_cache()
    registros = list(atual.get("registros") or []) + list(registros_novos or [])
    meta = dict(atual.get("metadados") or {})
    meta.update(metadados or {})
    meta["ultima_atualizacao"] = datetime.now().isoformat(timespec="seconds")
    return salvar_cache(registros, meta)


def salvar_xlsx(registros, metadados=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "Boletos WidePay"
    headers = [
        "cliente_original_widepay",
        "cliente_normalizado",
        "lote_original",
        "lote_canonico",
        "quadra",
        "referencia",
        "forma",
        "origem",
        "status",
        "vencimento",
        "data_pagamento",
        "valor_original",
        "valor_recebido",
        "id_boleto",
        "pagina_origem",
        "coletado_em",
        "fonte",
    ]
    ws.append(headers)
    for item in registros:
        ws.append([item.get(h, "") for h in headers])
    meta_ws = wb.create_sheet("Metadados")
    meta_ws.append(["campo", "valor"])
    for key, value in (metadados or {}).items():
        meta_ws.append([key, value])
    for sheet in wb.worksheets:
        for col in sheet.columns:
            width = min(max(len(str(cell.value or "")) for cell in col) + 2, 60)
            sheet.column_dimensions[col[0].column_letter].width = width
    wb.save(config.WIDEPAY_BOLETOS_CACHE_XLSX)


def carregar_cache():
    if not config.WIDEPAY_BOLETOS_CACHE_JSON.exists():
        return {"metadados": {}, "registros": []}
    with open(config.WIDEPAY_BOLETOS_CACHE_JSON, "r", encoding="utf-8") as f:
        payload = json.load(f)
    payload.setdefault("metadados", {})
    payload.setdefault("registros", [])
    return payload


def cache_recente(minutos=30):
    payload = carregar_cache()
    atualizado = payload.get("metadados", {}).get("ultima_atualizacao")
    if not atualizado:
        return False
    try:
        dt = datetime.fromisoformat(str(atualizado))
    except ValueError:
        return False
    return datetime.now() - dt <= timedelta(minutes=minutos)


def filtrar_por_cliente_lote(cliente="", lote="", quadra="", pasta_local=""):
    payload = carregar_cache()
    cliente_slug = slug_busca(cliente)
    lote_can = normalizar_lote_quadra(lote, quadra, "", pasta_local)
    matches = []
    for item in payload.get("registros", []):
        nome_ok = not cliente_slug or cliente_slug in item.get("cliente_normalizado", "") or item.get("cliente_normalizado", "") in cliente_slug
        lote_item = item.get("lote_canonico") or chave_lote_canonica(item)
        lote_ok = not lote_can or lote_item == lote_can
        if nome_ok and lote_ok:
            matches.append(item)
    return matches


def montar_raw_cliente(cliente="", lote="", quadra="", pasta_local=""):
    boletos = filtrar_por_cliente_lote(cliente, lote, quadra, pasta_local)
    carnes = []
    cobrancas = []
    for item in boletos:
        if item.get("fonte") == "carne":
            carnes.append({
                "carne": item.get("id_boleto"),
                "referencia": item.get("referencia"),
                "valor_parcela": item.get("valor_original"),
                "parcelas_geradas": 0,
                "parcelas_pagas": 0,
                "parcelas_restantes": 0,
                "total_recebido": item.get("valor_recebido"),
                "total_pendente": 0,
                "proximo_vencimento": item.get("vencimento"),
                "ultimo_vencimento": item.get("data_pagamento") or item.get("vencimento"),
                "status": item.get("status"),
            })
        else:
            cobrancas.append({
                "id": item.get("id_boleto"),
                "forma": item.get("forma"),
                "cliente": item.get("cliente_original_widepay"),
                "descricao": item.get("referencia"),
                "valor_original": item.get("valor_original"),
                "valor_recebido": item.get("valor_recebido"),
                "vencimento": item.get("vencimento"),
                "pagamento": item.get("data_pagamento"),
                "status": item.get("status"),
                "pertence_a_carne": "carne" in normalizar_texto(item.get("referencia")).lower(),
                "avulsa": "carne" not in normalizar_texto(item.get("referencia")).lower(),
            })
    if not carnes and not cobrancas:
        return None
    return {
        "cliente": cliente,
        "status_conexao": "CACHE_WIDEPAY_GLOBAL",
        "carnes": carnes,
        "cobrancas": cobrancas,
        "metadados_cache_global": carregar_cache().get("metadados", {}),
    }
