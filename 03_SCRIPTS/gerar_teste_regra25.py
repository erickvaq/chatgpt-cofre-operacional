# -*- coding: utf-8 -*-
"""
Script de teste controlado para a REGRA 25.
Gera HTML + PDF emparelhados e atalhos bat de abertura na pasta designada.
"""
import os
import sys
from pathlib import Path

PROJETO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJETO_ROOT))

# Pasta de saída
SAIDA_DIR = PROJETO_ROOT / "02_RELATORIOS_GERADOS" / "TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1"
os.makedirs(SAIDA_DIR, exist_ok=True)

HTML_PATH = SAIDA_DIR / "TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1.html"
PDF_PATH = SAIDA_DIR / "TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1.pdf"
BAT_PDF_PATH = SAIDA_DIR / "01_ABRIR_PDF_FINAL.bat"
BAT_HTML_PATH = SAIDA_DIR / "02_ABRIR_PREVIA_HTML.bat"

# 1. Gerar HTML
html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Validação da REGRA 25</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #ECEFF1;
            margin: 0;
            padding: 40px 20px;
            color: #37474F;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #FFFFFF;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #1A237E, #283593);
            color: #FFFFFF;
            padding: 24px;
            border-radius: 6px;
            text-align: center;
            margin-bottom: 25px;
        }
        .header h1 {
            margin: 0;
            font-size: 22px;
            letter-spacing: 1px;
        }
        .details {
            line-height: 1.6;
            font-size: 14px;
        }
        .details ul {
            padding-left: 20px;
        }
        .details li {
            margin-bottom: 8px;
        }
        .footer {
            margin-top: 30px;
            border-top: 1px solid #1A237E;
            padding-top: 15px;
            text-align: center;
            font-size: 12px;
            color: #90A4AE;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Controle de Sincronização — REGRA 25</h1>
        </div>
        <div class="details">
            <p>Este arquivo valida a persistência e publicação de todos os artefatos de execução no GitHub.</p>
            <p><strong>Informações da Entrega de Controle:</strong></p>
            <ul>
                <li><strong>Nome do Teste:</strong> Teste de Validação da REGRA 25</li>
                <li><strong>Objetivo:</strong> Confirmar que todo artefato gerado possui caminho local e link do GitHub real.</li>
                <li><strong>Data de Criação:</strong> 2026-06-20</li>
                <li><strong>Versão:</strong> V1</li>
                <li><strong>Projeto:</strong> Relatorio_WidePay_Lotes</li>
                <li><strong>Loteamento:</strong> Loteamento Água Viva — Iaçú-BA</li>
            </ul>
        </div>
        <div class="footer">
            Relatório gerado em 20/06/2026 | Antigravity IDE & Codex
        </div>
    </div>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML gerado com sucesso em: {HTML_PATH}")

# 2. Gerar PDF usando ReportLab
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
except ImportError:
    print("ReportLab não instalado. Abortando geração de PDF.")
    sys.exit(1)

doc = SimpleDocTemplate(
    str(PDF_PATH), pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()
normal_style = styles['Normal']

title_style = ParagraphStyle(
    'title', parent=normal_style, fontSize=20,
    textColor=colors.HexColor("#FFFFFF"), alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'body', parent=normal_style, fontSize=11,
    textColor=colors.HexColor("#37474F"), fontName='Helvetica',
    spaceAfter=10, leading=16
)

bullet_style = ParagraphStyle(
    'bullet', parent=normal_style, fontSize=11,
    textColor=colors.HexColor("#37474F"), fontName='Helvetica',
    leftIndent=20, firstLineIndent=-10, spaceAfter=6, leading=14
)

footer_style = ParagraphStyle(
    'footer', parent=normal_style, fontSize=9,
    textColor=colors.HexColor("#90A4AE"), alignment=TA_CENTER,
    fontName='Helvetica-Oblique'
)

elements = []

# Cabeçalho
header_table = Table([[Paragraph("Controle de Sincronização — REGRA 25", title_style)]], colWidths=[17*cm])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1A237E")),
    ('TOPPADDING', (0,0), (-1,-1), 20),
    ('BOTTOMPADDING', (0,0), (-1,-1), 20),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
]))
elements.append(header_table)
elements.append(Spacer(1, 1*cm))

# Corpo
elements.append(Paragraph("Este arquivo valida a persistência e publicação de todos os artefatos de execução no GitHub.", body_style))
elements.append(Spacer(1, 0.5*cm))
elements.append(Paragraph("<b>Informações da Entrega de Controle:</b>", body_style))

# Detalhes
details = [
    "• <b>Nome do Teste:</b> Teste de Validação da REGRA 25",
    "• <b>Objetivo:</b> Confirmar que todo artefato gerado possui caminho local e link do GitHub real.",
    "• <b>Data de Criação:</b> 2026-06-20",
    "• <b>Versão:</b> V1",
    "• <b>Projeto:</b> Relatorio_WidePay_Lotes",
    "• <b>Loteamento:</b> Loteamento Água Viva — Iaçú-BA"
]

for d in details:
    elements.append(Paragraph(d, bullet_style))

elements.append(Spacer(1, 2*cm))

# Rodapé
elements.append(Paragraph("Relatório gerado em 20/06/2026 | Antigravity IDE & Codex", footer_style))

doc.build(elements)
print(f"PDF gerado com sucesso em: {PDF_PATH}")

# 3. Gerar arquivos BAT de abertura
with open(BAT_PDF_PATH, "w", encoding="utf-8") as f:
    f.write('@echo off\ncd /d "%~dp0"\nstart "" "TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1.pdf"\n')

with open(BAT_HTML_PATH, "w", encoding="utf-8") as f:
    f.write('@echo off\ncd /d "%~dp0"\nstart "" "TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1.html"\n')

print("Batch files de abertura gerados.")
