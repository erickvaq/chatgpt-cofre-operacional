# -*- coding: utf-8 -*-
"""Cache global de boletos/carnes coletados do WidePay."""

import json
import os
import re
import shutil
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path

from openpyxl import Workbook

from app import config
from app.versionamento_dados import criar_snapshot_versionado


QUADRA_LETRAS = "ABCDEFGH"


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFD", str(texto or ""))
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()


def slug_busca(texto):
    return re.sub(r"[^a-z0-9]+", " ", normalizar_texto(texto).lower()).strip()


def slug_identidade_nome(texto):
    """Normaliza variantes ortograficas aprovadas sem recorrer a fuzzy irrestrito."""
    aliases = {
        "sousa": "souza",
        "emanuel": "emmanuel",
    }
    identidade = " ".join(aliases.get(token, token) for token in slug_busca(texto).split())
    # Equivalencias confirmadas no proprio WidePay pelo mesmo lote/referencia.
    # Mantemos a lista explicita para nao aproximar nomes diferentes por fuzzy.
    nomes_confirmados = {
        "telma valadares dos santos": "telma valadares dos anjos carvalho",
        "telma valadares dos anjos": "telma valadares dos anjos carvalho",
        "ana carolina nery da s borgens": "ana carolina nery da s borges de barros",
        "ana carolina nery da silva borges": "ana carolina nery da s borges de barros",
        "joice carla de magalhaes gomes": "joice carla de magalhaes goncalves",
        "rodrigo monteiro": "rodrigo monteiro de melo",
        "emanuel felix da costa filho": "emmanuel felix da costa filho",
        "emmanuel felix da costa": "emmanuel felix da costa filho",
        "emanuel felix da costa": "emmanuel felix da costa filho",
    }
    return nomes_confirmados.get(identidade, identidade)


def normalizar_lote_quadra(lote="", quadra="", referencia="", pasta_local="", cliente=""):
    """Converte variacoes como G14, 14/G e Quadra G Lote 14 para G14.
    Aplica tambem regras especificas para Emmanuel (LT G3 -> G18) e Rodrigo (G1/G19).
    """
    cliente_norm = slug_busca(cliente or "")
    referencia_upper = normalizar_texto(referencia).upper()
    lote_upper = normalizar_texto(lote).upper()
    quadra_upper = normalizar_texto(quadra).upper()
    partes = " ".join(str(v or "") for v in (lote, quadra, referencia, Path(str(pasta_local or "")).name))
    texto = normalizar_texto(partes).upper()

    # 1. Regra especifica para Emmanuel: LT G3 / G3 -> G18
    if "emmanuel" in cliente_norm or "emanuel" in cliente_norm:
        if ("G3" in texto or "LT G3" in texto or "LT.G3" in texto or "LT-G3" in texto) and not ("G2" in texto and "G18" in texto):
            return "G18"

    # 2. Regra para Rodrigo: grupo G1/G19 vs F19
    if "rodrigo" in cliente_norm:
        if "F19" in texto or lote_upper == "F19":
            return "F19"
        if (
            re.search(r"\bG1\s*[-/]?\s*G?19\b", texto)
            or re.search(r"\bLT\.?\s*G?\s*1\s*/\s*19\b", texto)
            or re.search(r"\bCARNE2\s+LT\s+G1\s*G-?19\b", texto)
            or "G1/19" in texto
            or "G1G19" in texto
            or "G1G-19" in texto
            or ("G1" in texto and "G19" in texto)
            or ("G1" in texto and "G2" in texto and "2025" in texto)
            or lote_upper in ("G1", "1", "G19", "19", "G1/G19", "01")
        ):
            return "G1/G19"

    # Regra geral para G1/G19
    if re.search(r"\b(?:LT\.?\s*|LOTE\s*)?G1\s*[-/]\s*G?19\b", texto) or re.search(r"\bG1G-?19\b", texto) or lote_upper == "G1/G19":
        return "G1/G19"

    # 3. Normalizacao geral de hiphens/espacos
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

    if quadra_upper in QUADRA_LETRAS:
        numero = re.search(r"0*(\d{1,3}[A-Z]?)", lote_upper)
        if numero:
            candidatos.insert(0, (quadra_upper, numero.group(1)))

    for quadra_can, lote_can in candidatos:
        if not quadra_can:
            continue
        numero = re.match(r"0*(\d+)([A-Z]?)$", lote_can)
        if not numero:
            continue
        numero_sem_zero = str(int(numero.group(1)))
        sufixo = numero.group(2) or ""
        return f"{quadra_can}{numero_sem_zero}{sufixo}"

    return lote_upper if lote_upper and lote_upper != "-" else ""


