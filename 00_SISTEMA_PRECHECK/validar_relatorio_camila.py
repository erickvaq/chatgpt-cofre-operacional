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
    raise NotImplementedError("Use validar() com o conteudo do arquivo alvo")


def validar(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo nao encontrado: {caminho_arquivo}")
        return False

    conteudo_norm = normalizar_texto(ler_arquivo(caminho_arquivo))
    try:
        if "contrato nao confirmado" in conteudo_norm:
            raise ValueError("relatorio ainda marcado como contrato nao confirmado")

        match = re.search(r"(\d+)\s+de\s+(\d+)", conteudo_norm)
        if not match:
            raise ValueError("nao foi possivel identificar o total de parcelas no relatorio")
        pagas = int(match.group(1))
        total_contrato = int(match.group(2))
        if total_contrato <= 0:
            raise ValueError("total de parcelas invalido no relatorio")

        restantes = max(0, total_contrato - pagas)
        percentual = int((pagas / total_contrato) * 100) if total_contrato else 0
        termos_obrigatorios = [
            f"{pagas} de {total_contrato}",
            f"{restantes} parcelas",
            f"{percentual}%",
        ]
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
