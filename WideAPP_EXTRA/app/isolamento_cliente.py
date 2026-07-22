# -*- coding: utf-8 -*-
"""Isolamento forte de dados por cliente e deduplicacao deterministica.

Este modulo centraliza a regra de propriedade de registros financeiros
(carnes e cobrancas do WidePay). Ele existe para impedir a contaminacao
historica em que registros de um cliente entravam no relatorio de outro por
causa de correspondencia parcial de nomes.

Exemplo real que motivou o modulo: o primeiro nome "ANA" (de ANA CLEIDE) e
uma substring de "SANTANA" (Carlos Alberto SANTANA, Eliel Hora SANTANA,
Marinalva Hora SANTANA). A comparacao por substring fazia esses tres clientes
serem gravados no arquivo de Ana Cleide.

Regra adotada aqui: comparacao por TOKENS inteiros, nunca por substring solta.
Um registro so pertence ao cliente selecionado quando o conjunto de tokens
significativos de um nome esta inteiramente contido no outro (com no minimo
dois tokens em comum) ou quando as identidades normalizadas sao iguais.
"""

import re
import unicodedata


# Conectores portugueses que nao ajudam a distinguir clientes.
_CONECTORES = {"de", "da", "do", "das", "dos", "e", "a", "o"}

# Variantes ortograficas confirmadas manualmente no proprio WidePay.
# Mantida explicita de proposito: nao usamos fuzzy irrestrito para aproximar
# nomes diferentes. Espelha a lista de widepay_boletos_cache.slug_identidade_nome.
_ALIASES_TOKEN = {
    "sousa": "souza",
}
_ALIASES_NOME = {
    "telma valadares dos santos": "telma valadares dos anjos carvalho",
    "telma valadares dos anjos": "telma valadares dos anjos carvalho",
    "ana carolina nery da s borgens": "ana carolina nery da s borges de barros",
    "ana carolina nery da silva borges": "ana carolina nery da s borges de barros",
    "joice carla de magalhaes gomes": "joice carla de magalhaes goncalves",
    "rodrigo monteiro": "rodrigo monteiro de melo",
}


def normalizar_nome(texto):
    """Minusculas, sem acento, apenas alfanumerico e espaco unico."""
    texto = unicodedata.normalize("NFD", str(texto or ""))
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", texto.lower()).strip()


def _e_token_lote(token):
    """Detecta tokens que sao lote/quadra (e5, g14, f05...) e nao nome."""
    return bool(re.fullmatch(r"[a-h]\d{1,3}[a-z]?", token))


def tokens_significativos(nome):
    """Tokens de nome uteis para comparar identidade (sem conectores/lotes)."""
    tokens = []
    for token in normalizar_nome(nome).split():
        if token in _CONECTORES:
            continue
        if _e_token_lote(token):
            continue
        tokens.append(_ALIASES_TOKEN.get(token, token))
    return tokens


def slug_identidade(nome):
    """Identidade canonica do cliente aplicando aliases confirmados."""
    base = " ".join(_ALIASES_TOKEN.get(t, t) for t in normalizar_nome(nome).split())
    return _ALIASES_NOME.get(base, base)


def mesma_identidade(nome_a, nome_b):
    """True somente quando dois nomes representam o mesmo cliente.

    Nunca decide por substring solta. Usa tokens inteiros:
    - identidades canonicas iguais; ou
    - o conjunto menor de tokens esta inteiramente contido no maior, com
      pelo menos dois tokens em comum (evita "ana" casar com "santana").
    """
    if slug_identidade(nome_a) == slug_identidade(nome_b) and slug_identidade(nome_a):
        return True
    ta = set(tokens_significativos(nome_a))
    tb = set(tokens_significativos(nome_b))
    if not ta or not tb:
        return False
    if ta == tb:
        return True
    menor, maior = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    return menor.issubset(maior) and len(menor) >= 2


def _nome_do_registro(registro, campos):
    for campo in campos:
        valor = registro.get(campo)
        if valor:
            return str(valor)
    return ""


