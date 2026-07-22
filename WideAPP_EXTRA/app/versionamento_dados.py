# -*- coding: utf-8 -*-
"""Snapshots imutaveis e verificaveis dos bancos internos da WideAPP."""

import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from app import paths


def _contar_registros_json(caminho):
    try:
        payload = json.loads(Path(caminho).read_text(encoding="utf-8"))
    except Exception:
        return None
    registros = payload.get("registros") if isinstance(payload, dict) else None
    return len(registros) if isinstance(registros, list) else None


def criar_snapshot_versionado(caminho, categoria="dados"):
    """Copia a versao atual antes da troca e grava hash/contagem em metadados."""
    origem = Path(caminho)
    if not origem.exists() or not origem.is_file():
        return None

    conteudo = origem.read_bytes()
    digest = hashlib.sha256(conteudo).hexdigest()
    destino_dir = paths.get_backups_dir() / "historico_dados" / categoria
    destino_dir.mkdir(parents=True, exist_ok=True)

    # Evita gerar varias copias identicas em aberturas sucessivas.
    existentes = list(destino_dir.glob(f"*_{digest[:12]}{origem.suffix}"))
    if existentes:
        return existentes[-1]

    agora = datetime.now()
    carimbo = agora.strftime("%Y%m%d_%H%M%S_%f")
    destino = destino_dir / f"{origem.stem}_{carimbo}_{digest[:12]}{origem.suffix}"
    temporario = destino.with_name(destino.name + ".tmp")
    meta = destino.with_suffix(destino.suffix + ".meta.json")
    meta_tmp = meta.with_name(meta.name + ".tmp")
    try:
        with open(origem, "rb") as entrada, open(temporario, "wb") as saida:
            shutil.copyfileobj(entrada, saida)
            saida.flush()
            os.fsync(saida.fileno())
        if hashlib.sha256(temporario.read_bytes()).hexdigest() != digest:
            raise IOError("Hash do snapshot divergiu do arquivo de origem.")
        os.replace(temporario, destino)

        metadados = {
            "criado_em": agora.isoformat(timespec="microseconds"),
            "categoria": categoria,
            "arquivo_origem": str(origem),
            "arquivo_snapshot": str(destino),
            "sha256": digest,
            "bytes": len(conteudo),
            "total_registros": _contar_registros_json(origem),
        }
        with open(meta_tmp, "w", encoding="utf-8") as saida:
            json.dump(metadados, saida, ensure_ascii=False, indent=2)
            saida.flush()
            os.fsync(saida.fileno())
        os.replace(meta_tmp, meta)
        return destino
    finally:
        for pendente in (temporario, meta_tmp):
            try:
                pendente.unlink(missing_ok=True)
            except OSError:
                pass
