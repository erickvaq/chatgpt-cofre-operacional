# STATUS - WIDEAPP_EXTRA ATUALIZAR CLIENTES INCREMENTAL - 2026-06-26

## Objetivo

Aprimorar o botao principal da WideAPP_EXTRA para atuar como atualizacao incremental da lista principal.

## Alteracao visual e funcional

- Nome antigo do botao: `Atualizar lista de clientes e contratos`.
- Nome novo do botao: `Atualizar clientes`.
- A coluna `Lote` e a coluna `Quadra` foram unificadas na exibicao como `Lote / Quadra`.
- Todas as colunas da grade foram centralizadas, exceto `Cliente`, que permanece alinhada a esquerda.

## Regra incremental aplicada

- A atualizacao consulta novamente os contratos locais.
- O nome exibido passa a priorizar o nome real encontrado no contrato confirmado.
- Dados financeiros ja persistidos no cache sao preservados.
- A atualizacao nao zera total pago, parcelas, status de atraso, situacao ou observacoes quando ja existe dado valido.
- O campo `data_atualizacao` e renovado a cada atualizacao por contrato/cache.
- A coluna `Atualizado em` usa `ultima_atualizacao_widepay` quando existir e `data_atualizacao` como fallback.

## Campos preservados

- cliente, lote, quadra, contrato, modalidade de contrato;
- parcelas pagas, total de parcelas, parcelas restantes;
- total pago;
- status de atraso recente;
- situacao, observacoes, divergencias;
- ultima atualizacao WidePay e data de atualizacao local.

## Campos atualizados por contrato

- nome completo do cliente;
- lote e quadra;
- contrato encontrado ou nao encontrado;
- modalidade resumida do contrato quando identificavel.

## Campos atualizados por WidePay

Os dados financeiros continuam sendo atualizados pelo fluxo WidePay/metricas ja existente:

- total pago;
- parcelas pagas equivalentes;
- parcelas restantes;
- indicador visual de atraso recente;
- situacao resumida;
- ultimo pagamento e observacoes.

## Status de atraso recente

A regra de cor permanece:

- `0 a 3`: verde;
- `4 a 5`: amarelo;
- `6 ou mais`: vermelho.

Pagamentos avulsos com indicios como `ref`, `referente`, `atraso` ou termos equivalentes continuam sendo tratados como possivel compensacao no calculo existente.

## Arquivos alterados

- `WideAPP_EXTRA/app/interface.py`
- `WideAPP_EXTRA/app/indexador_clientes.py`
- `WideAPP_EXTRA/app/pipeline_runner.py`

## Testes executados

- `py_compile` em `interface.py`, `indexador_clientes.py` e `pipeline_runner.py`.
- `smoke_test` da interface principal: 77 registros.
- `smoke_test` da interface isolada: 77 registros.
- Atualizacao leve isolada com `indexar_clientes(validar_widepay=False)`.
- Contagem antes/depois no cache isolado: 77 antes, 77 depois.
- Evidencias de nomes atualizados por contrato:
  - `ADALBERTO OLIVEIRA FILHO`, lote `A3`, quadra `A`;
  - `ALEX SANTOS DE AZEVEDO`, lote `B2`, quadra `B`.

## Pendencias

- O ambiente isolado mostrou avisos de PDF sem `pypdf` durante leitura de contratos em PDF, mas a atualizacao concluiu e preservou os 77 registros.
- A etapa nao reexecutou uma varredura WidePay completa para todos os clientes; a regra financeira completa permanece no pipeline de metricas/relatorios.

## Commit GitHub

Pendente ate o commit/push desta rodada.
