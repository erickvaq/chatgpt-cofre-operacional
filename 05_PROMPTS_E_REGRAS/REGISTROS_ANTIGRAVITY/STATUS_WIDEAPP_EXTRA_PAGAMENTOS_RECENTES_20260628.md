# STATUS WIDEAPP_EXTRA - PAGAMENTOS RECENTES - 2026-06-28

## Objetivo

Adicionar ao `WideAPP_EXTRA` uma aba `Pagamentos Recentes` ao lado de `Ativos`, usando a mesma base de clientes ativos e exibindo uma janela movel dos ultimos 5 meses com status mensal vindo do WidePay/cache.

## Versao desta entrega

- Versao: `V1.2`
- Fonte central da versao: `WideAPP_EXTRA/VERSION`

## Resultado consolidado

- Aba `Pagamentos Recentes`: concluida
- Mesmo conjunto filtrado de clientes da aba `Ativos`: concluido
- 5 colunas dinamicas por mes: concluido
- Persistencia em `clientes_indexados.json`: concluida
- Recalculo automatico ao usar `Atualizar clientes`: concluido
- Exportacao para aba `Pagamentos_Recentes` no banco visual XLSX: concluida
- Validacao no projeto principal: concluida
- Validacao no ambiente isolado: concluida

## Arquivos de codigo envolvidos

- `WideAPP_EXTRA/VERSION`
- `WideAPP_EXTRA/app/indexador_clientes.py`
- `WideAPP_EXTRA/app/interface.py`

## Regras de dados aplicadas

- status mensal validos: `Pago`, `Vencido` ou `-`
- prioridade por mes: `Pago` prevalece sobre `Vencido` quando houver mais de um registro relevante
- exclusoes do calculo mensal: `entrada`, `atraso`, `avulso` e `duplicidade`
- origem principal: cobrancas normalizadas do WidePay/cache global

## Validacao tecnica no projeto principal

- `py_compile` em `indexador_clientes.py` e `interface.py`
- `python WideAPP_EXTRA/main.py --smoke-test-interface`
- instancia da interface confirmando:
  - titulo `WideAPP_EXTRA - Versao V1.2`
  - badge `Versao V1.2`
  - segunda aba `Pagamentos Recentes`
  - meses `Fev/26`, `Mar/26`, `Abr/26`, `Mai/26`, `Jun/26`

Resultado: aprovado.

## Validacao no ambiente isolado

Escopo usado:

- `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA`

Backup local antes da copia:

- `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA\backups\pagamentos_recentes_v1_2_20260628_200225`

Arquivos sincronizados no isolado:

- `VERSION`
- `app/indexador_clientes.py`
- `app/interface.py`

Validacoes no isolado:

- `py_compile`
- `python main.py --smoke-test-interface`

Resultado: aprovado.

## Observacao funcional

Quando nao existe evidencia mensal suficiente no cache para aquele cliente/mes, a celula fica como `-` em vez de inventar `Pago` ou `Vencido`.
