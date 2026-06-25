# VERSÃO SANITIZADA DO EXCEL - Edmilson F05 (1402)

## Aba: Resumo

| Campo | Valor |
|---|---|
| Cliente | Edm***tos |
| Lote / Quadra | F05 / Quadra F |
| Loteamento | Água Viva — Iaçú-BA |
| Data do Relatório | 25/06/2026 |
| Valor Total Contratado | 10500 |
| Entrada ou Valor Fora do Parcelamento | 600 |
| Saldo Parcelado | 9900 |
| Total de Parcelas (Contrato) | 100 |
| Valor Base da Parcela | 99 |
| RESUMO FINANCEIRO |  |
| Total Pago Recebido | 3585.91 |
| Parcelas Pagas Confirmadas | 34 |
| Parcelas Restantes | 66 |
| % Parcelas Quitadas | 0.34 |
| % Financeiro Pago | 0.3415152380952381 |
| Situação Calculada | INICIAL |


## Aba: Pagamentos Recebidos

**Colunas (14):** Cliente, Lote/Quadra, ID, Tipo, Descrição WidePay, Vencimento, Data Pagamento, Valor Original, Valor Recebido, Status, Valor Base Parcela, Referências, Parcelas Quitadas, Observação

**Total de linhas:** 31

**Linha de Totalizacao:** Original R$ None, Recebido R$ None, Qtd Parc None


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

