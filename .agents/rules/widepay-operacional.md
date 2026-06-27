# Regras Operacionais locais do Agente — Loteamento Água Viva / WidePay

## Prioridade Operacional e Resolução de Conflitos
Antes de consultar o WidePay, use obrigatoriamente o procedimento documentado em:
`05_PROMPTS_E_REGRAS\PROCEDIMENTO_WIDEPAY_OPERA_CDP_WMI.md`

Em caso de conflito de instruções, a seguinte ordem de prioridade prevalece:
1. **Regras Persistentes do Projeto** (`05_PROMPTS_E_REGRAS\REGRAS_PERSISTENTES_DO_PROJETO.md`)
2. **Procedimento WidePay Opera CDP WMI** (`05_PROMPTS_E_REGRAS\PROCEDIMENTO_WIDEPAY_OPERA_CDP_WMI.md`)
3. **Skills Customizadas do WidePay** (`widepay-core-operacional`, etc.)
4. **Pedido atual do usuário**

Sempre que a solicitação ou tarefa envolver:
* WidePay, clientes, contratos, lotes, quadras, parcelas, carnês, cobrança;
* Geração, padronização, auditoria de relatórios financeiros;
* Geração de arquivos PDF, DOCX, HTML, HTA;
* Busca de cliente, atalhos, painel de acesso;
* Abertura de arquivos, conferência ou entrega final;

O agente deve ativar e seguir as diretrizes das Skills:
* `widepay-core-operacional`
* `widepay-relatorio-pdf`
* `widepay-abertura-externa`

## Execução Obrigatória de Segurança

Antes de qualquer processamento ou geração de entregas, o agente deve executar o precheck automaticamente:
```
python 00_SISTEMA_PRECHECK\precheck_regras.py
```
E ler na íntegra as regras contidas em:
```
05_PROMPTS_E_REGRAS\REGRAS_PERSISTENTES_DO_PROJETO.md
```

O usuário não precisa solicitar a leitura de regras, ativação das skills ou execução do precheck. Estes procedimentos são automáticos e obrigatórios.

## Modo Econômico Obrigatório
Sempre que a tarefa consistir em conferir, validar ou revisar dados já gerados localmente, utilizar **Modo Econômico** (ler JSON/MD localmente usando o script `validar_resultado_rapido.py`, sem abrir navegador ou reprocessar tudo).

