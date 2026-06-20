# RELATÓRIO DE CONFERÊNCIA — CLIENTE TESTE USO REAL
# Gerado em: 20/06/2026
# Finalidade: Auditar cálculos antes de gerar o PDF final (Versão V2 Corrigida)

---

## 1. DADOS DO CONTRATO (Fonte: Contrato físico localizado na pasta de consulta)

| Campo                    | Valor                          |
|--------------------------|--------------------------------|
| Cliente                  | CLIENTE TESTE USO REAL         |
| Lote                     | TESTE-01 (Quadra TESTE)        |
| Empreendimento           | Loteamento Água Viva, Iaçú-BA  |
| Total de parcelas        | **100 parcelas**               |
| Valor de cada parcela    | R$ 100.00 (nominal)            |
| Valor total do contrato  | R$ 10000.00                    |
| Vencimento               | 10/07/2026                     |
| Data de assinatura       | 20 de junho de 2026            |
| Previsão de quitação     | 10/10/2034                     |

---

## 2. DADOS DO WIDEPAY (Fonte: Histórico de Carnês no WidePay)

| Carnê | Valor/Parcela | Parcelas Geradas | Parcelas Pagas | Total Recebido | Último Vencimento | Status     |
|-------|--------------|------------------|----------------|----------------|-------------------|------------|
| 999   | R$ 100.00     | 100              | 30             | R$ 3000.00     | 10/06/2026        | Ativo      |

---

## 3. CÁLCULO DAS PARCELAS E SALDOS

| Indicador                   | Valor correto         | Fonte                         |
|-----------------------------|-----------------------|-------------------------------|
| Total do contrato           | **100 parcelas**      | Contrato físico |
| Parcelas pagas (WidePay)    | **30 parcelas**       | Soma dos recebimentos WidePay |
| Parcelas vencidas (não pagas)| 0                     | Verificação de cobranças em atraso |
| Parcelas em aberto (ativas) | 70                    | Parcelas restantes no contrato |
| Parcelas restantes (contrato)| **70 parcelas**      | Total - Pagas |
| Percentual pago             | **30%**               | Parcelas pagas / Total × 100 |
| Percentual restante         | **70%**               | Parcelas restantes / Total × 100 |
| Total pago em reais         | R$ 3000.00            | Recebimentos WidePay |
| Total ainda a pagar (nominal)| R$ 7000.00            | Restantes × Valor da parcela |

---

## 4. DIVERGÊNCIAS E AUDITORIA

1. **Dados validados:** Teste corrigido de uso real (REGRA 24 e 25) executado com sucesso.
2. **Cálculos Gerais:** Auditados e em conformidade.
3. **Status:** CONFERIDO, ATUALIZADO E VALIDADO.
