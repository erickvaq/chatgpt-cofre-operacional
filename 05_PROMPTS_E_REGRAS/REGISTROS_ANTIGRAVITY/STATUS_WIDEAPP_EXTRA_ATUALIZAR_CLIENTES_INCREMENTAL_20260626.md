# STATUS - WideAPP_EXTRA Atualizar clientes incremental - 2026-06-26

## Objetivo

Aprimorar a funcao principal da WideAPP_EXTRA para que o botao `Atualizar clientes` atualize a base principal de clientes, contratos e resumo financeiro de forma incremental, preservando o cache anterior quando a nova varredura nao encontrar dados.

## Botao

- Nome antigo: `Atualizar lista de clientes e contratos`
- Nome novo: `Atualizar clientes`

## Arquivos alterados

- `WideAPP_EXTRA/app/interface.py`
- `WideAPP_EXTRA/app/indexador_clientes.py`
- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/STATUS_WIDEAPP_EXTRA_ATUALIZAR_CLIENTES_INCREMENTAL_20260626.md`

## Regra de atualizacao incremental

- A lista principal deixa de depender de uma recriacao destrutiva.
- A varredura local atualiza registros encontrados.
- Registros existentes que nao aparecem na nova varredura permanecem no cache.
- Campos antigos validos nao sao apagados quando o novo dado vem vazio, zerado ou ausente.
- Se uma tentativa de WidePay falhar, o ultimo estado valido e preservado e o registro recebe observacao de falha.

## Regra de preservacao do cache

- Clientes ja conhecidos sao preservados por chave de pasta/lote ou cliente/lote.
- Contrato previamente confirmado nao e rebaixado para `Nao encontrado` por falha temporaria de varredura.
- Total pago, parcelas, status, observacoes e ultima atualizacao WidePay sao mantidos quando nao ha dado novo confiavel.

## Campos atualizados por contrato

- nome completo validado;
- lote;
- quadra;
- modalidade do contrato;
- total de parcelas;
- valor base da parcela;
- valor total contratado;
- entrada ou valor fora do parcelamento;
- origem do contrato.

## Campos atualizados pelo WidePay

- total pago recebido;
- parcelas pagas identificadas;
- parcelas restantes;
- status;
- situacao resumida;
- ultimo vencimento pago;
- ultima parcela paga;
- valor do ultimo pagamento;
- status de atraso recente;
- observacoes/divergencias.

## Regra do Atualizado em

- `data_atualizacao` e atualizada na varredura incremental local.
- `ultima_atualizacao_widepay` e atualizada somente quando houver metrica ou coleta WidePay aplicada.
- O campo exibido como `Atualizado em` usa `ultima_atualizacao_widepay` e cai para `data_atualizacao` quando necessario.

## Status de atraso recente

- `0 a 3`: verde.
- `4 a 5`: amarelo.
- `6 ou mais`: vermelho.
- A contagem usa boletos/cobrancas vencidos recentes e dados normalizados do WidePay quando disponiveis.

## Compensacao por boletos avulsos pagos

- Pagamentos avulsos com termos como `ref`, `referente`, `atraso`, `atrazo` ou equivalentes reduzem a contagem de atraso recente quando identificados.
- A origem do status fica registrada em `status_atraso_origem`.

## Testes executados

- `python -m py_compile WideAPP_EXTRA\app\indexador_clientes.py WideAPP_EXTRA\app\interface.py WideAPP_EXTRA\app\extrator_widepay.py WideAPP_EXTRA\app\pipeline_runner.py`
- `python 00_SISTEMA_PRECHECK\precheck_regras.py`
- Teste em memoria `incremental_preserva_cache`: confirmou que contrato previamente encontrado, total pago, total de parcelas e `ultima_atualizacao_widepay` nao sao apagados quando a nova varredura nao encontra contrato.

## Pendencias

- Conferir interface reaberta visualmente.
- Executar fluxo real com WidePay logado para validar coleta resumida em ambiente operacional.
- Atualizar a pasta isolada se houver build/empacotamento paralelo ativo.
- `WideAPP_EXTRA/COMO_USAR.md` ainda contem uma referencia textual antiga fora do escopo de arquivos solicitados para commit.
- Avaliar commit/push com cuidado porque o reposititorio ja tinha alteracoes nao relacionadas antes desta execucao.

## Commit GitHub

- Pendente. Commit/push nao deve incluir alteracoes nao relacionadas nem dados sensiveis.
