Quero que voce me ajude a gerar um relatorio financeiro individual no WidePay.com.

Contexto:
Vou escolher manualmente um cliente no momento da busca. O objetivo e consultar os boletos, carnes, parcelas pagas e debitos em aberto desse cliente, mas somente para um lote especifico.

Antes de executar qualquer acao, leia o arquivo:
05_PROMPTS_E_REGRAS/REGRAS_RELATORIO_WIDEPAY.md

Fluxo desejado:

1. Abrir o navegador e acessar:
https://widepay.com

2. Aguardar eu fazer login manualmente.

3. Depois do login, me orientar a pesquisar o cliente desejado.

4. Quando o cliente for encontrado, analisar visualmente os boletos, carnes, cobrancas ou parcelas disponiveis.

5. Identificar se existem cobrancas de mais de um lote.

6. Pedir que eu confirme qual lote sera analisado.

7. Para o lote escolhido, coletar:
- Nome do cliente
- CPF ou identificador, se visivel
- Identificacao do lote
- Numero do contrato, se existir
- Boletos pagos
- Boletos em aberto
- Boletos vencidos
- Boletos a vencer
- Valor de cada parcela
- Data de vencimento de cada parcela
- Data de pagamento, se existir
- Valor total pago
- Valor total pendente
- Quantidade de parcelas pagas
- Quantidade de parcelas restantes
- Status geral do lote

8. Procurar na pasta 01_CONTRATOS_CLIENTES um contrato correspondente ao nome do cliente e ao lote.

9. Se encontrar contrato em PDF, DOCX ou TXT, extrair:
- Nome do cliente
- Lote
- Valor total do contrato
- Quantidade total de parcelas
- Valor das parcelas
- Data de inicio
- Data prevista de conclusao
- Condicoes de pagamento

10. Comparar contrato e WidePay.

11. Gerar relatorio final em Markdown e, se possivel, tambem em PDF ou DOCX.

12. Gerar tambem uma planilha CSV ou XLSX com o resumo financeiro.

13. Salvar os arquivos com o padrao:
RELATORIO_CLIENTE_[NOME]_LOTE_[NUMERO]_[DATA]

Importante:
Nao alterar nada no WidePay.
Nao excluir arquivos.
Nao baixar dados em massa.
Nao consultar clientes que eu nao escolher.
Sempre pedir confirmacao antes de qualquer acao sensivel.
