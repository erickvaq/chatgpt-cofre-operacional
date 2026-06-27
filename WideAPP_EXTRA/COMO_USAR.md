# Como usar a WideAPP_EXTRA

## Abrir a aplicacao

Use o arquivo:

```text
WideAPP_EXTRA\INICIAR_WIDEAPP_EXTRA.bat
```

Ele abre a `WideAPP_EXTRA` com o Python isolado do projeto:

```text
WideAPP_EXTRA\.venv\Scripts\python.exe
```

Nao use Python global para executar a aplicacao.

## Interface visual

Ao abrir o `.bat`, o programa abre a interface visual da `WideAPP_EXTRA`.

A tela contem:

- botao `Atualizar lista de clientes e contratos`;
- campo `Pesquisar cliente`;
- filtro de status;
- tabela dinamica cliente + lote;
- selecao individual e multipla;
- botoes `Selecionar todos` e `Limpar selecao`;
- botao `Gerar relatorio dos selecionados`;
- botao `Gerar relatorio de todos os clientes ativos`;
- botoes para abrir pasta local e XLSX;
- area de logs/status;
- area de links/status do Google Drive.

## Menu terminal alternativo

O menu antigo em terminal continua disponivel para fallback:

```powershell
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --terminal
```

Ele mostra:

1. consultar cliente especifico;
2. consultar cliente + lote;
3. consultar por letra inicial;
4. consultar intervalo de letras;
5. gerar relatorio consolidado;
6. apenas validar ambiente;
7. sair.

## Validacao antes da execucao

Antes de qualquer auditoria real, a aplicacao valida:

- uso do Python do `.venv`;
- dependencias instaladas;
- precheck de regras persistentes;
- Chrome/CDP dedicado;
- aba WidePay acessivel.

Se a validacao falhar, a execucao e cancelada e o motivo aparece no terminal e no log.

## Coleta paginada obrigatoria no WidePay

A `WideAPP_EXTRA` nao aprova relatorio quando a coleta do WidePay fica limitada a primeira pagina.

Antes de coletar carnes, cobrancas, boletos ou recebimentos, a aplicacao deve:

- tentar selecionar o maior valor em `Registros por pagina`, preferencialmente 500;
- percorrer todas as paginas disponiveis;
- registrar quantidade coletada por pagina;
- ler o total exibido pelo WidePay, por exemplo `Exibindo 26 a 36 de 36 registros`;
- deduplicar os registros coletados;
- comparar total coletado contra total exibido pelo WidePay.

Se a conferencia falhar, o pipeline bloqueia o relatorio com:

```text
COLETA_INCOMPLETA_PAGINACAO_OU_REGISTROS_POR_PAGINA_WIDEPAY
```

O modulo responsavel por essa trava e:

```text
WideAPP_EXTRA\app\coletor_tabelas_paginadas.py
```

## Logs

Cada abertura gera um log em:

```text
WideAPP_EXTRA\logs
```

## Saidas

Os relatorios finais continuam sendo gerados em:

```text
02_RELATORIOS_GERADOS
```

## Uso avancado

Tambem e possivel chamar a aplicacao por linha de comando, ainda usando o `.venv`:

```powershell
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --validar-ambiente
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --atualizar-clientes
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --pesquisar "A a E"
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --smoke-test-interface
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --executar --cliente "NOME DO CLIENTE" --lote F05
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --executar --letra A --letra-fim E --consolidado
```

O modo `--executar` apenas encaminha argumentos para `executar_auditoria.py`, reaproveitando a logica ja existente da `WideAPP_EXTRA`.

## Google Drive

A aplicacao cria e atualiza:

```text
WideAPP_EXTRA\LINKS_GOOGLE_DRIVE.md
```

Por padrao, quando `WIDEAPP_RCLONE_REMOTE` nao estiver configurado, a aplicacao usa uma pasta Drive local operacional:

```text
WideAPP_EXTRA\drive_local
```

Tambem e possivel apontar outra pasta com:

```powershell
$env:WIDEAPP_DRIVE_LOCAL="C:\caminho\para\Google Drive"
```

Se `WIDEAPP_RCLONE_REMOTE` estiver configurado, o modulo tenta enviar via `rclone`. Em todos os casos, o manifesto registra o status real e nao inventa links.
