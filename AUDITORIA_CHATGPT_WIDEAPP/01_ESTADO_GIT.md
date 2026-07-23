# 01 - Estado Atual do Git

## Informações do Repositório
* **Branch Atual**: `wideapp-v1.7-final`
* **Commit HEAD**: `00b24b9191e263ce9f39b61963239ccc0f2d9c8f`

## Remoto (-v)
```text
origin	https://github.com/erickvaq/chatgpt-cofre-operacional.git (fetch)
origin	https://github.com/erickvaq/chatgpt-cofre-operacional.git (push)
```

## Git Status
```text
On branch wideapp-v1.7-final
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   .agents/AGENTS.md
	modified:   WideAPP_EXTRA/app/indexador_clientes.py
	modified:   WideAPP_EXTRA/app/interface.py
	modified:   WideAPP_EXTRA/app/normalizador_pagamentos.py
	modified:   WideAPP_EXTRA/app/saneamento_clientes.py
	modified:   WideAPP_EXTRA/app/widepay_boletos_cache.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	00_IMPORTAR_DOCUMENTOS/
	00_SISTEMA_ABERTURA_EXTERNA/
	01_DOCUMENTOS_CONVERTIDOS/
	03_PLANILHAS/
	03_SCRIPTS/criar_atalhos_camila.py
	03_SCRIPTS/criar_planilha_teste.py
	03_SCRIPTS/gerar_consolidado_atrasos_widepay.py
	03_SCRIPTS/gerar_pdf_camila_v2.py
	03_SCRIPTS/inspect_cobrancas_page.py
	03_SCRIPTS/inspect_dom.py
	03_SCRIPTS/inspect_inputs.py
	03_SCRIPTS/inspect_pagination.py
	03_SCRIPTS/inspect_search_cobrancas.py
	03_SCRIPTS/inspect_tds.py
	03_SCRIPTS/inspect_text_inputs.py
	03_SCRIPTS/list_all_inputs_cobrancas.py
	03_SCRIPTS/list_folders.py
	03_SCRIPTS/list_links.py
	03_SCRIPTS/test_cobrancas.py
	03_SCRIPTS/testar_cdp_widepay.py
	03_SCRIPTS/validar_resultado_rapido.py
	06_MODELOS_RELATORIO/
	ABRIR_ARQUIVO_EXTERNO.bat
	ABRIR_CHROME_WIDEPAY_DEBUG.bat
	ABRIR_OPERA_WIDEPAY_DEBUG.bat
	ABRIR_OPERA_WIDEPAY_DEBUG_EXTERNAMENTE.vbs
	ABRIR_OPERA_WIDEPAY_DEBUG_VISIVEL.bat
	ABRIR_PAINEL_CAMILA_VISIVEL.bat
	ABRIR_PASTA_DO_PROJETO.bat
	ABRIR_PASTA_RELATORIOS.bat
	ABRIR_PDF.bat
	ABRIR_PREVIA_CAMILA.bat
	ABRIR_RELATORIO_CAMILA.bat
	ABRIR_RESULTADO_CAMILA_AGORA.bat
	ATALHOS_DO_PROJETO.md
	AUDITORIA_CORRECAO_LOTES_EMMANUEL_RODRIGO.md
	BUSCAR_CLIENTE.bat
	COMANDOS_RAPIDOS_DO_PROJETO.md
	CONVERTER_DOCUMENTOS.py
	CONVERTER_DOCUMENTOS_SEGURO.bat
	DIAGNOSTICAR_OPERA_WIDEPAY_CDP.ps1
	GERAR_CONFERENCIA_CLIENTE_SEGURO.bat
	GERAR_CONSOLIDADO_ATRASOS_WIDEPAY.bat
	GERAR_RELATORIO_SEGURO.bat
	INDICE_ARQUIVOS_CLICAVEIS_DO_PROJETO.hta
	INDICE_ARQUIVOS_CLICAVEIS_DO_PROJETO.md
	INICIAR_PROJETO_SEGURO.bat
	INICIAR_WIDEPAY_OPERA_AUTOMATICO.bat
	README_COMO_USAR.md
	REINICIAR_OPERA_WIDEPAY_DEBUG.bat
	WideAPP_EXTRA/app/assets/
	WideAPP_EXTRA/assets/widepay_icon_transparente_centralizado_ok.ico
	WideAPP_EXTRA/assets/widepay_icon_transparente_centralizado_ok.png
	WideAPP_EXTRA/widepay_icon_transparente_centralizado_ok.ico
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260627_212533.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260627_212814.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260627_213216.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_173012.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_174704.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_174901.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_175105.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_175244.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_175508.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_175731.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_180543.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_180544.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_180545.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_180546.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_180547.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260628_180548.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260710_131008.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260710_131518.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260710_131918.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260710_132536.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260722_124708.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260722_161939.xlsx
	backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_20260722_231440.xlsx
	backups/fix_colunas_xlsx_20260629_014355/
	backups/historico_dados/
	backups/wideapp_atualizar_clientes_20260627_105234/
	backups/wideapp_banco_widepay_global_20260627_163954/
	backups/wideapp_v18_pago_avulso_manual_20260711_102308/
	documentacao/CONTINUIDADE_V2_1_REFERENCIAS_WIDEPAY/
	scratch/atualizar_bat_isolado.ps1
	scratch/atualizar_emmanuel_direcionado.py
	scratch/auto_rclone.py
	scratch/capture_screenshot.py
	scratch/checar_cobertura_local.py
	scratch/check_bat_bom.ps1
	scratch/check_hashes.ps1
	scratch/check_logged_in.py
	scratch/confirmar_atalhos_oficiais.ps1
	scratch/criar_atalhos_desktop.ps1
	scratch/detalhar_quadras_ae.py
	scratch/extrair_tudo_preliminar.py
	scratch/find_shortcuts.ps1
	scratch/gerar_icone_wideapp.py
	scratch/inspect_login_state.py
	scratch/mod_excel.py
	scratch/obter_contatos_widepay.py
	scratch/preparar_auditoria_chatgpt.py
	scratch/preparar_teste_isolado.ps1
	scratch/preparar_teste_isolado_v2.ps1
	scratch/previa_emmanuel_rodrigo.py
	scratch/print_raw_data.py
	scratch/print_raw_data_cobrancas.py
	scratch/processar_lote_ae.py
	scratch/sync_target_files_only.ps1
	scratch/sync_to_start_menu_target.ps1
	scratch/temp_zip.ps1
	scratch/test_cdp_click.py
	scratch/test_cdp_eval.py
	scratch/test_clean_names.py
	scratch/test_enter_cdp.py
	scratch/test_format.py
	scratch/test_login_autofill.py
	scratch/teste_obter_abas.py
	scratch/teste_rpp_input.py

no changes added to commit (use "git add" and/or "git commit -a")
```

