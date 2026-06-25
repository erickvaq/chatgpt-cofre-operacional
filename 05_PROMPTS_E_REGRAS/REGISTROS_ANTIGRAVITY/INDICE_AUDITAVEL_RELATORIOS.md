# INDICE AUDITAVEL - Relatorios Financeiros Locais

## Finalidade
Registrar a geração dos arquivos completos e a sua rastreabilidade, garantindo que o arquivo final foi para o Google Drive e as evidências estão acessíveis.

## Registro 001 - XLSX Edmilson / Edimson F05

| Campo | Valor |
|---|---|
| Arquivo | `RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_SILVA_DOS_SANTOS_LOTE_F05_20260625_1312.xlsx` |
| Caminho local | `02_RELATORIOS_GERADOS/` |
| Cliente/lote | Edmilson / Edimson - F05 |
| Tipo | Relatorio financeiro principal em XLSX |
| Status | Gerado localmente - consultado no WidePay em 25/06/2026 |
| Arquivo Completo | Sim |
| Upload Google Drive | Sim (Regra 13) |
| Versao publica | `RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_F05_SANITIZADO_1312.md` (publicado no GitHub) |
| Proximo passo | Validacao manual local |

## Registro 002 - Conferencia MD Edmilson / Edimson F05

| Campo | Valor |
|---|---|
| Arquivo | `CONFERENCIA_CALCULOS_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO.md` |
| Caminho local | `07_DADOS_TEMPORARIOS/` |
| Cliente/lote | Edmilson / Edimson - F05 |
| Tipo | Conferencia financeira com pagamentos interpretados |
| Status | Gerado localmente com base na consulta WidePay de 25/06/2026 |
| Arquivo Completo | Sim |
| Upload Google Drive | Sim (Regra 13) |
| Versao publica | Registro sanitizado no indice publico |

## Registro 003 - JSON WidePay Edmilson

| Campo | Valor |
|---|---|
| Arquivo | `WIDEPAY_EDMILSON.json` |
| Caminho local | `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/` |
| Cliente/lote | Edmilson / Edimson - F05 |
| Tipo | Extracao bruta do WidePay |
| Status | Mantido localmente (gerado em 25/06/2026) |
| Arquivo Completo | Sim |
| Upload Google Drive | N/A (Arquivo Temporario Bruto) |
| Versao publica | Registro sanitizado no indice publico |

## Regra de Publicacao
* XLS/XLSX e o formato principal de relatorio financeiro.
* PDF somente deve ser gerado quando o usuario pedir explicitamente.
* O arquivo completo original nao tem mais bloqueios de sensibilidade (Regra 13).
