# -*- coding: utf-8 -*-
"""
Constantes visuais e estilos ReportLab padrão para relatórios do projeto.
"""
import os
from pathlib import Path

# Constantes de Grafia e Localidade (REGRA 17)
TITULO_RELATORIO = "RELATÓRIO FINANCEIRO"
LOCALIDADE = "Loteamento Água Viva — Iaçú-BA"

# Diretório raiz do projeto
PROJETO_ROOT = Path(__file__).resolve().parent.parent.parent

try:
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    
    # Cores Corporativas/Padrão
    CORES = {
        'VERDE_ESCURO': colors.HexColor("#1B5E20"),
        'VERDE_MEDIO': colors.HexColor("#2E7D32"),
        'VERDE_CLARO': colors.HexColor("#C8E6C9"),
        'VERDE_LINHA': colors.HexColor("#A5D6A7"),
        'AZUL': colors.HexColor("#1565C0"),
        'AMARELO': colors.HexColor("#F9A825"),
        'VERMELHO': colors.HexColor("#C62828"),
        'CINZA_ESCURO': colors.HexColor("#37474F"),
        'CINZA_CLARO': colors.HexColor("#ECEFF1"),
        'CINZA_BARRA': colors.HexColor("#B0BEC5"),
        'BRANCO': colors.white
    }
    
    def criar_estilos():
        s = getSampleStyleSheet()['Normal']
        return {
            'titulo': ParagraphStyle('titulo', parent=s, fontSize=22, textColor=CORES['BRANCO'], alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=3),
            'subtitulo': ParagraphStyle('subtitulo', parent=s, fontSize=11, textColor=CORES['VERDE_CLARO'], alignment=TA_CENTER, fontName='Helvetica', spaceAfter=2),
            'secao': ParagraphStyle('secao', parent=s, fontSize=13, textColor=CORES['VERDE_ESCURO'], fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=4),
            'normal': ParagraphStyle('normal', parent=s, fontSize=10, textColor=CORES['CINZA_ESCURO'], fontName='Helvetica', spaceAfter=2),
            'rodape': ParagraphStyle('rodape', parent=s, fontSize=8, textColor=colors.HexColor("#90A4AE"), alignment=TA_CENTER, fontName='Helvetica-Oblique'),
            'bold_verde': ParagraphStyle('bold_verde', parent=s, fontSize=10, textColor=CORES['VERDE_MEDIO'], fontName='Helvetica-Bold'),
            'bold_verm': ParagraphStyle('bold_verm', parent=s, fontSize=10, textColor=CORES['VERMELHO'], fontName='Helvetica-Bold'),
            'pct': ParagraphStyle('pct', parent=s, fontSize=10, textColor=CORES['VERDE_ESCURO'], fontName='Helvetica-Bold', alignment=TA_CENTER),
            'card_label': ParagraphStyle('card_label', parent=s, fontSize=9, textColor=CORES['BRANCO'], fontName='Helvetica', alignment=TA_CENTER),
            'card_valor': ParagraphStyle('card_valor', parent=s, fontSize=15, textColor=CORES['BRANCO'], fontName='Helvetica-Bold', alignment=TA_CENTER),
            'card_label_dark': ParagraphStyle('card_label_dark', parent=s, fontSize=9, textColor=CORES['CINZA_ESCURO'], fontName='Helvetica', alignment=TA_CENTER),
            'card_valor_dark': ParagraphStyle('card_valor_dark', parent=s, fontSize=15, textColor=CORES['CINZA_ESCURO'], fontName='Helvetica-Bold', alignment=TA_CENTER)
        }

except ImportError:
    CORES = {}
    def criar_estilos():
        print("Aviso: ReportLab nao instalado. Nao foi possivel criar estilos.")
        return None
