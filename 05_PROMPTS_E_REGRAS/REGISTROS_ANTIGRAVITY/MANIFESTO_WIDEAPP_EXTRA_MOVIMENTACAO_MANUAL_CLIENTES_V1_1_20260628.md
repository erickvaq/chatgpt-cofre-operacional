# MANIFESTO - WIDEAPP_EXTRA MOVIMENTACAO MANUAL DE CLIENTES - V1.1

## Entrega versionada

- Versao documental: `V1.1`
- Data: `2026-06-28`
- Tipo: `feature + validacao real em ambiente isolado`
- Fonte central da versao do app: `WideAPP_EXTRA/VERSION`

## Arquivos incluidos no commit

- `WideAPP_EXTRA/app/saneamento_clientes.py`
- `WideAPP_EXTRA/app/indexador_clientes.py`
- `WideAPP_EXTRA/app/interface.py`
- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/STATUS_WIDEAPP_EXTRA_MOVIMENTACAO_MANUAL_CLIENTES_20260628.md`
- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/CHANGELOG_WIDEAPP_EXTRA_MOVIMENTACAO_MANUAL_CLIENTES_V1_1_20260628.md`
- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/MANIFESTO_WIDEAPP_EXTRA_MOVIMENTACAO_MANUAL_CLIENTES_V1_1_20260628.md`

## Evidencias locais nao publicadas

Mantidas fora do commit por conterem detalhes locais e operacionais:

- log detalhado da execucao real no isolado
- backups locais do ambiente isolado
- dados reais de clientes em JSON/XLSX do ambiente isolado

## Criterios atendidos

- sem exclusao definitiva de dados
- alteracao restrita ao saneamento operacional
- persistencia manual preservada apos reaplicacao
- validacao real com backup previo e smoke-test posterior

## Criterio de publicacao

Publicar somente artefatos sanitizados e codigo. Nao publicar base real de clientes do ambiente isolado.
