# -*- coding: utf-8 -*-
"""Camada persistente de saneamento manual dos clientes da WideAPP_EXTRA."""

import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook

from app import config, paths


ARQUIVO_SANEAMENTO = paths.get_internal_data_dir() / "saneamento_clientes.json"
ACOES_MANUAIS = {"quitado", "bloqueado", "ignorar", "atencao"}
ALIAS_NOMES = {
    "emanuel felix da costa filho": "EMMANUEL FELIX DA COSTA FILHO",
    "emmanuel felix da costa filho": "EMMANUEL FELIX DA COSTA FILHO",
}
PLACEHOLDER_RE = re.compile(
    r"(^[\-_.\s]*$|x{3,}\s*y{2,}|^quadra\s+[a-h]$|^total\b|^cliente$|^nome$)",
    re.IGNORECASE,
)


def normalizar(texto):
    texto = str(texto or "")
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()


def slug_busca(texto):
    return re.sub(r"[^a-z0-9]+", " ", normalizar(texto).lower()).strip()


def nome_canonico(nome):
    slug = slug_busca(nome)
    for alias, canonico in ALIAS_NOMES.items():
        if alias in slug:
            return canonico
    return normalizar(nome).upper()


def lote_canonico(registro):
    chave = str(registro.get("chave_lote_canonica") or "").strip().upper()
    if chave and chave not in ("-", "NONE"):
        return chave
    quadra = str(registro.get("quadra") or "").strip().upper()
    lote = str(registro.get("lote") or "").strip().upper()
    if re.fullmatch(r"[A-H]\d{1,3}[A-Z]?", lote):
        return lote
    if quadra and lote and lote not in ("-", "OCORRER", "SER", "DE", "S"):
        return f"{quadra}{lote}".replace(" ", "")
    return lote if lote and lote != "-" else ""


def chave_saneamento(registro):
    nome = nome_canonico(registro.get("cliente") or registro.get("nome") or "")
    lote = lote_canonico(registro)
    return f"{slug_busca(nome)}|{lote}"


def _linha_para_registro(ws, row):
    headers = [str(ws.cell(1, c).value or "").strip() for c in range(1, ws.max_column + 1)]
    data = {}
    for c, header in enumerate(headers, 1):
        if header:
            data[header] = ws.cell(row, c).value
    return {
        "cliente": data.get("cliente") or data.get("Cliente") or data.get("nome") or "",
        "lote": data.get("lote") or data.get("Lote") or "",
        "quadra": data.get("quadra") or data.get("Quadra") or "",
        "chave_lote_canonica": data.get("chave_lote_canonica") or data.get("chave") or "",
        "contrato_resumo": data.get("contrato_resumo") or "",
        "status": data.get("status") or "",
    }


def _acao_por_cor(ws, row):
    cores = []
    for col in range(1, min(ws.max_column, 12) + 1):
        fg = ws.cell(row, col).fill.fgColor
        if fg.type == "rgb" and fg.rgb:
            cores.append(str(fg.rgb).upper())
        elif fg.type == "indexed":
            try:
                cores.append(f"INDEXED:{int(fg.indexed)}")
            except Exception:
                pass
    if "FF0070C0" in cores:
        return "quitado"
    if "INDEXED:2" in cores:
        return "bloqueado"
    if "INDEXED:5" in cores:
        return "atencao"
    return ""


def encontrar_planilha_marcada():
    candidatos = [
        paths.get_app_root() / "MARCADOS remover BANCO_DADOS_WIDEAPP_EXTRA - Copia.xlsx",
        config.APP_DIR / "MARCADOS remover BANCO_DADOS_WIDEAPP_EXTRA - Copia.xlsx",
        config.APP_DIR.parent / "MARCADOS remover BANCO_DADOS_WIDEAPP_EXTRA - Copia.xlsx",
    ]
    for path in candidatos:
        if path.exists():
            return path
    return None


def carregar_saneamento():
    if not ARQUIVO_SANEAMENTO.exists():
        return {"gerado_em": "", "decisoes": {}, "resumo": {}}
    with open(ARQUIVO_SANEAMENTO, "r", encoding="utf-8") as f:
        payload = json.load(f)
    payload.setdefault("decisoes", {})
    payload.setdefault("resumo", {})
    return payload


