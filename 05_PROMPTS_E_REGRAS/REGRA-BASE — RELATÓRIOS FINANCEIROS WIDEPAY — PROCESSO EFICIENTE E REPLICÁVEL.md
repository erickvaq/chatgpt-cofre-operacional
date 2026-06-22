# REGRA-BASE — RELATÓRIOS FINANCEIROS WIDEPAY — PROCESSO EFICIENTE E REPLICÁVEL

## Projeto

```text
C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes
```

## Objetivo

Padronizar o processo de levantamento financeiro, conferência e geração de relatórios de clientes/lotes a partir do WidePay, com execução leve, segura, modular e replicável.

---

# 1. FONTE PRINCIPAL

A fonte principal para situação financeira atual é o WidePay.

Usar o WidePay para conferir:

* Carnês ativos;
* Carnês cancelados;
* Cobranças;
* Boletos avulsos;
* Pagamentos recebidos;
* Parcelas vencidas;
* Parcelas em aberto;
* Reajustes;
* Renegociações;
* Distratos;
* Aditivos;
* Boletos substitutos;
* Pagamentos fora de ordem;
* Movimentações recentes.

Links principais:

* https://www.widepay.com/
* https://www.widepay.com/conta/recebimentos
* https://www.widepay.com/conta/recebimentos/carnes
* https://www.widepay.com/conta/configuracoes/contatos#recebimentos

---

# 2. FONTE COMPLEMENTAR

A pasta local de contratos deve ser usada apenas como apoio:

```text
C:\Users\Windows User\Desktop\AGUA VIVA\- CONTRATOS AGUA VIVA
```

Esse caminho significa:

* Pasta principal: `C:\Users\Windows User\Desktop\AGUA VIVA`
* Subpasta de contratos: `- CONTRATOS AGUA VIVA`

Contratos locais podem estar desatualizados.

Usar contratos locais somente para apoiar a conferência de:

* Nome correto do cliente;
* Lote;
* Quadra;
* Quantidade total de parcelas contratadas;
* Data de início;
* Data prevista de conclusão;
* Valor inicial das parcelas;
* Informações contratuais complementares.

Em caso de divergência entre WidePay e contrato local, considerar o WidePay como fonte principal da situação financeira atual.

---

# 3. DEFINIÇÃO DE CLIENTE ATIVO

Considerar como cliente ativo apenas aquele que possui evidência financeira no WidePay, como:

* Carnê ativo;
* Cobrança ativa;
* Boleto em aberto;
* Boleto recebido;
* Parcela vencida;
* Histórico financeiro vinculado a lote;
* Movimentação financeira recente;
* Registro financeiro em carnês ou cobranças.

Não considerar cliente ativo apenas porque o nome aparece nos contatos do WidePay.

Contatos sem carnê, cobrança, boleto ou evidência financeira devem ser marcados como:

* “sem evidência financeira ativa”; ou
* “pendente de conferência”.

---

# REGRA — CHECAGEM DE COBERTURA OBRIGATÓRIA NO WIDEPAY

Sempre que eu pedir para conferir clientes, fazer levantamento preliminar, revisar clientes por letras ou gerar relatórios por grupo de clientes, execute automaticamente uma checagem de cobertura antes de concluir.

Objetivo:
Garantir que nenhum cliente ativo das iniciais solicitadas fique de fora.

Processo obrigatório:

1. Consultar primeiro o WidePay.
2. Verificar clientes/contatos.
3. Verificar carnês.
4. Verificar cobranças/boletos.
5. Cruzar nomes repetidos para evitar duplicidade.
6. Consolidar todos os registros do mesmo cliente/lote.
7. Classificar cada nome encontrado como:
   * Ativo confirmado;
   * Sem evidência financeira ativa;
   * Pendente de conferência.
8. Não excluir cliente apenas porque não encontrou contrato local.
9. Usar a pasta de contratos somente como apoio complementar.
10. Se o cliente aparecer no WidePay, mas não houver contrato local, manter na tabela com:
    “Contrato local não encontrado — pendente de conferência.”

Antes de finalizar qualquer levantamento preliminar, informar obrigatoriamente:
* Total de nomes avaliados;
* Total de clientes ativos confirmados;
* Total de clientes sem evidência financeira ativa;
* Total de clientes pendentes de conferência;
* Se alguma página, filtro, busca, carnê ou cobrança do WidePay não pôde ser conferida completamente.

Esta checagem deve ser feita automaticamente sempre que eu pedir para conferir clientes ou fazer preliminar por letras, mesmo que eu use comando curto, como:
“Fazer preliminar A a E.”
“Conferir clientes F a G.”
“Revisar clientes da etapa anterior.”
“Continuar próximas letras.”

Esta regra deve ser incorporada ao método aprovado do WidePay para evitar que algum cliente fique de fora.

---

# REGRA — LOGIN MANUAL NO WIDEPAY SEM ENCERRAR O PROCESSO

Sempre que o Antigravity precisar acessar o WidePay e encontrar a tela de login, o processo não deve ser encerrado, cancelado nem reiniciado.

