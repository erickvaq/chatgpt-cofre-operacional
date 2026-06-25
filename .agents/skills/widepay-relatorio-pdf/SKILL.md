---
name: widepay-relatorio-pdf
description: Usar sempre que o pedido envolver relatório financeiro, PDF, HTML, tabela, resumo financeiro, padrão visual ou conferência antes de PDF.
---
# Skill: widepay-relatorio-pdf

Esta skill define as regras de formatação, layout visual e cálculo matemático dos relatórios consolidados em HTML e PDF do projeto `Relatorio_WidePay_Lotes`.

## 1. Prioridade
**Alta.** Garante a consistência visual e matemática antes da exportação de qualquer arquivo de auditoria final.

## 2. Quando usar
* Desenho e renderização do layout verde-escuro do relatório final do cliente (modelo Camila V4).
* Geração do arquivo de visualização prévia em HTML (`_PREVIA.html`).
* Geração do PDF final consolidado na pasta `02_RELATORIOS_GERADOS/`.
* Verificação da conformidade matemática dos totais de parcelas pagas, pendentes e progresso.

## 3. Quando não usar
* Abertura do arquivo final no visualizador do Windows (usar `widepay-abertura-externa`).
* Login no WidePay ou extrações via CDP (usar `widepay-core-operacional`).

## 4. Gatilhos de ativação
Palavras-chave: `gerar PDF`, `relatório final`, `layout visual`, `cards de resumo`, `previa HTML`, `gerar consolidado`.

## 5. Fluxo obrigatório
1. **Conferência Prévia:** Verificar se o arquivo de conferência `.md` em `07_DADOS_TEMPORARIOS` já foi criado e aprovado pelo usuário.
2. **Desenho Visual Verde:** Aplicar o padrão de cores unificado: Título principal "RELATÓRIO FINANCEIRO" com fundo verde escuro (`#2E7D32` → `#1B5E20`) e subtítulo "Loteamento Água Viva — Iaçú-BA".
3. **Cards de Três Colunas:** Adicionar no topo do documento os cartões de "Total Pago", "Parcelas Pagas" (X de Y) e "Falta Pagar".
4. **Barras de Progresso:** Renderizar a barra proporcional verde (pagas) vs cinza (restantes) com percentual explícito.
5. **Diferenciação de Boletos Avulsos:** Identificar boletos avulsos pagos e vinculá-los às parcelas vencidas indevidamente em atraso para amortização.
6. **Par de Entrega:** Sempre gerar os arquivos em par (PDF + Prévia HTML) no mesmo diretório de destino.

## 6. Rotinas e scripts relacionados
* `python 03_SCRIPTS\gerar_pdf_camila_v2.py`
* `python 03_SCRIPTS\gerar_relatorio_cliente.py`
* `python 03_SCRIPTS\gerar_conferencia_cliente.py`

## 7. Logs obrigatórios
Ao gerar o PDF/HTML:
```text
SKILL CARREGADA: widepay-relatorio-pdf
PRODUTO GERADO: HTML de prévia e PDF criados na mesma pasta
VALIDAÇÃO VISUAL: cards de três colunas e barra de progresso aplicados
```

## 8. Erros proibidos
* **ERRO 1:** Sobrescrever relatórios antigos do mesmo cliente (usar sempre sufixos `_V2`, `_V3` ou `_CORRIGIDO` caso já existam).
* **ERRO 2:** Herdar constantes numéricas do caso Camila Ferrolho (recalcular do zero para cada novo cliente).
* **ERRO 3:** Omitir juros e multas nos recebimentos ou gerar o PDF sem a aprovação do relatório de conferência Markdown.
* **ERRO 4:** Expor dados de parcelas e valores financeiros no GitHub público (dados sensíveis devem ficar apenas locais).

## 9. Critérios de validação
* Tabela de carnês informando ID, referência, valor da parcela, parcelas geradas/pagas, total recebido e status.
* Total Geral Pago idêntico ao somatório de todos os carnês e boletos avulsos pagos do WidePay.

## 10. Precheck relacionado
* O script `precheck_regras.py` valida as restrições visuais e de versionamento.

## 11. Exemplos curtos de decisão
* *Cenário:* O relatório do cliente "Adailton" de E22A foi aprovado pelo usuário.
* *Decisão:* Gerar `02_RELATORIOS_GERADOS/Adailton_Resumo_V1.pdf` e `02_RELATORIOS_GERADOS/Adailton_Resumo_V1_PREVIA.html` simultaneamente e abrir a pasta de destino no Windows Explorer.
* *Cenário:* O usuário pede o PDF consolidado sem passar pela validação de Markdown.
* *Decisão:* Parar, emitir um alerta informando a necessidade do precheck em Markdown e aguardar aprovação dos valores no chat.
