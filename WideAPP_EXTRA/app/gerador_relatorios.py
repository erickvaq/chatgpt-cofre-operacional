# -*- coding: utf-8 -*-
import os
import sys
import shutil
import json
import subprocess
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

try:
    from app.relatorios_pdf.gerar_pdf_final import gerar_pdf
    from app.relatorios_pdf.gerar_html_previa import gerar_html
except ImportError as e:
    print(f"Aviso ao importar geradores PDF/HTML do relatorios_pdf: {e}")
    gerar_pdf = None
    gerar_html = None

def formatar_moeda(val):
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_markdown_conferencia(dados_contrato, dados_calculados, dados_normalizados, caminho_md):
    """Gera o arquivo de conferência MD com base nos dados consolidados e normalizados."""
    cliente = dados_contrato.get("cliente", "Desconhecido")
    lote = dados_contrato.get("lote", "-")
    quadra = dados_contrato.get("quadra", "-")
    area = dados_contrato.get("area", "-")
    entrada = dados_contrato.get("entrada", 0.0)
    total_parcelas = dados_contrato.get("total_parcelas", 0)
    valor_parcela = dados_contrato.get("valor_parcela", 0.0)
    valor_total_contrato = dados_contrato.get("valor_total_contrato", 0.0)
    data_assinatura = dados_contrato.get("data_assinatura", "-")
    vencimento = dados_contrato.get("vencimento", "-")
    previsao_quitacao = dados_contrato.get("previsao_quitacao", "-")
    
    carnes = dados_normalizados.get("carnes") or []
    cobrancas = dados_normalizados.get("cobrancas") or []
    duplicidades = dados_normalizados.get("duplicidades") or []
    
    # 2. Linhas de Carnês
    linhas_carnes = "| Carnê | Valor/Parcela | Parcelas Geradas | Parcelas Pagas | Total Recebido | Último Vencimento | Status     |\n"
    linhas_carnes += "|-------|--------------|------------------|----------------|----------------|-------------------|------------|\n"
    for c in carnes:
        linhas_carnes += f"| {c['carne']} | R$ {float(c['valor_parcela']):.2f} | {c['parcelas_geradas']} | {c['parcelas_pagas']} | R$ {float(c['total_recebido']):.2f} | {c['ultimo_vencimento']} | {c['status']} |\n"
        
    # 3. Linhas de Cobranças
    linhas_cobrancas = "| ID | Forma | Descrição | Valor Original | Valor Recebido | Vencimento | Status | Tipo |\n"
    linhas_cobrancas += "|----|-------|-----------|----------------|----------------|------------|--------|------|\n"
    for cob in cobrancas:
        tipo = "Carnê" if cob.get("pertence_a_carne") else "Avulsa"
        linhas_cobrancas += f"| {cob['id']} | {cob['forma']} | {cob['descricao']} | R$ {cob['valor_original']:.2f} | R$ {cob['valor_recebido']:.2f} | {cob['vencimento']} | {cob['status']} | {tipo} |\n"
        
    # 4. Boletos Avulsos Recebidos
    avulsos_recebidos = [cob for cob in cobrancas if cob.get("classificacao") == "avulso" and cob.get("status", "").lower() == "recebido"]
    if avulsos_recebidos:
        linhas_avulsos_recebidos = "| ID | Descrição | Valor Recebido | Vencimento | Pagamento | Status |\n"
        linhas_avulsos_recebidos += "|----|-----------|----------------|------------|-----------|--------|\n"
        for cob in avulsos_recebidos:
            linhas_avulsos_recebidos += f"| {cob['id']} | {cob['descricao']} | R$ {cob['valor_recebido']:.2f} | {cob['vencimento']} | {cob['pagamento']} | {cob['status']} |\n"
    else:
        linhas_avulsos_recebidos = "Nenhum boleto avulso recebido."
        
    # 5. Boletos Avulsos em Aberto
    avulsos_abertos = [cob for cob in cobrancas if cob.get("classificacao") == "pendência"]
    if avulsos_abertos:
        linhas_avulsos_abertos = "| ID | Descrição | Valor Original | Vencimento | Status |\n"
        linhas_avulsos_abertos += "|----|-----------|----------------|------------|--------|\n"
        for cob in avulsos_abertos:
            linhas_avulsos_abertos += f"| {cob['id']} | {cob['descricao']} | R$ {cob['valor_original']:.2f} | {cob['vencimento']} | {cob['status']} |\n"
    else:
        linhas_avulsos_abertos = "Nenhum boleto avulso em aberto/vencido."
        
    # 6. Duplicidades
    if duplicidades:
        linhas_duplicidades = "| ID | Descrição | Valor Original | Valor Recebido | Vencimento | Status |\n"
        linhas_duplicidades += "|----|-----------|----------------|----------------|------------|--------|\n"
        for cob in duplicidades:
            linhas_duplicidades += f"| {cob['id']} | {cob['descricao']} | R$ {cob['valor_original']:.2f} | R$ {cob['valor_recebido']:.2f} | {cob['vencimento']} | {cob['status']} |\n"
    else:
        linhas_duplicidades = "Nenhuma possível duplicidade encontrada."
        
    # 6.1 Pagamentos Interpretados
    pagamentos_interpretados = dados_calculados.get("pagamentos_interpretados") or []
    if pagamentos_interpretados:
        linhas_interpretados = "| Cliente | Lote/Quadra | ID | Tipo | Descricao WidePay | Vencimento | Pagamento | Valor Original | Valor Recebido | Valor Base Parcela | Referencias | Qtd. Parcelas | Observacao |\n"
        linhas_interpretados += "|---------|-------------|----|------|-------------------|------------|-----------|----------------|----------------|--------------------|-------------|---------------|------------|\n"
        for p in pagamentos_interpretados:
            tipo_desc = "Carne" if p["classificacao"] == "parcela normal" else "Avulsa"
            linhas_interpretados += (
                f"| {cliente} | {lote} / {quadra} | {p['id']} | {tipo_desc} | {p['descricao']} | "
                f"{p['vencimento']} | {p['pagamento']} | R$ {p['valor_original']:.2f} | R$ {p['valor_recebido']:.2f} | "
                f"R$ {p['valor_base']:.2f} | {p['vencimento']} | {p['qtd']} | {p['classificacao']} |\n"
            )
    else:
        linhas_interpretados = "Nenhum pagamento recebido interpretado."

    conteudo = f"""# RELATÓRIO DE CONFERÊNCIA — {cliente.upper()}
# Gerado em: 25/06/2026
# Finalidade: Auditar cálculos antes de gerar o PDF final

---

## 1. DADOS DO CONTRATO (Fonte: Contrato físico localizado na pasta de consulta)

| Campo                    | Valor                          |
|--------------------------|--------------------------------|
| Cliente                  | {cliente} |
| Lote                     | {lote} (Quadra {quadra}) |
| Empreendimento           | Fazenda Água Viva, Iaçú-BA     |
| Área                     | {area} |
| Entrada                  | R$ {entrada:.2f} |
| Total de parcelas        | **{total_parcelas} parcelas** |
| Status do contrato       | {'CONTRATO CONFIRMADO' if total_parcelas > 0 else 'CONTRATO NAO CONFIRMADO'} |
| Valor de cada parcela    | R$ {valor_parcela:.2f} (nominal) |
| Valor total do contrato  | R$ {valor_total_contrato:.2f} |
| Vencimento               | {vencimento} |
| Data de assinatura       | {data_assinatura} |
| Previsão de quitação     | {previsao_quitacao} |

---

## 2. CARNÊS ENCONTRADOS (Fonte: Histórico de Carnês no WidePay)

{linhas_carnes}

---

## 3. COBRANÇAS/BOLETOS ENCONTRADOS (Fonte: Histórico de Cobranças no WidePay)

{linhas_cobrancas}

---

## 4. BOLETOS AVULSOS RECEBIDOS (Exclui duplicidades e boletos vinculados a carnês)

{linhas_avulsos_recebidos}

---

## 5. BOLETOS AVULSOS EM ABERTO

{linhas_avulsos_abertos}

---

## 6. POSSÍVEIS DUPLICIDADES (Desconsiderados dos cálculos para evitar dupla contagem)

{linhas_duplicidades}

---

## 6.1 PAGAMENTOS RECEBIDOS INTERPRETADOS

{linhas_interpretados}

---

## 7. TOTAL PAGO EM CARNÊS
R$ {dados_calculados['total_pago_carnes']:.2f} (baseado em {dados_calculados['parcelas_pagas_equivalentes']} parcelas pagas nos carnês)

---

## 8. TOTAL PAGO EM COBRANÇAS AVULSAS
R$ {dados_calculados['total_pago_avulsos']:.2f}

---

## 9. TOTAL PAGO CONSOLIDADO
R$ {dados_calculados['total_pago_consolidado']:.2f} (Carnês + Avulsos pagos)

---

## 10. TOTAL PENDENTE CONSOLIDADO
R$ {dados_calculados['total_pendente_consolidado']:.2f} (Carnês pendentes + Avulsos em aberto/vencidos)

---

## 11. DIVERGÊNCIAS E AUDITORIA
- Verificado via validador automatico de regras.

---

## 12. STATUS
`AGUARDANDO VALIDAÇÃO DO USUÁRIO`
"""
    with open(caminho_md, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"MD de Conferencia gerado em {caminho_md}")

