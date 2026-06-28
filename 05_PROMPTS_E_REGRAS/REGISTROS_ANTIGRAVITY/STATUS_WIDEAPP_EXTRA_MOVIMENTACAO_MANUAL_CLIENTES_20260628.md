# STATUS WIDEAPP_EXTRA - MOVIMENTACAO MANUAL DE CLIENTES - 2026-06-28

## Objetivo

Entregar a movimentacao manual de clientes entre as abas:

- `Ativos`
- `Quitados`
- `Bloqueados / Removidos`

com persistencia, auditoria, atualizacao do XLSX e validacao real no ambiente isolado.

## Versao desta entrega

- Versao: `V1.1`
- Fonte central da versao do app: `WideAPP_EXTRA/VERSION`

## Resultado consolidado

- Backend de movimentacao manual: concluido
- Persistencia em `saneamento_clientes.json`: concluida
- Menu de contexto por botao direito: concluido
- Selecao multipla: concluida
- Auditoria manual: concluida
- Atualizacao do XLSX visual: concluida
- Validacao no isolado real gravando no arquivo real: concluida
- Restauracao automatica em caso de erro: comprovada

## Arquivos de codigo envolvidos

- `WideAPP_EXTRA/app/saneamento_clientes.py`
- `WideAPP_EXTRA/app/indexador_clientes.py`
- `WideAPP_EXTRA/app/interface.py`

## Validacao tecnica no projeto

- `python -m py_compile WideAPP_EXTRA/app/saneamento_clientes.py WideAPP_EXTRA/app/indexador_clientes.py WideAPP_EXTRA/app/interface.py`
- `WideAPP_EXTRA/main.py --smoke-test-interface`

Resultado: aprovado.

## Validacao real no ambiente isolado

Escopo autorizado:

- somente em `TESTE_WIDEAPP_EXTRA_ISOLADO`
- com backup local previo dos 3 arquivos operacionais
- sem alterar nada fora do ambiente isolado

### Garantias executadas

1. Backup datado dos 3 arquivos antes da gravacao
2. Interrupcao apenas das instancias do app isolado para evitar lock
3. Teste real no proprio app isolado
4. Validacao de JSON, XLSX e smoke-test apos gravacao
5. Restauracao automatica testada em uma primeira tentativa com falha de automacao

### Menu de contexto verificado

- Em `Ativos`:
  - `Mover para Quitados`
  - `Mover para Bloqueados / Removidos`
- Em `Quitados`:
  - `Restaurar para Ativos`
  - `Mover para Bloqueados / Removidos`
- Em `Bloqueados / Removidos`:
  - `Restaurar para Ativos`
  - `Mover para Quitados`

### Casos executados com sucesso

1. `Ativo -> Quitados`
2. `Ativo -> Bloqueados / Removidos`
3. `Selecao multipla -> Quitados`
4. `Quitado -> Ativos`
5. `Bloqueado -> Ativos`
6. Reaplicacao do saneamento preservando override manual
7. XLSX continuou abrindo
8. JSONs continuaram validos
9. `smoke-test-interface` continuou aprovando

## Resumo quantitativo

### Antes

- Ativos: `50`
- Quitados: `22`
- Bloqueados / Removidos: `11`
- Ignorados: `4`
- Fora do roster: `0`
- Atencao: `10`

### Depois

- Ativos: `48`
- Quitados: `24`
- Bloqueados / Removidos: `11`
- Ignorados: `4`
- Fora do roster: `0`
- Atencao: `10`

### XLSX depois

- Aba `Ativos`: `48` linhas
- Aba `Quitados`: `24` linhas
- Aba `Bloqueados_Removidos`: `11` linhas
- Aba `Auditoria`: `27` linhas

## Evidencia local

O log detalhado da execucao real, com clientes e caminhos locais completos, foi mantido apenas no ambiente isolado e nao entrou no versionamento publico:

- `WideAPP_EXTRA/logs/teste_real_movimentacao_manual_20260628_191403.md`

## Situacao final

Status: `VALIDADO NO ISOLADO REAL`

Pendencia remanescente:

- consolidar aprovacao final do usuario sobre a feature
