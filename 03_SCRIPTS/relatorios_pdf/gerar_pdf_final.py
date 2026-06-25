# -*- coding: utf-8 -*-
"""
Gerador de PDFs finais do projeto usando ReportLab estruturado.
"""
import os
import sys
from xml.sax.saxutils import escape as xml_escape
from .modelo_visual_relatorio import CORES, criar_estilos, TITULO_RELATORIO, LOCALIDADE
from .calculos_financeiros import formatar_moeda

def gerar_pdf(dados_cliente, resumo_financeiro, carnes_widepay, cobrancas_widepay, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.lib.styles import ParagraphStyle
    except ImportError:
        print("Erro: ReportLab nao instalado para geracao de PDF.")
        return False
        
    estilos = criar_estilos()
    if not estilos:
        return False
        
    doc = SimpleDocTemplate(
        caminho_saida, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    
    elementos = []
    cobrancas_widepay = cobrancas_widepay or {}
    cobrancas_encontradas = cobrancas_widepay.get("cobrancas_encontradas") or []
    boletos_avulsos_recebidos = cobrancas_widepay.get("boletos_avulsos_recebidos") or []
    boletos_avulsos_abertos = cobrancas_widepay.get("boletos_avulsos_abertos") or []
    boletos_avulsos_abertos_texto = cobrancas_widepay.get("boletos_avulsos_abertos_texto") or []

    cab_col = ParagraphStyle('hcol', parent=estilos['normal'], fontSize=9, textColor=CORES['BRANCO'], fontName='Helvetica-Bold', alignment=TA_CENTER)
    cel_s   = ParagraphStyle('cel',  parent=estilos['normal'], fontSize=9, textColor=CORES['CINZA_ESCURO'], fontName='Helvetica', alignment=TA_CENTER)
    tot_s   = ParagraphStyle('tot',  parent=estilos['normal'], fontSize=10, textColor=CORES['BRANCO'], fontName='Helvetica-Bold', alignment=TA_CENTER)

    def par(txt, st=None):
        return Paragraph(xml_escape(str(txt)), st or cel_s)

    def montar_tabela_dados(titulo, colunas, registros, campos, larguras, vazio="Nenhum registro encontrado."):
        elementos.append(Paragraph(titulo, estilos['secao']))
        if not registros:
            elementos.append(Paragraph(vazio, estilos['normal']))
            elementos.append(Spacer(1, 0.2*cm))
            return
        linhas = [[Paragraph(f"<b>{col}</b>", cab_col) for col in colunas]]
        for registro in registros:
            linha = []
            for campo in campos:
                valor = registro.get(campo, "-")
                if isinstance(valor, (int, float)) and "valor" in campo:
                    valor = formatar_moeda(float(valor))
                linha.append(par(valor))
            linhas.append(linha)
        tabela_local = Table(linhas, colWidths=larguras)
        tabela_local.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,0),  CORES['VERDE_ESCURO']),
            ('ROWBACKGROUNDS',(0,1), (-1,-1), [CORES['BRANCO'], CORES['CINZA_CLARO']]),
            ('GRID',          (0,0), (-1,-1), 0.5, CORES['VERDE_LINHA']),
            ('TOPPADDING',    (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos.append(tabela_local)
        elementos.append(Spacer(1, 0.3*cm))

    parcelas_geradas_widepay = 0
    for c in carnes_widepay:
        try:
            if "cancelado" not in str(c.get("status", "")).lower():
                parcelas_geradas_widepay += int(c.get("parcelas_geradas", 0))
        except Exception:
            pass
    parcelas_pendentes_geradas = max(0, parcelas_geradas_widepay - resumo_financeiro['parcelas_pagas'])
    parcelas_nao_geradas = max(0, resumo_financeiro['total_contrato'] - parcelas_geradas_widepay)
    faixas_parcelas = []
    if resumo_financeiro['parcelas_pagas'] > 0:
        faixas_parcelas.append((f"1 - {resumo_financeiro['parcelas_pagas']}", resumo_financeiro['parcelas_pagas'], "Pagas no contrato"))
    if parcelas_pendentes_geradas > 0:
        inicio = resumo_financeiro['parcelas_pagas'] + 1
        fim = parcelas_geradas_widepay
        faixas_parcelas.append((f"{inicio} - {fim}", parcelas_pendentes_geradas, "Em cobrança no WidePay"))
    if parcelas_nao_geradas > 0:
        inicio = parcelas_geradas_widepay + 1
        fim = resumo_financeiro['total_contrato']
        faixas_parcelas.append((f"{inicio} - {fim}", parcelas_nao_geradas, "Ainda nao geradas no WidePay"))
    
    # 1. Cabecalho (REGRA 17)
    cab = Table([
        [Paragraph(TITULO_RELATORIO, estilos['titulo'])],
        [Paragraph(dados_cliente['nome'], estilos['subtitulo'])],
        [Paragraph(f"Lote: {dados_cliente['lote']}  Quadra: {dados_cliente['quadra']}   |   {LOCALIDADE}", estilos['subtitulo'])],
    ], colWidths=[17*cm])
    
    cab.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), CORES['VERDE_MEDIO']),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING',   (0,0), (-1,-1), 16),
        ('RIGHTPADDING',  (0,0), (-1,-1), 16),
    ]))
    elementos.append(cab)
    elementos.append(Spacer(1, 0.4*cm))
    
    # 2. Cards Principais
    def make_card(label, valor, bg):
        t = Table([[Paragraph(f"<b>{label}</b>", estilos['card_label'])],
                   [Paragraph(f"<b>{valor}</b>", estilos['card_valor'])]], colWidths=[5.3*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), bg),
            ('TOPPADDING',    (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        return t
        
    c1 = make_card("TOTAL PAGO DO TERRENO/LOTE", formatar_moeda(resumo_financeiro['valor_pago']), CORES['VERDE_MEDIO'])
    c2 = make_card("PARCELAS PAGAS", f"{resumo_financeiro['parcelas_pagas']} de {resumo_financeiro['total_contrato']}", CORES['AZUL'])
    c3 = make_card("FALTA PAGAR", formatar_moeda(resumo_financeiro['valor_restante']), CORES['AMARELO'])
    
    cards = Table([[c1, c2, c3]], colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
    cards.setStyle(TableStyle([
        ('ALIGN',   (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',  (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',  (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elementos.append(cards)
    elementos.append(Spacer(1, 0.35*cm))
    
    # 3. Informacoes do Contrato
    info = Table([
        [Paragraph("<b>Inicio do Contrato</b>", estilos['normal']),   Paragraph(dados_cliente['data_assinatura'], estilos['normal']),
         Paragraph("<b>Proximo Vencimento</b>", estilos['normal']),   Paragraph(dados_cliente['vencimento'], estilos['normal'])],
        [Paragraph("<b>Previsao de Quitacao</b>", estilos['normal']), Paragraph(dados_cliente['previsao_quitacao'], estilos['normal']),
         Paragraph("<b>Valor da Parcela</b>", estilos['normal']),     Paragraph(f"{formatar_moeda(dados_cliente['valor_parcela'])}/mes", estilos['normal'])],
        [Paragraph("<b>Situacao Atual</b>", estilos['normal']),       Paragraph("<b>EM DIA</b>", estilos['bold_verde']),
         Paragraph("<b>Parcelas Restantes</b>", estilos['normal']),   Paragraph(f"{resumo_financeiro['parcelas_restantes']} parcelas", estilos['normal'])],
        [Paragraph("<b>Parcelas geradas no WidePay</b>", estilos['normal']), Paragraph(f"{parcelas_geradas_widepay} parcelas", estilos['normal']),
         Paragraph("<b>Parcelas em cobranca no WidePay</b>", estilos['normal']), Paragraph(f"{parcelas_pendentes_geradas} parcelas", estilos['normal'])],
        [Paragraph("<b>Ainda nao geradas no WidePay</b>", estilos['normal']), Paragraph(f"{parcelas_nao_geradas} parcelas", estilos['normal']),
         Paragraph("<b>Boletos avulsos recebidos</b>", estilos['normal']), Paragraph(f"{len(boletos_avulsos_recebidos)} registros", estilos['normal'])],
    ], colWidths=[4.5*cm, 4*cm, 4.5*cm, 4*cm])
    
    info.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [CORES['CINZA_CLARO'], CORES['BRANCO']]),
        ('GRID',          (0,0), (-1,-1), 0.5, CORES['VERDE_LINHA']),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ]))
    elementos.append(info)
    elementos.append(Spacer(1, 0.3*cm))

    # 3. Mapa das parcelas do contrato
    elementos.append(Paragraph("Mapa de Parcelas do Contrato", estilos['secao']))
    mapa = [[Paragraph("<b>Faixa</b>", cab_col), Paragraph("<b>Quantidade</b>", cab_col), Paragraph("<b>Status</b>", cab_col)]]
    for faixa, qtd, status in faixas_parcelas:
        mapa.append([par(faixa), par(qtd), par(status)])
    mapa_tbl = Table(mapa, colWidths=[6*cm, 3*cm, 8*cm])
    mapa_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  CORES['VERDE_ESCURO']),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [CORES['BRANCO'], CORES['CINZA_CLARO']]),
        ('GRID',          (0,0), (-1,-1), 0.5, CORES['VERDE_LINHA']),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elementos.append(mapa_tbl)
    elementos.append(Spacer(1, 0.3*cm))

    # 4. Cobranças e Boletos em Cobrança no WidePay
    montar_tabela_dados(
        "Cobranças/Boletos Encontrados no WidePay",
        ["ID", "Forma", "Descricao", "Valor Original", "Valor Recebido", "Vencimento", "Status", "Tipo"],
        cobrancas_encontradas,
        ["id", "forma", "descricao", "valor_original", "valor_recebido", "vencimento", "status", "tipo"],
        [1.5*cm, 2*cm, 4.5*cm, 2.2*cm, 2.2*cm, 2.5*cm, 2.2*cm, 1.8*cm],
    )
    montar_tabela_dados(
        "Boletos Avulsos Recebidos",
        ["ID", "Descricao", "Valor Recebido", "Vencimento", "Pagamento", "Status"],
        boletos_avulsos_recebidos,
        ["id", "descricao", "valor_recebido", "vencimento", "pagamento", "status"],
        [1.5*cm, 6*cm, 2.6*cm, 2.5*cm, 2.6*cm, 2.2*cm],
        vazio="Nenhum boleto avulso recebido."
    )
    if boletos_avulsos_abertos:
        montar_tabela_dados(
            "Boletos Avulsos em Aberto",
            ["ID", "Descricao", "Valor Original", "Vencimento", "Status"],
            boletos_avulsos_abertos,
            ["id", "descricao", "valor_original", "vencimento", "status"],
            [1.5*cm, 8*cm, 3*cm, 2.7*cm, 2.0*cm],
            vazio="Nenhum boleto avulso em aberto/vencido."
        )
    elif boletos_avulsos_abertos_texto:
        elementos.append(Paragraph("Boletos Avulsos em Aberto", estilos['secao']))
        for linha_txt in boletos_avulsos_abertos_texto:
            elementos.append(Paragraph(xml_escape(linha_txt), estilos['normal']))
        elementos.append(Spacer(1, 0.2*cm))
    
    # 5. Historico de Carnes
    elementos.append(Paragraph("Historico de Carnes no WidePay", estilos['secao']))
    
    colunas = ["Carne", "Valor/Parcela", "Geradas", "Pagas", "Total Recebido", "Ult. Vencimento", "Status"]
        
    linhas = [[par(col, cab_col) for col in colunas]]
    for c in carnes_widepay:
        status_style = estilos['bold_verde'] if c['status'].upper() == "ATIVO" else (estilos['bold_verm'] if "CANCELADO" in c['status'].upper() else cel_s)
        linhas.append([
            par(c['carne']),
            par(formatar_moeda(c['valor_parcela'])),
            par(c['parcelas_geradas']),
            par(c['parcelas_pagas']),
            par(formatar_moeda(c['total_recebido'])),
            par(c['ultimo_vencimento']),
            Paragraph(f"<b>{c['status']}</b>", status_style)
        ])
        
    # Linha totalizadora
    linhas.append([
        par("", tot_s), par("", tot_s), par("", tot_s),
        Paragraph(f"<b>{resumo_financeiro['parcelas_pagas']}</b>", tot_s),
        Paragraph(f"<b>{formatar_moeda(resumo_financeiro['valor_pago'])}</b>", tot_s),
        par("", tot_s),
        Paragraph(f"<b>{resumo_financeiro['parcelas_pagas']} parcelas</b>", tot_s)
    ])
    
    tabela = Table(linhas, colWidths=[2*cm, 2.5*cm, 1.8*cm, 1.8*cm, 2.7*cm, 2.7*cm, 2.5*cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  CORES['VERDE_ESCURO']),
        ('BACKGROUND',    (0,-1),(-1,-1), CORES['VERDE_ESCURO']),
        ('ROWBACKGROUNDS',(0,1), (-1,-2), [CORES['BRANCO'], CORES['CINZA_CLARO']]),
        ('GRID',          (0,0), (-1,-1), 0.5, CORES['VERDE_LINHA']),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1, 0.4*cm))
    
    # 5. Barra de Progresso
    elementos.append(Paragraph("Progresso de Pagamento", estilos['secao']))
    
    barra_total = 17*cm
    barra_paga  = barra_total * resumo_financeiro['percentual_pago']
    barra_rest  = barra_total * resumo_financeiro['percentual_restante']
    
    if barra_paga <= 0.1:
        barra = Table([
            [Paragraph(f"<b>Restantes: {resumo_financeiro['parcelas_restantes']}</b>", ParagraphStyle('br', parent=estilos['normal'], fontSize=9, textColor=CORES['CINZA_ESCURO'], fontName='Helvetica-Bold', alignment=TA_CENTER))]
        ], colWidths=[barra_total], rowHeights=[1.1*cm])
        barra.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), CORES['CINZA_BARRA']),
            ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
            ('GRID',       (0,0), (-1,-1), 0, CORES['BRANCO']),
        ]))
    elif barra_rest <= 0.1:
        barra = Table([
            [Paragraph(f"<b>Pagas: {resumo_financeiro['parcelas_pagas']} (Quitado)</b>", ParagraphStyle('bp', parent=estilos['normal'], fontSize=9, textColor=CORES['BRANCO'], fontName='Helvetica-Bold', alignment=TA_CENTER))]
        ], colWidths=[barra_total], rowHeights=[1.1*cm])
        barra.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), CORES['VERDE_MEDIO']),
            ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
            ('GRID',       (0,0), (-1,-1), 0, CORES['BRANCO']),
        ]))
    else:
        barra = Table([
            [Paragraph(f"<b>Pagas: {resumo_financeiro['parcelas_pagas']}</b>", ParagraphStyle('bp', parent=estilos['normal'], fontSize=9, textColor=CORES['BRANCO'], fontName='Helvetica-Bold', alignment=TA_CENTER)),
             Paragraph(f"<b>Restantes: {resumo_financeiro['parcelas_restantes']}</b>", ParagraphStyle('br', parent=estilos['normal'], fontSize=9, textColor=CORES['CINZA_ESCURO'], fontName='Helvetica-Bold', alignment=TA_CENTER))]
        ], colWidths=[barra_paga, barra_rest], rowHeights=[1.1*cm])
        barra.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), CORES['VERDE_MEDIO']),
            ('BACKGROUND', (1,0), (1,0), CORES['CINZA_BARRA']),
            ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
            ('GRID',       (0,0), (-1,-1), 0, CORES['BRANCO']),
        ]))
    elementos.append(barra)
    elementos.append(Spacer(1, 0.15*cm))
    elementos.append(Paragraph(
        f"<b>{resumo_financeiro['parcelas_pagas']} de {resumo_financeiro['total_contrato']} parcelas pagas  ({int(resumo_financeiro['percentual_pago']*100)}% do contrato)   |   "
        f"{resumo_financeiro['parcelas_restantes']} restantes do contrato ({int(resumo_financeiro['percentual_restante']*100)}%)   |   "
        f"Total pago do terreno/lote: {formatar_moeda(resumo_financeiro['valor_pago'])}   |   "
        f"{parcelas_geradas_widepay} geradas no WidePay | {parcelas_pendentes_geradas} geradas e ainda em aberto | {parcelas_nao_geradas} ainda nao geradas | Quitacao prevista: {dados_cliente['previsao_quitacao']}</b>",
        estilos['pct']
    ))
    elementos.append(Spacer(1, 0.4*cm))
    
    # Rodape
    elementos.append(HRFlowable(width="100%", thickness=0.5, color=CORES['VERDE_LINHA'], spaceAfter=4))
    elementos.append(Paragraph(
        f"Relatorio gerado em 16/06/2026  |  Dados extraidos do WidePay e do contrato fisico  |  Uso interno",
        estilos['rodape']
    ))
    
    doc.build(elementos)
    print(f"PDF salvo com sucesso em: {caminho_saida}")
    return True
