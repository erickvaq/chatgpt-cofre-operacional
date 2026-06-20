# Regras do Projeto - Relatorio WidePay por Cliente e Lote

Objetivo:
Gerar relatorio financeiro individual de um cliente escolhido manualmente no WidePay, separando boletos, carnes, parcelas pagas e debitos por lote especifico.

Regras obrigatorias para relatorio individual:

1. Nunca consultar todos os clientes automaticamente.
2. O usuario deve escolher manualmente o cliente durante a busca.
3. O usuario deve confirmar qual lote sera analisado.
4. O agente deve apenas ler informacoes, organizar dados e gerar relatorio.
5. O agente nao deve alterar, cancelar, baixar em massa, excluir ou modificar cobrancas no WidePay.
6. O agente nao deve salvar senha em arquivo.
7. O login no WidePay deve ser feito manualmente pelo usuario.
8. O agente deve pedir confirmacao antes de clicar em botoes sensiveis.
9. O agente deve separar pagamentos por lote.
10. O relatorio deve conter somente dados do cliente e lote selecionado.
11. Sempre comparar os dados do WidePay com o contrato local, quando o contrato existir.
12. Se houver divergencia entre contrato e WidePay, destacar no relatorio.
13. Salvar o relatorio final na pasta 02_RELATORIOS_GERADOS.
14. Salvar planilha resumida na pasta 03_PLANILHAS.
15. Salvar prints ou evidencias uteis na pasta 04_EVIDENCIAS_PRINTS.
16. [SKILL MEMORIA PERSISTENTE] Quando o usuario enviar prints (capturas de tela) de cobrancas/parcelas e afirmar que elas pertencem a um lote especifico (ex: "todas estao ai nos prints do lote G3"), ESSA INFORMACAO DEVE SER CONSIDERADA A VERDADE ABSOLUTA. Ignore conclusoes previas do sistema WidePay (ex: descricoes ou valores associados a outros lotes) e consolide APENAS as cobrancas presentes nos prints fornecidos dentro do lote indicado pelo usuario.
17. [MEMÓRIA PERSISTENTE - IDIOMA E VOZ] O usuário sempre se comunicará e programará em PORTUGUÊS. O agente deve sempre responder em português e assumir este idioma por padrão. Além disso, o conversor de voz para texto do usuário frequentemente transcreve "WidePay" como "webplay" (ou "webpay", "web play"). O agente deve interpretar e corrigir automaticamente essas palavras para "WidePay" em toda a comunicação e lógica do projeto.

Modo consolidado autorizado:

18. A regra 1 vale para relatorios individuais. Quando o usuario pedir explicitamente "todos os clientes", "lista geral", "relatorio consolidado", "atrasos de todos" ou equivalente, fica autorizado gerar relatorio consolidado somente leitura a partir do WidePay real ou dos JSONs ja extraidos do WidePay.
19. O relatorio consolidado deve ser rapido e economico: preferir JSONs locais recentes em `07_DADOS_TEMPORARIOS\WIDEPAY_CONSULTAS`; so consultar o WidePay novamente quando o usuario pedir atualizacao real ou quando nao houver JSON confiavel.
20. O relatorio consolidado nao substitui o relatorio individual por cliente/lote. Ele deve criar arquivos novos com nome proprio em `07_DADOS_TEMPORARIOS` ou `02_RELATORIOS_GERADOS`, sem sobrescrever relatorios individuais.
21. Boletos avulsos podem representar parcelas atrasadas regularizadas. Para cada cobranca avulsa, o agente deve tentar inferir a parcela original pela descricao informal de referencia, como `ref 10/08/24 atraso`, `ref 10/08/2024`, `atraso 10/08/24`, `mes 08/2024` ou texto semelhante.
22. Quando a data inferida do boleto avulso coincidir com vencimento de parcela/carne e o boleto avulso estiver recebido/pago, a parcela deve ser classificada como "atraso pago por boleto avulso". Quando nao houver boleto avulso pago correspondente, manter como "atraso em aberto/sem avulso pago".
23. Toda inferencia de data por texto informal deve ser marcada como inferencia, nao como fato confirmado, e deve registrar a descricao original usada.
24. O relatorio consolidado deve listar, por cliente/lote: carne, referencia, parcelas atrasadas em aberto, boletos avulsos pagos de atraso, valor atrasado em aberto, valor pago em avulso, data da parcela inferida e observacao.
25. Antes de gerar PDF final consolidado, gerar primeiro Markdown/HTML/CSV de conferencia e apresentar ao usuario. O PDF consolidado so deve ser criado apos validacao.

Dados sensiveis:
- Nao copiar senhas.
- Nao armazenar CPF desnecessariamente em arquivos temporarios.
- Nao enviar dados para servicos externos sem autorizacao.
- Nao compartilhar relatorios automaticamente.

Modo recomendado:
- Navegacao assistida com confirmacao.
- Revisao manual antes de gerar arquivo final.
- Confirmacao antes de qualquer clique sensivel.
