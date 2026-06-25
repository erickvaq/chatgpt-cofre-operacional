---
name: widepay-relatorio-pdf
description: Usar sempre que o pedido envolver relatorio financeiro, Excel/XLSX, PDF, HTML, tabela, resumo financeiro, padrao visual ou conferencia antes de entrega final.
---
# Skill: widepay-relatorio-pdf

Esta skill define as regras de formatacao, layout visual e calculo matematico dos relatorios financeiros do projeto `Relatorio_WidePay_Lotes`.

## 0.1 Formato principal de entrega: Excel (.xlsx)
A partir da decisao do usuario em 2026-06-25, o formato principal de entrega de relatorios financeiros e **Excel (.xlsx)**.

PDF e HTML passam a ser formatos complementares:
* gerar PDF somente quando o usuario pedir explicitamente PDF, impressao ou arquivo para envio nesse formato;
* gerar HTML somente quando o usuario pedir previa visual, painel HTML ou conferencia visual;
* nao gerar PDF automaticamente no fluxo padrao de relatorio financeiro;
* nao substituir o Excel quando o pedido for relatorio financeiro padrao.

O Excel deve conter abas de apoio:
1. **Resumo:** dados do cliente, lote, contrato, totais, percentuais e situacao.
2. **Pagamentos Recebidos:** registros com status Recebido/Pago e valor positivo.
3. **Interpretacao das Parcelas:** cada recebimento interpretado individualmente.
4. **Validacao:** checagens matematicas cruzadas.
5. **Alertas:** divergencias e referencias nao identificadas, quando houver.

Script principal: `python 03_SCRIPTS\gerar_relatorio_excel.py`

## 0. Regra Universal
Esta skill vale para qualquer cliente especifico, letra unica, intervalo de letras, grupo de clientes, lote, todos os clientes, relatorio financeiro individual ou consolidado.
WidePay vem primeiro, a conferencia em Markdown vem antes da entrega final quando exigida, e o Excel e o formato principal do relatorio financeiro.
Se o WidePay real ainda nao foi aberto, a geracao deve parar antes de qualquer XLSX, HTML ou PDF.

## 1. Prioridade
**Alta.** Garante a consistencia visual e matematica antes da exportacao de qualquer arquivo de auditoria final.

## 2. Quando usar
* Geracao de Excel/XLSX como relatorio financeiro principal.
* Desenho e renderizacao de HTML/PDF quando pedidos explicitamente ou necessarios como apoio visual solicitado.
* Geracao do arquivo de visualizacao previa em HTML (`_PREVIA.html`), quando solicitado.
* Geracao do PDF final consolidado na pasta `02_RELATORIOS_GERADOS/`, quando solicitado.
* Verificacao da conformidade matematica dos totais de parcelas pagas, pendentes e progresso.

## 3. Quando nao usar
* Abertura do arquivo final no visualizador do Windows (usar `widepay-abertura-externa`).
* Login no WidePay ou extracoes via CDP (usar `widepay-core-operacional`).

## 4. Gatilhos de ativacao
Palavras-chave: `gerar Excel`, `gerar XLSX`, `relatorio final`, `relatorio financeiro`, `gerar PDF`, `previa HTML`, `gerar consolidado`.

