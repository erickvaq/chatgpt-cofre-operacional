# -*- coding: utf-8 -*-
"""Filtros de pesquisa para clientes indexados."""

import re

from app.indexador_clientes import slug_busca


def intervalo_letras(termo):
    match = re.fullmatch(r"\s*([a-zA-Z])\s*a\s*([a-zA-Z])\s*", termo or "")
    if not match:
        return None
    ini, fim = match.group(1).lower(), match.group(2).lower()
    if ini > fim:
        ini, fim = fim, ini
    return ini, fim


def corresponde(item, termo="", status="Todos"):
    if status and status != "Todos" and item.get("status") != status:
        return False
    termo = (termo or "").strip()
    if not termo:
        return True
    termo_norm = slug_busca(termo)
    nome_norm = slug_busca(item.get("cliente", ""))
    lote_norm = slug_busca(item.get("lote", ""))
    quadra_norm = slug_busca(item.get("quadra", ""))
    intervalo = intervalo_letras(termo)
    if intervalo:
        inicial = nome_norm[:1]
        return intervalo[0] <= inicial <= intervalo[1]
    if len(termo_norm) == 1 and termo_norm.isalpha():
        return nome_norm.startswith(termo_norm)
    if termo_norm.startswith("quadra "):
        return quadra_norm == termo_norm.replace("quadra ", "").strip()
    return termo_norm in nome_norm or termo_norm in lote_norm or termo_norm in quadra_norm


def filtrar(registros, termo="", status="Todos"):
    return [item for item in registros if corresponde(item, termo, status)]
