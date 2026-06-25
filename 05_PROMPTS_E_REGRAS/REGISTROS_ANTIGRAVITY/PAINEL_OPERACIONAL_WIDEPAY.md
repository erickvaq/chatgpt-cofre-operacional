# PAINEL OPERACIONAL WIDEPAY - Relatorio_WidePay_Lotes

## Estado Atual
* **Data da atualizacao:** 2026-06-25
* **Branch atual:** `main`
* **Status do precheck:** `REGRAS PERSISTENTES CARREGADAS COM SUCESSO - 9 regras encontradas`
* **Regra principal:** WidePay primeiro, contratos depois
* **Abertura real:** navegador dedicado via CDP; Opera `9444` ou Chrome `9333`
* **Seguranca:** WidePay somente leitura; nao acessar `Configuracoes > Contatos`

## Regras Ativas
* Regra consolidada de 32 regras antigas para 9 regras persistentes.
* Parcelas restantes somente pelo total confirmado no contrato.
* Relatorio deve consultar Carnes e Cobrancas/Boletos no WidePay antes do apoio local.
* Alias/erro de digitacao do nome pode ser usado quando evidencia financeira e contrato apontarem para o mesmo lote.
* Todo relatorio final deve conter `Pagamentos Recebidos Interpretados`.
* Total pago do terreno/lote soma todos os recebimentos reais do WidePay pertencentes ao cliente/lote correto.

## Registro Sanitizado da Rodada
* **Cliente/lote:** Edmilson / Edimson - F05
* **Fonte principal consultada:** WidePay real pelo Chrome dedicado `localhost:9333`
* **Resultado operacional:** conferencia, HTML e PDF atualizados localmente
* **Cobertura usada:** carnes + cobrancas/boletos + boletos avulsos + alias de nome
* **Validacao:** tabela de pagamentos interpretados presente no Markdown e HTML
* **Arquivos financeiros completos:** mantidos somente localmente por conter dados sensiveis
* **GitHub publico:** receber somente regras, scripts e painel sanitizado

## Arquivos Locais Sensiveis Registrados
* `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO.md`
* `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/WIDEPAY_EDMILSON.json`
* `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/WIDEPAY_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO.json`
* `02_RELATORIOS_GERADOS/CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO_V3_FINAL/RESUMO_FINANCEIRO_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO_CORRIGIDO_V8.pdf`
* `02_RELATORIOS_GERADOS/RESUMO_FINANCEIRO_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO_CORRIGIDO_V3_PREVIA_V6.html`

## Links Publicos
* **Regra consolidada:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md
* **Painel normal:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md
* **Painel raw:** https://raw.githubusercontent.com/erickvaq/chatgpt-cofre-operacional/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md

## Proximo Passo
* Conferir localmente o PDF/HTML V8/V6 do Edmilson/Edimson antes de seguir para outro cliente.
