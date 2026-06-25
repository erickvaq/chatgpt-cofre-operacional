# -*- coding: utf-8 -*-
import os
import sys
import re
from pathlib import Path

# Ajustar sys.path para carregar os mÃ³dulos de relatorio e precheck
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

def dividir_linha_md_tabela(linha):
    conteudo = linha.strip().strip("|")
    if not conteudo:
        return []
    return [p.strip() for p in conteudo.split("|")]

def identificar_referencias_pagamento(descricao):
    texto = normalizar_texto(descricao or "")
    refs = []
    meses_nome = {
        "janeiro": "01", "jan": "01", "fevereiro": "02", "fev": "02",
        "marco": "03", "mar": "03", "abril": "04", "abr": "04",
        "maio": "05", "mai": "05", "junho": "06", "jun": "06",
        "julho": "07", "jul": "07", "agosto": "08", "ago": "08",
        "setembro": "09", "set": "09", "outubro": "10", "out": "10",
        "novembro": "11", "nov": "11", "dezembro": "12", "dez": "12",
    }
    for nome, numero in meses_nome.items():
        if re.search(rf"\b{re.escape(nome)}\b", texto) and numero not in refs:
            refs.append(numero)

    termos_ref = ("ref", "referente", "atraso", "atrazo", "parcela", "apart", "competencia", "mes", "meses")
    if any(t in texto for t in termos_ref):
        for token in re.findall(r"\b\d{1,2}\b", texto):
            try:
                mes = int(token)
            except ValueError:
                continue
            if 1 <= mes <= 12:
                ref = f"{mes:02d}"
                if ref not in refs:
                    refs.append(ref)
    return refs

def interpretar_pagamentos_recebidos(dados_cliente, resumo_financeiro, cobrancas_widepay):
    valor_base = float(dados_cliente.get("valor_parcela") or 0.0)
    pagamentos = []
    total_recebido = 0.0
    parcelas_equivalentes = 0
    divergencias = []

    for cob in cobrancas_widepay.get("cobrancas_encontradas", []):
        status = str(cob.get("status", "")).strip().lower()
        if "recebido" not in status:
            continue

        tipo_original = str(cob.get("tipo", "") or "").strip()
        tipo_norm = normalizar_texto(tipo_original)
        descricao = str(cob.get("descricao", "") or "").strip()
        refs = identificar_referencias_pagamento(descricao)
        valor_original = float(cob.get("valor_original") or 0.0)
        valor_recebido = float(cob.get("valor_recebido") or 0.0)
        observacao = []

        if refs:
            qtd = len(refs)
            observacao.append("referencias identificadas na descricao")
        elif "carn" in tipo_norm:
            qtd = 1
            venc = str(cob.get("vencimento", "") or "").strip()
            refs = [venc] if venc else ["vencimento do boleto"]
            observacao.append("boleto de carne tratado pelo vencimento")
        elif valor_base > 0 and valor_original > 0:
            proporcao = valor_original / valor_base
            qtd = max(1, int(round(proporcao)))
            if abs(proporcao - qtd) <= 0.20:
                observacao.append("quantidade inferida por valor original/base da parcela")
            else:
                observacao.append("REFERENCIA NAO IDENTIFICADA - proporcao de valor nao exata")
                divergencias.append(f"Recebimento {cob.get('id')} sem referencia clara e proporcao {proporcao:.2f}")
        else:
            qtd = 1
            observacao.append("REFERENCIA NAO IDENTIFICADA")
            divergencias.append(f"Recebimento {cob.get('id')} sem referencia e sem valor base suficiente")

        total_recebido += valor_recebido
        parcelas_equivalentes += qtd
        pagamentos.append({
            "cliente": dados_cliente.get("nome", "-"),
            "lote_quadra": f"{dados_cliente.get('lote', '-')} / {dados_cliente.get('quadra', '-')}",
            "id": cob.get("id", "-"),
            "tipo": tipo_original or "cobranca",
            "descricao": descricao or "-",
            "vencimento": cob.get("vencimento", "-"),
            "pagamento": cob.get("pagamento", "-"),
            "valor_original": valor_original,
            "valor_recebido": valor_recebido,
            "valor_base_parcela": valor_base,
            "referencias": ", ".join(refs) if refs else "REFERENCIA NAO IDENTIFICADA",
            "parcelas_quitadas": qtd,
            "observacao": "; ".join(observacao),
        })

    cobrancas_widepay["pagamentos_interpretados"] = pagamentos
    cobrancas_widepay["divergencias_interpretacao"] = divergencias
    if pagamentos:
        resumo_financeiro["parcelas_pagas"] = parcelas_equivalentes
        resumo_financeiro["valor_pago"] = round(total_recebido, 2)
    return pagamentos

