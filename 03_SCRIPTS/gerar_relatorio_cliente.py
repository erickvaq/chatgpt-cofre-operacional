# -*- coding: utf-8 -*-
import os
import sys
import re
from pathlib import Path

# Ajustar sys.path para carregar os módulos de relatorio e precheck
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "00_SISTEMA_PRECHECK"))
sys.path.append(str(ROOT_DIR / "03_SCRIPTS"))

try:
    from precheck_regras import executar_precheck, normalizar_texto
    executar_precheck("gerar_relatorio_cliente.py")
except ImportError as e:
    print(f"ERRO: Nao foi possivel carregar o precheck de regras: {e}")
    sys.exit(1)

from widepay_bootstrap import garantir_widepay_real_ou_parar
from relatorios_pdf import gerar_pdf, gerar_html, abrir_externo

def extrair_valor_numerico(texto):
    """Extrai float de strings monetarias como 'R$ 4.410,81' ou '4876.45'."""
    limpo = re.sub(r'[^\d,.-]', '', texto)
    if ',' in limpo and '.' in limpo:
        limpo = limpo.replace('.', '').replace(',', '.')
    elif ',' in limpo:
        limpo = limpo.replace(',', '.')
    try:
        return float(limpo)
    except ValueError:
        return 0.0

def proximo_arquivo_disponivel(caminho_inicial):
    caminho = Path(caminho_inicial)
    if not caminho.exists():
        return caminho

    padrao = re.compile(r"(.*_V)(\d+)(\.[^.]+)$", re.IGNORECASE)
    match = padrao.match(caminho.name)
    if not match:
        base = caminho.stem
        sufixo = caminho.suffix
        idx = 2
        while True:
            candidato = caminho.with_name(f"{base}_V{idx}{sufixo}")
            if not candidato.exists():
                return candidato
            idx += 1

    prefixo, num, extensao = match.groups()
    idx = int(num) + 1
    while True:
        candidato = caminho.with_name(f"{prefixo}{idx}{extensao}")
        if not candidato.exists():
            return candidato
        idx += 1

