# -*- coding: utf-8 -*-
"""Upload/manifesto Google Drive para arquivos finais."""

import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from app import config


def registrar_manifesto(itens, grupo):
    config.ensure_dirs()
    linhas = []
    if not config.LINKS_DRIVE_MD.exists():
        linhas.extend(
            [
                "# Links Google Drive - WideAPP_EXTRA",
                "",
                "| Data/hora | Grupo | Cliente | Lote | Arquivo | Caminho local | Link Google Drive | Status |",
                "|---|---|---|---|---|---|---|---|",
            ]
        )
    timestamp = datetime.now().isoformat(timespec="seconds")
    for item in itens:
        linhas.append(
            f"| {timestamp} | {grupo} | {item.get('cliente', '')} | {item.get('lote', '')} | "
            f"{item.get('arquivo', '')} | `{item.get('caminho_local', '')}` | "
            f"{item.get('link', '')} | {item.get('status', '')} |"
        )
    with open(config.LINKS_DRIVE_MD, "a", encoding="utf-8") as f:
        if config.LINKS_DRIVE_MD.stat().st_size > 0:
            f.write("\n")
        f.write("\n".join(linhas) + "\n")
    return config.LINKS_DRIVE_MD


def enviar_arquivos(arquivos, grupo="GRUPO"):
    resultados = []
    destino_relativo = f"Relatorio_WidePay_Lotes/WideAPP_EXTRA/{datetime.now().strftime('%Y-%m-%d')}/{grupo}"

    if config.RCLONE_REMOTE and config.RCLONE_EXE.exists():
        for arquivo in arquivos:
            arquivo_path = Path(arquivo["caminho_local"])
            cmd = [
                str(config.RCLONE_EXE),
                "copy",
                str(arquivo_path),
                f"{config.RCLONE_REMOTE}:{destino_relativo}",
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            status = "ENVIADO_RCLONE" if proc.returncode == 0 else f"ERRO_RCLONE: {proc.stderr.strip()}"
            resultados.append({**arquivo, "link": f"{config.RCLONE_REMOTE}:{destino_relativo}/{arquivo_path.name}", "status": status})
    elif config.DRIVE_LOCAL_DIR:
        destino = Path(config.DRIVE_LOCAL_DIR) / destino_relativo
        destino.mkdir(parents=True, exist_ok=True)
        for arquivo in arquivos:
            arquivo_path = Path(arquivo["caminho_local"])
            destino_arquivo = destino / arquivo_path.name
            shutil.copy2(arquivo_path, destino_arquivo)
            resultados.append({**arquivo, "link": str(destino_arquivo), "status": "COPIADO_DRIVE_LOCAL"})
    else:
        for arquivo in arquivos:
            resultados.append(
                {
                    **arquivo,
                    "link": "",
                    "status": "PENDENTE_CONFIGURACAO_DRIVE",
                }
            )

    registrar_manifesto(resultados, grupo)
    return resultados


def abrir_destino_drive(grupo="GRUPO"):
    if config.DRIVE_LOCAL_DIR:
        destino = Path(config.DRIVE_LOCAL_DIR) / f"Relatorio_WidePay_Lotes/WideAPP_EXTRA/{datetime.now().strftime('%Y-%m-%d')}/{grupo}"
        destino.mkdir(parents=True, exist_ok=True)
        return destino
    if config.RCLONE_REMOTE:
        return f"{config.RCLONE_REMOTE}:Relatorio_WidePay_Lotes/WideAPP_EXTRA/{datetime.now().strftime('%Y-%m-%d')}/{grupo}"
    return None
