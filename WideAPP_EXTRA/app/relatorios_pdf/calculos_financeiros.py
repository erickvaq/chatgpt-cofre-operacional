# -*- coding: utf-8 -*-
"""
Funções de cálculo financeiro e formatação para relatórios.
"""

def calcular_resumo(total_contrato, parcelas_pagas, valor_parcela, valor_pago_real):
    parcelas_restantes = total_contrato - parcelas_pagas
    percentual_pago = parcelas_pagas / total_contrato if total_contrato > 0 else 0.0
    percentual_restante = parcelas_restantes / total_contrato if total_contrato > 0 else 0.0
    valor_restante = parcelas_restantes * valor_parcela
    
    return {
        'total_contrato': total_contrato,
        'parcelas_pagas': parcelas_pagas,
        'parcelas_restantes': parcelas_restantes,
        'percentual_pago': percentual_pago,
        'percentual_restante': percentual_restante,
        'valor_pago': valor_pago_real,
        'valor_restante': valor_restante,
        'valor_parcela': valor_parcela
    }

def validar_dados(resumo):
    avisos = []
    if resumo['parcelas_pagas'] > resumo['total_contrato']:
        avisos.append("Erro: Parcelas pagas excedem o total do contrato.")
    if resumo['valor_pago'] < 0:
        avisos.append("Erro: Valor pago nao pode ser negativo.")
    return avisos

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
