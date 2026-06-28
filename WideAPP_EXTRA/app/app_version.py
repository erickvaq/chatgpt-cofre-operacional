# -*- coding: utf-8 -*-
"""Fonte central da versao da WideAPP_EXTRA."""

from pathlib import Path


VERSION_FILE = Path(__file__).resolve().parents[1] / "VERSION"
DEFAULT_APP_VERSION = "V0.0-UNKNOWN"


def load_app_version():
    try:
        value = VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        value = ""
    return value or DEFAULT_APP_VERSION


APP_VERSION = load_app_version()
APP_VERSION_LABEL = f"Versao {APP_VERSION}"
APP_WINDOW_TITLE = f"WideAPP_EXTRA - {APP_VERSION_LABEL}"
