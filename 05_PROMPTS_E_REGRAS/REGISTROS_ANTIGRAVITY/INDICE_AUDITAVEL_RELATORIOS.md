# INDICE AUDITAVEL - Relatorios Financeiros Locais

## Finalidade
Registrar arquivos sensiveis mantidos localmente sem publicar valores financeiros, IDs detalhados, datas de pagamento individualizadas ou dados pessoais completos no GitHub publico.

## Registro 001 - XLSX Edmilson / Edimson F05

| Campo | Valor |
|---|---|
| Arquivo | `RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_SILVA_DOS_SANTOS_LOTE_F05_20260625_V2.xlsx` |
| Caminho local | `02_RELATORIOS_GERADOS/` |
| Cliente/lote | Edmilson / Edimson - F05 |
| Tipo | Relatorio financeiro principal em XLSX |
| Status | Gerado localmente - consultado no WidePay em 25/06/2026 |
| Conteudo sensivel | Sim |
| Motivo de nao subir completo | Contem dados financeiros individualizados |
| Versao publica | `RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_F05_SANITIZADO_V2.md` (publicado no GitHub) |
| Proximo passo | Validacao manual local |

## Registro 002 - Conferencia MD Edmilson / Edimson F05

| Campo | Valor |
|---|---|
| Arquivo | `CONFERENCIA_CALCULOS_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO.md` |
| Caminho local | `07_DADOS_TEMPORARIOS/` |
| Cliente/lote | Edmilson / Edimson - F05 |
| Tipo | Conferencia financeira com pagamentos interpretados |
| Status | Gerado localmente com base na consulta WidePay de 25/06/2026 |
| Conteudo sensivel | Sim |
| Motivo de nao subir completo | Contem tabela de pagamentos, IDs, valores e datas |
| Versao publica | Registro sanitizado no indice publico |

## Registro 003 - JSON WidePay Edmilson

| Campo | Valor |
|---|---|
| Arquivo | `WIDEPAY_EDMILSON.json` |
| Caminho local | `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/` |
| Cliente/lote | Edmilson / Edimson - F05 |
| Tipo | Extracao bruta do WidePay |
| Status | Mantido localmente (gerado em 25/06/2026) |
| Conteudo sensivel | Sim |
| Motivo de nao subir completo | Contem dados financeiros brutos de carnes, cobrancas e boletos |
| Versao publica | Registro sanitizado no indice publico |

## Regra de Publicacao
* XLS/XLSX e o formato principal de relatorio financeiro.
* PDF somente deve ser gerado quando o usuario pedir explicitamente.
* Este indice nao deve conter valores financeiros detalhados.
