# -*- coding: utf-8 -*-
"""Abertura de arquivos e pastas no Windows."""

import os
import subprocess
from pathlib import Path


def abrir(path):
    alvo = Path(path)
    if not alvo.exists():
        raise FileNotFoundError(str(alvo))
    if os.name == "nt":
        os.startfile(str(alvo))  # noqa: S606 - abertura local solicitada pelo usuario
    else:
        subprocess.Popen(["xdg-open", str(alvo)])


def abrir_pasta(path):
    alvo = Path(path)
    if alvo.is_file():
        alvo = alvo.parent
    abrir(alvo)
