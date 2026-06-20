# -*- coding: utf-8 -*-
"""
Script de correção fina para a entrega do cliente fictício.
Lê o MD de conferência V2 e gera os arquivos PDF, HTML e BAT na mesma pasta.
"""
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "00_SISTEMA_PRECHECK"))
sys.path.append(str(ROOT_DIR / "03_SCRIPTS"))

try:
    from precheck_regras import executar_precheck
    executar_precheck("gerar_teste_uso_real_v2.py")
except ImportError as e:
    print(f"ERRO: Nao foi possivel carregar o precheck: {e}")
    sys.exit(1)

from relatorios_pdf import gerar_pdf, gerar_html, abrir_externo
from gerar_relatorio_cliente import ler_md_conferencia

def main():
    md_path = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "CONFERENCIA_CALCULOS_CLIENTE_TESTE_USO_REAL_2026-06-20_V2.md"
    
    if not md_path.exists():
        print(f"Caminho inválido: {md_path}")
        sys.exit(1)
        
    print(f"Lendo dados de conferencia em: {md_path}...")
    dados_cliente, resumo, carnes = ler_md_conferencia(str(md_path))
    
    if not dados_cliente or not dados_cliente['nome']:
        print("Erro ao ler dados do relatorio.")
        sys.exit(1)
        
    # Caminhos solicitados pelo usuário
    pasta_entrega = ROOT_DIR / "02_RELATORIOS_GERADOS" / "CLIENTE_TESTE_USO_REAL_2026-06-20_V2_FINAL"
    os.makedirs(pasta_entrega, exist_ok=True)
    
    pdf_saida = pasta_entrega / "RESUMO_FINANCEIRO_CLIENTE_TESTE_USO_REAL_2026-06-20_V2.pdf"
    html_saida_previa = pasta_entrega / "RESUMO_FINANCEIRO_CLIENTE_TESTE_USO_REAL_2026-06-20_V2_PREVIA.html"
    bat_pdf = pasta_entrega / "01_ABRIR_PDF_FINAL.bat"
    bat_html = pasta_entrega / "02_ABRIR_PREVIA_HTML.bat"
    
    # Gerar PDF e HTML na mesma pasta
    print("\nGerando PDF...")
    ok_pdf = gerar_pdf(dados_cliente, resumo, carnes, str(pdf_saida))
    
    print("Gerando Previa HTML...")
    gerar_html(dados_cliente, resumo, carnes, str(html_saida_previa))
    
    # Gerar BATs relativos
    with open(bat_pdf, "w", encoding="utf-8") as f:
        f.write('@echo off\ncd /d "%~dp0"\nstart "" "RESUMO_FINANCEIRO_CLIENTE_TESTE_USO_REAL_2026-06-20_V2.pdf"\n')
        
    with open(bat_html, "w", encoding="utf-8") as f:
        f.write('@echo off\ncd /d "%~dp0"\nstart "" "RESUMO_FINANCEIRO_CLIENTE_TESTE_USO_REAL_2026-06-20_V2_PREVIA.html"\n')
        
    print("BATs relativos gerados com sucesso.")
    
    if ok_pdf:
        print("\nAbrindo arquivos gerados externamente...")
        abrir_externo(str(pdf_saida))
        abrir_externo(str(html_saida_previa))
        abrir_externo(str(pasta_entrega))
        print("\nProcesso finalizado com sucesso!")

if __name__ == "__main__":
    main()
