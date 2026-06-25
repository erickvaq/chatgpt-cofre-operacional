# -*- coding: utf-8 -*-
import json
import os
import re
import sys


def normalizar_texto(texto):
    if not texto:
        return ""
    return re.sub(r"\s+", " ", texto).lower()


def extrair_texto_pdf(caminho_pdf):
    try:
        import pypdf
        reader = pypdf.PdfReader(caminho_pdf)
        return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        print(f"Erro ao ler PDF {caminho_pdf}: {e}")
        sys.exit(1)


def ler_arquivo(caminho):
    if os.path.splitext(caminho)[1].lower() == ".pdf":
        return extrair_texto_pdf(caminho)
    for encoding in ("utf-8", "latin-1"):
        try:
            with open(caminho, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    print(f"Erro ao ler arquivo {caminho}")
    sys.exit(1)


def termos_atuais_widepay():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    json_path = os.path.join(
        root_dir,
        "07_DADOS_TEMPORARIOS",
        "WIDEPAY_CONSULTAS",
        "WIDEPAY_CAMILA_DE_OLIVEIRA_FERROLHO.json",
    )
    if not os.path.exists(json_path):
        raise FileNotFoundError(json_path)
    with open(json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)
    totais = dados.get("totais_carnes") or {}
    pagas = int(totais.get("parcelas_pagas", 0))
    geradas = int(totais.get("parcelas_geradas", 0))
    restantes = max(0, geradas - pagas)
    percentual = int((pagas / geradas) * 100) if geradas else 0
    return [
        f"{pagas} de {geradas}",
        f"{restantes} parcelas",
        f"{percentual}%",
    ]


def validar(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo nao encontrado: {caminho_arquivo}")
        return False

    conteudo_norm = normalizar_texto(ler_arquivo(caminho_arquivo))
    try:
        termos_obrigatorios = termos_atuais_widepay()
    except Exception as e:
        print(f"ERRO: nao foi possivel carregar JSON atual do WidePay: {e}")
        return False

    erros = [termo for termo in termos_obrigatorios if termo.lower() not in conteudo_norm]
    if erros:
        print(f"\n--- FALHA NA VALIDACAO DE DADOS: {os.path.basename(caminho_arquivo)} ---")
        for termo in erros:
            print(f"  [X] Termo obrigatorio ausente: '{termo}'")
        print("---------------------------------------------------\n")
        return False

    print(f"SUCESSO: Arquivo {os.path.basename(caminho_arquivo)} passou na validacao WidePay atual.")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python validar_relatorio_camila.py <caminho_do_arquivo>")
        sys.exit(1)
    sys.exit(0 if validar(sys.argv[1]) else 1)
