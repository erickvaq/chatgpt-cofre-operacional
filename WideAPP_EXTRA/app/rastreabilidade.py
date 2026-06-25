# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def registrar_log(status, acao, cliente, detalhes=""):
    """Escreve um registro no log global da auditoria (07_DADOS_TEMPORARIOS/auditoria_rastreabilidade.jsonl)."""
    pasta_logs = ROOT_DIR / "07_DADOS_TEMPORARIOS"
    os.makedirs(pasta_logs, exist_ok=True)
    caminho_log = pasta_logs / "auditoria_rastreabilidade.jsonl"
    
    registro = {
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "acao": acao,
        "cliente": cliente,
        "detalhes": detalhes
    }
    
    with open(caminho_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        
    print(f"[{status}] {acao} - {cliente} : {detalhes}")

def preparar_diretorio_entrega(cliente, lote):
    """Cria e retorna a pasta dedicada de entrega dos relatórios finais do cliente."""
    nome_limpo = re_slug(cliente)
    lote_slug = re_slug(lote)
    
    pasta = ROOT_DIR / "02_RELATORIOS_GERADOS" / f"{nome_limpo}_LOTE_{lote_slug}_FINAL"
    os.makedirs(pasta, exist_ok=True)
    return pasta

def re_slug(texto):
    if not texto:
        return "INDETERMINADO"
    texto = texto.upper().strip()
    texto = re_sub_slug(texto)
    return texto

def re_sub_slug(texto):
    import re
    import unicodedata
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^A-Z0-9]+", "_", texto)
    return texto.strip("_")
