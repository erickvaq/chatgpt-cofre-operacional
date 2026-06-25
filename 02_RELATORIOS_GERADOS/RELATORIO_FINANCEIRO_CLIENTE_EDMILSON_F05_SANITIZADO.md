# VERSÃO SANITIZADA DO EXCEL - Edmilson F05

## Aba: Resumo

| Campo | Valor |
|---|---|
| Cliente | Edm***tos |
| Lote / Quadra | F05 / Quadra F |
| Loteamento | Água Viva — Iaçú-BA |
| Data do Relatório | 25/06/2026 |
| Total de Parcelas (Contrato) | 100 |
| Valor Base da Parcela | 99 |
| Valor Total Contratado | 10500 |
| RESUMO FINANCEIRO |  |
| Total Pago Recebido | 3585.91 |
| Parcelas Pagas Equivalentes | 34 |
| Parcelas Restantes | 66 |
| % Parcelas Quitadas | 0.34 |
| % Financeiro Pago | 0.3415152380952381 |
| Situação Calculada | INICIAL |


## Aba: Pagamentos Recebidos

**Colunas (14):** Cliente, Lote/Quadra, ID, Tipo, Descrição WidePay, Vencimento, Data Pagamento, Valor Original, Valor Recebido, Status, Valor Base Parcela, Referências, Parcelas Quitadas, Observação

**Total de linhas:** 31

**Linha de Totais:** Valor Original: None | Valor Recebido: None | Parcelas: None


| ID (mascarado) | Vencimento | Data Pagamento | Valor Orig. | Valor Rec. | Parcelas |
|---|---|---|---|---|---|
| 8A*** | 10/01/2021 | 29/01/2021 | 99 | 105.35 | 1 |
| 51*** | 10/08/2021 | 19/10/2021 | 99 | 117.14 | 1 |
| 20*** | 10/09/2021 | 19/10/2021 | 99 | 109.98 | 1 |
| 50*** | 10/10/2021 | 19/10/2021 | 99 | 103.05 | 1 |
| 5A*** | 10/12/2021 | 31/01/2022 | 99 | 112.99 | 1 |
| ... | ... | ... | ... | ... | ... |


## Aba: Interpretação Parcelas



## Aba: Validação

| # | Validação | Resultado | Status |
|---|---|---|---|
| 1 | Total pago = soma dos valores recebidos | R$ 3585.91 vs R$ 3585.91 | ✅ OK |
| 2 | Parcelas pagas = soma das parcelas interpretadas | 34 vs 34 | ✅ OK |
| 3 | Parcelas restantes = contrato - pagas | 66 = 100 - 34 | ✅ OK |
| 4 | % parcelas = pagas / contrato | 34.00% = 34 / 100 | ✅ OK |
| 5 | % financeiro = recebido / contratado | 34.15% = R$ 3585.91 / R$ 10500.00 | ✅ OK |
| 6 | Nenhum vencido/aguardando/cancelado na aba Pagamentos | Todos 29 registros são Recebido/Pago | ✅ OK |
| 7 | Nenhum Recebido com valor R$ 0,00 | Checagem de 29 registros | ✅ OK |
| 8 | Todo pagamento recebido possui interpretação | 29 pagamentos interpretados | ✅ OK |

