# Auditoria GitHub - WideAPP_EXTRA interface dinamica

## Objetivo

Publicar a etapa de interface dinamica da `WideAPP_EXTRA` para lista de clientes/lotes, pesquisa, selecao multipla, XLSX consolidado e manifesto Google Drive.

## Links publicos de auditoria

- `WideAPP_EXTRA/main.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/main.py

- `WideAPP_EXTRA/INICIAR_WIDEAPP_EXTRA.bat`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/INICIAR_WIDEAPP_EXTRA.bat

- `WideAPP_EXTRA/COMO_USAR.md`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/COMO_USAR.md

- `WideAPP_EXTRA/app/config.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/app/config.py

- `WideAPP_EXTRA/app/interface.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/app/interface.py

- `WideAPP_EXTRA/app/indexador_clientes.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/app/indexador_clientes.py

- `WideAPP_EXTRA/app/pesquisa_clientes.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/app/pesquisa_clientes.py

- `WideAPP_EXTRA/app/seletor_clientes.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/app/seletor_clientes.py

- `WideAPP_EXTRA/app/drive_uploader.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/app/drive_uploader.py

- `WideAPP_EXTRA/app/abridor_arquivos.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/app/abridor_arquivos.py

- `WideAPP_EXTRA/app/gerador_xlsx_consolidado.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/app/gerador_xlsx_consolidado.py

- `WideAPP_EXTRA/app/pipeline_runner.py`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/app/pipeline_runner.py

- Status da etapa  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/STATUS_WIDEAPP_EXTRA_INTERFACE_DINAMICA_CLIENTES_20260625.md

- Status ETAPA 2 Drive + pipeline  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/STATUS_WIDEAPP_EXTRA_APROVACAO_FINAL_DRIVE_PIPELINE_20260625.md

- Este indice de auditoria  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/AUDITORIA_LINKS_GITHUB_WIDEAPP_INTERFACE_DINAMICA_20260625.md

## Arquivos locais nao publicados

- `WideAPP_EXTRA/data/clientes_indexados.json`
- `WideAPP_EXTRA/data/clientes_indexados.xlsx`
- `WideAPP_EXTRA/LINKS_GOOGLE_DRIVE.md`
- `WideAPP_EXTRA/logs/*.log`

Motivo: contem dados locais de clientes/lotes, logs de ambiente ou manifesto operacional local.

## Resultado resumido dos testes

- 83 cliente/lote indexados.
- Pesquisa por `Edm`, `A a E` e `F05` funcionando.
- Smoke test da interface aprovado.
- XLSX consolidado de teste gerado.
- Drive local copiou arquivo real para `WideAPP_EXTRA/drive_local`.
- Pipeline real foi acionado, tentou login automatico e falhou por erro de usuario/senha no WidePay; etapa final nao aprovada.