def ler_md_conferencia(caminho_md):
    if not os.path.exists(caminho_md):
        print(f"ERRO: Relatorio de conferencia nao encontrado em {caminho_md}")
        return None, None, None
        
    dados_cliente = {
        'nome': 'Desconhecido',
        'lote': '-',
        'quadra': '-',
        'data_assinatura': '-',
        'vencimento': '-',
        'previsao_quitacao': '-',
        'valor_parcela': 0.0
    }
    
    resumo_financeiro = {
        'total_contrato': 0,
        'parcelas_pagas': 0,
        'parcelas_restantes': 0,
        'percentual_pago': 0.0,
        'percentual_restante': 0.0,
        'valor_pago': 0.0,
        'valor_restante': 0.0
    }
    
    carnes_widepay = []
    
    with open(caminho_md, "r", encoding="utf-8") as f:
        linhas = f.readlines()
        
    secao_atual = 0  # 1 = dados contrato, 2 = dados widepay, 3 = calculo parcelas, 7 = total carnes, 9 = total pago consolidado, 10 = total pendente consolidado, 0 = outros
    
    for linha in linhas:
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue
            
        # Identificar seções para evitar falsos positivos de tabelas de erro ou auditoria
        if "## 1. DADOS DO CONTRATO" in linha:
            secao_atual = 1
            continue
        elif "## 2. DADOS DO WIDEPAY" in linha or "## 2. CARNÊS ENCONTRADOS" in linha or "## 2. CARNES ENCONTRADOS" in linha:
            secao_atual = 2
            continue
        elif "## 3. CÁLCULO" in linha or "## 3. CALCULO" in linha:
            secao_atual = 3
            continue
        elif "## 7. TOTAL PAGO EM CARNÊS" in linha or "## 7. TOTAL PAGO EM CARNES" in linha:
            secao_atual = 7
            continue
        elif "## 9. TOTAL PAGO CONSOLIDADO" in linha:
            secao_atual = 9
            continue
        elif "## 10. TOTAL PENDENTE CONSOLIDADO" in linha:
            secao_atual = 10
            continue
        elif linha_limpa.startswith("## "):
            secao_atual = 0
            continue
            
        # Processar valores fora de tabelas nas novas seções de totais
        if secao_atual == 7 and (linha_limpa.startswith("R$") or "R$" in linha_limpa):
            match = re.search(r'baseado em (\d+) parcelas', linha_limpa, re.IGNORECASE)
            if match:
                resumo_financeiro['parcelas_pagas'] = int(match.group(1))
            continue
        elif secao_atual == 9 and (linha_limpa.startswith("R$") or "R$" in linha_limpa):
            resumo_financeiro['valor_pago'] = extrair_valor_numerico(linha_limpa)
            continue
        elif secao_atual == 10 and (linha_limpa.startswith("R$") or "R$" in linha_limpa):
            resumo_financeiro['valor_restante'] = extrair_valor_numerico(linha_limpa)
            continue
            
        if "|" in linha and secao_atual in (1, 2, 3):
            partes = [p.strip() for p in linha.split("|")]
            # Filtrar cabeçalhos ou divisores
            if len(partes) < 3 or all(c == '-' for c in partes[1]) or partes[1].lower() == "carne":
                continue
                
            if secao_atual == 2 and len(partes) >= 8:
                try:
                    carne_id = partes[1]
                    val_p = extrair_valor_numerico(partes[2])
                    geradas = partes[3]
                    pagas = int(partes[4])
                    recebido = extrair_valor_numerico(partes[5])
                    ult_venc = partes[6]
                    status = partes[7]
                    
                    carnes_widepay.append({
                        'carne': f"Carnê {carne_id}",
                        'valor_parcela': val_p,
                        'parcelas_geradas': geradas,
                        'parcelas_pagas': str(pagas),
                        'total_recebido': recebido,
                        'ultimo_vencimento': ult_venc,
                        'status': status
                    })
                except Exception as e:
                    print(f"[Aviso] Erro ao parsear linha de carne: {linha_limpa} -> {e}")
                continue
                
            col1 = normalizar_texto(partes[1])
            col2 = partes[2].replace("**", "").replace("*", "").strip()
            
            # Dados do Contrato (Seção 1)
            if secao_atual == 1:
                if "cliente" in col1 and not dados_cliente['nome'] != 'Desconhecido':
                    dados_cliente['nome'] = col2
                elif "lote" in col1:
                    dados_cliente['lote'] = col2
                    # Tenta inferir quadra
                    match = re.search(r'([A-H])\s*\d+|\d+\s*,\s*Quadra\s*([A-H])', col2, re.IGNORECASE)
                    if match:
                        dados_cliente['quadra'] = match.group(1) or match.group(2)
                elif "assinatura" in col1:
                    dados_cliente['data_assinatura'] = col2
                elif "vencimento" in col1:
                    dados_cliente['vencimento'] = col2
                elif "quitacao" in col1:
                    dados_cliente['previsao_quitacao'] = col2
                elif "valor de cada parcela" in col1 or "valor da parcela" in col1:
                    dados_cliente['valor_parcela'] = extrair_valor_numerico(col2)
                elif "total de parcelas" in col1:
                    try:
                        resumo_financeiro['total_contrato'] = int(re.sub(r'[^\d]', '', col2))
                    except ValueError:
                        pass
                    
            # Dados Financeiros / Resumo (Seção 3)
            elif secao_atual == 3:
                if "total do contrato" in col1:
                    try:
                        resumo_financeiro['total_contrato'] = int(re.sub(r'[^\d]', '', col2))
                    except ValueError:
                        pass
                elif "parcelas pagas" in col1:
                    try:
                        resumo_financeiro['parcelas_pagas'] = int(re.sub(r'[^\d]', '', col2))
                    except ValueError:
                        pass
                elif "parcelas restantes" in col1:
                    try:
                        resumo_financeiro['parcelas_restantes'] = int(re.sub(r'[^\d]', '', col2))
                    except ValueError:
                        pass
                elif "total pago in reais" in col1 or "total pago" in col1 or "valor total pago" in col1:
                    resumo_financeiro['valor_pago'] = extrair_valor_numerico(col2)
                elif "total ainda a pagar" in col1 or "valor restante" in col1 or "total ainda a pagar (nominal)" in col1:
                    resumo_financeiro['valor_restante'] = extrair_valor_numerico(col2)
                
    # Regra operacional: parcelas restantes so podem nascer do contrato confirmado.
    # O WidePay informa pagamentos/cobrancas; ele nao substitui o total contratado.
    resumo_financeiro['contrato_total_confirmado'] = resumo_financeiro['total_contrato'] > 0

    # Reajustar parcelas restantes e percentuais
    if resumo_financeiro['contrato_total_confirmado']:
        resumo_financeiro['parcelas_restantes'] = max(0, resumo_financeiro['total_contrato'] - resumo_financeiro['parcelas_pagas'])
        resumo_financeiro['percentual_pago'] = resumo_financeiro['parcelas_pagas'] / resumo_financeiro['total_contrato']
        resumo_financeiro['percentual_restante'] = resumo_financeiro['parcelas_restantes'] / resumo_financeiro['total_contrato']
    else:
        resumo_financeiro['parcelas_restantes'] = 0
        resumo_financeiro['percentual_pago'] = 0.0
        resumo_financeiro['percentual_restante'] = 0.0
        
    return dados_cliente, resumo_financeiro, carnes_widepay