def extrair_lotes_referencia(referencia="", quadra_hint="", cliente=""):
    """Extrai todos os lotes explicitamente citados em uma referencia WidePay."""
    texto = normalizar_texto(referencia).upper()
    cliente_norm = slug_busca(cliente or "")
    encontrados = []

    def adicionar(lote_cand):
        if lote_cand and lote_cand not in encontrados:
            encontrados.append(lote_cand)

    # 1. Regra Emmanuel: LT G3 / G3 -> G18
    if ("emmanuel" in cliente_norm or "emanuel" in cliente_norm) and not ("G2" in texto and "G18" in texto):
        if re.search(r"\b(?:LT\.?\s*|LOTE\s*)?G3\b", texto) or re.search(r"\bG3\b", texto):
            adicionar("G18")

    # 2. Regra Rodrigo: G1/G19
    if ("rodrigo" in cliente_norm and not "F19" in texto) and (
        re.search(r"\bG1\s*[-/]?\s*G?19\b", texto)
        or re.search(r"\bLT\.?\s*G?\s*1\s*/\s*19\b", texto)
        or "G1" in texto
    ):
        adicionar("G1/G19")
    elif re.search(r"\b(?:LT\.?\s*|LOTE\s*)?G1\s*[-/]\s*G?19\b", texto) or re.search(r"\bG1G-?19\b", texto):
        adicionar("G1/G19")

    # 3. Conjuntos explicitos G2 e G18 (Emmanuel)
    if "G2" in texto and "G18" in texto:
        adicionar("G2")
        adicionar("G18")

    # Formas como C 8/9 ou C8/9: os dois numeros pertencem a mesma quadra.
    for match in re.finditer(
        r"(?:\bLT\.?\s*|\bLOTE\s*)?([A-H])\s*0*(\d{1,3}[A-Z]?)\s*/\s*0*(\d{1,3}[A-Z]?)(?![A-Z0-9])",
        texto,
    ):
        q, l1, l2 = match.group(1), match.group(2), match.group(3)
        if q == "G" and l1 == "1" and l2 == "19":
            adicionar("G1/G19")
        else:
            adicionar(normalizar_lote_quadra(lote=l1, quadra=q, cliente=cliente))
            adicionar(normalizar_lote_quadra(lote=l2, quadra=q, cliente=cliente))

    # Formas prefixadas como LTF2 e LT F2.
    for match in re.finditer(
        r"\b(?:LT\.?|LOTE)\s*([A-H])\s*[-/]?\s*0*(\d{1,3}[A-Z]?)(?![A-Z0-9])",
        texto,
    ):
        adicionar(normalizar_lote_quadra(lote=match.group(2), quadra=match.group(1), cliente=cliente))

    # Formas independentes compactas como G6, C8 e E19.
    for match in re.finditer(r"(?<![A-Z0-9])([A-H])0*(\d{1,3}[A-Z]?)(?![A-Z0-9])", texto):
        q, l = match.group(1), match.group(2)
        if q == "G" and l == "3" and ("emmanuel" in cliente_norm or "emanuel" in cliente_norm):
            adicionar("G18")
        elif q == "G" and l in ("1", "19") and "rodrigo" in cliente_norm:
            adicionar("G1/G19")
        else:
            adicionar(normalizar_lote_quadra(lote=l, quadra=q, cliente=cliente))

    return encontrados


