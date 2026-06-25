# -*- coding: utf-8 -*-

def classificar_registro(cob, valor_base):
    desc_lower = (cob.get("descricao") or "").lower()
    status_lower = (cob.get("status") or "").lower()
    
    if "entrada" in desc_lower or "sinal" in desc_lower:
        return "entrada"
    if any(term in desc_lower for term in ["atraso", "atrazos", "ref atraso", "atr"]):
        return "atraso"
    if status_lower in ["aguardando", "vencido"]:
        return "pendência"
        
    pertence = cob.get("pertence_a_carne", False)
    if pertence:
        return "parcela normal"
        
    # Heurística baseada no valor base do contrato
    if valor_base > 0 and abs(cob.get("valor_original", 0) - valor_base) < 0.01:
        return "parcela normal"
        
    return "avulso"

def normalizar_e_deduplicar(dados_raw_wp, valor_base=0.0):
    """Filtra, limpa duplicidades e classifica os boletos e carnês do WidePay."""
    carnes_raw = dados_raw_wp.get("carnes") or []
    cobrancas_raw = dados_raw_wp.get("cobrancas") or []
    
    carnes_lista = []
    for c in carnes_raw:
        if c.get("status", "").lower() != "cancelado":
            carnes_lista.append(c)
            
    cobrancas_unicas = []
    possiveis_duplicidades = []
    
    for cob in cobrancas_raw:
        is_duplicate = False
        # Identificar duplicidade exata
        for existing in cobrancas_unicas:
            if (existing.get("id") == cob.get("id") and cob.get("id")) or (
                existing.get("descricao") == cob.get("descricao") and 
                existing.get("vencimento") == cob.get("vencimento") and 
                abs(existing.get("valor_original", 0) - cob.get("valor_original", 0)) < 0.01 and 
                abs(existing.get("valor_recebido", 0) - cob.get("valor_recebido", 0)) < 0.01 and 
                existing.get("status") == cob.get("status")
            ):
                is_duplicate = True
                break
                
        # Heurística para confirmar se pertence a carne
        desc_lower = (cob.get("descricao") or "").lower()
        pertence_a_carne = "carne" in desc_lower or "carnê" in desc_lower
        
        if not pertence_a_carne:
            for c in carnes_lista:
                if abs(cob.get("valor_original", 0) - float(c.get("valor_parcela", 0))) < 0.01:
                    ref_lower = c.get("referencia", "").lower()
                    if not (cob.get("descricao") or "").strip() or (ref_lower and ref_lower in desc_lower):
                        if not any(word in desc_lower for word in ["atraso", "atrazos", "ref atraso", "atr", "mês", "mes"]):
                            pertence_a_carne = True
                            break
                            
        cob["pertence_a_carne"] = pertence_a_carne
        cob["avulsa"] = not pertence_a_carne
        cob["duplicidade"] = is_duplicate
        cob["classificacao"] = classificar_registro(cob, valor_base)
        
        if is_duplicate:
            possiveis_duplicidades.append(cob)
        else:
            cobrancas_unicas.append(cob)
            
    return {
        "carnes": carnes_lista,
        "cobrancas": cobrancas_unicas,
        "duplicidades": possiveis_duplicidades
    }
