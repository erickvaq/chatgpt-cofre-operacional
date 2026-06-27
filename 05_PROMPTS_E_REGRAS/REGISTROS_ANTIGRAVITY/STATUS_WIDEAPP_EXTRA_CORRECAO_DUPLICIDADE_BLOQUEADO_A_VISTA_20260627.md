# STATUS - WideAPP_EXTRA correcao duplicidade, bloqueado e a vista - 2026-06-27

## Objetivo

Fechar os dois problemas ainda visiveis na lista da `WideAPP_EXTRA`:

1. duplicacao de cliente/lote por formatos diferentes de lote;
2. mistura entre modalidade do contrato e situacao financeira.

## Fonte validada

App isolado em uso:

`C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA`

Cache saneado:

- `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA\data\clientes_indexados.json`
- `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA\data\clientes_indexados.xlsx`

Backup antes da mesclagem:

`C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\backups\dedupe_modalidade_20260627_184502`

## Regras aplicadas

### Lote canonico

`chave_lote_canonica = QUADRA + NUMERO_DO_LOTE_SEM_ZERO_A_ESQUERDA`

Exemplos:

- `F6`, `F06`, `06 / F`, `6 / F` => `F6`
- `G13`, `G013`, `13 / G`, `13 / Quadra G` => `G13`
- `G14`, `G014`, `14 / G`, `14 / Quadra G` => `G14`

### Mesclagem

Quando dois registros apontam para o mesmo cliente/pasta/lote canonico, manter o mais completo:

1. contrato encontrado;
2. nome mais completo;
3. modalidade confirmada;
4. valor total preenchido;
5. total pago preenchido;
6. data mais recente;
7. observacoes e divergencias preservadas.

### Modalidade x situacao financeira

Contrato a vista:

- `contrato_modalidade = a_vista`
- `contrato_resumo = A VISTA`
- `parcelas_resumo = A VISTA / quitado`
- `parcelas_restantes = 0`

Contrato parcelado sem pagamento recente:

- `contrato_modalidade = parcelado`
- `contrato_resumo = Parcelado`
- `situacao_final = Bloqueado`
- observacao recebe aviso de sem pagamento recente quando o ultimo pagamento tem mais de 8 meses;
- status visual fica vermelho quando a situacao financeira esta bloqueada.

## Antes

Arquivo-base de comparacao:

`C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\backups\dedupe_modalidade_20260627_184502\clientes_indexados.json`

Indicadores:

- registros antes: `136`
- duplicatas por chave canonica antes: `54`
- exemplos de duplicidade encontrados: Ana Cleide `E5`, Belmiro `F6`, Camila `G13`, Alexandre `G14`, entre outros.

## Depois

Indicadores depois da correcao:

- registros depois: `82`
- duplicatas por chave canonica depois: `0`
- registros mesclados/removidos da lista: `54`
- contratos a vista detectados: `12`
- registros parcelados com situacao financeira bloqueada: `8`
- registros parcelados bloqueados especificamente por regra de mais de 8 meses sem pagamento: `2`

## Casos obrigatorios

### Belmiro

Resultado:

- cliente: `BELMIRO SANTOS PIRES`
- lote exibido: `F6 / F`
- chave canonica: `F6`
- modalidade: `parcelado`
- contrato: `Parcelado`
- situacao: `Em andamento`
- duplicidade: `0`

### Camila

Resultado para Camila de Oliveira:

- cliente: `CAMILA DE OLIVEIRA FERROLHO`
- lote exibido: `G13 / G`
- chave canonica: `G13`
- modalidade: `parcelado`
- contrato: `Parcelado`
- situacao: `Bloqueado`
- duplicidade do lote `G13`: `0`

Observacao: existe outra cliente diferente chamada `CAMILA CARVALHO SAZHYN`, lote canonico `D7`; nao foi mesclada com Camila de Oliveira porque e outra pessoa/lote.

### Alexandre

Resultado:

- cliente: `ALEXANDRE ARRUDA SANTANA`
- lote exibido: `G14 / G`
- chave canonica: `G14`
- modalidade: `parcelado`
- contrato: `Parcelado`
- situacao: `Bloqueado`
- status visual: `vermelho`
- ultimo pagamento: `10/07/2024`
- duplicidade: `0`

### Ana Cleide

Resultado adicional observado no print:

- cliente: `ANA CLEIDE DOS SANTOS DIAS`
- lote exibido: `E5 / E`
- chave canonica: `E5`
- modalidade: `parcelado`
- contrato: `Parcelado`
- situacao: `Bloqueado`
- status visual: `vermelho`
- duplicidade: `0`

## Testes executados

Compilacao no projeto principal:

```powershell
python -m py_compile WideAPP_EXTRA\app\config.py WideAPP_EXTRA\app\widepay_boletos_cache.py WideAPP_EXTRA\app\indexador_clientes.py WideAPP_EXTRA\app\interface.py WideAPP_EXTRA\executar_auditoria.py
```

Compilacao no app isolado:

```powershell
& 'C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA\.venv\Scripts\python.exe' -m py_compile 'C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA\app\indexador_clientes.py'
```

Resultado: aprovado.

## Hashes

Cache JSON saneado:

`FD7840E86225E10723F908F27C60EEB597940B60DE401690CC6F1F573566B114`

Planilha XLSX saneada:

`03D27CE84A82BAA529A887B0F1AFE260BF29A3BDEE1349C7F90E558EC11779E9`

## Pendencias

- Reiniciar a janela da WideAPP_EXTRA isolada para carregar o codigo atualizado em memoria.
- Reexecutar conferencia visual na lista apos reinicio.
- Publicar no GitHub somente os arquivos leves/codigo/relatorios, sem cache bruto financeiro.
