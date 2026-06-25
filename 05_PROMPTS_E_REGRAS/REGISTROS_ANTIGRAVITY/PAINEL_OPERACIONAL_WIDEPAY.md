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
* **Cliente/lote:** Edmilson Silva dos Santos - F05
* **Fonte principal consultada:** WidePay real consultado em 25/06/2026 via fluxo CDP (Chrome 9333)
* **Arquivo principal local:** XLSX financeiro gerado localmente em 25/06/2026 15:48
* **PDF/HTML:** HTML previa e PDF de conferência local gerados; PDF final aguardando validação
* **Status:** Concluido (Auditoria PENDENTE por aviso de descrição vaga no boleto 4701)
* **Exposicao:** Arquivo completo disponibilizado via link publico do Google Drive

## Arquivos Gerados Registrados (Completos)
* `02_RELATORIOS_GERADOS/EDMILSON_LOTE_05_FINAL/RELATORIO_FINANCEIRO_EDMILSON_SILVA_DOS_SANTOS_20260625_1548.xlsx`
* `02_RELATORIOS_GERADOS/EDMILSON_LOTE_05_FINAL/CONFERENCIA_CALCULOS_EDMILSON_SILVA_DOS_SANTOS_20260625_1548.md`
* `02_RELATORIOS_GERADOS/EDMILSON_LOTE_05_FINAL/RESUMO_FINANCEIRO_EDMILSON_SILVA_DOS_SANTOS_20260625_1548_PREVIA.html`
* `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/WIDEPAY_EDMILSON_SILVA_DOS_SANTOS.json`

## Links Publicos
* **Regras consolidadas:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md
* **Painel normal:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md
* **Painel raw:** https://raw.githubusercontent.com/erickvaq/chatgpt-cofre-operacional/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md
* **Indice auditavel:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/INDICE_AUDITAVEL_RELATORIOS.md
* **Google Drive (Pasta de Entrega):** https://drive.google.com/open?id=1GLQU5AhZmfQd4CMngC8w9Ck2LLX_gu4s
* **Google Drive (Planilha Excel XLSX):** https://drive.google.com/open?id=1uGiZhmk-JbZVyysTzMsAh-BkhNNPbWq0
* **Google Drive (WidePay JSON Bruto):** https://drive.google.com/open?id=15yhcLfc4bEK4qdatz_eVzzPRPvWRxEuv

## Proximo Passo
* Validar a planilha XLSX do Edmilson com o usuário.
* Aguardar aprovação para geração do PDF Final com ReportLab ou correção de boletos.
