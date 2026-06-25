# PAINEL OPERACIONAL WIDEPAY - Relatorio_WidePay_Lotes

## Estado Atual
* **Data da atualização:** 2026-06-25 12:37 (UTC-3)
* **Branch atual:** `main`
* **Status do precheck:** `REGRAS PERSISTENTES CARREGADAS COM SUCESSO - 10 regras encontradas`
* **Regra principal:** WidePay primeiro, contratos depois
* **Regra de rastreabilidade:** GitHub como procedimento padrão de conferência (REGRA 10)
* **Abertura real:** navegador dedicado via CDP; Opera `9444` ou Chrome `9333`
* **Segurança:** WidePay somente leitura; não acessar `Configurações > Contatos`

## Regras Ativas
* Regra consolidada de 32 regras antigas para 10 regras persistentes.
* REGRA 10 adicionada em 2026-06-25: GitHub como procedimento padrão obrigatório de rastreabilidade.
* Parcelas restantes somente pelo total confirmado no contrato.
* Relatório deve consultar Carnês e Cobranças/Boletos no WidePay antes do apoio local.
* Alias/erro de digitação do nome pode ser usado quando evidência financeira e contrato apontarem para o mesmo lote.
* Todo relatório final deve conter `Pagamentos Recebidos Interpretados`.
* Total pago do terreno/lote soma todos os recebimentos reais do WidePay pertencentes ao cliente/lote correto.
* Formato principal de entrega: Excel `.xlsx` com 5 abas obrigatórias.
* PDF e HTML são formatos secundários, somente sob demanda.

## Formato Padrão de Relatório (atualizado 2026-06-25)
* **Formato:** Excel `.xlsx`
* **Script:** `python 03_SCRIPTS/gerar_relatorio_excel.py`
* **Abas obrigatórias:** Resumo / Pagamentos Recebidos / Interpretação Parcelas / Validação / Alertas (se houver)
* **Filtro:** somente status Recebido/Pago com valor > R$ 0,00

## Último Cliente Processado
* **Cliente:** Edmilson Silva Dos Santos (alias: Edimson Silva Dos Santis)
* **Lote/Quadra:** F05 / Quadra F
* **Fonte consultada:** JSON `WIDEPAY_EDMILSON.json` (extração anterior do WidePay real)
* **Arquivo gerado:** `RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_SILVA_DOS_SANTOS_LOTE_F05_20260625.xlsx`
* **Pagamentos recebidos:** 29
* **Total pago:** R$ 3.585,91
* **Parcelas pagas equiv.:** 34 de 100
* **Parcelas restantes:** 66
* **Alertas:** 0
* **Validação matemática:** 8/8 OK
* **Status:** Aguardando validação manual do usuário

## Arquivos Locais Sensíveis Registrados (REGRA 10.4)
* `02_RELATORIOS_GERADOS/RELATORIO_FINANCEIRO_CLIENTE_EDMILSON_SILVA_DOS_SANTOS_LOTE_F05_20260625.xlsx`
  * Tipo: Relatório financeiro Excel — dados individualizados
  * Índice auditável: `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/INDICE_AUDITAVEL_RELATORIOS.md`
* `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO.md`
  * Tipo: Conferência MD com tabela de pagamentos
* `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/WIDEPAY_EDMILSON.json`
  * Tipo: Extração bruta do WidePay com cobranças e carnês
* `02_RELATORIOS_GERADOS/CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO_V3_FINAL/` (PDF V8 — sessão anterior)

## Links Públicos
* **Regras consolidadas:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md
* **Painel normal:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md
* **Painel raw:** https://raw.githubusercontent.com/erickvaq/chatgpt-cofre-operacional/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md
* **Índice auditável:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/INDICE_AUDITAVEL_RELATORIOS.md
* **Skill relatórios:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/.agents/skills/widepay-relatorio-pdf/SKILL.md
* **Script Excel:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/03_SCRIPTS/gerar_relatorio_excel.py

## Próximo Passo
* Usuário deve validar o Excel do Edmilson localmente.
* Após validação, registrar como "VALIDADO" neste painel.
* Aguardar aprovação para avançar para próximo cliente.
