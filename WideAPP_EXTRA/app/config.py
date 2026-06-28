# -*- coding: utf-8 -*-
"""Configuracao central da WideAPP_EXTRA."""

import os
from pathlib import Path
from app import paths


APP_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = paths.get_app_root()
DATA_DIR = paths.get_internal_data_dir()
LOG_DIR = APP_DIR / "logs"
OUTPUT_DIR = ROOT_DIR / "02_RELATORIOS_GERADOS"
TEMP_DIR = ROOT_DIR / "07_DADOS_TEMPORARIOS"
PRECHECK_DIR = ROOT_DIR / "00_SISTEMA_PRECHECK"
VENV_PYTHON = APP_DIR / ".venv" / "Scripts" / "python.exe"
EXECUTOR = APP_DIR / "executar_auditoria.py"
CLIENTES_JSON = DATA_DIR / "clientes_indexados.json"
CLIENTES_XLSX = DATA_DIR / "clientes_indexados.xlsx"
WIDEPAY_BOLETOS_CACHE_JSON = DATA_DIR / "widepay_boletos_cache.json"
WIDEPAY_BOLETOS_CACHE_XLSX = DATA_DIR / "widepay_boletos_cache.xlsx"
VISUAL_XLSX = paths.get_visual_database_path()
LINKS_DRIVE_MD = APP_DIR / "LINKS_GOOGLE_DRIVE.md"
RCLONE_EXE = ROOT_DIR / "ferramentas" / "rclone" / "rclone.exe"
RCLONE_REMOTE = os.environ.get("WIDEAPP_RCLONE_REMOTE", "").strip()
DRIVE_LOCAL_DIR = os.environ.get("WIDEAPP_DRIVE_LOCAL", "").strip() or str(APP_DIR / "drive_local")

CONTRATOS_DIR = Path(
    os.environ.get(
        "WIDEAPP_CONTRATOS_DIR",
        r"C:\Users\Windows User\Desktop\AGUA VIVA\- CONTRATOS AGUA VIVA",
    )
)


def ensure_dirs():
    for path in (DATA_DIR, LOG_DIR, OUTPUT_DIR, TEMP_DIR, Path(DRIVE_LOCAL_DIR), paths.get_backups_dir()):
        path.mkdir(parents=True, exist_ok=True)