def exportar_relatorios_finais(dados_contrato, dados_calculados, dados_normalizados, pasta_entrega, data_sufixo):
    """Gera arquivos XLSX, PDF, HTML, MD e JSON na pasta de entrega."""
    cliente = dados_contrato.get("cliente", "Desconhecido")
    nome_slug = re.sub(r'[^a-zA-Z0-9]', '_', normalizar_texto(cliente).upper())
    lote = dados_contrato.get("lote", "-")
    
    os.makedirs(pasta_entrega, exist_ok=True)
    
    # 1. Caminhos dos arquivos
    caminho_json_extraido = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "WIDEPAY_CONSULTAS" / f"WIDEPAY_{nome_slug}.json"
    caminho_md = pasta_entrega / f"CONFERENCIA_CALCULOS_{nome_slug}_{data_sufixo}.md"
    caminho_html = pasta_entrega / f"RESUMO_FINANCEIRO_{nome_slug}_{data_sufixo}_PREVIA.html"
    caminho_pdf = pasta_entrega / f"RESUMO_FINANCEIRO_{nome_slug}_{data_sufixo}.pdf"
    caminho_json = pasta_entrega / f"METRICAS_{nome_slug}_{data_sufixo}.json"
    caminho_xlsx = pasta_entrega / f"RELATORIO_FINANCEIRO_{nome_slug}_{data_sufixo}.xlsx"
    
    # 2. Salvar JSON consolidado
    relatorio_json = {
        "contrato": dados_contrato,
        "calculos": dados_calculados,
        "normalizado": dados_normalizados
    }
    with open(caminho_json, "w", encoding="utf-8") as fj:
        json.dump(relatorio_json, fj, indent=4, ensure_ascii=False)
        
    # 3. Gerar MD
    gerar_markdown_conferencia(dados_contrato, dados_calculados, dados_normalizados, caminho_md)
    
    # 4. Mapear para gerar HTML e PDF
    dados_cliente_map = {
        'nome': cliente,
        'lote': lote,
        'quadra': dados_contrato.get("quadra", "-"),
        'data_assinatura': dados_contrato.get("data_assinatura", "-"),
        'vencimento': dados_contrato.get("vencimento", "-"),
        'previsao_quitacao': dados_contrato.get("previsao_quitacao", "-"),
        'valor_parcela': dados_contrato.get("valor_parcela", 0.0)
    }
    
    total_contrato = dados_calculados.get("total_parcelas_contrato", 0)
    resumo_financeiro_map = {
        'total_contrato': total_contrato,
        'parcelas_pagas': dados_calculados.get("parcelas_pagas_equivalentes", 0),
        'parcelas_restantes': dados_calculados.get("parcelas_restantes", 0),
        'percentual_pago': (dados_calculados["parcelas_pagas_equivalentes"] / total_contrato) if total_contrato > 0 else 0.0,
        'percentual_restante': (dados_calculados["parcelas_restantes"] / total_contrato) if total_contrato > 0 else 0.0,
        'valor_pago': dados_calculados.get("total_pago_consolidado", 0.0),
        'valor_restante': dados_calculados.get("valor_restante_contrato", 0.0),
        'valor_total_contrato': float(dados_contrato.get("valor_total_contrato") or 0.0),
        'percentual_financeiro_pago': (dados_calculados["total_pago_consolidado"] / float(dados_contrato.get("valor_total_contrato") or 1.0)) if float(dados_contrato.get("valor_total_contrato") or 0.0) > 0 else 0.0,
    }
    
    cobrancas_widepay_map = {
        'cobrancas_encontradas': dados_normalizados.get("cobrancas") or [],
        'pagamentos_interpretados': dados_calculados.get("pagamentos_interpretados") or [],
        'boletos_avulsos_recebidos': [cob for cob in dados_normalizados.get("cobrancas", []) if cob.get("classificacao") == "avulso" and cob.get("status", "").lower() == "recebido"],
        'boletos_avulsos_abertos': [cob for cob in dados_normalizados.get("cobrancas", []) if cob.get("classificacao") == "pendência"],
        'duplicidades': dados_normalizados.get("duplicidades") or []
    }
    
    # Gerar HTML
    if gerar_html:
        try:
            gerar_html(dados_cliente_map, resumo_financeiro_map, dados_normalizados.get("carnes") or [], cobrancas_widepay_map, str(caminho_html))
            print(f"HTML Previa gerado em {caminho_html}")
        except Exception as e:
            print(f"Erro ao gerar HTML: {e}")
            
    # Gerar PDF
    if gerar_pdf:
        try:
            gerar_pdf(dados_cliente_map, resumo_financeiro_map, dados_normalizados.get("carnes") or [], cobrancas_widepay_map, str(caminho_pdf))
            print(f"PDF Final gerado em {caminho_pdf}")
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            
    # 5. Gerar planilha Excel (.xlsx) chamando o script de suporte
    print("Gerando planilha Excel...")
    script_xlsx = ROOT_DIR / "WideAPP_EXTRA" / "app" / "gerar_relatorio_excel.py"
    
    args_xlsx = [
        sys.executable,
        str(script_xlsx),
        "--json", str(caminho_json_extraido),
        "--cliente", cliente,
        "--lote", lote,
        "--quadra", dados_contrato.get("quadra", "-"),
        "--parcelas-contrato", str(total_contrato),
        "--valor-parcela", f"{dados_contrato.get('valor_parcela', 0.0):.2f}",
        "--valor-total-contrato", f"{dados_contrato.get('valor_total_contrato', 0.0):.2f}"
    ]
    
    res_xlsx = subprocess.run(args_xlsx, capture_output=True, text=True)
    if res_xlsx.returncode == 0:
        # Procurar o XLSX gerado em 02_RELATORIOS_GERADOS e mover para a pasta_entrega com nome padronizado
        nome_antigo_xlsx = f"RELATORIO_FINANCEIRO_CLIENTE_{nome_slug}_LOTE_{lote.replace(' ', '_').upper()}"
        # Acha qualquer xlsx na pasta de relatorios gerados com o nome do cliente
        pasta_saida_xlsx = ROOT_DIR / "02_RELATORIOS_GERADOS"
        xlsx_gerado = None
        for f in os.listdir(pasta_saida_xlsx):
            if f.endswith(".xlsx") and nome_slug in f.upper():
                xlsx_gerado = pasta_saida_xlsx / f
                break
                
        if xlsx_gerado:
            # Mover para a pasta final
            shutil.move(xlsx_gerado, caminho_xlsx)
            print(f"Excel XLSX final movido com sucesso para {caminho_xlsx}")
        else:
            print("Aviso: Nao foi possivel localizar o arquivo XLSX gerado para mover.")
    else:
        print(f"Erro ao executar gerador Excel: ReturnCode={res_xlsx.returncode}")
        print(f"STDOUT: {res_xlsx.stdout}")
        print(f"STDERR: {res_xlsx.stderr}")
        
    # Criar atalho BAT de abertura rápida
    bat_saida = pasta_entrega / "01_ABRIR_PDF_FINAL.bat"
    with open(bat_saida, "w", encoding="utf-8") as f:
        f.write(f'@echo off\ncd /d "%~dp0"\nstart "" "{caminho_pdf.name}"\n')
        
    return {
        "md": caminho_md,
        "html": caminho_html,
        "pdf": caminho_pdf,
        "json": caminho_json,
        "xlsx": caminho_xlsx,
        "bat": bat_saida
    }

def normalizar_texto(texto):
    if not texto:
        return ""
    texto = texto.lower()
    substituicoes = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'ã': 'a', 'õ': 'o', 'ç': 'c',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
    }
    for k, v in substituicoes.items():
        texto = texto.replace(k, v)
    return texto.strip()
