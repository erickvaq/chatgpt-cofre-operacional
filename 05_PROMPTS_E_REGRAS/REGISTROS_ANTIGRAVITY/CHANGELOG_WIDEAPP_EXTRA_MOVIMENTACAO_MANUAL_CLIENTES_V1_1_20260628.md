# CHANGELOG - WIDEAPP_EXTRA MOVIMENTACAO MANUAL DE CLIENTES - V1.1

Data: 2026-06-28
Escopo: entrega incremental da funcionalidade de reorganizacao manual de clientes.
Fonte central da versao do app: `WideAPP_EXTRA/VERSION`

## V1.1

### Adicionado

- Movimento manual entre `Ativos`, `Quitados` e `Bloqueados / Removidos`
- Persistencia de override manual em `saneamento_clientes.json`
- Auditoria manual de cada acao
- Atualizacao do `BANCO_DADOS_WIDEAPP_EXTRA.xlsx` apos movimentacao
- Confirmacao para selecao unica e multipla

### Ajustado

- Reaplicacao do saneamento passou a respeitar override manual
- Interface passou a recarregar abas e resumo apos movimentacao

### Validado

- `py_compile`
- `smoke-test-interface`
- teste real no ambiente isolado com gravacao no XLSX real do isolado
- restauracao automatica em caso de erro

## Observacao de versionamento

O rotulo `V1.1` foi aplicado aos artefatos desta entrega para marcar a primeira consolidacao funcional apos a base `1.0` mencionada pelo usuario.

O texto visual de versao exibido na interface nao foi alterado nesta rodada para evitar trocar a convencao do aplicativo sem regra local explicita.
