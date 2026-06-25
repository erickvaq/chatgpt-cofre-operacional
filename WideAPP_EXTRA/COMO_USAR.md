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

## Menu disponivel

Ao abrir o `.bat`, o programa mostra um menu com:

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
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --executar --cliente "NOME DO CLIENTE" --lote F05
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\main.py --executar --letra A --letra-fim E --consolidado
```

O modo `--executar` apenas encaminha argumentos para `executar_auditoria.py`, reaproveitando a logica ja existente da `WideAPP_EXTRA`.