def salvar_saneamento(payload):
    ARQUIVO_SANEAMENTO.parent.mkdir(parents=True, exist_ok=True)
    with open(ARQUIVO_SANEAMENTO, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def importar_planilha_marcada():
    payload = carregar_saneamento()
    decisoes = payload.setdefault("decisoes", {})
    planilha = encontrar_planilha_marcada()
    if not planilha:
        payload["resumo"] = {"planilha_marcada": "nao_encontrada", "decisoes": len(decisoes)}
        salvar_saneamento(payload)
        return payload

    wb = load_workbook(planilha, data_only=True)
    agora = datetime.now().isoformat(timespec="seconds")
    importadas = {"quitado": 0, "bloqueado": 0, "atencao": 0}
    for ws in wb.worksheets:
        for row in range(2, ws.max_row + 1):
            acao = _acao_por_cor(ws, row)
            if not acao:
                continue
            registro = _linha_para_registro(ws, row)
            nome = nome_canonico(registro.get("cliente"))
            chave = chave_saneamento(registro)
            if not slug_busca(nome):
                continue
            decisoes[chave] = {
                "chave": chave,
                "cliente_canonico": nome,
                "lote_canonico": lote_canonico(registro),
                "acao": acao,
                "origem": "planilha_marcada",
                "arquivo_origem": str(planilha),
                "aba_origem": ws.title,
                "linha_origem": row,
                "atualizado_em": agora,
                "observacao": f"Classificacao manual por cor: {acao}",
            }
            importadas[acao] += 1

    payload["gerado_em"] = agora
    payload["resumo"] = {
        "planilha_marcada": str(planilha),
        "decisoes": len(decisoes),
        "importadas": importadas,
    }
    salvar_saneamento(payload)
    return payload


def _decisao_para_registro(registro, decisoes):
    chave = chave_saneamento(registro)
    if chave in decisoes:
        return decisoes[chave]
    slug_nome = slug_busca(nome_canonico(registro.get("cliente")))
    candidatos = [d for d in decisoes.values() if str(d.get("chave", "")).startswith(slug_nome + "|")]
    if len(candidatos) == 1:
        return candidatos[0]
    return None


def _acao_automatica(registro):
    nome = slug_busca(registro.get("cliente"))
    if PLACEHOLDER_RE.search(nome):
        return "ignorar", "placeholder_ou_divisor_estrutural"
    contrato = slug_busca(registro.get("contrato_resumo") or registro.get("contrato_modalidade"))
    parcelas = slug_busca(registro.get("parcelas_resumo"))
    if "a vista" in contrato or "quitado" in contrato or "quitado" in parcelas:
        return "quitado", "contrato_quitado_ou_a_vista"
    situacao = slug_busca(registro.get("situacao_final"))
    rotulo = slug_busca(registro.get("status_atraso_rotulo"))
    if "bloqueado" in situacao and ("sem pagamento recente" in rotulo or int_safe(registro.get("status_atraso_qtd")) >= 6):
        return "bloqueado", "bloqueio_operacional_sem_pagamento_recente"
    return "", ""


def int_safe(valor):
    try:
        return int(float(str(valor).replace(",", ".")))
    except Exception:
        return 0


def aplicar_saneamento(registros):
    payload = importar_planilha_marcada()
    decisoes = payload.get("decisoes", {})
    saneados = []
    resumo = {"ativos": 0, "quitados": 0, "bloqueados_removidos": 0, "ignorados": 0, "atencao": 0}
    vistos_ativos = set()

    for registro in registros:
        item = dict(registro or {})
        item["cliente_canonico"] = nome_canonico(item.get("cliente"))
        item["chave_saneamento"] = chave_saneamento(item)
        decisao = _decisao_para_registro(item, decisoes)
        acao = ""
        origem = ""
        observacao = ""
        if decisao:
            acao = decisao.get("acao") or ""
            origem = decisao.get("origem") or "planilha_marcada"
            observacao = decisao.get("observacao") or ""
        else:
            acao, origem = _acao_automatica(item)
            observacao = origem

        if acao not in ACOES_MANUAIS:
            acao = "ativo"

        item["saneamento_acao"] = acao
        item["saneamento_origem"] = origem
        item["saneamento_observacao"] = observacao
        item["quitado_manual"] = acao == "quitado" and origem == "planilha_marcada"
        item["bloqueado_removido_manual"] = acao in ("bloqueado", "ignorar") and origem == "planilha_marcada"
        item["atencao_manual"] = acao == "atencao"
        item["ignorado_manual"] = acao == "ignorar"

        if acao == "quitado":
            item["saneamento_categoria"] = "quitados"
            resumo["quitados"] += 1
        elif acao in ("bloqueado", "ignorar"):
            item["saneamento_categoria"] = "bloqueados_removidos"
            resumo["bloqueados_removidos"] += 1
            if acao == "ignorar":
                resumo["ignorados"] += 1
        else:
            item["saneamento_categoria"] = "ativos"
            if acao == "atencao":
                resumo["atencao"] += 1
            chave = item.get("chave_saneamento")
            if chave in vistos_ativos:
                item["saneamento_categoria"] = "bloqueados_removidos"
                item["saneamento_acao"] = "ignorar"
                item["saneamento_origem"] = "deduplicacao_ativa"
                item["saneamento_observacao"] = "Duplicidade obvia da lista ativa"
                resumo["bloqueados_removidos"] += 1
                resumo["ignorados"] += 1
            else:
                vistos_ativos.add(chave)
                resumo["ativos"] += 1
        saneados.append(item)

    payload["ultimo_resumo_aplicado"] = resumo
    salvar_saneamento(payload)
    return saneados, resumo


def separar_por_categoria(registros):
    grupos = {"ativos": [], "quitados": [], "bloqueados_removidos": [], "atencao": []}
    for item in registros:
        categoria = item.get("saneamento_categoria") or "ativos"
        if categoria not in grupos:
            categoria = "ativos"
        grupos[categoria].append(item)
        if item.get("saneamento_acao") == "atencao":
            grupos["atencao"].append(item)
    return grupos
