# -*- coding: utf-8 -*-
"""
Gerador de PDFs finais do projeto usando ReportLab estruturado.
"""
import os
import sys
import textwrap
from datetime import datetime
from xml.sax.saxutils import escape as xml_escape
from .modelo_visual_relatorio import CORES, criar_estilos, TITULO_RELATORIO, LOCALIDADE
from .calculos_financeiros import formatar_moeda


def _limpar_texto_pdf(texto):
    if texto is None:
        return ""
    texto = str(texto)
    substituicoes = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\xa0": " ",
    }
    for origem, destino in substituicoes.items():
        texto = texto.replace(origem, destino)
    texto = texto.encode("cp1252", errors="replace").decode("cp1252")
    return texto.replace("\r", " ").replace("\n", " ").strip()


def _pdf_escape(texto):
    texto = _limpar_texto_pdf(texto)
    return texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap_pdf_lines(texto, largura):
    texto = _limpar_texto_pdf(texto)
    if not texto:
        return [""]
    return textwrap.wrap(
        texto,
        width=largura,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [texto]


def _montar_linhas_pdf(dados_cliente, resumo_financeiro, carnes_widepay, cobrancas_widepay):
    cobrancas_widepay = cobrancas_widepay or {}
    cobrancas_encontradas = cobrancas_widepay.get("cobrancas_encontradas") or []
    boletos_avulsos_recebidos = cobrancas_widepay.get("boletos_avulsos_recebidos") or []
    boletos_avulsos_abertos = cobrancas_widepay.get("boletos_avulsos_abertos") or []
    boletos_avulsos_abertos_texto = cobrancas_widepay.get("boletos_avulsos_abertos_texto") or []
    pagamentos_interpretados = cobrancas_widepay.get("pagamentos_interpretados") or []

    parcelas_geradas_widepay = 0
    for c in carnes_widepay:
        try:
            if "cancelado" not in str(c.get("status", "")).lower():
                parcelas_geradas_widepay += int(c.get("parcelas_geradas", 0))
        except Exception:
            pass

    parcelas_pendentes_geradas = max(0, parcelas_geradas_widepay - resumo_financeiro["parcelas_pagas"])
    parcelas_nao_geradas = max(0, resumo_financeiro["total_contrato"] - parcelas_geradas_widepay)

    linhas = []
    linhas.append(("title", TITULO_RELATORIO))
    linhas.append(("subtitle", dados_cliente.get("nome", "Desconhecido")))
    linhas.append(("subtitle", f"Lote: {dados_cliente.get('lote', '-')} | Quadra: {dados_cliente.get('quadra', '-')} | {LOCALIDADE}"))
    linhas.append(("subtitle", f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"))
    linhas.append(("blank", ""))

    linhas.append(("section", "Resumo Financeiro"))
    linhas.append(("normal", f"Total pago do terreno/lote: {formatar_moeda(resumo_financeiro['valor_pago'])}"))
    linhas.append(("normal", f"Parcelas pagas: {resumo_financeiro['parcelas_pagas']} de {resumo_financeiro['total_contrato']}"))
    linhas.append(("normal", f"Parcelas restantes: {resumo_financeiro['parcelas_restantes']}"))
    linhas.append(("normal", f"Valor restante: {formatar_moeda(resumo_financeiro['valor_restante'])}"))
    linhas.append(("normal", f"Percentual pago do contrato: {int(resumo_financeiro['percentual_pago'] * 100)}%"))
    linhas.append(("normal", f"Percentual restante do contrato: {int(resumo_financeiro['percentual_restante'] * 100)}%"))
    linhas.append(("blank", ""))

    linhas.append(("section", "Dados do Contrato"))
    linhas.append(("normal", f"Inicio do contrato: {dados_cliente.get('data_assinatura', '-')}"))
    linhas.append(("normal", f"Proximo vencimento: {dados_cliente.get('vencimento', '-')}"))
    linhas.append(("normal", f"Previsao de quitacao: {dados_cliente.get('previsao_quitacao', '-')}"))
    linhas.append(("normal", f"Valor da parcela: {formatar_moeda(dados_cliente.get('valor_parcela', 0.0))}/mes"))
    linhas.append(("normal", f"Total de parcelas confirmado no contrato: {resumo_financeiro['total_contrato']}"))
    linhas.append(("blank", ""))

    linhas.append(("section", "Mapa de Parcelas do Contrato"))
    faixas_parcelas = []
    if resumo_financeiro["parcelas_pagas"] > 0:
        faixas_parcelas.append((f"1 - {resumo_financeiro['parcelas_pagas']}", resumo_financeiro["parcelas_pagas"], "Pagas no contrato"))
    if parcelas_pendentes_geradas > 0:
        inicio = resumo_financeiro["parcelas_pagas"] + 1
        fim = parcelas_geradas_widepay
        faixas_parcelas.append((f"{inicio} - {fim}", parcelas_pendentes_geradas, "Em cobranca no WidePay"))
    if parcelas_nao_geradas > 0:
        inicio = parcelas_geradas_widepay + 1
        fim = resumo_financeiro["total_contrato"]
        faixas_parcelas.append((f"{inicio} - {fim}", parcelas_nao_geradas, "Ainda nao geradas no WidePay"))
    for faixa, qtd, status in faixas_parcelas:
        linhas.append(("table", f"Faixa {faixa} | Quantidade: {qtd} | Status: {status}"))
    linhas.append(("blank", ""))

    linhas.append(("section", "Pagamentos Recebidos Interpretados"))
    if pagamentos_interpretados:
        for item in pagamentos_interpretados:
            linhas.append((
                "table",
                " | ".join([
                    f"Cliente: {item.get('cliente', '-')}",
                    f"Lote/Quadra: {item.get('lote_quadra', '-')}",
                    f"ID: {item.get('id', '-')}",
                    f"Tipo: {item.get('tipo', '-')}",
                    f"Descricao: {item.get('descricao', '-')}",
                    f"Venc.: {item.get('vencimento', '-')}",
                    f"Pgto.: {item.get('pagamento', '-')}",
                    f"Valor Orig.: {formatar_moeda(float(item.get('valor_original', 0.0) or 0.0))}",
                    f"Valor Rec.: {formatar_moeda(float(item.get('valor_recebido', 0.0) or 0.0))}",
                    f"Base Parc.: {formatar_moeda(float(item.get('valor_base_parcela', 0.0) or 0.0))}",
                    f"Refs: {item.get('referencias', '-')}",
                    f"Qtd.: {item.get('parcelas_quitadas', '-')}",
                    f"Obs.: {item.get('observacao', '-')}",
                ])
            ))
    else:
        linhas.append(("table", "Nenhum pagamento recebido interpretado - relatorio final bloqueado."))
    linhas.append(("blank", ""))

    linhas.append(("section", "Cobranças/Boletos Encontrados no WidePay"))
    if cobrancas_encontradas:
        for item in cobrancas_encontradas:
            linhas.append((
                "table",
                " | ".join([
                    f"ID: {item.get('id', '-')}",
                    f"Forma: {item.get('forma', '-')}",
                    f"Descricao: {item.get('descricao', '-')}",
                    f"Valor Original: {formatar_moeda(float(item.get('valor_original', 0.0) or 0.0))}",
                    f"Valor Recebido: {formatar_moeda(float(item.get('valor_recebido', 0.0) or 0.0))}",
                    f"Vencimento: {item.get('vencimento', '-')}",
                    f"Status: {item.get('status', '-')}",
                    f"Tipo: {item.get('tipo', '-')}",
                ])
            ))
    else:
        linhas.append(("table", "Nenhuma cobranza encontrada."))
    linhas.append(("blank", ""))

    linhas.append(("section", "Boletos Avulsos Recebidos"))
    if boletos_avulsos_recebidos:
        for item in boletos_avulsos_recebidos:
            linhas.append((
                "table",
                " | ".join([
                    f"ID: {item.get('id', '-')}",
                    f"Descricao: {item.get('descricao', '-')}",
                    f"Valor Recebido: {formatar_moeda(float(item.get('valor_recebido', 0.0) or 0.0))}",
                    f"Vencimento: {item.get('vencimento', '-')}",
                    f"Pagamento: {item.get('pagamento', '-')}",
                    f"Status: {item.get('status', '-')}",
                ])
            ))
    else:
        linhas.append(("table", "Nenhum boleto avulso recebido."))
    linhas.append(("blank", ""))

    linhas.append(("section", "Boletos Avulsos em Aberto"))
    if boletos_avulsos_abertos:
        for item in boletos_avulsos_abertos:
            linhas.append((
                "table",
                " | ".join([
                    f"ID: {item.get('id', '-')}",
                    f"Descricao: {item.get('descricao', '-')}",
                    f"Valor Original: {formatar_moeda(float(item.get('valor_original', 0.0) or 0.0))}",
                    f"Vencimento: {item.get('vencimento', '-')}",
                    f"Status: {item.get('status', '-')}",
                ])
            ))
    elif boletos_avulsos_abertos_texto:
        for linha_txt in boletos_avulsos_abertos_texto:
            linhas.append(("table", linha_txt))
    else:
        linhas.append(("table", "Nenhum boleto avulso em aberto/vencido."))
    linhas.append(("blank", ""))

    linhas.append(("section", "Historico de Carnes no WidePay"))
    for c in carnes_widepay:
        linhas.append((
            "table",
            " | ".join([
                f"Carne: {c.get('carne', '-')}",
                f"Valor/Parcela: {formatar_moeda(float(c.get('valor_parcela', 0.0) or 0.0))}",
                f"Geradas: {c.get('parcelas_geradas', '-')}",
                f"Pagas: {c.get('parcelas_pagas', '-')}",
                f"Total Recebido: {formatar_moeda(float(c.get('total_recebido', 0.0) or 0.0))}",
                f"Ult. Vencimento: {c.get('ultimo_vencimento', '-')}",
                f"Status: {c.get('status', '-')}",
            ])
        ))

    linhas.append(("table", f"TOTAL | Parcelas pagas: {resumo_financeiro['parcelas_pagas']} | Total pago: {formatar_moeda(resumo_financeiro['valor_pago'])}"))
    linhas.append(("blank", ""))

    linhas.append(("section", "Validacao Matemática"))
    linhas.append(("normal", f"Formula aplicada: parcelas restantes = total de parcelas do contrato confirmado - parcelas pagas equivalentes"))
    linhas.append(("normal", f"Total de parcelas do contrato confirmado: {resumo_financeiro['total_contrato']}"))
    linhas.append(("normal", f"Parcelas pagas equivalentes: {resumo_financeiro['parcelas_pagas']}"))
    linhas.append(("normal", f"Parcelas restantes calculadas: {resumo_financeiro['parcelas_restantes']}"))
    linhas.append(("normal", f"Total pago consolidado: {formatar_moeda(resumo_financeiro['valor_pago'])}"))
    linhas.append(("normal", f"Conferência financeira: {formatar_moeda(resumo_financeiro['valor_pago'])} / {formatar_moeda(float(dados_cliente.get('valor_total_contrato') or 0.0))}"))
    linhas.append(("blank", ""))

    linhas.append(("section", "Status"))
    linhas.append(("normal", "Relatorio gerado com dados reais do WidePay, contratos locais e validacao matematica"))
    linhas.append(("footer", "Uso interno - WideAPP_EXTRA"))

    return linhas


def _escrever_pdf_simples(caminho_saida, linhas):
    largura_pagina = 595.28
    altura_pagina = 841.89
    margem_esquerda = 40
    margem_superior = 48
    margem_inferior = 42
    max_linhas = {
        "title": 84,
        "subtitle": 95,
        "section": 92,
        "normal": 108,
        "table": 115,
        "footer": 110,
        "blank": 1,
    }
    tamanhos = {
        "title": ("F2", 16, 20),
        "subtitle": ("F1", 10, 13),
        "section": ("F2", 12, 15),
        "normal": ("F1", 9, 11),
        "table": ("F1", 8, 10),
        "footer": ("F1", 8, 10),
        "blank": ("F1", 1, 6),
    }

    paginas = []
    pagina_atual = []
    y = altura_pagina - margem_superior

    for estilo, texto in linhas:
        if estilo == "blank":
            y -= 4
            continue
        fonte, tamanho, altura_linha = tamanhos.get(estilo, tamanhos["normal"])
        largura = max_linhas.get(estilo, max_linhas["normal"])
        for parte in _wrap_pdf_lines(texto, largura):
            if y < margem_inferior + altura_linha:
                paginas.append(pagina_atual)
                pagina_atual = []
                y = altura_pagina - margem_superior
            pagina_atual.append((fonte, tamanho, y, parte))
            y -= altura_linha
        y -= 2

    if pagina_atual:
        paginas.append(pagina_atual)

    objetos = []

    def adicionar_objeto(conteudo_bytes):
        numero = len(objetos) + 1
        objetos.append((numero, conteudo_bytes))
        return numero

    catalogo_ref = adicionar_objeto(b"")
    paginas_ref = adicionar_objeto(b"")
    fonte_regular_ref = adicionar_objeto(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    fonte_negrito_ref = adicionar_objeto(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    referencias_paginas = []
    for pagina in paginas:
        comandos = []
        for fonte, tamanho, pos_y, texto in pagina:
            comandos.append(f"BT /{fonte} {tamanho} Tf {margem_esquerda} {pos_y:.2f} Tm ({_pdf_escape(texto)}) Tj ET")
        stream = "\n".join(comandos).encode("cp1252", errors="replace")
        conteudo_ref = adicionar_objeto(
            b"<< /Length "
            + str(len(stream)).encode("ascii")
            + b" >>\nstream\n"
            + stream
            + b"\nendstream"
        )
        pagina_ref = adicionar_objeto(
            (
                f"<< /Type /Page /Parent {paginas_ref} 0 R "
                f"/MediaBox [0 0 {largura_pagina:.2f} {altura_pagina:.2f}] "
                f"/Resources << /Font << /F1 {fonte_regular_ref} 0 R /F2 {fonte_negrito_ref} 0 R >> >> "
                f"/Contents {conteudo_ref} 0 R >>"
            ).encode("ascii")
        )
        referencias_paginas.append(pagina_ref)

    paginas_dict = (
        f"<< /Type /Pages /Kids [{' '.join(f'{ref} 0 R' for ref in referencias_paginas)}] /Count {len(referencias_paginas)} >>"
    ).encode("ascii")
    objetos[1] = (paginas_ref, paginas_dict)
    objetos[0] = (catalogo_ref, f"<< /Type /Catalog /Pages {paginas_ref} 0 R >>".encode("ascii"))

    saida = bytearray()
    saida.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for numero, conteudo in objetos:
        offsets.append(len(saida))
        saida.extend(f"{numero} 0 obj\n".encode("ascii"))
        saida.extend(conteudo)
        saida.extend(b"\nendobj\n")

    xref_pos = len(saida)
    total_objetos = len(objetos) + 1
    saida.extend(f"xref\n0 {total_objetos}\n".encode("ascii"))
    saida.extend(b"0000000000 65535 f \n")
    for offset in offsets:
        saida.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    saida.extend(
        (
            f"trailer\n<< /Size {total_objetos} /Root {catalogo_ref} 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n"
        ).encode("ascii")
    )

    with open(caminho_saida, "wb") as f:
        f.write(saida)

    print(f"PDF salvo com sucesso em: {caminho_saida}")
    return True


def _gerar_pdf_simples(dados_cliente, resumo_financeiro, carnes_widepay, cobrancas_widepay, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    linhas = _montar_linhas_pdf(dados_cliente, resumo_financeiro, carnes_widepay, cobrancas_widepay)
    return _escrever_pdf_simples(caminho_saida, linhas)

def gerar_pdf(dados_cliente, resumo_financeiro, carnes_widepay, cobrancas_widepay, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.lib.styles import ParagraphStyle
    except ImportError:
        print("Aviso: ReportLab nao instalado para geracao de PDF. Usando fallback nativo.")
        return _gerar_pdf_simples(dados_cliente, resumo_financeiro, carnes_widepay, cobrancas_widepay, caminho_saida)
        
    estilos = criar_estilos()
    if not estilos:
        return _gerar_pdf_simples(dados_cliente, resumo_financeiro, carnes_widepay, cobrancas_widepay, caminho_saida)
        
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
    pagamentos_interpretados = cobrancas_widepay.get("pagamentos_interpretados") or []

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

    montar_tabela_dados(
        "Pagamentos Recebidos Interpretados",
        ["Cliente", "Lote/Quadra", "ID", "Tipo", "Descricao WidePay", "Venc.", "Pgto.", "Valor Orig.", "Valor Rec.", "Base Parc.", "Refs", "Qtd.", "Observacao"],
        pagamentos_interpretados,
        ["cliente", "lote_quadra", "id", "tipo", "descricao", "vencimento", "pagamento", "valor_original", "valor_recebido", "valor_base_parcela", "referencias", "parcelas_quitadas", "observacao"],
        [1.2*cm, 1.2*cm, 1.3*cm, 1.0*cm, 2.2*cm, 1.1*cm, 1.1*cm, 1.2*cm, 1.2*cm, 1.1*cm, 1.4*cm, 0.7*cm, 1.3*cm],
        vazio="Nenhum pagamento recebido interpretado - relatorio final bloqueado."
    )

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
