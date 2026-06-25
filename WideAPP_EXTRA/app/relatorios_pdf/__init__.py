# -*- coding: utf-8 -*-
"""
Pacote de módulos para geração de relatórios PDF.
"""
from .modelo_visual_relatorio import CORES, criar_estilos, TITULO_RELATORIO, LOCALIDADE
from .calculos_financeiros import calcular_resumo, validar_dados, formatar_moeda
from .gerar_html_previa import gerar_html
from .gerar_pdf_final import gerar_pdf
from .abrir_resultado import abrir_externo, abrir_via_bat
