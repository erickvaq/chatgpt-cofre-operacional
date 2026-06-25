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
    total_contrato = total_contrato_confirmado()
    if total_contrato <= 0:
        raise ValueError(
            "contrato nao confirmou total de parcelas; nao validar restantes por parcelas geradas no WidePay"
        )
    restantes = max(0, total_contrato - pagas)
    percentual = int((pagas / total_contrato) * 100) if total_contrato else 0
    return [
        f"{pagas} de {total_contrato}",
        f"{restantes} parcelas",
        f"{percentual}%",
    ]


def total_contrato_confirmado():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    md_path = os.path.join(
        root_dir,
        "07_DADOS_TEMPORARIOS",
        "CONFERENCIA_CALCULOS_CAMILA_DE_OLIVEIRA_FERROLHO.md",
    )
    if not os.path.exists(md_path):
        raise FileNotFoundError(md_path)
    conteudo = ler_arquivo(md_path)
    match = re.search(r"Total de parcelas\s*\|\s*\*\*(\d+)\s+parcelas\*\*", conteudo, re.IGNORECASE)
    if not match:
        raise ValueError("total de parcelas do contrato nao encontrado na conferencia")
    return int(match.group(1))


def validar(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo nao encontrado: {caminho_arquivo}")
        return False

    conteudo_norm = normalizar_texto(ler_arquivo(caminho_arquivo))
    try:
        termos_obrigatorios = termos_atuais_widepay()
    except Exception as e:
        print(f"ERRO: validacao bloqueada: {e}")
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
