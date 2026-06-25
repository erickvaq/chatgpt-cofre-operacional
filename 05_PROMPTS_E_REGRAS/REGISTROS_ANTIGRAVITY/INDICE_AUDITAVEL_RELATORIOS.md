# ÍNDICE AUDITÁVEL — Relatórios Financeiros Locais
# Gerado em: 2026-06-25
# Finalidade: Rastreabilidade dos arquivos sensíveis gerados localmente (REGRA 10.4)

---

## Registro 001 — Excel Edmilson F05

| Campo                | Valor |
|---------------------|-------|
| Arquivo              | `RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_SILVA_DOS_SANTOS_LOTE_F05_20260625.xlsx` |
| Caminho local        | `02_RELATORIOS_GERADOS/` |
| Cliente              | Edmilson Silva Dos Santos (alias: Edimson Silva Dos Santis) |
| Lote / Quadra        | F05 / Quadra F |
| Data/hora de geração | 2026-06-25 12:25 (UTC-3) |
| Tipo de dado         | Relatório financeiro individual com valores e datas de pagamento |
| Status               | Gerado — aguardando validação do usuário |
| Abas geradas         | Resumo, Pagamentos Recebidos, Interpretação Parcelas, Validação |
| Pagamentos incluídos | 29 registros com status Recebido/Pago e valor > R$ 0,00 |
| Total pago registrado | R$ 3.585,91 |
| Parcelas pagas equiv. | 34 de 100 |
| Parcelas restantes   | 66 |
| Alertas              | 0 |
| Validação matemática | 8 de 8 checagens OK |
| JSON fonte           | `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/WIDEPAY_EDMILSON.json` |
| Script gerador       | `03_SCRIPTS/gerar_relatorio_excel.py` |
| Motivo de não subir completo | Contém dados financeiros individualizados com datas e valores de pagamento |
| Versão sanitizada    | Este índice auditável |

---

## Registro 002 — Conferência MD Edmilson F05

| Campo                | Valor |
|---------------------|-------|
| Arquivo              | `CONFERENCIA_CALCULOS_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO.md` |
| Caminho local        | `07_DADOS_TEMPORARIOS/` |
| Cliente              | Edmilson F05 Água Viva LÉO |
| Data/hora de geração | 2026-06-16 (gerado em sessão anterior) |
| Tipo de dado         | Conferência financeira com tabela de pagamentos interpretados |
| Status               | Gerado — aguardando validação final do usuário |
| Motivo de não subir completo | Contém tabela de pagamentos com IDs, valores e datas individuais |
| Versão sanitizada    | Totais disponíveis no painel operacional |

---

## Registro 003 — JSON WidePay Edmilson

| Campo                | Valor |
|---------------------|-------|
| Arquivo              | `WIDEPAY_EDMILSON.json` |
| Caminho local        | `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/` |
| Cliente              | Edmilson / Edimson — F05 |
| Data/hora de geração | Sessão anterior (junho 2026) |
| Tipo de dado         | Extração bruta do WidePay — cobranças, carnês, boletos |
| Status               | Mantido local — fonte para o Excel gerado |
| Motivo de não subir completo | Dado financeiro bruto com IDs de boleto e valores individuais |
| Versão sanitizada    | Este índice auditável |

---

_Atualizado conforme REGRA 10.4 — Antigravity — 2026-06-25_