## Comportamento obrigatório

Quando aparecer a tela de login do WidePay, o Antigravity deve:

1. Abrir ou manter visível a janela/navegador dedicado do WidePay.
2. Informar claramente que o usuário precisa fazer login manualmente.
3. Pausar a execução e aguardar confirmação do usuário.
4. Aceitar como confirmação respostas como:
   * “Logado”
   * “Pode continuar”
   * “Já entrei”
   * “Pode seguir”
5. Não encerrar a tarefa.
6. Não reiniciar o levantamento do zero.
7. Não exigir que o usuário repita o comando completo.
8. Após a confirmação do login, continuar exatamente do ponto em que parou.

## Resposta padrão ao encontrar login

Quando o WidePay estiver na tela de login, responder:

“O WidePay está na tela de login. Faça login manualmente na janela do navegador dedicada. Vou aguardar sua confirmação. Quando estiver logado, responda ‘Logado’ ou ‘Pode continuar’ para eu seguir exatamente do ponto atual.”

## Aplicação obrigatória

Aplicar esta regra em todos os fluxos do WidePay, incluindo:

* Levantamento preliminar;
* Checagem de cobertura;
* Conferência de cliente específico;
* Geração de relatórios;
* Consulta de carnês;
* Consulta de cobranças/boletos;
* Consulta de contatos.

## Objetivo

Esta regra deve evitar:

* perda de tempo;
* repetição de comandos;
* reinício desnecessário do processo;
* abandono da tarefa quando o login manual for necessário.

---

# 4. MODO 1 — LEVANTAMENTO PRELIMINAR

O levantamento preliminar deve ser sempre a primeira etapa de cada grupo de letras ou clientes.

Nesta etapa:

* Não gerar PDF;
* Não gerar HTML;
* Não gerar DOCX;
* Não gerar XLSX;
* Não criar arquivos finais;
* Não alterar arquivos do projeto;
* Não mover contratos;
* Não copiar documentos;
* Não alterar nada no WidePay;
* Não fazer cálculos finais;
* Não gerar relatório individual final.

Executar somente:

1. Consultar WidePay;
2. Identificar clientes ativos do grupo solicitado;
3. Verificar carnês, cobranças e boletos avulsos;
4. Conferir indícios em contratos locais, quando necessário;
5. Consolidar duplicidades;
6. Apontar pendências;
7. Apresentar tabela preliminar diretamente no chat.

A tabela preliminar deve conter:

* Letra inicial;
* Nome do cliente;
* Cliente ativo confirmado: Sim, Não ou Pendente;
* Lote(s) identificado(s);
* Quadra;
* Fonte encontrada no WidePay: carnê, cobrança, boleto avulso ou contato;
* Contrato local encontrado: Sim, Não ou Pendente;
* Indício de boletos avulsos;
* Indício de reajuste, distrato, aditivo, renegociação ou pagamento fora de ordem;
* Status da conferência;
* Observação inicial.

Após apresentar a tabela preliminar, parar e aguardar aprovação antes de gerar qualquer arquivo final.

---

# 5. MODO 2 — GERAÇÃO DE ARQUIVOS FINAIS

Executar somente após aprovação expressa da lista preliminar.

Quando autorizado, gerar os arquivos finais necessários:

1. Relatório individual simples por cliente/lote;
2. Relatório interno completo, se necessário;
3. Planilha XLSX geral da etapa;
4. Evidências, prints ou arquivos auxiliares, quando necessário;
5. Registros do processo.

Organização das saídas:

Relatórios individuais:

```text
02_RELATORIOS_GERADOS
```

Planilha geral XLSX:

```text
03_PLANILHAS
```

Evidências, prints ou arquivos auxiliares:

```text
04_EVIDENCIAS_PRINTS
```

Registros do processo:

```text
05_PROMPTS_E_REGRAS
```

Padrão de nomes:

```text
RELATORIO_CLIENTE_[NOME]_LOTE_[LOTE]_[DATA]
```

```text
PLANILHA_GERAL_CLIENTES_[LETRAS]_[DATA]
```

---

# 6. REGRAS DE INTERPRETAÇÃO

1. Um mesmo cliente pode ter mais de um lote. Separar informações por lote quando houver confirmação.

2. Um mesmo cliente pode aparecer in contatos, carnês, cobranças, boletos avulsos e contratos locais. Consolidar as informações e evitar duplicidade.

3. Um cliente pode pagar:

* Um único carnê para vários lotes;
* Carnês separados por lote;
* Parte por carnê e parte por boleto avulso;
* Boletos avulsos referentes a atrasos;
* Boletos substitutos;
* Pagamentos fora de ordem.

4. Em boletos avulsos, analisar referência, descrição, valor, vencimento, cliente, lote e histórico.

5. Não usar somente a data de vencimento do boleto avulso para concluir qual parcela foi quitada.

6. Referências como “01-26”, “02-26”, “03-2026” ou “12-2025” podem indicar mês e ano.

