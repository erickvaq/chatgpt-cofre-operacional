from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from tkinter import Tk, messagebox


def show_error(title: str, text: str) -> int:
    root = Tk()
    root.withdraw()
    try:
        messagebox.showerror(title, text)
    finally:
        root.destroy()
    return 1


def detectar_base_dir() -> Path:
    exe_dir = Path(sys.executable).resolve().parent
    if (exe_dir / "WideAPP_EXTRA").exists():
        return exe_dir
    script_dir = Path(__file__).resolve().parent
    if script_dir.name.lower() == "wideapp_extra":
        return script_dir.parent
    return exe_dir


def main() -> int:
    base_dir = detectar_base_dir()
    app_dir = base_dir / "WideAPP_EXTRA"
    app_bat = app_dir / "INICIAR_WIDEAPP_EXTRA.bat"

    if not app_dir.exists():
        return show_error("WideAPP_EXTRA", f"Pasta da aplicacao nao encontrada:\n{app_dir}")
    if not app_bat.exists():
        return show_error("WideAPP_EXTRA", f"Launcher interno nao encontrado:\n{app_bat}")

    os.startfile(str(app_bat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
