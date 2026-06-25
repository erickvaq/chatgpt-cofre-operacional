# PAINEL OPERACIONAL WIDEPAY - Relatorio_WidePay_Lotes

## Estado Atual
* **Data da atualizacao:** 2026-06-25
* **Branch atual:** `main`
* **Status do precheck:** `REGRAS PERSISTENTES CARREGADAS COM SUCESSO - 9 regras encontradas`
* **Regra principal:** WidePay primeiro, contratos depois
* **Abertura real:** Opera dedicado via CDP `localhost:9444`
* **Login salvo:** usar autopreenchimento do navegador e tentar login automatico antes de pedir intervencao manual
* **Seguranca:** WidePay somente leitura; nao acessar `Configuracoes > Contatos`

## Regras Ativas
* Regra consolidada de 32 regras antigas para blocos operacionais curtos
* Parcelas restantes somente pelo total de parcelas confirmado no contrato
* Relatorio de cliente deve consultar carnês e cobranças/boletos no WidePay
* Alias/erro de digitacao do nome pode ser usado quando evidencia financeira e contrato apontarem para o mesmo lote
* Exemplo registrado: `Edmilson` / `Edimson`
* Total pago do terreno/lote soma carnês pagos e cobranças/boletos recebidos

## Registro Sanitizado da Rodada
* **Cliente/lote:** Edmilson / F05
* **Fonte principal consultada:** WidePay real
* **Resultado operacional:** relatório individual atualizado
* **Cobertura usada:** carnês + cobranças/boletos + alias de nome
* **Arquivos financeiros completos:** mantidos somente localmente por conter dados sensiveis
* **GitHub publico:** deve receber apenas regras, scripts e painel sanitizado
* **Status:** pronto para conferencia local

## Arquivos Locais Sensíveis Registrados
* `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO.md`
* `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/WIDEPAY_EDMILSON.json`
* `02_RELATORIOS_GERADOS/CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO_V3_FINAL/RESUMO_FINANCEIRO_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO_CORRIGIDO_V7.pdf`
* `02_RELATORIOS_GERADOS/RESUMO_FINANCEIRO_CONTRATO_EDMILSON_F05_AGUA_VIVA_LEO_CORRIGIDO_V3_PREVIA_V5.html`

## Links Publicos
* **Regra consolidada:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md
* **Painel normal:** https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md
* **Painel raw:** https://raw.githubusercontent.com/erickvaq/chatgpt-cofre-operacional/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md

## Proximo Passo
* Conferir localmente o PDF/HTML do Edmilson e seguir para outro cliente somente após aprovação.
