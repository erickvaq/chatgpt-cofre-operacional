# -*- coding: utf-8 -*-
"""
Gerador de prévia HTML estilizada para o relatório de conferência do cliente.
"""
import os
from html import escape as html_escape
from .calculos_financeiros import formatar_moeda

def gerar_html(dados_cliente, resumo_financeiro, carnes_widepay, cobrancas_widepay, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    pct_pago_pct = int(resumo_financeiro['percentual_pago'] * 100)
    pct_rest_pct = 100 - pct_pago_pct
    cobrancas_widepay = cobrancas_widepay or {}
    cobrancas_encontradas = cobrancas_widepay.get("cobrancas_encontradas") or []
    boletos_avulsos_recebidos = cobrancas_widepay.get("boletos_avulsos_recebidos") or []
    boletos_avulsos_abertos = cobrancas_widepay.get("boletos_avulsos_abertos") or []
    boletos_avulsos_abertos_texto = cobrancas_widepay.get("boletos_avulsos_abertos_texto") or []
    parcelas_geradas_widepay = 0
    for c in carnes_widepay:
        try:
            if "cancelado" not in str(c.get("status", "")).lower():
                parcelas_geradas_widepay += int(c.get("parcelas_geradas", 0))
        except Exception:
            pass
    parcelas_pendentes_geradas = max(0, parcelas_geradas_widepay - resumo_financeiro['parcelas_pagas'])
    parcelas_nao_geradas = max(0, resumo_financeiro['total_contrato'] - parcelas_geradas_widepay)

    def linhas_html_tabela(registros, campos, vazio, colunas):
        if not registros:
            return f'<tr><td colspan="{len(colunas)}" style="text-align:left;">{html_escape(vazio)}</td></tr>'
        linhas = []
        for item in registros:
            celulas = []
            for campo in campos:
                valor = item.get(campo, "-")
                if isinstance(valor, float):
                    if "valor" in campo or "recebido" in campo or "original" in campo:
                        valor = formatar_moeda(valor)
                    else:
                        valor = f"{valor:.2f}"
                celulas.append(f"<td>{html_escape(str(valor))}</td>")
            linhas.append("<tr>" + "".join(celulas) + "</tr>")
        return "".join(linhas)
    
    # Gerar linhas da tabela de carnês
    linhas_carnes = ""
    for c in carnes_widepay:
        status_color = "#2E7D32" if c['status'].upper() == "ATIVO" else ("#C62828" if "CANCELADO" in c['status'].upper() else "#37474F")
        linhas_carnes += f"""
        <tr>
            <td>{html_escape(str(c['carne']))}</td>
            <td>{html_escape(formatar_moeda(c['valor_parcela']))}</td>
            <td>{html_escape(str(c['parcelas_geradas']))}</td>
            <td>{html_escape(str(c['parcelas_pagas']))}</td>
            <td>{html_escape(formatar_moeda(c['total_recebido']))}</td>
            <td>{html_escape(str(c['ultimo_vencimento']))}</td>
            <td style="color: {status_color}; font-weight: bold;">{html_escape(str(c['status']))}</td>
        </tr>
        """

    linhas_cobrancas = linhas_html_tabela(
        cobrancas_encontradas,
        ["id", "forma", "descricao", "valor_original", "valor_recebido", "vencimento", "status", "tipo"],
        "Nenhuma cobrança encontrada.",
        ["ID", "Forma", "Descricao", "Valor Original", "Valor Recebido", "Vencimento", "Status", "Tipo"]
    )
    linhas_avulsos_recebidos = linhas_html_tabela(
        boletos_avulsos_recebidos,
        ["id", "descricao", "valor_recebido", "vencimento", "pagamento", "status"],
        "Nenhum boleto avulso recebido.",
        ["ID", "Descricao", "Valor Recebido", "Vencimento", "Pagamento", "Status"]
    )
    linhas_avulsos_abertos = linhas_html_tabela(
        boletos_avulsos_abertos,
        ["id", "descricao", "valor_original", "vencimento", "status"],
        "Nenhum boleto avulso em aberto/vencido.",
        ["ID", "Descricao", "Valor Original", "Vencimento", "Status"]
    )
    linhas_avulsos_abertos_texto = "".join(
        f'<tr><td colspan="5" style="text-align:left;">{html_escape(linha)}</td></tr>'
        for linha in boletos_avulsos_abertos_texto
    )
    
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
                <div class="card-label">Total Pago do Terreno/Lote</div>
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
                <td style="text-align: left; font-weight: bold;">Em cobrança no WidePay</td>
                <td style="text-align: left;">{parcelas_pendentes_geradas} parcelas</td>
            </tr>
            <tr>
                <td style="text-align: left; font-weight: bold;">Ainda não geradas</td>
                <td style="text-align: left;">{parcelas_nao_geradas} parcelas</td>
                <td style="text-align: left; font-weight: bold;">Avulsos recebidos</td>
                <td style="text-align: left;">{len(boletos_avulsos_recebidos)} registros</td>
            </tr>
        </table>

        <div class="section-title">Cobranças/Boletos Encontrados no WidePay</div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Forma</th>
                    <th>Descricao</th>
                    <th>Valor Original</th>
                    <th>Valor Recebido</th>
                    <th>Vencimento</th>
                    <th>Status</th>
                    <th>Tipo</th>
                </tr>
            </thead>
            <tbody>
                {linhas_cobrancas}
            </tbody>
        </table>

        <div class="section-title">Boletos Avulsos Recebidos</div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Descricao</th>
                    <th>Valor Recebido</th>
                    <th>Vencimento</th>
                    <th>Pagamento</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {linhas_avulsos_recebidos}
            </tbody>
        </table>

        <div class="section-title">Boletos Avulsos em Aberto</div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Descricao</th>
                    <th>Valor Original</th>
                    <th>Vencimento</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {linhas_avulsos_abertos if boletos_avulsos_abertos else linhas_avulsos_abertos_texto}
            </tbody>
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
                {resumo_financeiro['parcelas_pagas']} de {resumo_financeiro['total_contrato']} parcelas pagas ({pct_pago_pct}% do contrato) | Total pago do terreno/lote: {formatar_moeda(resumo_financeiro['valor_pago'])} | {parcelas_geradas_widepay} geradas no WidePay | {parcelas_pendentes_geradas} em cobrança no WidePay | {parcelas_nao_geradas} ainda não geradas | Quitação prevista: {dados_cliente['previsao_quitacao']}
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
