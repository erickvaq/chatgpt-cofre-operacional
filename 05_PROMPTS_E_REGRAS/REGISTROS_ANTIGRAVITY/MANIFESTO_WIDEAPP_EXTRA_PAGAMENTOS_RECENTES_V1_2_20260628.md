# MANIFESTO - WIDEAPP_EXTRA PAGAMENTOS RECENTES - V1.2

## Entrega versionada

- Versao documental: `V1.2`
- Data: `2026-06-28`
- Tipo: `feature de interface + persistencia + validacao principal/isolado`
- Fonte central da versao do app: `WideAPP_EXTRA/VERSION`

## Arquivos incluidos no commit

- `WideAPP_EXTRA/VERSION`
- `WideAPP_EXTRA/app/indexador_clientes.py`
- `WideAPP_EXTRA/app/interface.py`
- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/STATUS_WIDEAPP_EXTRA_PAGAMENTOS_RECENTES_20260628.md`
- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/CHANGELOG_WIDEAPP_EXTRA_PAGAMENTOS_RECENTES_V1_2_20260628.md`
- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/MANIFESTO_WIDEAPP_EXTRA_PAGAMENTOS_RECENTES_V1_2_20260628.md`
- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/REGISTRO_VERSAO_WIDEAPP_EXTRA_V1_2_20260628.md`

## Evidencias locais nao publicadas

Mantidas fora do commit:

- base real de clientes do cache principal e do isolado
- backups locais do ambiente isolado
- XLSX real do ambiente isolado

## Criterios atendidos

- nenhuma segunda lista paralela de ativos foi criada
- a aba nova reaproveita os mesmos filtros e a mesma ordem da aba `Ativos`
- o calculo mensal nao inventa status quando o cache nao comprova o mes
- a versao visivel da interface ficou alinhada com a versao documental
