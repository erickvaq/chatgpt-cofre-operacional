# CHANGELOG - WIDEAPP_EXTRA PAGAMENTOS RECENTES - V1.2

Data: 2026-06-28
Escopo: nova visao mensal para clientes ativos.
Fonte central da versao do app: `WideAPP_EXTRA/VERSION`

## V1.2

### Adicionado

- aba `Pagamentos Recentes` ao lado de `Ativos`
- 5 colunas mensais dinamicas em ordem cronologica
- derivacao persistida de `pagamentos_recentes_5m` por cliente
- exportacao da aba `Pagamentos_Recentes` no `BANCO_DADOS_WIDEAPP_EXTRA.xlsx`

### Ajustado

- `carregar_cache()` passou a enriquecer registros antigos sem mapa mensal usando o cache global WidePay
- menu de contexto e selecao passaram a funcionar tambem na aba nova
- versao visual do app passou para `V1.2` pela fonte central

### Validado

- `py_compile`
- `WideAPP_EXTRA/main.py --smoke-test-interface`
- instancia local da interface com conferencia de titulo, badge, aba e rotulos dos meses
- `python main.py --smoke-test-interface` no ambiente isolado
