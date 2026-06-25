---
name: widepay-relatorio-pdf
description: Usar sempre que o pedido envolver relatorio financeiro, PDF, HTML, tabela, resumo financeiro, padrao visual ou conferencia antes de PDF.
---
# Skill: widepay-relatorio-pdf

Esta skill define as regras de formatacao, layout visual e calculo matematico dos relatorios consolidados em HTML e PDF do projeto `Relatorio_WidePay_Lotes`.

## 0. Regra Universal
Esta skill vale para qualquer cliente especifico, letra unica, intervalo de letras, grupo de clientes, lote, todos os clientes, relatorio financeiro individual ou consolidado.
WidePay vem primeiro, a conferencia em Markdown vem antes do PDF e, quando houver mais de um cliente, a planilha consolidada `.xlsx` deve existir antes do fechamento final.
Se o WidePay real ainda nao foi aberto, a geracao visual deve parar antes de qualquer PDF ou HTML.

## 1. Prioridade
**Alta.** Garante a consistencia visual e matematica antes da exportacao de qualquer arquivo de auditoria final.

## 2. Quando usar
* Desenho e renderizacao do layout verde-escuro do relatorio final do cliente (modelo Camila V4).
* Geracao do arquivo de visualizacao previa em HTML (`_PREVIA.html`).
* Geracao do PDF final consolidado na pasta `02_RELATORIOS_GERADOS/`.
* Verificacao da conformidade matematica dos totais de parcelas pagas, pendentes e progresso.

## 3. Quando nao usar
* Abertura do arquivo final no visualizador do Windows (usar `widepay-abertura-externa`).
* Login no WidePay ou extracoes via CDP (usar `widepay-core-operacional`).

## 4. Gatilhos de ativacao
Palavras-chave: `gerar PDF`, `relatorio final`, `layout visual`, `cards de resumo`, `previa HTML`, `gerar consolidado`.

## 5. Fluxo obrigatorio
1. **Conferencia previa:** verificar se o arquivo de conferencia `.md` em `07_DADOS_TEMPORARIOS` ja foi criado e aprovado pelo usuario.
2. **Desenho visual verde:** aplicar o padrao de cores unificado: titulo principal "RELATORIO FINANCEIRO" com fundo verde escuro (`#2E7D32` -> `#1B5E20`) e subtitulo "Loteamento Agua Viva - Iacu-BA".
3. **Cards de tres colunas:** adicionar no topo do documento os cartoes de "Total Pago", "Parcelas Pagas" (X de Y) e "Falta Pagar".
4. **Barras de progresso:** renderizar a barra proporcional verde (pagas) vs cinza (restantes) com percentual explicito.
5. **Diferenca de boletos avulsos:** identificar boletos avulsos pagos e vincular as parcelas vencidas indevidamente em atraso para amortizacao.
6. **Par de entrega:** sempre gerar os arquivos em par (PDF + Previa HTML) no mesmo diretorio de destino.
7. **Consolidado multi-cliente:** quando o pedido envolver mais de um cliente, exigir que a base consolidada e a planilha `.xlsx` ja existam antes do fechamento do PDF final.

## 6. Rotinas e scripts relacionados
* `python 03_SCRIPTS\gerar_pdf_camila_v2.py`
* `python 03_SCRIPTS\gerar_relatorio_cliente.py`
* `python 03_SCRIPTS\gerar_conferencia_cliente.py`

## 7. Logs obrigatorios
Ao gerar o PDF/HTML:
```text
SKILL CARREGADA: widepay-relatorio-pdf
PRODUTO GERADO: HTML de previa e PDF criados na mesma pasta
VALIDACAO VISUAL: cards de tres colunas e barra de progresso aplicados
```

## 8. Erros proibidos
* **ERRO 1:** Sobrescrever relatorios antigos do mesmo cliente (usar sempre sufixos `_V2`, `_V3` ou `_CORRIGIDO` caso ja existam).
* **ERRO 2:** Herdar constantes numericas do caso Camila Ferrolho (recalcular do zero para cada novo cliente).
* **ERRO 3:** Omitir juros e multas nos recebimentos ou gerar o PDF sem a aprovacao do relatorio de conferencia Markdown.
* **ERRO 4:** Expor dados de parcelas e valores financeiros no GitHub publico (dados sensiveis devem ficar apenas locais).
* **ERRO 5:** Fechar PDF final sem conferencia previa e sem base consolidada quando o pedido envolver mais de um cliente.

## 9. Critérios de validação
* Tabela de carnes informando ID, referencia, valor da parcela, parcelas geradas/pagas, total recebido e status.
* Total Geral Pago identico ao somatorio de todos os carnes e boletos avulsos pagos do WidePay.

## 10. Precheck relacionado
* O script `precheck_regras.py` valida as restricoes visuais, de versionamento e a Regra Universal.

## 11. Exemplos curtos de decisao
* *Cenario:* O relatorio do cliente "Adailton" de E22A foi aprovado pelo usuario.
* *Decisao:* Gerar `02_RELATORIOS_GERADOS/Adailton_Resumo_V1.pdf` e `02_RELATORIOS_GERADOS/Adailton_Resumo_V1_PREVIA.html` simultaneamente e abrir a pasta de destino no Windows Explorer.
* *Cenario:* O usuario pede o PDF consolidado sem passar pela validacao de Markdown.
* *Decisao:* Parar, emitir um alerta informando a necessidade do precheck em Markdown e aguardar aprovacao dos valores no chat.