7. Referências como “30-01”, “30-03” ou semelhantes podem indicar data, vencimento, parcela ou referência interna.

Quando houver dúvida, marcar como:

```text
referência ambígua — pendente de conferência
```

8. Exemplos reais de referências que podem aparecer em boletos avulsos:

* “atrazo ref: 01-26 e 03-26”;
* “Ref 30-01 30-03 2026 atrazo e5”;
* “ref 12-2025 e 01-2026”;
* “Ref 02 - 03 - 04 de 2026 atrazo”;
* “d1 d2 atrazo 01 03 04 2026”;
* “Ref atrasos meses 01-26 02-26 03-2026 04-2026”.

9. Se a referência indicar vários meses, registrar quais meses aparentam estar sendo quitados.

10. Se a referência estiver ambígua, não forçar interpretação. Marcar como pendente de conferência.

11. Boletos avulsos recebidos devem ser somados ao total pago somente no relatório final e apenas quando houver correspondência com o lote analisado.

12. Boletos e carnês cancelados não devem ser considerados dívida ativa, exceto quando houver indicação clara de substituição por nova cobrança em aberto.

13. Reajuste de valor no WidePay não significa automaticamente troca de lote. Pode representar atraso, compensação, renegociação, continuação de parcelas ou cobrança complementar.

14. Carnês com valores diferentes para o mesmo cliente/lote devem ser analisados com cuidado. Podem representar:

* Reajuste;
* Carnê substituto;
* Carnê complementar;
* Continuação de parcelas;
* Cobrança de atraso;
* Pagamento fora de ordem;
* Renegociação.

15. Informações de reajuste, distrato, aditivo ou renegociação devem ser percebidas principalmente no WidePay, porque a pasta de contratos geralmente pode estar desatualizada.

16. Não inventar valores, datas, parcelas, lotes ou interpretações.

Quando algo não estiver confirmado, usar:

* “não confirmado”;
* “pendente de conferência”;
* “referência ambígua — pendente de conferência”.

---

# 7. REGRA DE EFICIÊNCIA

O processo deve evitar consumo excessivo de tokens e tempo.

Aplicar sempre:

* Primeiro levantamento preliminar leve;
* Depois arquivos finais somente dos clientes aprovados;
* Não reprocessar clientes já conferidos sem necessidade;
* Reaproveitar métodos aprovados;
* Consolidar informações duplicadas;
* Evitar explicações longas quando a tarefa for operacional;
* Registrar apenas o necessário para continuidade.

---

# 8. REGRA DE REPLICABILIDADE

Métodos aprovados ou que funcionarem corretamente devem ser reaplicados nas próximas etapas.

Não exigir que o usuário repita toda a regra-base a cada execução.

Comandos curtos devem ser suficientes, por exemplo:

* “Fazer preliminar A a E.”
* “Fazer preliminar F a G seguindo o método aprovado.”
* “Gerar arquivos finais dos clientes aprovados da etapa A a E.”
* “Continuar próximas letras com o mesmo padrão.”
* “Revisar cliente específico seguindo o padrão WidePay.”

---

# 9. REGRA DE SEGURANÇA

Não alterar nada no WidePay sem autorização expressa.

Proibido sem autorização:

* Cancelar boleto;
* Emitir cobrança;
* Editar cliente;
* Excluir cliente;
* Alterar carnê;
* Alterar cobrança;
* Mover ou excluir arquivos locais;
* Sobrescrever relatório final aprovado.

Prioridade do processo:

1. Consultar com segurança;
2. Não alterar dados;
3. Não inventar informações;
4. Economizar tokens;
5. Gerar preliminar antes dos arquivos;
6. Gerar arquivos somente quando autorizado;
7. Manter método reaproveitável para próximas etapas.

---

# 10. COMANDO CURTO PADRÃO — PRELIMINAR

Quando o usuário pedir algo como:

```text
Fazer preliminar A a E.
```

Interpretar como:

Fazer levantamento preliminar dos clientes ativos no WidePay com as iniciais indicadas, seguindo esta regra-base.

Não gerar arquivos.
Não fazer cálculos finais.
Apresentar somente a tabela preliminar no chat e aguardar aprovação.

---

# 11. COMANDO CURTO PADRÃO — ARQUIVOS FINAIS

Quando o usuário pedir algo como:

```text
Gerar arquivos finais dos clientes aprovados da etapa A a E.
```

Interpretar como:

Gerar relatórios e planilha final somente dos clientes aprovados pelo usuário, seguindo esta regra-base, organizando os arquivos nas pastas do projeto e sem alterar nada no WidePay.

---

# 12. COMANDO PARA SALVAR ESTA REGRA

Salve esta regra-base como:

```text
REGRA-BASE — RELATÓRIOS FINANCEIROS WIDEPAY — PROCESSO EFICIENTE E REPLICÁVEL
```

no projeto:

```text
C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes
```

Use esta regra como método fixo para levantamentos preliminares e geração futura de relatórios financeiros do WidePay.