def chave_lote_canonica(registro):
    cliente = registro.get("cliente_original_widepay") or registro.get("cliente") or registro.get("cliente_normalizado") or ""
    lote = registro.get("lote") or registro.get("lote_original") or ""
    quadra = registro.get("quadra") or ""
    referencia = registro.get("referencia") or registro.get("descricao") or ""

    chave = normalizar_lote_quadra(lote, quadra, referencia, registro.get("pasta_local"), cliente=cliente)
    if chave:
        return chave

    lotes_referencia = extrair_lotes_referencia(
        referencia,
        quadra_hint=quadra,
        cliente=cliente,
    )
    if len(lotes_referencia) == 1:
        return lotes_referencia[0]
    elif "G1/G19" in lotes_referencia:
        return "G1/G19"
    return registro.get("chave_lote_canonica") or registro.get("lote_canonico") or ""


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
    cliente_original = item.get("cliente") or item.get("cliente_original_widepay") or cliente_fallback
    lotes_referencia = extrair_lotes_referencia(referencia, quadra_hint=quadra, cliente=cliente_original)
    if lote_original or quadra:
        chave = normalizar_lote_quadra(
            lote_original, quadra, referencia, item.get("pasta_local"), cliente=cliente_original
        )
    else:
        # A referencia so define lote quando contem uma forma realmente
        # explicita (F5, LT F5, LOTE F5...). Listas de competencia como
        # "04, 05, 06 de 2026" nunca devem produzir F405/E4/E202.
        chave = lotes_referencia[0] if len(lotes_referencia) == 1 else ("G1/G19" if "G1/G19" in lotes_referencia else "")
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


def obter_chave_identidade_cobranca(registro):
    """Identidade estavel do boleto, sem campos mutaveis como status/valor recebido."""
    item = dict(registro or {})
    fonte = str(item.get("fonte") or "").strip().lower()
    identificador = str(item.get("id_boleto") or "").strip().lower()
    if identificador:
        return f"{fonte}|id:{identificador}"
    return "|".join(
        str(item.get(campo) or "").strip().lower()
        for campo in (
            "fonte",
            "cliente_normalizado",
            "lote_canonico",
            "referencia",
            "vencimento",
            "data_pagamento",
            "valor_original",
        )
    )


def deduplicar_boletos(registros):
    unicos = {}
    ordem = []
    for registro in registros:
        item = dict(registro)
        item["lote_canonico"] = chave_lote_canonica(item)
        item["chave_lote_canonica"] = item["lote_canonico"]
        chave = chave_boleto(item)
        if chave not in unicos:
            ordem.append(chave)
        unicos[chave] = item
    return [unicos[chave] for chave in ordem]