def isolar_registros(registros, cliente_alvo, campos_nome=("cliente", "cliente_original_widepay")):
    """Separa registros que pertencem ao cliente alvo dos de terceiros.

    Retorna um dicionario com:
      - mantidos: pertencem comprovadamente ao cliente alvo;
      - descartados: pertencem a terceiros (motivo: proprietario_divergente);
      - nao_verificados: sem nome de proprietario no registro; mantidos, porem
        sinalizados como pendencia de auditoria (nao sao terceiros provados).
    Nenhum registro de terceiro provado entra em 'mantidos'.
    """
    mantidos = []
    descartados = []
    nao_verificados = []
    for registro in registros or []:
        dono = _nome_do_registro(registro, campos_nome)
        if not dono:
            nao_verificados.append(registro)
            mantidos.append(registro)
            continue
        if mesma_identidade(dono, cliente_alvo):
            mantidos.append(registro)
        else:
            descartados.append({"registro": registro, "proprietario": dono})
    return {
        "mantidos": mantidos,
        "descartados": descartados,
        "nao_verificados": nao_verificados,
    }


def _chave_dedup(registro, id_fields, fallback_fields):
    for campo in id_fields:
        valor = str(registro.get(campo) or "").strip()
        if valor and valor not in ("-", "0"):
            return f"id:{valor.lower()}"
    return "|".join(str(registro.get(c) or "").strip().lower() for c in fallback_fields)


def deduplicar(registros, id_fields, fallback_fields):
    """Deduplicacao deterministica priorizando o ID unico do WidePay.

    Duas fontes internas que trazem a mesma transacao (mesmo ID) contam uma
    unica vez. Sem ID, usa uma chave composta estavel como ultimo recurso.
    """
    vistos = {}
    ordem = []
    removidos = 0
    for registro in registros or []:
        chave = _chave_dedup(registro, id_fields, fallback_fields)
        if chave in vistos:
            removidos += 1
            continue
        vistos[chave] = registro
        ordem.append(chave)
    return [vistos[c] for c in ordem], removidos


def deduplicar_cobrancas(cobrancas):
    return deduplicar(
        cobrancas,
        id_fields=("id", "id_boleto"),
        fallback_fields=("descricao", "vencimento", "valor_original", "valor_recebido", "status"),
    )


def deduplicar_carnes(carnes):
    return deduplicar(
        carnes,
        id_fields=("carne", "id", "id_boleto"),
        fallback_fields=("referencia", "valor_parcela", "ultimo_vencimento", "status"),
    )


# ---------------------------------------------------------------------------
# Diagnostico de clientes classificados como "sem boleto"
# ---------------------------------------------------------------------------

MOTIVOS_SEM_BOLETO = {
    "NENHUM_REGISTRO_WIDEPAY": "Nenhum registro localizado no WidePay para o cliente.",
    "APENAS_TERCEIROS": "Registros encontrados pertenciam a terceiros e foram descartados.",
    "LOTE_DIVERGENTE": "Registros do cliente existem, mas nenhum casou com o lote solicitado.",
    "CARNE_SEM_COBRANCA": "Carne localizado, porem sem cobrancas associadas.",
    "COLETA_INCOMPLETA": "Coleta/paginacao possivelmente incompleta.",
    "NAO_SINCRONIZADO": "Dados ainda nao sincronizados (cache ausente/antigo).",
}


def diagnosticar_sem_boleto(cliente_alvo, registros_cliente, registros_terceiros_no_lote=0,
                            houve_coleta=True, cache_disponivel=True):
    """Explica por que um cliente ficou 'sem boleto', sem mascarar falhas."""
    if not cache_disponivel:
        return "NAO_SINCRONIZADO"
    if not houve_coleta:
        return "COLETA_INCOMPLETA"
    if registros_cliente:
        carnes = [r for r in registros_cliente if r.get("fonte") == "carne"]
        cobr = [r for r in registros_cliente if r.get("fonte") != "carne"]
        if carnes and not cobr:
            return "CARNE_SEM_COBRANCA"
        return "LOTE_DIVERGENTE"
    if registros_terceiros_no_lote:
        return "APENAS_TERCEIROS"
    return "NENHUM_REGISTRO_WIDEPAY"
