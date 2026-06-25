# -*- coding: utf-8 -*-

def validar_conciliacao(dados_calculados, dados_contrato):
    """
    Valida as regras matemáticas do projeto e retorna o status da auditoria.
    Retorna (status, notas, bloqueado).
    """
    status = "APROVADO"
    bloqueado = False
    notas = []
    
    total_parcelas_contrato = dados_calculados.get("total_parcelas_contrato", 0)
    valor_base = dados_calculados.get("valor_base_parcela", 0.0)
    
    # 1. Bloqueio se não houver contrato confirmado
    if not dados_contrato or total_parcelas_contrato <= 0 or valor_base <= 0.0:
        status = "ERRO"
        bloqueado = True
        notas.append("BLOQUEIO: Contrato local nao localizado ou nao contem parcelas/valores confirmados.")
        return status, notas, bloqueado
        
    # 2. Verificação de parcelas pagas + restantes
    pagas_eq = dados_calculados.get("parcelas_pagas_equivalentes", 0)
    restantes = dados_calculados.get("parcelas_restantes", 0)
    
    soma_parcelas = pagas_eq + restantes
    if soma_parcelas != total_parcelas_contrato:
        status = "ERRO"
        bloqueado = True
        notas.append(f"DIVERGENCIA: A soma das parcelas pagas ({pagas_eq}) e restantes ({restantes}) nao bate com o total do contrato ({total_parcelas_contrato}).")
        
    # 3. Verificação de valores gerados no WidePay excedendo o contrato
    total_pago = dados_calculados.get("total_pago_consolidado", 0.0)
    valor_total_contrato = float(dados_contrato.get("valor_total_contrato") or 0.0)
    
    if total_pago > valor_total_contrato and valor_total_contrato > 0:
        status = "PENDENTE"
        notas.append(f"ALERTA: Total pago extraido (R$ {total_pago:.2f}) excede o valor total pactuado no contrato (R$ {valor_total_contrato:.2f}).")
        
    # 4. Outras divergências menores (ex: cobranças avulsas sem descrição clara)
    pagamentos_interpretados = dados_calculados.get("pagamentos_interpretados") or []
    for p in pagamentos_interpretados:
        if p.get("classificacao") == "avulso" and "competencia" not in p.get("descricao", "").lower():
            if status != "ERRO":
                status = "PENDENTE"
            notas.append(f"AVISO: Cobranca avulsa ID {p['id']} de R$ {p['valor_recebido']:.2f} com descricao vaga ('{p['descricao']}').")
            
    if not notas:
        notas.append("Reconciliacao concluida com sucesso. Sem divergencias encontradas.")
        
    return status, notas, bloqueado