def salvar_cache(registros, metadados=None, permitir_vazio=False):
    config.ensure_dirs()
    registros = deduplicar_boletos(registros)
    cache_anterior = carregar_cache()
    registros_anteriores = list(cache_anterior.get("registros") or [])
    if not registros and registros_anteriores and not permitir_vazio:
        raise ValueError(
            "Gravacao de cache vazio recusada: o ultimo cache WidePay valido foi preservado."
        )
    # MERGE/UPSERT por identidade: uma coleta parcial/filtrada (ex.: somente
    # Cobrancas com Status=Recebido) NUNCA substitui o historico inteiro. Os
    # registros que nao vieram nesta execucao sao preservados; os que vieram
    # atualizam/adicionam. Isso substitui a antiga regra que recusava a gravacao
    # apenas porque a coleta trazia menos registros que o cache completo.
    if registros_anteriores:
        por_identidade = {
            obter_chave_identidade_cobranca(r): r for r in registros_anteriores
        }
        for r in registros:
            por_identidade[obter_chave_identidade_cobranca(r)] = r
        registros = deduplicar_boletos(list(por_identidade.values()))
        # Protecao contra perda REAL: o conjunto mesclado nunca pode ter menos
        # identidades distintas que o historico ja gravado.
        base_historico = {obter_chave_identidade_cobranca(r) for r in registros_anteriores}
        identidades_finais = {obter_chave_identidade_cobranca(r) for r in registros}
        if len(identidades_finais) < len(base_historico) and not permitir_vazio:
            raise ValueError(
                "Gravacao recusada: o merge perderia registros do historico WidePay."
            )
    novos_por_chave = {obter_chave_identidade_cobranca(r): r for r in registros}
    regressoes_recebidos = []
    for anterior in registros_anteriores:
        if normalizar_texto(anterior.get("status")).lower() not in (
            "recebido",
            "pago",
            "quitado",
            "liquidado",
        ):
            continue
        chave = obter_chave_identidade_cobranca(anterior)
        novo = novos_por_chave.get(chave)
        status_novo = normalizar_texto((novo or {}).get("status")).lower()
        if not novo or status_novo not in ("recebido", "pago", "quitado", "liquidado"):
            regressoes_recebidos.append((chave, status_novo or "ausente"))
    if regressoes_recebidos:
        raise ValueError(
            "Gravacao recusada: cobrancas recebidas regrediriam no cache WidePay. "
            f"Ocorrencias: {len(regressoes_recebidos)}."
        )
    metadados = dict(metadados or {})
    metadados.setdefault("fim_coleta", datetime.now().isoformat(timespec="seconds"))
    metadados.setdefault("ultima_atualizacao", metadados["fim_coleta"])
    metadados.setdefault("total_registros", len(registros))
    metadados.setdefault("total_carnes", sum(1 for r in registros if r.get("fonte") == "carne"))
    metadados.setdefault("total_cobrancas", sum(1 for r in registros if r.get("fonte") == "cobranca"))
    metadados.setdefault("total_clientes_reconhecidos", len({r.get("cliente_normalizado") for r in registros if r.get("cliente_normalizado")}))
    payload = {"metadados": metadados, "registros": registros}
    destino = config.WIDEPAY_BOLETOS_CACHE_JSON
    temporario = destino.with_name(destino.name + ".tmp")
    backup = destino.with_name(destino.name + ".bak")
    backup_temporario = backup.with_name(backup.name + ".tmp")
    try:
        with open(temporario, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        with open(temporario, "r", encoding="utf-8") as f:
            payload_validado = json.load(f)
        if len(payload_validado.get("registros") or []) != len(registros):
            raise ValueError("Validacao do cache temporario falhou; cache anterior preservado.")
        if destino.exists():
            criar_snapshot_versionado(destino, categoria="widepay_boletos_cache")
            with open(destino, "rb") as origem, open(backup_temporario, "wb") as copia:
                shutil.copyfileobj(origem, copia)
                copia.flush()
                os.fsync(copia.fileno())
            os.replace(backup_temporario, backup)
        os.replace(temporario, destino)
    finally:
        for pendente in (temporario, backup_temporario):
            try:
                pendente.unlink(missing_ok=True)
            except OSError:
                pass
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


def criar_indice_cache(payload_cache=None):
    """Agrupa registros por lote canonico para consultas em lote sem varrer todo o cache."""
    payload = payload_cache if isinstance(payload_cache, dict) else carregar_cache()
    por_lote = {}
    por_nome = {}
    for item in payload.get("registros", []):
        lote_item = item.get("lote_canonico") or chave_lote_canonica(item)
        por_lote.setdefault(lote_item, []).append(item)
        nome_item = item.get("cliente_normalizado") or item.get("cliente", "")
        nome_identidade = slug_identidade_nome(nome_item)
        if nome_identidade:
            por_nome.setdefault(nome_identidade, []).append(item)
    por_lote["__por_nome__"] = por_nome
    return por_lote


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


def filtrar_por_cliente_lote(
    cliente="",
    lote="",
    quadra="",
    pasta_local="",
    payload_cache=None,
    indice_cache=None,
    permitir_nome_sem_lote=False,
):
    payload = payload_cache if isinstance(payload_cache, dict) else carregar_cache()
    cliente_slug = slug_busca(cliente)
    cliente_identidade = slug_identidade_nome(cliente)
    lote_can = normalizar_lote_quadra(lote, quadra, "", pasta_local, cliente=cliente)
    matches = []
    ids_matches = set()

    def adicionar_match(item):
        item_proc = item
        if ("emmanuel" in cliente_slug or "emanuel" in cliente_slug) and lote_can in ("G2", "G18"):
            ref = normalizar_texto(item.get("referencia") or item.get("descricao") or "").upper()
            if "G2" in ref and "G18" in ref:
                item_proc = dict(item)
                val_orig = float(item.get("valor_original") or 0.0)
                val_rec = float(item.get("valor_recebido") or 0.0)
                if abs(val_orig - 198.0) < 1.0 or val_orig == 0:
                    item_proc["valor_original"] = round(val_orig / 2.0, 2) if val_orig > 0 else 99.0
                    item_proc["valor_recebido"] = round(val_rec / 2.0, 2)
                item_proc["lote_canonico"] = lote_can
                item_proc["chave_lote_canonica"] = lote_can

        identidade = (
            item_proc.get("fonte"),
            item_proc.get("id_boleto"),
            item_proc.get("referencia"),
            item_proc.get("vencimento"),
            item_proc.get("valor_original"),
            item_proc.get("valor_recebido"),
        )
        if identidade not in ids_matches:
            ids_matches.add(identidade)
            matches.append(item_proc)

    candidatos = payload.get("registros", [])
    for item in candidatos:
        from app.isolamento_cliente import mesma_identidade
        nome_item = item.get("cliente_normalizado") or slug_busca(item.get("cliente", ""))
        identidade_forte = bool(
            cliente_identidade and slug_identidade_nome(nome_item) == cliente_identidade
        ) or mesma_identidade(cliente, nome_item) or mesma_identidade(cliente, item.get("cliente_original_widepay", ""))
        nome_ok = (
            not cliente_slug
            or cliente_slug in nome_item
            or nome_item in cliente_slug
            or identidade_forte
        )
        if not nome_ok:
            continue

        lote_item = item.get("lote_canonico") or chave_lote_canonica(item)
        lotes_ref = extrair_lotes_referencia(item.get("referencia") or item.get("descricao") or "", quadra_hint=item.get("quadra"), cliente=cliente)

        # Regras especificas de lote por cliente
        if "emmanuel" in cliente_slug or "emanuel" in cliente_slug:
            ref = normalizar_texto(item.get("referencia") or item.get("descricao") or "").upper()
            if "G2" in ref and "G18" in ref:
                if lote_can in ("G2", "G18"):
                    item_cp = dict(item)
                    val_orig = float(item.get("valor_original") or 0)
                    val_rec = float(item.get("valor_recebido") or item.get("recebido") or item.get("valor_pago") or 0)
                    half_orig = round(val_orig / 2.0, 2)
                    half_rec = round(val_rec / 2.0, 2)
                    if lote_can == "G2":
                        item_cp["valor_original"] = half_orig
                        item_cp["valor_recebido"] = half_rec
                    else:
                        item_cp["valor_original"] = round(val_orig - half_orig, 2)
                        item_cp["valor_recebido"] = round(val_rec - half_rec, 2)
                    adicionar_match(item_cp)
                    continue
            elif ("G3" in ref or "LT G3" in ref) and lote_can == "G18":
                adicionar_match(item)
                continue
            elif "G2" in ref and lote_can == "G2":
                adicionar_match(item)
                continue

        if "rodrigo" in cliente_slug:
            ref = normalizar_texto(item.get("referencia") or item.get("descricao") or "").upper()
            e_g1_19 = (
                lote_item == "G1/G19"
                or "G1/G19" in lotes_ref
                or any(k in ref for k in ["G1/19", "G1 G19", "G1G19", "G1G-19", "LT G 1/19", "G1 G2"])
                or ("G1" in ref and not "F19" in ref)
                or (item.get("fonte") == "carne" and item.get("id_boleto") in ("42", "128", "183", "204", "232"))
            )
            if lote_can in ("G1/G19", "G1") and e_g1_19:
                adicionar_match(item)
                continue
            elif lote_can == "F19" and not e_g1_19:
                adicionar_match(item)
                continue

        if not lote_can:
            lote_ok = True
        elif lote_item == lote_can or lote_can in lotes_ref:
            lote_ok = True
        elif not lote_item and not lotes_ref:
            lote_ok = identidade_forte
        else:
            lote_ok = False

        if lote_ok:
            adicionar_match(item)

    return matches


def montar_raw_cliente(
    cliente="",
    lote="",
    quadra="",
    pasta_local="",
    payload_cache=None,
    indice_cache=None,
    permitir_nome_sem_lote=False,
):
    payload = payload_cache if isinstance(payload_cache, dict) else carregar_cache()
    boletos = filtrar_por_cliente_lote(
        cliente,
        lote,
        quadra,
        pasta_local,
        payload_cache=payload,
        indice_cache=indice_cache,
        permitir_nome_sem_lote=permitir_nome_sem_lote,
    )
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
        "metadados_cache_global": payload.get("metadados", {}),
    }
