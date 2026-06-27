# -*- coding: utf-8 -*-
"""Indexacao local de clientes/lotes para a interface dinamica."""

import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook

from app import config
from app.leitor_contratos import (
    extrair_texto_docx,
    extrair_texto_pdf,
    extrair_nome_cliente,
    parsear_dados_contrato,
)


LOTE_RE = re.compile(r"\b([A-H]\s*[-.]?\s*\d{1,3}[A-Z]?)\b", re.IGNORECASE)
QUADRA_RE = re.compile(r"\bquadra\s*([A-H])\b", re.IGNORECASE)
CONTRATO_A_VISTA_RE = re.compile(r"\b(a\s+vista|avista|pagamento\s+a\s+vista)\b", re.IGNORECASE)
CONTRATO_QUITADO_RE = re.compile(r"\b(quitad[oa]?|quitacao|sem parcelas pendentes)\b", re.IGNORECASE)
PASTA_IGNORADA_RE = re.compile(r"\b(backup|bkp|nova pasta|temporari[oa])\b", re.IGNORECASE)
COMPENSACAO_ATRASO_RE = re.compile(r"\b(atras[oa]s?|atrazos?|ref(?:erente)?|referencia)\b", re.IGNORECASE)
REMOVE_WORDS_RE = re.compile(
    r"\b(contrato|copia|final|corrigido|previa|carne\d*|apart\d*|agua|viva|leandro|meirelles|leo|docx|pdf|txt|html|md)\b",
    re.IGNORECASE,
)

PERSISTIR_CAMPOS = (
    "status",
    "parcelas_pagas_identificadas",
    "parcelas_total_contrato",
    "parcelas_restantes",
    "parcelas_resumo",
    "contrato_resumo",
    "contrato_modalidade",
    "valor_base_parcela",
    "valor_total_contratado",
    "entrada_valor",
    "origem_contrato",
    "valor_total_pago",
    "ultima_parcela_paga",
    "ultimo_vencimento_pago",
    "valor_ultimo_pagamento",
    "ultima_atualizacao_widepay",
    "situacao_final",
    "status_atraso_qtd",
    "status_atraso_cor",
    "status_atraso_rotulo",
    "status_atraso_origem",
    "observacoes",
    "divergencias",
    "boletos_atrasados",
    "origem_dados",
)

PRESERVAR_EM_REINDEXACAO = (
    "selecionado",
    "cliente",
    "status",
    "parcelas_pagas_identificadas",
    "parcelas_total_contrato",
    "parcelas_restantes",
    "parcelas_resumo",
    "contrato_resumo",
    "contrato_modalidade",
    "valor_base_parcela",
    "valor_total_contratado",
    "entrada_valor",
    "origem_contrato",
    "valor_total_pago",
    "ultima_parcela_paga",
    "ultimo_vencimento_pago",
    "valor_ultimo_pagamento",
    "data_atualizacao",
    "ultima_atualizacao_widepay",
    "situacao_final",
    "status_atraso_qtd",
    "status_atraso_cor",
    "status_atraso_rotulo",
    "status_atraso_origem",
    "observacoes",
    "divergencias",
    "boletos_atrasados",
    "origem_dados",
)


CAMPOS_NUNCA_ESVAZIAR = set(PERSISTIR_CAMPOS) | {
    "cliente",
    "lote",
    "quadra",
    "contrato",
    "contrato_arquivo",
    "pasta_local",
}


def normalizar(texto):
    texto = texto or ""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()


def slug_busca(texto):
    return re.sub(r"[^a-z0-9]+", " ", normalizar(texto).lower()).strip()


def inteiro(valor, default=0):
    if valor in (None, ""):
        return default
    try:
        return int(float(str(valor).replace(",", ".")))
    except (TypeError, ValueError):
        return default


def decimal(valor, default=0.0):
    if valor in (None, ""):
        return default
    try:
        if isinstance(valor, str):
            limpo = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
            return float(limpo)
        return float(valor)
    except (TypeError, ValueError):
        return default


def valor_preenchido(valor):
    if valor is None:
        return False
    if isinstance(valor, str):
        return valor.strip() not in ("", "-", "None", "NAO CONFIRMADO", "Nao encontrado")
    return True


def aplicar_se_preenchido(registro, campo, valor):
    if valor_preenchido(valor):
        registro[campo] = valor