## Git Diff --stat
```text
warning: in the working copy of '.agents/AGENTS.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'WideAPP_EXTRA/app/interface.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'WideAPP_EXTRA/app/normalizador_pagamentos.py', LF will be replaced by CRLF the next time Git touches it
 .agents/AGENTS.md                            |    5 +
 WideAPP_EXTRA/app/indexador_clientes.py      | 1354 +++++++++++++++++++++++---
 WideAPP_EXTRA/app/interface.py               |  946 ++++++++++++++++--
 WideAPP_EXTRA/app/normalizador_pagamentos.py |   22 +-
 WideAPP_EXTRA/app/saneamento_clientes.py     |  586 ++++++++++-
 WideAPP_EXTRA/app/widepay_boletos_cache.py   |  278 ++++--
 6 files changed, 2881 insertions(+), 310 deletions(-)
```

## Git Diff --name-status
```text
warning: in the working copy of '.agents/AGENTS.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'WideAPP_EXTRA/app/interface.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'WideAPP_EXTRA/app/normalizador_pagamentos.py', LF will be replaced by CRLF the next time Git touches it
M	.agents/AGENTS.md
M	WideAPP_EXTRA/app/indexador_clientes.py
M	WideAPP_EXTRA/app/interface.py
M	WideAPP_EXTRA/app/normalizador_pagamentos.py
M	WideAPP_EXTRA/app/saneamento_clientes.py
M	WideAPP_EXTRA/app/widepay_boletos_cache.py
```
