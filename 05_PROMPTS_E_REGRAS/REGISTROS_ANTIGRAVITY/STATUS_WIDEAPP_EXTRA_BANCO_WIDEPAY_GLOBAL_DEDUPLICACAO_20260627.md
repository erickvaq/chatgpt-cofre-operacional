# STATUS - WideAPP_EXTRA banco WidePay global e deduplicacao - 2026-06-27

## Objetivo da mudanca

Transformar a atualizacao WidePay da WideAPP_EXTRA em fluxo de coleta global: coletar carnes/cobrancas em bloco, salvar um banco interno local de boletos e usar esse banco para atualizar lista e relatorios sem repetir paginacao completa por cliente quando o cache estiver recente.

## Problema atual

O fluxo anterior ja tinha extracao em bloco, mas ainda nao deixava um banco interno explicito `widepay_boletos_cache.json/.xlsx` como fonte rapida. A lista tambem podia tratar variacoes do mesmo lote como registros diferentes, por exemplo `G14` e `14 / G`, `F06` e `06 / F`, `E5` e `5 / E`.

## Arquivos alterados

- `WideAPP_EXTRA/app/config.py`
- `WideAPP_EXTRA/app/widepay_boletos_cache.py`
- `WideAPP_EXTRA/app/indexador_clientes.py`
- `WideAPP_EXTRA/app/interface.py`
- `WideAPP_EXTRA/executar_auditoria.py`

## Estrutura do novo cache WidePay

Arquivos criados/atualizados pelo sistema:

- `WideAPP_EXTRA/data/widepay_boletos_cache.json`
- `WideAPP_EXTRA/data/widepay_boletos_cache.xlsx`

Campos principais:

- `cliente_original_widepay`
- `cliente_normalizado`
- `lote_original`
- `lote_canonico`
- `chave_lote_canonica`
- `quadra`
- `referencia`
- `forma`
- `origem`
- `status`
- `vencimento`
- `data_pagamento`
- `valor_original`
- `valor_recebido`
- `id_boleto`
- `pagina_origem`
- `coletado_em`
- `fonte`

Metadados principais:

- `inicio_coleta`
- `fim_coleta`
- `ultima_atualizacao`
- `total_registros`
- `total_registros_coletados`
- `total_carnes`
- `total_cobrancas`
- `total_clientes_reconhecidos`
- `origem`

## Mudancas implementadas

- Criado modulo central `widepay_boletos_cache.py`.
- Criada funcao central `normalizar_lote_quadra(lote, quadra, referencia, pasta_local)`.
- Criada chave canonica `chave_lote_canonica`.
- Atualizada deduplicacao da lista para usar lote canonico.
- Atualizada mesclagem de duplicados para priorizar registro mais completo, contrato confirmado, dados financeiros e observacoes preservadas.
- Atualizada exibicao da coluna `Lote / Quadra` para preferir lote canonico.
- Atualizado fluxo `Atualizar clientes` para gravar banco interno global depois da coleta WidePay em bloco.
- Atualizado `executar_auditoria.py` para usar cache global recente antes de fazer nova coleta real.
- Coletas complementares de relatorio agora mesclam com o cache existente, sem apagar o banco global.
- Ampliada deteccao de contrato a vista com termos como `quitado`, `quitacao`, `integralmente pago`, `valor integral`, `sem parcelamento` e `parcela unica`.
- Contratos a vista passam a exibir `A VISTA` e `A VISTA / quitado`, com `parcelas_restantes = 0`.

## Total de registros coletados

Nao executado nesta etapa. A alteracao de codigo foi validada por compilacao e teste local de normalizacao, sem coleta real no WidePay.

## Total de paginas percorridas

Nao executado nesta etapa. A contagem real sera preenchida na proxima execucao do botao `Atualizar clientes`.

## Total de clientes reconhecidos

Nao executado nesta etapa. O campo sera preenchido nos metadados do cache na coleta real.

## Total de registros nao associados

Nao executado nesta etapa. O fluxo atual ainda depende dos metadados retornados pelo coletor em bloco para auditoria detalhada de nao associados.

## Duplicidades encontradas

Casos-alvo tratados pela regra canonica:

- `G14` = `14 / G`
- `F6` = `F06` = `06 / F`
- `G13` = `13 / G`
- `E5` = `5 / E`

## Duplicidades corrigidas

Corrigida a causa estrutural na chave de deduplicacao. A limpeza efetiva da lista existente ocorre ao rodar `Atualizar clientes`, que reindexa e salva `clientes_indexados.json/.xlsx`.

## Casos Belmiro/Camila/Alexandre

- Belmiro: regra cobre `F6`, `F06`, `06 / F`.
- Camila: regra cobre `G13`, `13 / G`.
- Alexandre: regra cobre `G14`, `14 / G`.

## Contratos a vista detectados

Deteccao ampliada no indexador local. Sem varredura real dos contratos nesta etapa.

## Testes executados

```powershell
python -m py_compile WideAPP_EXTRA\app\config.py WideAPP_EXTRA\app\widepay_boletos_cache.py WideAPP_EXTRA\app\indexador_clientes.py WideAPP_EXTRA\app\interface.py WideAPP_EXTRA\executar_auditoria.py
```

Resultado: aprovado, sem saida de erro.

Teste local de normalizacao:

```text
('G14', 'G', '', '') => G14
('14', 'G', '', '') => G14
('F06', 'F', '', '') => F6
('06', 'F', '', '') => F6
('', '', 'Quadra G Lote 14', '') => G14
('5', 'E', '', '') => E5
('E5', '-', '', '') => E5
```

## Pendencias

- Rodar `Atualizar clientes` com WidePay real logado.
- Conferir se `widepay_boletos_cache.json` e `.xlsx` foram gerados com registros reais.
- Validar lista visual sem duplicidades obvias.
- Conferir exemplos reais Belmiro, Camila, Alexandre e Ana Cleide depois da coleta.
- Melhorar preenchimento de `pagina_origem` caso o coletor JS exponha pagina por registro.
- Registrar totais reais de paginas, registros, clientes reconhecidos e nao associados apos coleta.

## Commit GitHub

Nao executado nesta etapa. O worktree tem muitos arquivos nao rastreados e alteracoes preexistentes fora do escopo; commit/push exige selecao de escopo e confirmacao especifica para nao misturar material sensivel ou arquivos grandes.
