# PAINEL OPERACIONAL WIDEPAY - Relatorio_WidePay_Lotes

## Estado Atual
* **Data da atualizacao:** 2026-06-25 (Regra 13 Ativada)
* **Branch atual:** `main`
* **Status do precheck:** `REGRAS PERSISTENTES CARREGADAS COM SUCESSO - 13 regras encontradas`
* **Regra principal:** WidePay primeiro, contratos depois
* **Formato principal:** XLS/XLSX para relatorios financeiros
* **PDF:** gerar somente quando o usuario pedir explicitamente
* **HTML:** gerar somente quando o usuario pedir previa/painel/conferencia visual
* **Abertura real:** navegador dedicado via CDP; Google Chrome 9333
* **Seguranca:** WidePay somente leitura; nao acessar `Configuracoes > Contatos`

## Regras Ativas
* Regra consolidada de 32 regras antigas para 11 regras persistentes.
* REGRA 10 (2026-06-25): GitHub como procedimento padrão obrigatório de rastreabilidade.
* REGRA 11 (2026-06-25): Acesso conferível ao conteúdo (versão sanitizada no GitHub obrigatória para arquivos sensíveis locais).
* Parcelas restantes somente pelo total confirmado no contrato.
* Relatorio deve consultar Carnes e Cobrancas/Boletos no WidePay antes do apoio local.
* Todo relatorio financeiro padrao deve priorizar XLS/XLSX.
* Todo relatorio final deve conter `Pagamentos Recebidos Interpretados`.
* O arquivo completo deve ser entregue no Google Drive e rastreado no GitHub.

## Registro Sanitizado da Rodada
* **Cliente/lote:** Edmilson / Edimson - F05
* **Fonte principal consultada:** WidePay real consultado em 25/06/2026 via fluxo CDP
* **Arquivo principal local:** XLSX financeiro V2 gerado localmente
* **PDF/HTML:** existem versoes locais anteriores; PDF so deve ser regenerado quando solicitado
* **Status:** Gerado e atualizado; aguardando validacao manual do usuario
* **Exposicao:** Arquivo completo disponibilizado via link publico do Google Drive

## Arquivos Gerados Registrados (Completos)
* `02_RELATORIOS_GERADOS/RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_SILVA_DOS_SANTOS_LOTE_F05_20260625_1402.xlsx`
* `02_RELATORIOS_GERADOS/RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_SILVA_DOS_SANTOS_LOTE_F05_20260625_1358.xlsx`
* `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO.md`
* `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/WIDEPAY_EDMILSON.json`
* `02_RELATORIOS_GERADOS/CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO_V3_FINAL/`

## Links Publicos
* **Regras consolidadas:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md
* **Painel normal:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md
* **Painel raw:** https://raw.githubusercontent.com/erickvaq/chatgpt-cofre-operacional/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md
* **Indice auditavel:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/INDICE_AUDITAVEL_RELATORIOS.md
* **Relatorio Sanitizado:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/02_RELATORIOS_GERADOS/RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_F05_SANITIZADO_1402.md
* **Google Drive (Acesso Prático):** https://drive.google.com/open?id=1O_lAtS4JGtThjtaz18AD5oAEWuBBsUfK
* **Script Excel:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/03_SCRIPTS/gerar_relatorio_excel.py

## Proximo Passo
* Validar o XLSX local do Edmilson/Edimson.
* Gerar PDF somente se o usuario pedir.
