# -*- coding: utf-8 -*-
"""Configuracao central da WideAPP_EXTRA."""

import os
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = APP_DIR.parent
DATA_DIR = APP_DIR / "data"
LOG_DIR = APP_DIR / "logs"
OUTPUT_DIR = ROOT_DIR / "02_RELATORIOS_GERADOS"
TEMP_DIR = ROOT_DIR / "07_DADOS_TEMPORARIOS"
PRECHECK_DIR = ROOT_DIR / "00_SISTEMA_PRECHECK"
VENV_PYTHON = APP_DIR / ".venv" / "Scripts" / "python.exe"
EXECUTOR = APP_DIR / "executar_auditoria.py"
CLIENTES_JSON = DATA_DIR / "clientes_indexados.json"
CLIENTES_XLSX = DATA_DIR / "clientes_indexados.xlsx"
LINKS_DRIVE_MD = APP_DIR / "LINKS_GOOGLE_DRIVE.md"
RCLONE_EXE = ROOT_DIR / "ferramentas" / "rclone" / "rclone.exe"
RCLONE_REMOTE = os.environ.get("WIDEAPP_RCLONE_REMOTE", "").strip()
DRIVE_LOCAL_DIR = os.environ.get("WIDEAPP_DRIVE_LOCAL", "").strip()

CONTRATOS_DIR = Path(
    os.environ.get(
        "WIDEAPP_CONTRATOS_DIR",
        r"C:\Users\Windows User\Desktop\AGUA VIVA\- CONTRATOS AGUA VIVA",
    )
)


def ensure_dirs():
    for path in (DATA_DIR, LOG_DIR, OUTPUT_DIR, TEMP_DIR):
        path.mkdir(parents=True, exist_ok=True)