def main():
    if len(sys.argv) > 1:
        md_path = sys.argv[1]
    else:
        md_path = input("Digite o caminho do arquivo MD de conferencia: ").strip()
        
    if not os.path.exists(md_path):
        print(f"Caminho invalido: {md_path}")
        sys.exit(1)

    print(f"Lendo dados de conferencia em: {md_path}...")
    dados_cliente, resumo, carnes = ler_md_conferencia(md_path)
    
    if not dados_cliente or not dados_cliente['nome']:
        print("Erro ao ler dados do relatorio.")
        sys.exit(1)

    garantir_widepay_real_ou_parar(dados_cliente['nome'])
        
    print(f"Cliente: {dados_cliente['nome']}")
    print(f"Lote: {dados_cliente['lote']}")
    print(f"Total Contrato: {resumo['total_contrato']}")
    print(f"Parcelas Pagas: {resumo['parcelas_pagas']}")
    print(f"WidePay Carnes: {len(carnes)} encontrado(s)")

    if not resumo.get('contrato_total_confirmado'):
        print("\n[ERRO CRITICO] Contrato nao confirmou o total de parcelas.")
        print("Parcelas restantes devem ser calculadas somente pelo contrato.")
        print("PDF/HTML final bloqueados para evitar relatorio com restantes derivados do WidePay.")
        sys.exit(1)
    
    # Gerar caminhos de saída
    nome_limpo = re.sub(r'[^a-zA-Z0-9]', '_', normalizar_texto(dados_cliente['nome']).upper())
    is_camila = "camila" in normalizar_texto(dados_cliente['nome'])
    
    if is_camila:
        # Padrão específico da Camila V4 para Etapa 5
        pasta_entrega = ROOT_DIR / "02_RELATORIOS_GERADOS" / "CAMILA_FERROLHO_V4_FINAL"
        os.makedirs(pasta_entrega, exist_ok=True)
        pdf_saida = proximo_arquivo_disponivel(ROOT_DIR / "02_RELATORIOS_GERADOS" / "RESUMO_FINANCEIRO_CAMILA_FERROLHO_CORRIGIDO_V4.pdf")
        html_saida_previa = proximo_arquivo_disponivel(ROOT_DIR / "02_RELATORIOS_GERADOS" / "RESUMO_FINANCEIRO_CAMILA_FERROLHO_CORRIGIDO_V4_PREVIA.html")
    else:
        pasta_entrega = ROOT_DIR / "02_RELATORIOS_GERADOS" / f"{nome_limpo}_V3_FINAL"
        os.makedirs(pasta_entrega, exist_ok=True)
        pdf_saida = proximo_arquivo_disponivel(pasta_entrega / f"RESUMO_FINANCEIRO_{nome_limpo}_CORRIGIDO_V3.pdf")
        html_saida_previa = proximo_arquivo_disponivel(ROOT_DIR / "02_RELATORIOS_GERADOS" / f"RESUMO_FINANCEIRO_{nome_limpo}_CORRIGIDO_V3_PREVIA.html")
        
    # Gerar PDF
    print("\nGerando PDF...")
    ok_pdf = gerar_pdf(dados_cliente, resumo, carnes, str(pdf_saida))
    
    # Gerar prévia HTML
    print("Gerando Previa HTML...")
    gerar_html(dados_cliente, resumo, carnes, str(html_saida_previa))
    
    # Criar atalho BAT de abertura relativa (REGRA 16)
    bat_saida = pasta_entrega / "01_ABRIR_PDF_FINAL.bat"
    with open(bat_saida, "w", encoding="utf-8") as f:
        f.write(f'@echo off\ncd /d "%~dp0"\nstart "" "{pdf_saida.name}"\n')
    print(f"BAT de abertura criado em: {bat_saida}")
    
    # Validar Camila se for ela
    if is_camila:
        print("\n[PRECHECK VALIDADOR CAMILA] Executando validacao automatica especifica...")
        import subprocess
        validador_path = str(ROOT_DIR / "00_SISTEMA_PRECHECK" / "validar_relatorio_camila.py")
        
        # Validar PDF
        res_pdf = subprocess.run([sys.executable, validador_path, str(pdf_saida)], capture_output=True, text=True)
        # Validar HTML
        res_html = subprocess.run([sys.executable, validador_path, str(html_saida_previa)], capture_output=True, text=True)
        
        if res_pdf.returncode != 0 or res_html.returncode != 0:
            print("\n[ERRO CRITICO] Validador de dados da Camila Ferrolho detectou erros!")
            print("PDF stdout:\n", res_pdf.stdout)
            print("PDF stderr:\n", res_pdf.stderr)
            print("HTML stdout:\n", res_html.stdout)
            print("HTML stderr:\n", res_html.stderr)
            print("A geracao e entrega foram bloqueadas.")
            sys.exit(1)
        else:
            print("Validador da Camila Ferrolho passou com sucesso!")
            
    if ok_pdf:
        # Abrir externamente (REGRA 9 & 16)
        print("\nAbrindo arquivos gerados externamente...")
        abrir_externo(str(pdf_saida))
        abrir_externo(str(html_saida_previa))
        abrir_externo(str(pasta_entrega))
        print("\nProcesso finalizado com sucesso!")
        
if __name__ == "__main__":
    main()