def formatar_moeda(valor):
    if valor in (None, ""):
        return ""
    numero = decimal(valor, None)
    if numero is None:
        return str(valor)
    return f"R$ {numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_data_hora(valor):
    if not valor:
        return "Nunca atualizado"
    bruto = str(valor).strip()
    for parser in (datetime.fromisoformat,):
        try:
            return parser(bruto).strftime("%d/%m/%Y %H:%M")
        except ValueError:
            pass
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(bruto, fmt).strftime("%d/%m/%Y %H:%M")
        except ValueError:
            pass
    return bruto


def parse_data(valor):
    if not valor:
        return None
    if isinstance(valor, datetime):
        return valor.date()
    bruto = str(valor).strip()
    if not bruto or bruto in ("-", "None"):
        return None
    try:
        return datetime.fromisoformat(bruto.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(bruto, fmt).date()
        except ValueError:
            pass
    return None


def classificar_status_atraso(qtd):
    qtd = inteiro(qtd)
    if qtd <= 3:
        return "verde"
    if qtd <= 5:
        return "amarelo"
    return "vermelho"


def rotulo_status_atraso(qtd):
    qtd = inteiro(qtd)
    cor = classificar_status_atraso(qtd)
    if cor == "verde":
        return "Em dia" if qtd == 0 else "Atraso leve"
    if cor == "amarelo":
        return "Atraso"
    return "Atraso critico"


def formatar_status_indicador(registro):
    valor = registro.get("status_atraso_qtd", registro.get("boletos_atrasados", 0))
    return str(inteiro(valor))


def calcular_atraso_recente(metrics, dias_recentes=210):
    normalizado = (metrics or {}).get("normalizado") or {}
    calculos = (metrics or {}).get("calculos") or {}
    cobrancas = normalizado.get("cobrancas") or []
    hoje = datetime.now().date()
    vencidos_recentes = 0

    for cob in cobrancas:
        status = normalizar(str(cob.get("status", ""))).lower()
        vencimento = parse_data(cob.get("vencimento") or cob.get("data_vencimento"))
        if not vencimento or vencimento >= hoje:
            continue
        if (hoje - vencimento).days > dias_recentes:
            continue
        if status in ("recebido", "pago", "cancelado", "baixado"):
            continue
        vencidos_recentes += 1

    compensacoes = 0
    pagamentos = list(calculos.get("pagamentos_interpretados") or [])
    pagamentos.extend(cob for cob in cobrancas if normalizar(str(cob.get("status", ""))).lower() in ("recebido", "pago"))

    for pgto in pagamentos:
        texto = " ".join(
            str(pgto.get(campo, ""))
            for campo in ("descricao", "referencia", "observacao", "cliente", "forma")
        )
        if not COMPENSACAO_ATRASO_RE.search(normalizar(texto).lower()):
            continue
        data_ref = parse_data(pgto.get("pagamento") or pgto.get("data_pagamento") or pgto.get("vencimento"))
        if data_ref and (hoje - data_ref).days > dias_recentes:
            continue
        if decimal(pgto.get("valor_recebido", pgto.get("recebido", pgto.get("valor")))) <= 0:
            continue
        compensacoes += max(1, inteiro(pgto.get("qtd"), 1))

    return max(0, vencidos_recentes - compensacoes)


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


def inferir_modalidade_contrato(contrato_path="", pasta_local="", dados_contrato=None):
    dados_contrato = dados_contrato or {}
    total_parcelas = inteiro(dados_contrato.get("total_parcelas"))
    if total_parcelas == 1:
        return "a_vista"
    referencia = normalizar(" ".join(filter(None, [str(contrato_path), str(pasta_local)]))).lower()
    if CONTRATO_A_VISTA_RE.search(referencia):
        return "a_vista"
    if CONTRATO_QUITADO_RE.search(referencia):
        return "quitado"
    if contrato_path:
        return "parcelado"
    return "nao_confirmado"


def deduzir_situacao_final(registro):
    contrato_status = registro.get("contrato")
    if contrato_status != "Encontrado":
        return "Sem contrato confirmado"

    status = str(registro.get("status") or "").strip().upper()
    total = inteiro(registro.get("parcelas_total_contrato"))
    pagas = inteiro(registro.get("parcelas_pagas_identificadas"))
    atualizado = bool(registro.get("ultima_atualizacao_widepay"))

    if status == "ERRO":
        return "Bloqueado"
    if status == "PENDENTE":
        if total > 0 and pagas >= total:
            return "Quitado com alerta"
        if atualizado and total > 0:
            return "Em andamento com alerta"
        return "Pendente de validacao"
    if total > 0 and pagas >= total:
        return "Quitado"
    if atualizado and total > 0:
        return "Em andamento"
    if atualizado:
        return "Atualizado"
    return "Pendente de auditoria"


def deduzir_resumo_contrato(registro):
    contrato_status = registro.get("contrato")
    if contrato_status != "Encontrado":
        return "NAO CONFIRMADO"

    modalidade = registro.get("contrato_modalidade") or inferir_modalidade_contrato(
        registro.get("contrato_arquivo"),
        registro.get("pasta_local"),
    )
    total = inteiro(registro.get("parcelas_total_contrato"))
    pagas = inteiro(registro.get("parcelas_pagas_identificadas"))
    restantes = inteiro(registro.get("parcelas_restantes"))

    if modalidade == "a_vista":
        if pagas >= max(total, 1) and max(total, 1) > 0:
            return "A VISTA"
        return "PAGAMENTO A VISTA"
    if modalidade == "quitado":
        return "QUITADO"
    if total > 0 and pagas >= total:
        return "CONTRATO QUITADO"
    if total > 0 and pagas > 0 and restantes == 0:
        return "SEM PARCELAS PENDENTES"
    if total > 0:
        return "Parcelado"
    return "NAO CONFIRMADO"


def deduzir_resumo_parcelas(registro):
    contrato_status = registro.get("contrato")
    if contrato_status != "Encontrado":
        return "NAO CONFIRMADO"

    modalidade = registro.get("contrato_modalidade") or inferir_modalidade_contrato(
        registro.get("contrato_arquivo"),
        registro.get("pasta_local"),
    )
    total = inteiro(registro.get("parcelas_total_contrato"))
    pagas = inteiro(registro.get("parcelas_pagas_identificadas"))

    if modalidade == "a_vista":
        if pagas >= max(total, 1) and max(total, 1) > 0:
            return "A VISTA / quitado"
        return "A VISTA"
    if total <= 0:
        return "NAO CONFIRMADO"
    if pagas >= total:
        return f"{pagas} / {total} quitado"
    return f"{pagas} / {total} pagas"


def normalizar_registro_cache(registro):
    item = dict(registro or {})
    item.setdefault("selecionado", False)
    item.setdefault("cliente", "")
    item.setdefault("lote", "-")
    item.setdefault("quadra", "-")
    item.setdefault("status", "Pendente validacao WidePay" if item.get("contrato") == "Encontrado" else "Sem contrato confirmado")
    item.setdefault("contrato", "Nao encontrado")
    item.setdefault("contrato_arquivo", "")
    item.setdefault("origem", "Contrato local")
    item.setdefault("parcelas_pagas_identificadas", "")
    item.setdefault("parcelas_total_contrato", "")
    item.setdefault("parcelas_restantes", "")
    item.setdefault("parcelas_resumo", "")
    item.setdefault("contrato_resumo", "")
    item.setdefault("contrato_modalidade", "")
    item.setdefault("valor_base_parcela", "")
    item.setdefault("valor_total_contratado", "")
    item.setdefault("entrada_valor", "")
    item.setdefault("origem_contrato", "")
    item.setdefault("valor_total_pago", "")
    item.setdefault("ultima_parcela_paga", "")
    item.setdefault("ultimo_vencimento_pago", "")
    item.setdefault("valor_ultimo_pagamento", "")
    item.setdefault("data_atualizacao", "")
    item.setdefault("ultima_atualizacao_widepay", "")
    item.setdefault("situacao_final", "")
    item.setdefault("status_atraso_qtd", item.get("boletos_atrasados", 0))
    item.setdefault("status_atraso_cor", "")
    item.setdefault("status_atraso_rotulo", "")
    item.setdefault("status_atraso_origem", "")
    item.setdefault("observacoes", "")
    item.setdefault("divergencias", "")
    item.setdefault("pasta_local", "")
    item.setdefault("boletos_atrasados", "")
    item.setdefault("origem_dados", "")

    if not item.get("contrato_modalidade"):
        item["contrato_modalidade"] = inferir_modalidade_contrato(
            item.get("contrato_arquivo"),
            item.get("pasta_local"),
        )
    item["contrato_resumo"] = deduzir_resumo_contrato(item)
    item["parcelas_resumo"] = deduzir_resumo_parcelas(item)
    if not item.get("situacao_final"):
        item["situacao_final"] = deduzir_situacao_final(item)
    item["status_atraso_qtd"] = inteiro(item.get("status_atraso_qtd", item.get("boletos_atrasados", 0)))
    item["boletos_atrasados"] = item["status_atraso_qtd"]
    item["status_atraso_cor"] = item.get("status_atraso_cor") or classificar_status_atraso(item["status_atraso_qtd"])
    item["status_atraso_rotulo"] = item.get("status_atraso_rotulo") or rotulo_status_atraso(item["status_atraso_qtd"])
    item["status_atraso_origem"] = item.get("status_atraso_origem") or ("WidePay/cache" if item.get("ultima_atualizacao_widepay") else "Pendente WidePay")
    if not item.get("origem_dados"):
        item["origem_dados"] = "Contrato local + cache" if item.get("ultima_atualizacao_widepay") else "Contrato local"
    return item


def aplicar_metricas_registro(registro, metrics, atualizado_em=None):
    if not metrics:
        return normalizar_registro_cache(registro)

    item = normalizar_registro_cache(registro)
    contrato = metrics.get("contrato") or {}
    calculos = metrics.get("calculos") or {}
    normalizado = metrics.get("normalizado") or {}
    cobrancas = normalizado.get("cobrancas") or []
    atualizado_iso = atualizado_em or datetime.now().isoformat(timespec="seconds")

    try:
        from app.validador_matematico import validar_conciliacao

        status_val, notas, bloqueado = validar_conciliacao(calculos, contrato)
    except Exception:
        status_val, notas, bloqueado = "PENDENTE", [], False

    cliente_real = contrato.get("cliente")
    if cliente_real:
        item["cliente"] = cliente_real
    lote_real = contrato.get("lote")
    if lote_real and item.get("lote") in ("", "-", None):
        item["lote"] = lote_real
    quadra_real = contrato.get("quadra")
    if quadra_real:
        item["quadra"] = quadra_real

    total_parcelas = inteiro(calculos.get("total_parcelas_contrato") or contrato.get("total_parcelas"))
    parcelas_pagas = inteiro(calculos.get("parcelas_pagas_equivalentes"))
    parcelas_restantes = inteiro(calculos.get("parcelas_restantes"))
    valor_total_pago = round(decimal(calculos.get("total_pago_consolidado")), 2)

    item["status"] = status_val
    if total_parcelas > 0 or parcelas_pagas > 0:
        item["parcelas_pagas_identificadas"] = parcelas_pagas
    if total_parcelas > 0:
        item["parcelas_total_contrato"] = total_parcelas
        item["parcelas_restantes"] = parcelas_restantes
    if valor_total_pago > 0:
        item["valor_total_pago"] = valor_total_pago
    item["ultima_atualizacao_widepay"] = atualizado_iso
    item["data_atualizacao"] = atualizado_iso
    aplicar_se_preenchido(item, "valor_base_parcela", contrato.get("valor_parcela"))
    aplicar_se_preenchido(item, "valor_total_contratado", contrato.get("valor_total_contrato"))
    aplicar_se_preenchido(item, "entrada_valor", contrato.get("entrada"))
    item["origem_dados"] = "Contrato local + WidePay"
    item["contrato_modalidade"] = inferir_modalidade_contrato(
        item.get("contrato_arquivo"),
        item.get("pasta_local"),
        contrato,
    )
    item["situacao_final"] = deduzir_situacao_final(item)
    item["contrato_resumo"] = deduzir_resumo_contrato(item)
    item["parcelas_resumo"] = deduzir_resumo_parcelas(item)

    observacoes = []
    if bloqueado:
        observacoes.append("Relatorio bloqueado")
    if notas:
        observacoes.extend(notas[:2])
    if observacoes:
        item["observacoes"] = " | ".join(observacoes)
    elif not item.get("observacoes"):
        item["observacoes"] = "Relatorio gerado"
    if len(notas) > 2:
        item["divergencias"] = " | ".join(notas[2:])

    pagamentos = calculos.get("pagamentos_interpretados") or []
    ultimo_pgto = None
    ultima_data = None
    for pagamento in pagamentos:
        data_ref = pagamento.get("pagamento") or pagamento.get("vencimento")
        if not data_ref:
            continue
        try:
            dt = datetime.strptime(str(data_ref), "%d/%m/%Y")
        except ValueError:
            continue
        if ultima_data is None or dt > ultima_data:
            ultima_data = dt
            ultimo_pgto = pagamento

    if ultimo_pgto:
        item["ultimo_vencimento_pago"] = ultimo_pgto.get("vencimento", "")
        item["ultima_parcela_paga"] = ultimo_pgto.get("descricao", "")
        valor_ultimo = ultimo_pgto.get("valor_recebido")
        if valor_ultimo is not None:
            item["valor_ultimo_pagamento"] = formatar_moeda(valor_ultimo)

    # Contagem de boletos vencidos no WidePay com abatimento/compensação por avulsos de atraso recebidos
    vencidos_list = [cob for cob in cobrancas if str(cob.get("status", "")).lower() == "vencido"]
    
    compensacoes = 0
    for cob in cobrancas:
        status_lower = str(cob.get("status", "")).lower()
        # Se o boleto avulso foi pago (recebido) e indica pagamento de atrasos
        if status_lower == "recebido" and cob.get("classificacao") == "avulso":
            desc_lower = str(cob.get("descricao", "")).lower()
            if any(term in desc_lower for term in ["atraso", "atrazos", "ref", "referente"]):
                compensacoes += 1
                
    boletos_atrasados = max(0, len(vencidos_list) - compensacoes)
    item["boletos_atrasados"] = boletos_atrasados
    atraso_recente = calcular_atraso_recente(metrics)
    item["status_atraso_qtd"] = atraso_recente
    item["status_atraso_cor"] = classificar_status_atraso(atraso_recente)
    item["status_atraso_rotulo"] = rotulo_status_atraso(atraso_recente)
    item["status_atraso_origem"] = "WidePay"
    item["boletos_atrasados"] = atraso_recente

    return item


def mesclar_registro_indexado(
    pasta,
    lote,
    quadra,
    contrato_status,
    contrato_path,
    origem,
    widepay_status,
    agora,
    registro_anterior=None,
    cliente_padrao="",
    dados_contrato=None,
):
    dados_contrato = dados_contrato or {}
    if registro_anterior:
        registro = dict(registro_anterior)
    else:
        registro = {}

    for campo in PRESERVAR_EM_REINDEXACAO:
        if registro_anterior and campo in registro_anterior:
            registro[campo] = registro_anterior.get(campo)

    registro["selecionado"] = bool(registro.get("selecionado", False))
    registro["cliente"] = cliente_padrao or registro.get("cliente") or ""
    lote_contrato = dados_contrato.get("lote")
    quadra_contrato = dados_contrato.get("quadra")
    registro["lote"] = lote_contrato if valor_preenchido(lote_contrato) else lote
    registro["quadra"] = quadra_contrato if valor_preenchido(quadra_contrato) else quadra
    if (
        registro_anterior
        and registro_anterior.get("contrato") == "Encontrado"
        and contrato_status != "Encontrado"
    ):
        contrato_status = "Encontrado"
        contrato_path = registro_anterior.get("contrato_arquivo") or contrato_path
        if not dados_contrato and contrato_path:
            dados_contrato = ler_dados_contrato_arquivo(contrato_path, registro.get("cliente"))
    registro["contrato"] = contrato_status
    registro["contrato_arquivo"] = contrato_path
    registro["origem"] = origem
    registro["pasta_local"] = str(pasta)
    registro["contrato_modalidade"] = inferir_modalidade_contrato(contrato_path, str(pasta), dados_contrato)
    aplicar_se_preenchido(registro, "parcelas_total_contrato", dados_contrato.get("total_parcelas"))
    aplicar_se_preenchido(registro, "valor_base_parcela", dados_contrato.get("valor_parcela"))
    aplicar_se_preenchido(registro, "valor_total_contratado", dados_contrato.get("valor_total_contrato"))
    aplicar_se_preenchido(registro, "entrada_valor", dados_contrato.get("entrada"))
    if dados_contrato:
        registro["origem_contrato"] = "Contrato local"
        registro["origem_dados"] = "Contrato local + cache preservado"

    if not registro.get("status"):
        registro["status"] = "Pendente validacao WidePay" if contrato_status == "Encontrado" else "Sem contrato confirmado"
    elif contrato_status != "Encontrado" and registro.get("status") == "Pendente validacao WidePay":
        registro["status"] = "Sem contrato confirmado"

    if registro.get("observacoes") in (None, ""):
        registro["observacoes"] = widepay_status

    registro["data_atualizacao"] = agora.isoformat(timespec="seconds")

    return normalizar_registro_cache(registro)


def iterar_pastas_cliente():
    base = config.CONTRATOS_DIR
    if not base.exists():
        return []
    candidatos = []
    for path in base.rglob("*"):
        if not path.is_dir():
            continue
        try:
            partes_relativas = path.relative_to(base).parts
        except ValueError:
            partes_relativas = path.parts
        if any(PASTA_IGNORADA_RE.search(normalizar(parte).lower()) for parte in partes_relativas):
            continue
        nome = path.name.strip()
        if not nome or nome.lower().startswith(("_", ".")) or "backup" in nome.lower():
            continue
        lote = extrair_lote(nome)
        contrato_status, contrato_path = detectar_contrato(path)
        if lote != "-" or contrato_status == "Encontrado":
            candidatos.append((path, lote, contrato_status, contrato_path))
    return candidatos


def obter_nome_real_contrato(contrato_path, nome_sugerido):
    if not contrato_path:
        return nome_sugerido
    try:
        p = Path(contrato_path)
        ext = p.suffix.lower()
        texto = ""
        if p.exists():
            if ext == '.docx':
                texto = extrair_texto_docx(p)
            elif ext == '.pdf':
                texto = extrair_texto_pdf(p)
        
        # Fallback: se o arquivo não existe ou é um scan ilegível, busca na pasta 01_DOCUMENTOS_CONVERTIDOS
        if not texto:
            convertidos_dir = config.ROOT_DIR / "01_DOCUMENTOS_CONVERTIDOS"
            if convertidos_dir.exists():
                slug_sug = slug_busca(nome_sugerido)
                for txt_path in convertidos_dir.glob("*.txt"):
                    if slug_sug in slug_busca(txt_path.stem):
                        try:
                            with open(txt_path, "r", encoding="utf-8") as tf:
                                texto = tf.read()
                            if texto:
                                break
                        except Exception:
                            pass
        
        if texto:
            return extrair_nome_cliente(texto, nome_sugerido)
    except Exception:
        pass
    return nome_sugerido


def ler_dados_contrato_arquivo(contrato_path, nome_sugerido):
    dados = {}
    if not contrato_path:
        return dados
    try:
        p = Path(contrato_path)
        texto = ""
        if p.exists():
            ext = p.suffix.lower()
            if ext == ".docx":
                texto = extrair_texto_docx(p)
            elif ext == ".pdf":
                texto = extrair_texto_pdf(p)
            elif ext == ".txt":
                texto = p.read_text(encoding="utf-8", errors="ignore")

        if not texto:
            convertidos_dir = config.ROOT_DIR / "01_DOCUMENTOS_CONVERTIDOS"
            if convertidos_dir.exists():
                slug_sug = slug_busca(nome_sugerido)
                for txt_path in convertidos_dir.glob("*.txt"):
                    if slug_sug in slug_busca(txt_path.stem):
                        texto = txt_path.read_text(encoding="utf-8", errors="ignore")
                        if texto:
                            break

        if texto:
            dados = parsear_dados_contrato(texto, nome_sugerido) or {}
    except Exception:
        return {}
    return dados


def carregar_metricas_historicas_locais(cliente, lote):
    """Busca no diretório de entrega o relatório JSON de métricas mais recente do cliente, usando busca flexível."""
    try:
        import re
        from app.rastreabilidade import re_slug
        cli_slug = re_slug(cliente)
        lot_slug = re_slug(lote)
        
        primeira_palavra = cli_slug.split("_")[0]
        
        # Limpar o lote (ex: "05", "5")
        num_lote = re.sub(r"[^0-9]", "", lot_slug)
        
        pasta_candidata = None
        if config.OUTPUT_DIR.exists():
            for p in config.OUTPUT_DIR.iterdir():
                if not p.is_dir() or not p.name.endswith("_FINAL"):
                    continue
                name_upper = p.name.upper()
                # A pasta deve conter a primeira palavra do cliente
                if primeira_palavra in name_upper:
                    # E o lote deve coincidir em slug completo ou parte numérica
                    if lot_slug in name_upper or (num_lote and num_lote.lstrip("0") in name_upper):
                        # A pasta deve conter de fato arquivos de métricas
                        if list(p.glob("METRICAS_*.json")):
                            pasta_candidata = p
                            break
                        
        if not pasta_candidata:
            pasta_candidata = config.OUTPUT_DIR / f"{cli_slug}_LOTE_{lot_slug}_FINAL"
            
        if not pasta_candidata.exists():
            return None, None
            
        arquivos = list(pasta_candidata.glob("METRICAS_*.json"))
        if not arquivos:
            return None, None
            
        # Pegar o arquivo mais recentemente modificado
        arquivos.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        mais_recente = arquivos[0]
        
        with open(mais_recente, "r", encoding="utf-8") as f:
            metrics_data = json.load(f)
            
        mtime_iso = datetime.fromtimestamp(mais_recente.stat().st_mtime).isoformat(timespec="seconds")
        return metrics_data, mtime_iso
    except Exception:
        return None, None


def chave_registro_cache(registro):
    pasta = str(registro.get("pasta_local") or "").strip().lower()
    lote = str(registro.get("lote") or "-").strip().upper()
    cliente = slug_busca(registro.get("cliente") or "")
    if pasta:
        return ("pasta", pasta, lote)
    return ("cliente_lote", cliente, lote)


def deduplicar_preservando_ordem(registros):
    unicos = {}
    ordem = []
    for registro in registros:
        chave = chave_registro_cache(registro)
        if chave not in unicos:
            ordem.append(chave)
        unicos[chave] = registro
    return [unicos[chave] for chave in ordem]


def montar_metricas_resumo_widepay(dados_raw_wp, dados_contrato):
    from app.calculadora_financeira import calcular_resumo
    from app.normalizador_pagamentos import normalizar_e_deduplicar

    valor_base = float(dados_contrato.get("valor_parcela") or 0.0)
    dados_normalizados = normalizar_e_deduplicar(dados_raw_wp, valor_base)
    dados_calculados = calcular_resumo(dados_normalizados, dados_contrato)
    return {
        "contrato": dados_contrato,
        "calculos": dados_calculados,
        "normalizado": dados_normalizados,
    }


def atualizar_resumo_widepay_incremental(registros, log_callback=None):
    confirmados = [r for r in registros if r.get("contrato") == "Encontrado"]
    if not confirmados:
        return registros

    def log(msg):
        if log_callback:
            log_callback(msg)

    try:
        import asyncio
        from app.extrator_widepay import extrair_dados_clientes_bloco
        from app.login_navegador import garantir_navegador_conectado

        ws_url = garantir_navegador_conectado()

        async def _coletar():
            atualizados_por_chave = {}
            for idx in range(0, len(confirmados), 3):
                bloco = confirmados[idx:idx + 3]
                payload = []
                contrato_por_nome = {}
                for reg in bloco:
                    dados_contrato = {
                        "cliente": reg.get("cliente"),
                        "lote": reg.get("lote"),
                        "quadra": reg.get("quadra"),
                        "valor_parcela": decimal(reg.get("valor_base_parcela")),
                        "total_parcelas": inteiro(reg.get("parcelas_total_contrato")),
                        "valor_total_contrato": decimal(reg.get("valor_total_contratado")),
                        "entrada": decimal(reg.get("entrada_valor")),
                    }
                    nome = dados_contrato["cliente"] or reg.get("cliente") or ""
                    contrato_por_nome[nome] = (reg, dados_contrato)
                    payload.append({
                        "nome": nome,
                        "lote": dados_contrato.get("lote") or "-",
                        "quadra": dados_contrato.get("quadra") or "-",
                    })
                log(f"WidePay leve: coletando bloco {idx // 3 + 1} com {len(payload)} cliente(s).")
                resultado_bloco = await extrair_dados_clientes_bloco(ws_url, payload)
                for nome, dados_raw in (resultado_bloco or {}).items():
                    reg, dados_contrato = contrato_por_nome.get(nome, ({}, {}))
                    if not reg:
                        continue
                    metrics = montar_metricas_resumo_widepay(dados_raw, dados_contrato)
                    atualizado = aplicar_metricas_registro(reg, metrics)
                    atualizado["origem_dados"] = "Contrato local + WidePay leve"
                    atualizados_por_chave[chave_registro_cache(reg)] = atualizado
            return atualizados_por_chave

        try:
            atualizados = asyncio.run(_coletar())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                atualizados = loop.run_until_complete(_coletar())
            finally:
                loop.close()

        return [atualizados.get(chave_registro_cache(r), r) for r in registros]
    except Exception as exc:
        log(f"Atualizacao WidePay falhou: {exc}. Mantendo dados anteriores.")
        mantidos = []
        agora = datetime.now().isoformat(timespec="seconds")
        for reg in registros:
            item = normalizar_registro_cache(reg)
            if item.get("contrato") == "Encontrado":
                obs = item.get("observacoes") or ""
                aviso = "Atualizacao falhou - mantidos dados anteriores"
                item["observacoes"] = aviso if not obs else f"{obs} | {aviso}"
                if not item.get("ultima_atualizacao_widepay"):
                    item["data_atualizacao"] = item.get("data_atualizacao") or agora
            mantidos.append(item)
        return mantidos


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
    
    # Carregar cache existente para preservar nomes de clientes já validados pela WidePay ou contratos
    cache_anterior = {}
    try:
        for r in carregar_cache():
            chave_cache = (str(r.get("pasta_local")).lower(), r.get("lote"))
            cache_anterior[chave_cache] = r
    except Exception:
        pass

    for pasta, lote, contrato_status, contrato_path in iterar_pastas_cliente():
        cliente_sugerido = limpar_nome_cliente(pasta.name)
        cliente = cliente_sugerido
        
        # O nome exibido deve priorizar o contrato local confirmado. Os dados financeiros
        # do cache anterior seguem preservados por mesclar_registro_indexado().
        chave_res = (str(pasta).lower(), lote)
        r_antigo = cache_anterior.get(chave_res)
        dados_contrato = {}
        if contrato_status == "Encontrado" and contrato_path:
            dados_contrato = ler_dados_contrato_arquivo(contrato_path, cliente_sugerido)
            cliente = dados_contrato.get("cliente") or obter_nome_real_contrato(contrato_path, cliente_sugerido)
        elif r_antigo and r_antigo.get("cliente"):
            cliente = r_antigo["cliente"]
        quadra = extrair_quadra(pasta.name, lote)
        chave = (slug_busca(cliente), lote if lote != "-" else str(pasta).lower())
        if chave in vistos:
            continue
        vistos.add(chave)
        origem = "Contrato local"
        registro = mesclar_registro_indexado(
            pasta=pasta,
            lote=lote,
            quadra=quadra,
            contrato_status=contrato_status,
            contrato_path=contrato_path,
            origem=origem,
            widepay_status=widepay_status,
            agora=agora,
            registro_anterior=r_antigo,
            cliente_padrao=cliente,
            dados_contrato=dados_contrato,
        )
        
        # Restauração automática de histórico físico
        if registro.get("contrato") == "Encontrado" and (registro.get("boletos_atrasados") == "" or registro.get("status") == "Pendente validacao WidePay"):
            metrics_data, mtime_iso = carregar_metricas_historicas_locais(cliente, lote)
            if metrics_data:
                registro = aplicar_metricas_registro(registro, metrics_data, atualizado_em=mtime_iso)

        registros.append(registro)

    chaves_atuais = {chave_registro_cache(r) for r in registros}
    for antigo in carregar_cache():
        chave_antiga = chave_registro_cache(antigo)
        if chave_antiga in chaves_atuais:
            continue
        preservado = normalizar_registro_cache(antigo)
        obs = preservado.get("observacoes") or ""
        aviso = "Nao localizado nesta varredura - mantido do cache anterior"
        preservado["observacoes"] = aviso if not obs else f"{obs} | {aviso}"
        registros.append(preservado)
        chaves_atuais.add(chave_antiga)

    registros = deduplicar_preservando_ordem(registros)
    if validar_widepay:
        registros = atualizar_resumo_widepay_incremental(registros, log_callback=log)

    registros.sort(key=lambda r: (slug_busca(r["cliente"]), r["lote"]))
    salvar_cache(registros)
    log(f"Indexacao concluida: {len(registros)} cliente/lote")
    return {"registros": registros, "log": str(log_path), "widepay_status": widepay_status}


def salvar_cache(registros):
    config.ensure_dirs()
    registros_normalizados = [normalizar_registro_cache(item) for item in registros]
    payload = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "quantidade": len(registros_normalizados),
        "registros": registros_normalizados,
    }
    with open(config.CLIENTES_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    salvar_xlsx(registros_normalizados)


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
        "contrato_resumo",
        "contrato_modalidade",
        "valor_base_parcela",
        "valor_total_contratado",
        "entrada_valor",
        "origem_contrato",
        "origem",
        "parcelas_pagas_identificadas",
        "parcelas_total_contrato",
        "parcelas_restantes",
        "parcelas_resumo",
        "valor_total_pago",
        "ultima_parcela_paga",
        "ultimo_vencimento_pago",
        "valor_ultimo_pagamento",
        "data_atualizacao",
        "ultima_atualizacao_widepay",
        "situacao_final",
        "status_atraso_qtd",
        "status_atraso_cor",
        "status_atraso_rotulo",
        "status_atraso_origem",
        "observacoes",
        "divergencias",
        "origem_dados",
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
    return [normalizar_registro_cache(item) for item in payload.get("registros", [])]