## 5. Fluxo obrigatorio
1. **WidePay primeiro:** nenhum XLSX/HTML/PDF final pode ser gerado sem consulta real do WidePay, salvo busca local explicitamente preliminar.
2. **Conferencia previa:** verificar se o arquivo de conferencia `.md` em `07_DADOS_TEMPORARIOS` ja foi criado e aprovado quando exigido.
3. **Excel principal:** gerar `.xlsx` como entrega padrao do relatorio financeiro.
4. **PDF/HTML complementares:** PDF somente quando o usuario pedir; HTML quando o usuario pedir previa/painel/conferencia visual.
5. **Versionamento:** nunca sobrescrever entrega final antiga; criar nova versao quando ja existir arquivo.
6. **Parcelas restantes pelo contrato:** calcular restantes somente por total de parcelas do contrato confirmado menos parcelas pagas; se o contrato nao confirmar o total, bloquear XLSX/HTML/PDF final com numero de restantes.
7. **Total pago do terreno/lote:** o valor pago no resumo deve somar carnes pagos e cobrancas/boletos recebidos do mesmo cliente/lote.
8. **Cobrancas/boletos visiveis:** XLSX, HTML e PDF devem listar cobrancas/boletos pagos ou em aberto encontrados no WidePay, alem dos carnes.
9. **Pagamentos interpretados:** todo XLSX/HTML/PDF/Markdown final deve conter a tabela `Pagamentos Recebidos Interpretados`, calculada recebimento por recebimento.
10. **Percentuais separados:** percentual de parcelas quitadas usa total de parcelas do contrato; percentual financeiro pago usa total recebido dividido pelo valor total contratado do terreno/lote.

## 6. Rotinas e scripts relacionados
* `python 03_SCRIPTS\gerar_relatorio_excel.py` - gerador principal Excel/XLSX.
* `python 03_SCRIPTS\gerar_conferencia_cliente.py` - conferencia previa em Markdown.
* `python 03_SCRIPTS\gerar_relatorio_cliente.py` - gerador complementar de HTML e PDF quando solicitados.

## 7. Logs obrigatorios
Ao gerar arquivos finais:
```text
SKILL CARREGADA: widepay-relatorio-pdf
PRODUTO GERADO: Excel .xlsx principal; PDF somente quando solicitado
VALIDACAO: pagamentos interpretados e percentuais separados conferidos
```

## 8. Erros proibidos
* **ERRO 1:** Sobrescrever relatorios antigos do mesmo cliente sem nova versao.
* **ERRO 2:** Herdar constantes numericas de outro cliente.
* **ERRO 3:** Omitir juros, multas, cobrancas ou recebimentos encontrados no WidePay.
* **ERRO 4:** Expor dados de parcelas e valores financeiros no GitHub publico.
* **ERRO 5:** Fechar entrega final sem conferencia previa quando exigida.
* **ERRO 6:** Usar parcelas geradas no WidePay como se fossem total do contrato.
* **ERRO 7:** Exibir total pago generico quando o relatorio precisa representar o total pago do terreno/lote.
* **ERRO 8:** Omitir cobrancas/boletos pagos ou em aberto do XLSX/HTML/PDF quando eles existem na conferencia WidePay.
* **ERRO 9:** Gerar XLSX/HTML/PDF final sem a tabela `Pagamentos Recebidos Interpretados`.
* **ERRO 10:** Misturar percentual financeiro pago com percentual de parcelas quitadas.
* **ERRO 11:** Tratar PDF/HTML como substitutos do Excel principal quando o pedido for relatorio financeiro padrao.
* **ERRO 12:** Gerar PDF automaticamente sem pedido explicito do usuario.

## 9. Criterios de validacao
* Tabela de carnes informando ID, referencia, valor da parcela, parcelas geradas/pagas, total recebido e status.
* Total Geral Pago identico ao somatorio de todos os carnes e boletos avulsos pagos do WidePay.
* Parcelas restantes compativeis somente com contrato fisico/local confirmado.
* Arquivos sensiveis completos ficam locais; GitHub recebe somente indice/painel sanitizado.

## 10. Precheck relacionado
* O script `precheck_regras.py` valida Excel principal, PDF/HTML complementares e ausencia de dados financeiros sensiveis no painel publico.

## 11. Exemplos curtos de decisao
* *Cenario:* O usuario pede "relatorio financeiro do cliente".
* *Decisao:* Gerar Excel `.xlsx` como arquivo principal.
* *Cenario:* O usuario pede "relatorio em PDF".
* *Decisao:* Gerar PDF complementar, mantendo a rastreabilidade.
