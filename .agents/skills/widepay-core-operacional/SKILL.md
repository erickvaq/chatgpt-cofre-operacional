---
name: widepay-core-operacional
description: Usar sempre que o pedido envolver WidePay, cliente, contrato, lote, quadra, parcelas, carnês, cobrança, busca de cliente ou conferência financeira.
---
# Skill: widepay-core-operacional

Esta skill centraliza as regras de negócio, auditoria financeira, busca de clientes e segurança do projeto `Relatorio_WidePay_Lotes`.

## 1. Prioridade
**Máxima operacional.** Sobrescreve orientações gerais de desenvolvimento de código e direciona o fluxo de checagem.

## 2. Quando usar
* Busca de dados cadastrais e financeiros de clientes do loteamento.
* Cruzamento de contratos físicos locais com lançamentos do site WidePay.
* Geração do relatório de conferência Markdown em `07_DADOS_TEMPORARIOS`.
* Processamento e normalização de nomes, quadras e lotes.
* Automação de login e controle de perfil de navegação.

## 3. Quando não usar
* Abertura direta de arquivos gerados (usar `widepay-abertura-externa`).
* Customização visual de relatórios ou conversão final de PDF/HTML (usar `widepay-relatorio-pdf`).

## 4. Gatilhos de ativação
Palavras-chave: `buscar cliente`, `auditar lote`, `WidePay`, `conferir parcelas`, `loteamento`, `quadra`, `verificar A a E`.

## 5. Fluxo obrigatório
1. **Precheck de Segurança:** Chamar `python 00_SISTEMA_PRECHECK\precheck_regras.py` antes de qualquer ação.
2. **Localização Local:** Procurar a pasta do cliente sob a respectiva quadra em `C:\Users\Windows User\Desktop\AGUA VIVA\- CONTRATOS AGUA VIVA\`.
3. **Login WidePay Seguro:** Chamar `ensure_widepay_logged_in()` para conectar ao Opera dedicado (`localhost:9444` via CDP) e preencher automaticamente caso a senha esteja salva.
4. **Extração de Registros:** Acessar passivamente `Recebimentos > Carnês` e `Recebimentos > Cobranças/Boletos` extraindo todos os registros.
5. **Cálculo de Quitação:** Cruzar o total nominal de parcelas do contrato físico com os recebimentos efetivos do WidePay.
6. **Arquivo de Conferência:** Salvar o log detalhado em `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_[CLIENTE].md`.

## 6. Rotinas e scripts relacionados
* `python 03_SCRIPTS\buscar_cliente.py <nome>`
* `python 03_SCRIPTS\consultar_widepay_cdp.py --cliente <nome>`
* `python 03_SCRIPTS\gerar_conferencia_cliente.py`

## 7. Logs obrigatórios
Ao iniciar a execução, imprimir no console:
```text
SKILL CARREGADA: widepay-core-operacional
PRECHECK SKILLS: aprovado
PRECHECK LOGIN WIDEPAY: perfil persistente Opera/CDP obrigatório
ensure_widepay_logged_in(): iniciado
```

## 8. Erros proibidos
* **ERRO 1:** Confundir iniciais dos nomes dos clientes com a letra da quadra/lote (ex: "Alex" pertence ao escopo A a E, embora seu lote B2 esteja na Quadra B).
* **ERRO 2:** Acessar a página de configurações `Configurações > Contatos` ou transferências.
* **ERRO 3:** Simular dados financeiros falsos ou preencher dados de quitação quando o WidePay não pôde ser consultado.
* **ERRO 4:** Calcular o total pago geral considerando apenas o primeiro carnê do cliente quando houver múltiplos carnês ativos/finalizados.

## 9. Critérios de validação
* Normalização rigorosa de nomes (remover termos como "Contrato", "Cópia", "Leo/Léo").
* Cobertura A a E baseada estritamente nas iniciais reais dos nomes.
* Tabela de pendências atualizada sem dados financeiros sensíveis expostos no GitHub público.

## 10. Precheck relacionado
* O script de validação `precheck_regras.py` valida a presença deste arquivo e suas 31 regras em `REGRAS_PERSISTENTES_DO_PROJETO.md`.

## 11. Exemplos curtos de decisão
* *Cenário:* O usuário pede checagem do cliente "Alex Santos de Azevedo" (Lote B2).
* *Decisão:* A inicial do nome é "A". Executar auditoria, pois está dentro da cobertura A a E (apesar de o lote estar na Quadra B).
* *Cenário:* O script CDP falha ao conectar ou a página de login está sem senha salva.
* *Decisão:* Interromper imediatamente, registrar `WIDEPAY NÃO CONSULTADO — AGUARDANDO LOGIN MANUAL` e solicitar ação do usuário.
