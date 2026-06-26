# STATUS - WIDEAPP_EXTRA INTERFACE, LISTA E FUNCOES PROMETIDAS

Data/hora: 2026-06-25

## Objetivo

Corrigir a interface da `WideAPP_EXTRA` para que as funcoes prometidas na lista de clientes funcionem de forma real:

- barra de rolagem vertical e horizontal na lista;
- nomes exibidos com menos ruido operacional;
- menu de botao direito funcional;
- botoes de abrir pasta, Drive, HTML, PDF e XLSX com retorno claro;
- execucao de multiplos clientes sem depender de argumento inexistente `--clientes`;
- coletor paginado tentando escrever `100` no controle de registros por pagina do WidePay.

## Arquivos alterados

- `WideAPP_EXTRA/app/interface.py`
- `WideAPP_EXTRA/app/pipeline_runner.py`
- `WideAPP_EXTRA/app/coletor_tabelas_paginadas.py`
- `WideAPP_EXTRA/app/extrator_widepay.py`
- `WideAPP_EXTRA/COMO_USAR.md`
- `00_SISTEMA_PRECHECK/precheck_regras.py`
- `05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md`
- `.agents/skills/widepay-core-operacional/SKILL.md`

## Ajustes aplicados

- Adicionada barra horizontal no `Treeview`.
- Adicionada rolagem por mouse na lista de nomes.
- Corrigido menu de botao direito:
  - gerar relatorio dos selecionados;
  - abrir pasta do cliente;
  - abrir planilha recente do cliente;
  - atualizar lista;
  - atualizar WidePay dos selecionados.
- Corrigidos imports ausentes que impediam `Abrir pasta do cliente` e `Abrir planilha recente do cliente`.
- Logs da interface agora sao enviados para a thread principal do Tkinter.
- Popups de erro da pipeline agora sao chamados via `root.after`.
- Pipeline de multiplos clientes passou a processar sequencialmente por cliente, registrando falhas parciais sem depender de `--clientes`.
- O coletor paginado passou a tentar localizar a caixa numerica de registros por pagina e escrever `100`.
- A copia isolada em `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA` recebeu os mesmos arquivos corrigidos.

## Testes executados

```powershell
WideAPP_EXTRA\.venv\Scripts\python.exe -m py_compile WideAPP_EXTRA\app\interface.py WideAPP_EXTRA\app\pipeline_runner.py WideAPP_EXTRA\app\coletor_tabelas_paginadas.py
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --smoke-test-interface
C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA\.venv\Scripts\python.exe -m py_compile ...\interface.py ...\pipeline_runner.py ...\coletor_tabelas_paginadas.py ...\extrator_widepay.py
C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA\.venv\Scripts\python.exe ...\main.py --smoke-test-interface
```

Resultados:

- `py_compile`: aprovado no repositorio principal.
- `smoke-test-interface`: aprovado no repositorio principal, cache com 83 registros.
- `py_compile`: aprovado na copia isolada.
- `smoke-test-interface`: aprovado na copia isolada, cache com 78 registros.

## Status

PARCIAL FUNCIONAL.

A interface e os botoes foram corrigidos e passaram no smoke test. O teste de pipeline financeiro completo nao foi marcado como aprovado nesta etapa porque a execucao real anterior ficou longa e foi interrompida por timeout. A aprovacao final ainda exige novo teste real pela janela da `WideAPP_EXTRA` com cliente selecionado, arquivos gerados e botoes abrindo artefatos reais.

## Conclusao

As funcoes da interface deixaram de ser apenas botoes visuais e agora possuem rotas executaveis, logs e mensagens de erro claras. A proxima validacao deve ser feita na interface isolada reaberta pelo `.bat`, selecionando um cliente por vez e depois dois clientes para confirmar falha parcial sem travamento.

## Limpeza pos-commit 277346b

Auditoria executada em seguida para verificar o que ficou fora do commit publicado:

```powershell
git status --short
git diff -- WideAPP_EXTRA/app/indexador_clientes.py
git diff -- WideAPP_EXTRA/app/leitor_contratos.py
git diff -- 07_DADOS_TEMPORARIOS/auditoria_rastreabilidade.jsonl
WideAPP_EXTRA\.venv\Scripts\python.exe -m py_compile WideAPP_EXTRA\app\indexador_clientes.py WideAPP_EXTRA\app\leitor_contratos.py
```

Classificacao:

- `WideAPP_EXTRA/app/indexador_clientes.py` -> `NECESSARIA PARA FUNCIONAMENTO`
  - ignora pastas `backup`;
  - tenta obter nome real do cliente a partir do contrato `docx/pdf/txt convertido`;
  - preserva nome validado anteriormente no cache;
  - reduz duplicidade quando o lote nao esta normalizado.
- `WideAPP_EXTRA/app/leitor_contratos.py` -> `NECESSARIA PARA FUNCIONAMENTO`
  - extrai nome real do comprador do contrato;
  - propaga esse nome para o parse financeiro;
  - usa a ultima data completa do texto como data de assinatura, melhorando contratos com varias datas.
- `07_DADOS_TEMPORARIOS/auditoria_rastreabilidade.jsonl` -> `GERADA AUTOMATICAMENTE / NAO COMMITAR`
  - arquivo append-only de execucoes reais e falhas/sucessos do WidePay;
  - mantido localmente como evidencia operacional.

Observacoes:

- Nada foi descartado automaticamente.
- Os hashes dos arquivos `indexador_clientes.py` e `leitor_contratos.py` na pasta isolada ja batiam com os arquivos locais no momento desta auditoria, portanto a copia isolada tambem ficou atualizada para essas duas correcoes.
- Se houver commit complementar para essas correcoes, ele deve conter apenas os dois `.py` acima e este registro de status, sem incluir o `jsonl`.
