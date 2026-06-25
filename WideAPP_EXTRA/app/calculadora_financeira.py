# -*- coding: utf-8 -*-

def interpretar_pagamentos(cobrancas, valor_base):
    """Interpreta os pagamentos recebidos no WidePay e calcula a equivalência em parcelas."""
    interpretados = []
    for cob in cobrancas:
        if "recebido" not in str(cob.get("status", "")).lower():
            continue
            
        valor_original = float(cob.get("valor_original") or 0.0)
        valor_recebido = float(cob.get("valor_recebido") or 0.0)
        
        # Proporção em relação ao valor base da parcela
        if valor_base > 0 and valor_original > 0:
            proporcao = valor_original / valor_base
            qtd = max(1, int(round(proporcao)))
        else:
            qtd = 1
            
        desc = cob.get("descricao") or "-"
        
        interpretados.append({
            "id": cob.get("id", "-"),
            "forma": cob.get("forma", "-"),
            "cliente": cob.get("cliente", "-"),
            "descricao": desc,
            "vencimento": cob.get("vencimento", "-"),
            "pagamento": cob.get("pagamento", "-"),
            "valor_original": valor_original,
            "valor_recebido": valor_recebido,
            "valor_base": valor_base,
            "qtd": qtd,
            "classificacao": cob.get("classificacao", "avulso")
        })
    return interpretados

def calcular_resumo(dados_normalizados, dados_contrato):
    """Calcula totais consolidados e reconcilia com as regras contratuais."""
    valor_base = float(dados_contrato.get("valor_parcela") or 0.0)
    total_parcelas_contrato = int(dados_contrato.get("total_parcelas") or 0)
    
    cobrancas = dados_normalizados.get("cobrancas") or []
    
    # Interpretar pagamentos recebidos
    pagamentos_interpretados = interpretar_pagamentos(cobrancas, valor_base)
    
    # Soma de parcelas pagas equivalentes
    parcelas_pagas_equivalentes = sum(p["qtd"] for p in pagamentos_interpretados)
    
    # Parcelas restantes (calculadas pelo contrato)
    if total_parcelas_contrato > 0:
        parcelas_restantes = max(0, total_parcelas_contrato - parcelas_pagas_equivalentes)
    else:
        parcelas_restantes = 0
        
    # Totais de Caixa (WidePay)
    total_pago_carnes = 0.0
    total_pago_avulsos = 0.0
    total_pendente_cobrancas = 0.0
    
    for cob in cobrancas:
        status_lower = cob.get("status", "").lower()
        val_original = float(cob.get("valor_original") or 0.0)
        val_recebido = float(cob.get("valor_recebido") or 0.0)
        
        if status_lower == "recebido":
            if cob.get("pertence_a_carne"):
                total_pago_carnes += val_recebido
            else:
                total_pago_avulsos += val_recebido
        elif status_lower in ["aguardando", "vencido"]:
            total_pendente_cobrancas += val_original
            
    total_pago_consolidado = total_pago_carnes + total_pago_avulsos
    valor_restante_contrato = parcelas_restantes * valor_base
    
    return {
        "valor_base_parcela": valor_base,
        "total_parcelas_contrato": total_parcelas_contrato,
        "parcelas_pagas_equivalentes": parcelas_pagas_equivalentes,
        "parcelas_restantes": parcelas_restantes,
        "total_pago_carnes": round(total_pago_carnes, 2),
        "total_pago_avulsos": round(total_pago_avulsos, 2),
        "total_pago_consolidado": round(total_pago_consolidado, 2),
        "total_pendente_consolidado": round(total_pendente_cobrancas, 2),
        "valor_restante_contrato": round(valor_restante_contrato, 2),
        "pagamentos_interpretados": pagamentos_interpretados
    }