def validar_interpretacao_pagamentos(resumo_financeiro, cobrancas_widepay):
    recebidos = [
        c for c in cobrancas_widepay.get("cobrancas_encontradas", [])
        if "recebido" in str(c.get("status", "")).strip().lower()
    ]
    interpretados = cobrancas_widepay.get("pagamentos_interpretados", [])
    erros = []
    if len(recebidos) != len(interpretados):
        erros.append(f"recebidos no WidePay={len(recebidos)} interpretados={len(interpretados)}")
    if recebidos and not interpretados:
        erros.append("nenhum pagamento recebido foi interpretado")
    if not resumo_financeiro.get("contrato_total_confirmado"):
        erros.append("contrato sem total de parcelas confirmado")
    return erros

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
        'valor_restante': 0.0,
        'valor_total_contrato': 0.0,
        'percentual_financeiro_pago': 0.0
    }
    
    carnes_widepay = []
    cobrancas_widepay = {
        'cobrancas_encontradas': [],
        'boletos_avulsos_recebidos': [],
        'boletos_avulsos_abertos': [],
        'duplicidades': [],
        'boletos_avulsos_abertos_texto': [],
    }
    
    with open(caminho_md, "r", encoding="utf-8") as f:
        linhas = f.readlines()
        
    secao_atual = 0  # 1 contrato, 2 carnes, 3 cobrancas, 4 avulsos pagos, 5 avulsos abertos, 6 duplicidades, 30 calculos
    
    for linha in linhas:
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue
            
        # Identificar seÃ§Ãµes para evitar falsos positivos de tabelas de erro ou auditoria
        if "## 1. DADOS DO CONTRATO" in linha:
            secao_atual = 1
            continue
        elif "## 2. CARN" in linha or "## 2. DADOS DO WIDEPAY" in linha:
            secao_atual = 2
            continue
        elif "## 3. CÃLCULO" in linha or "## 3. CALCULO" in linha:
            secao_atual = 30
            continue
        elif "## 3. COBRAN" in linha:
            secao_atual = 3
            continue
        elif "## 4. BOLETOS AVULSOS RECEBIDOS" in linha:
            secao_atual = 4
            continue
        elif "## 5. BOLETOS AVULSOS EM ABERTO" in linha:
            secao_atual = 5
            continue
        elif "## 6. POSS" in linha:
            secao_atual = 6
            continue
        elif "## 7. TOTAL PAGO EM CARN" in linha:
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
            
        # Processar valores fora de tabelas nas novas seÃ§Ãµes de totais
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
            
        if "|" in linha and secao_atual in (1, 2, 3, 4, 5, 6):
            partes = dividir_linha_md_tabela(linha)
            # Filtrar cabeÃ§alhos ou divisores
            if len(partes) < 2 or all(c == '-' for c in partes[0]) or partes[0].lower() in {"carne", "carne", "id", "campo"} or partes[0].lower().startswith("carn"):
                continue
                
            if secao_atual == 2 and len(partes) >= 7:
                try:
                    carne_id = partes[0]
                    val_p = extrair_valor_numerico(partes[1])
                    geradas = partes[2]
                    pagas = int(re.sub(r'[^\d]', '', partes[3]) or 0)
                    recebido = extrair_valor_numerico(partes[4])
                    ult_venc = partes[5]
                    status = partes[6]
                    
                    carnes_widepay.append({
                        'carne': f"CarnÃª {carne_id}",
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
            if secao_atual == 3 and len(partes) >= 8:
                try:
                    if partes[0].lower() == "id" or partes[0].startswith("---"):
                        continue
                    tipo = partes[7] if len(partes) > 7 else ""
                    cobrancas_widepay['cobrancas_encontradas'].append({
                        'id': partes[0],
                        'forma': partes[1],
                        'descricao': partes[2],
                        'valor_original': extrair_valor_numerico(partes[3]),
                        'valor_recebido': extrair_valor_numerico(partes[4]),
                        'vencimento': partes[5],
                        'status': partes[6],
                        'tipo': tipo,
                    })
                except Exception as e:
                    print(f"[Aviso] Erro ao parsear linha de cobranca: {linha_limpa} -> {e}")
                continue
            if secao_atual == 4 and len(partes) >= 6:
                try:
                    if partes[0].lower() == "id" or partes[0].startswith("---"):
                        continue
                    cobrancas_widepay['boletos_avulsos_recebidos'].append({
                        'id': partes[0],
                        'descricao': partes[1],
                        'valor_recebido': extrair_valor_numerico(partes[2]),
                        'vencimento': partes[3],
                        'pagamento': partes[4],
                        'status': partes[5],
                    })
                except Exception as e:
                    print(f"[Aviso] Erro ao parsear linha de boleto avulso recebido: {linha_limpa} -> {e}")
                continue
            if secao_atual == 5:
                if len(partes) >= 5:
                    try:
                        if partes[0].lower() == "id" or partes[0].startswith("---"):
                            continue
                        cobrancas_widepay['boletos_avulsos_abertos'].append({
                            'id': partes[0],
                            'descricao': partes[1],
                            'valor_original': extrair_valor_numerico(partes[2]),
                            'vencimento': partes[3],
                            'status': partes[4],
                        })
                    except Exception as e:
                        print(f"[Aviso] Erro ao parsear linha de boleto avulso em aberto: {linha_limpa} -> {e}")
                elif linha_limpa and "Nenhum boleto avulso" not in linha_limpa:
                    cobrancas_widepay['boletos_avulsos_abertos_texto'].append(linha_limpa)
                continue
                
            col1 = normalizar_texto(partes[0])
            col2 = partes[1].replace("**", "").replace("*", "").strip()
            
            # Dados do Contrato (SeÃ§Ã£o 1)
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
                elif "valor total do contrato" in col1:
                    resumo_financeiro['valor_total_contrato'] = extrair_valor_numerico(col2)
                    
            # Dados Financeiros / Resumo (SeÃ§Ã£o 3)
            elif secao_atual == 30:
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
    interpretar_pagamentos_recebidos(dados_cliente, resumo_financeiro, cobrancas_widepay)

    # Reajustar parcelas restantes e percentuais
    if resumo_financeiro['contrato_total_confirmado']:
        resumo_financeiro['parcelas_restantes'] = max(0, resumo_financeiro['total_contrato'] - resumo_financeiro['parcelas_pagas'])
        resumo_financeiro['percentual_pago'] = resumo_financeiro['parcelas_pagas'] / resumo_financeiro['total_contrato']
        resumo_financeiro['percentual_restante'] = resumo_financeiro['parcelas_restantes'] / resumo_financeiro['total_contrato']
        if resumo_financeiro.get('valor_total_contrato', 0) > 0:
            resumo_financeiro['percentual_financeiro_pago'] = resumo_financeiro['valor_pago'] / resumo_financeiro['valor_total_contrato']
    else:
        resumo_financeiro['parcelas_restantes'] = 0
        resumo_financeiro['percentual_pago'] = 0.0
        resumo_financeiro['percentual_restante'] = 0.0
        resumo_financeiro['percentual_financeiro_pago'] = 0.0
        
    return dados_cliente, resumo_financeiro, carnes_widepay, cobrancas_widepay

def main():
    if len(sys.argv) > 1:
        md_path = sys.argv[1]
    else:
        md_path = input("Digite o caminho do arquivo MD de conferencia: ").strip()
        
    if not os.path.exists(md_path):
        print(f"Caminho invalido: {md_path}")
        sys.exit(1)

    print(f"Lendo dados de conferencia em: {md_path}...")
    dados_cliente, resumo, carnes, cobrancas = ler_md_conferencia(md_path)
    
    if not dados_cliente or not dados_cliente['nome']:
        print("Erro ao ler dados do relatorio.")
        sys.exit(1)

    garantir_widepay_real_ou_parar(dados_cliente['nome'])
        
    print(f"Cliente: {dados_cliente['nome']}")
    print(f"Lote: {dados_cliente['lote']}")
    print(f"Total Contrato: {resumo['total_contrato']}")
    print(f"Parcelas Pagas: {resumo['parcelas_pagas']}")
    print(f"WidePay Carnes: {len(carnes)} encontrado(s)")
    print(f"WidePay Cobrancas: {len(cobrancas.get('cobrancas_encontradas', []))} encontrado(s)")
    print(f"Boletos avulsos recebidos: {len(cobrancas.get('boletos_avulsos_recebidos', []))}")
    print(f"Boletos avulsos em aberto: {len(cobrancas.get('boletos_avulsos_abertos', []))}")
    print(f"Pagamentos recebidos interpretados: {len(cobrancas.get('pagamentos_interpretados', []))}")

    if not resumo.get('contrato_total_confirmado'):
        print("\n[ERRO CRITICO] Contrato nao confirmou o total de parcelas.")
        print("Parcelas restantes devem ser calculadas somente pelo contrato.")
        print("PDF/HTML final bloqueados para evitar relatorio com restantes derivados do WidePay.")
        sys.exit(1)

    erros_interpretacao = validar_interpretacao_pagamentos(resumo, cobrancas)
    if erros_interpretacao:
        print("\n[ERRO CRITICO] Interpretacao individual de pagamentos incompleta.")
        for erro in erros_interpretacao:
            print(f"- {erro}")
        print("PDF/HTML final bloqueados ate todos os recebimentos do WidePay serem interpretados.")
        sys.exit(1)
    
    # Gerar caminhos de saÃ­da
    nome_limpo = re.sub(r'[^a-zA-Z0-9]', '_', normalizar_texto(dados_cliente['nome']).upper())
    is_camila = "camila" in normalizar_texto(dados_cliente['nome'])
    
    if is_camila:
        # PadrÃ£o especÃ­fico da Camila V4 para Etapa 5
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
    ok_pdf = gerar_pdf(dados_cliente, resumo, carnes, cobrancas, str(pdf_saida))
    
    # Gerar prÃ©via HTML
    print("Gerando Previa HTML...")
    gerar_html(dados_cliente, resumo, carnes, cobrancas, str(html_saida_previa))
    
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
