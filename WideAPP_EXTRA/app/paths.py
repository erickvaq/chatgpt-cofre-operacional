# -*- coding: utf-8 -*-
"""Gerenciador central de caminhos da WideAPP_EXTRA para portabilidade."""

import sys
from pathlib import Path

def get_app_root() -> Path:
    """
    Retorna a raiz operacional da aplicação.
    Diferencia execução empacotada (.exe) de script Python.
    """
    if getattr(sys, "frozen", False):
        # Executando como executável compilado (.exe)
        return Path(sys.executable).resolve().parent

    # Executando como script Python (.py)
    # Busca o ancestral que contém a pasta 'WideAPP_EXTRA'
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "WideAPP_EXTRA").exists():
            return parent

    # Fallback para o diretório atual de trabalho
    return Path.cwd().resolve()


def get_visual_database_path() -> Path:
    """Retorna o caminho do banco de dados visual do usuário (XLSX) na raiz do app."""
    return get_app_root() / "BANCO_DADOS_WIDEAPP_EXTRA.xlsx"


def get_backups_dir() -> Path:
    """Retorna e garante a existência da pasta de backups na raiz do app."""
    path = get_app_root() / "backups"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_internal_data_dir() -> Path:
    """Retorna e garante a existência da pasta técnica de dados da aplicação."""
    path = get_app_root() / "WideAPP_EXTRA" / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path
