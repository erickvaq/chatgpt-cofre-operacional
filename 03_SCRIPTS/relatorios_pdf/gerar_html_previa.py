# -*- coding: utf-8 -*-
"""
Gerador de prévia HTML estilizada para o relatório de conferência do cliente.
"""
import os
from .calculos_financeiros import formatar_moeda

def gerar_html(dados_cliente, resumo_financeiro, carnes_widepay, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    pct_pago_pct = int(resumo_financeiro['percentual_pago'] * 100)
    pct_rest_pct = 100 - pct_pago_pct
    parcelas_geradas_widepay = 0
    for c in carnes_widepay:
        try:
            if "cancelado" not in str(c.get("status", "")).lower():
                parcelas_geradas_widepay += int(c.get("parcelas_geradas", 0))
        except Exception:
            pass
    parcelas_pendentes_geradas = max(0, parcelas_geradas_widepay - resumo_financeiro['parcelas_pagas'])
    parcelas_nao_geradas = max(0, resumo_financeiro['total_contrato'] - parcelas_geradas_widepay)
    
    # Gerar linhas da tabela de carnês
    linhas_carnes = ""
    for c in carnes_widepay:
        status_color = "#2E7D32" if c['status'].upper() == "ATIVO" else ("#C62828" if "CANCELADO" in c['status'].upper() else "#37474F")
        linhas_carnes += f"""
        <tr>
            <td>{c['carne']}</td>
            <td>{formatar_moeda(c['valor_parcela'])}</td>
            <td>{c['parcelas_geradas']}</td>
            <td>{c['parcelas_pagas']}</td>
            <td>{formatar_moeda(c['total_recebido'])}</td>
            <td>{c['ultimo_vencimento']}</td>
            <td style="color: {status_color}; font-weight: bold;">{c['status']}</td>
        </tr>
        """
        
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Previa - Relatório Financeiro</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #ECEFF1;
            margin: 0;
            padding: 40px 20px;
            color: #37474F;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #FFFFFF;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #1B5E20, #2E7D32);
            color: #FFFFFF;
            padding: 24px;
            border-radius: 6px;
            text-align: center;
            margin-bottom: 25px;
        }}
        .header h1 {{
            margin: 0 0 8px 0;
            font-size: 24px;
            letter-spacing: 1px;
        }}
        .header p {{
            margin: 4px 0;
            font-size: 14px;
            opacity: 0.9;
        }}
        .cards {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            margin-bottom: 25px;
        }}
        .card {{
            padding: 15px;
            border-radius: 6px;
            color: #FFFFFF;
            text-align: center;
        }}
        .card.pago {{ background-color: #2E7D32; }}
        .card.parcelas {{ background-color: #1565C0; }}
        .card.restante {{ background-color: #F9A825; }}
        .card-label {{ font-size: 11px; text-transform: uppercase; font-weight: 600; opacity: 0.95; }}
        .card-value {{ font-size: 20px; font-weight: 700; margin-top: 5px; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0 25px 0;
        }}
        th {{
            background-color: #1B5E20;
            color: #FFFFFF;
            padding: 10px;
            font-size: 13px;
            text-align: center;
        }}
        td {{
            padding: 10px;
            border: 1px solid #A5D6A7;
            text-align: center;
            font-size: 13px;
        }}
        tr:nth-child(even) td {{
            background-color: #ECEFF1;
        }}
        .section-title {{
            font-size: 16px;
            font-weight: 700;
            color: #1B5E20;
            margin-top: 25px;
            margin-bottom: 10px;
            border-left: 4px solid #2E7D32;
            padding-left: 10px;
        }}
        .progress-container {{
            margin: 20px 0;
        }}
        .progress-bar {{
            display: flex;
            height: 24px;
            border-radius: 4px;
            overflow: hidden;
            background-color: #B0BEC5;
        }}
        .progress-pago {{
            background-color: #2E7D32;
            color: #FFFFFF;
            font-size: 11px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .progress-rest {{
            background-color: #B0BEC5;
            color: #37474F;
            font-size: 11px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .footer {{
            border-top: 1px solid #A5D6A7;
            margin-top: 30px;
            padding-top: 15px;
            text-align: center;
            font-size: 11px;
            color: #90A4AE;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>RELATÓRIO FINANCEIRO</h1>
            <p><strong>{dados_cliente['nome']}</strong></p>
            <p>Loteamento Água Viva — Iaçú-BA</p>
        </div>
        
        <div class="cards">
            <div class="card pago">
                <div class="card-label">Total Pago</div>
                <div class="card-value">{formatar_moeda(resumo_financeiro['valor_pago'])}</div>
            </div>
            <div class="card parcelas">
                <div class="card-label">Parcelas Pagas</div>
                <div class="card-value">{resumo_financeiro['parcelas_pagas']} de {resumo_financeiro['total_contrato']}</div>
            </div>
            <div class="card restante">
                <div class="card-label">Falta Pagar</div>
                <div class="card-value">{formatar_moeda(resumo_financeiro['valor_restante'])}</div>
            </div>
        </div>
        
        <div class="section-title">Dados do Contrato</div>
        <table style="text-align: left;">
            <tr>
                <td style="text-align: left; font-weight: bold; width: 25%;">Início do Contrato</td>
                <td style="text-align: left; width: 25%;">{dados_cliente['data_assinatura']}</td>
                <td style="text-align: left; font-weight: bold; width: 25%;">Próximo Vencimento</td>
                <td style="text-align: left; width: 25%;">{dados_cliente['vencimento']}</td>
            </tr>
            <tr>
                <td style="text-align: left; font-weight: bold;">Previsão de Quitação</td>
                <td style="text-align: left;">{dados_cliente['previsao_quitacao']}</td>
                <td style="text-align: left; font-weight: bold;">Valor da Parcela</td>
                <td style="text-align: left;">{formatar_moeda(dados_cliente['valor_parcela'])}/mês</td>
            </tr>
            <tr>
                <td style="text-align: left; font-weight: bold;">Situação Atual</td>
                <td style="text-align: left; color: #2E7D32; font-weight: bold;">EM DIA</td>
                <td style="text-align: left; font-weight: bold;">Parcelas Restantes</td>
                <td style="text-align: left;">{resumo_financeiro['parcelas_restantes']} parcelas</td>
            </tr>
            <tr>
                <td style="text-align: left; font-weight: bold;">Geradas no WidePay</td>
                <td style="text-align: left;">{parcelas_geradas_widepay} parcelas</td>
                <td style="text-align: left; font-weight: bold;">Ainda não geradas</td>
                <td style="text-align: left;">{parcelas_nao_geradas} parcelas</td>
            </tr>
        </table>
        
        <div class="section-title">Histórico de Carnês no WidePay</div>
        <table>
            <thead>
                <tr>
                    <th>Carnê</th>
                    <th>Valor/Parcela</th>
                    <th>Geradas</th>
                    <th>Pagas</th>
                    <th>Total Recebido</th>
                    <th>Últ. Vencimento</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {linhas_carnes}
                <tr style="background-color: #1B5E20 !important; color: #FFFFFF; font-weight: bold;">
                    <td>TOTAL</td>
                    <td>-</td>
                    <td>-</td>
                    <td>{resumo_financeiro['parcelas_pagas']}</td>
                    <td>{formatar_moeda(resumo_financeiro['valor_pago'])}</td>
                    <td>-</td>
                    <td>{resumo_financeiro['parcelas_pagas']} parcelas</td>
                </tr>
            </tbody>
        </table>
        
        <div class="section-title">Progresso de Pagamento</div>
        <div class="progress-container">
            <div class="progress-bar">
                <div class="progress-pago" style="width: {pct_pago_pct}%;">Pagas: {resumo_financeiro['parcelas_pagas']} ({pct_pago_pct}%)</div>
                <div class="progress-rest" style="width: {pct_rest_pct}%;">Restantes: {resumo_financeiro['parcelas_restantes']} ({pct_rest_pct}%)</div>
            </div>
            <p style="text-align: center; font-size: 12px; font-weight: bold; margin-top: 10px; color: #2E7D32;">
                {resumo_financeiro['parcelas_pagas']} de {resumo_financeiro['total_contrato']} parcelas pagas ({pct_pago_pct}% do contrato) | {parcelas_geradas_widepay} geradas no WidePay | {parcelas_pendentes_geradas} geradas e ainda em aberto | {parcelas_nao_geradas} ainda não geradas | Quitação prevista: {dados_cliente['previsao_quitacao']}
            </p>
        </div>
        
        <div class="footer">
            Relatório gerado automaticamente | Dados extraídos do WidePay e do contrato físico | Uso Interno
        </div>
    </div>
</body>
</html>
"""
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Previa HTML gerada com sucesso em: {caminho_saida}")
