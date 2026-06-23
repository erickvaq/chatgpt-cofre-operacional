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

Não acessar a área de contatos/configurações.

Clientes sem carnê, cobrança ou evidência financeira ativa no WidePay devem ser marcados como:

* “sem evidência financeira ativa”; ou
* “pendente de conferência”.

---

# REGRA — CHECAGEM DE COBERTURA OBRIGATÓRIA NO WIDEPAY

Sempre que eu pedir para conferir clientes, fazer levantamento preliminar, revisar clientes por letras ou gerar relatórios por grupo de clientes, execute automaticamente uma checagem de cobertura antes de concluir.

Objetivo:
Garantir que nenhum cliente ativo das iniciais solicitadas fique de fora.

Processo obrigatório:

1. Consultar primeiro o WidePay.
2. Verificar carnês (nunca acessar Configurações > Contatos).
3. Verificar cobranças/boletos.
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

# REGRA — LOGIN WIDEPAY COM AUTOPREENCHIMENTO SEGURO DO NAVEGADOR

Quando o WidePay abrir na tela de login, o Antigravity/Codex não deve encerrar o processo, não deve reiniciar a tarefa e não deve pedir para eu repetir o comando completo.

Antes de pedir minha intervenção manual, ele pode verificar apenas visualmente se o navegador dedicado já preencheu automaticamente os campos de login pelo próprio recurso de autofill/senha salva do navegador.

Essa verificação deve ser feita de forma segura, sem ler, copiar, exibir, extrair ou armazenar senha.

## Comportamento permitido

Se a tela de login estiver aberta e os campos já estiverem preenchidos automaticamente pelo navegador, o Antigravity/Codex pode:

1. Clicar no botão “Entrar”, “Acessar”, “Login” ou equivalente;
2. Pressionar Enter, se isso apenas confirmar o login já preenchido;
3. Aguardar o carregamento da área logada;
4. Confirmar que saiu da tela de login;
5. Continuar exatamente do ponto em que parou.

O agente pode reconhecer visualmente que o campo de senha está preenchido quando aparecer mascarado, por exemplo com bolinhas ou pontos, mas não pode tentar ler o conteúdo do campo.

## Restrições obrigatórias de segurança

O Antigravity/Codex não deve, em hipótese alguma:

1. Ler minha senha;
2. Copiar minha senha;
3. Exibir minha senha;
4. Salvar minha senha em arquivo, log, print, cache, script ou variável;
5. Digitar senha manualmente;
6. Alterar senha;
7. Acessar o gerenciador de senhas do navegador;
8. Usar DevTools para ler campos sensíveis;
9. Ler o atributo `value` de campo `password`;
10. Exportar, consultar ou manipular credenciais salvas;
11. Tentar burlar autenticação;
12. Prosseguir sozinho se aparecer captcha, 2FA, código por SMS/e-mail, confirmação sensível ou bloqueio de segurança.

## Se o navegador preencher automaticamente

Se o navegador já tiver preenchido os campos e faltar apenas confirmar o acesso, o Antigravity/Codex pode clicar em “Entrar” ou pressionar Enter.

Depois disso, deve aguardar a área logada carregar e continuar o processo exatamente do ponto atual, sem reiniciar a tarefa.

## Se o navegador não preencher automaticamente

Se os campos estiverem vazios, se o login salvo não aparecer, se houver captcha, 2FA, código por SMS/e-mail, confirmação sensível ou qualquer dúvida, o Antigravity/Codex deve parar e responder:

“O WidePay está na tela de login. O navegador não preencheu automaticamente os dados ou há confirmação manual necessária. Faça login manualmente na janela dedicada. Vou aguardar sua confirmação e depois continuo exatamente do ponto atual.”

## Respostas aceitas do usuário

Após o login manual, aceitar como autorização para continuar respostas como:

* “Logado”
* “Pode continuar”
* “Já entrei”
* “Pode seguir”
* “Continue”
* “Pronto”

## Objetivo da regra

Reduzir intervenção manual desnecessária quando o navegador dedicado já possui sessão ou preenchimento automático seguro, mantendo a proteção total das credenciais.

O Antigravity/Codex pode apenas confirmar o login já preenchido pelo navegador.

Se exigir senha manual, captcha, 2FA, código externo ou qualquer confirmação sensível, deve aguardar minha intervenção.

## Versão curta da regra

Se o WidePay abrir na tela de login e o navegador já preencher os campos automaticamente, pode clicar em “Entrar” e continuar. Não leia, copie, extraia, salve, exiba nem digite minha senha. Não use DevTools nem gerenciador de senhas. Se os campos estiverem vazios, houver captcha, 2FA, código externo ou qualquer dúvida, pare e aguarde meu login manual.

---

# REGRA — FOCO NO RESULTADO FINAL: RELATÓRIOS DE TODOS OS CLIENTES COM EFICIÊNCIA

O objetivo principal dos fluxos do WidePay não é narrar cada etapa, criar timers, fazer verificações repetidas ou consumir contexto explicando o processo.

O objetivo principal é:

**gerar e entregar os relatórios financeiros de todos os clientes solicitados, com segurança, conferência e o menor consumo possível de tempo, contexto e tokens.**

## Interpretação obrigatória da intenção do usuário

Quando o usuário pedir levantamento, conferência, extração ou relatório de clientes do WidePay, o Antigravity deve interpretar que o usuário quer o **resultado final organizado**, e não acompanhamento passo a passo desnecessário.

O Antigravity deve agir como executor operacional, tomando decisões simples e seguras sozinho, sem pedir confirmação para cada microetapa.

## Comportamento obrigatório

Sempre que possível, o Antigravity deve:

1. Automatizar processos repetitivos.
2. Processar clientes in lote.
3. Reaproveitar sessão, navegador, scripts e dados já coletados.
4. Evitar repetir buscas ou extrações já feitas.
5. Evitar narrar esperas longas.
6. Evitar timers repetidos.
7. Evitar mensagens intermediárias sem valor.
8. Consolidar erros, pendências e dados parciais em um único resumo.
9. Continuar o fluxo até entregar os relatórios ou até encontrar bloqueio real.
10. Só pedir intervenção do usuário quando houver login, 2FA, erro crítico, dúvida de dados ou risco de alterar algo indevidamente.

## O que deve ser evitado

É proibido transformar a tarefa em uma sequência longa de mensagens como:

* “vou verificar”;
* “vou aguardar”;
* “vou tentar novamente”;
* “timer expirou”;
* “vou abrir outro timer”;
* “vou analisar mais um pouco”;
* “preciso confirmar cada cliente”;
* “vou fazer cliente por cliente manualmente sem necessidade”.

Essas mensagens gastam contexto e tokens sem aproximar o usuário do resultado final.

## Estratégia correta

Para relatórios de vários clientes, o Antigravity deve trabalhar assim:

1. Identificar a lista de clientes.
2. Extrair dados do WidePay da forma mais automatizada possível.
3. Consultar carnês, cobranças e pagamentos sem repetir passos desnecessários.
4. Validar cobertura dos dados.
5. Gerar os relatórios finais no padrão do projeto.
6. Separar clientes concluídos, clientes com pendência e clientes com erro.
7. Apresentar ao usuário um resumo objetivo com os arquivos gerados.

## Quando houver demora ou travamento

Se uma extração demorar, o Antigravity deve verificar o status real uma única vez e responder de forma objetiva:

“A extração está demorando. Verifiquei o status: [rodando/travado]. Última etapa: [etapa]. Último log relevante: [log]. Dados parciais disponíveis: [sim/não]. Deseja que eu aguarde mais uma vez, interrompa com segurança ou apresente os dados parciais?”

Não criar timers repetidos.
Não narrar espera infinita.
Não continuar consumindo contexto sem avanço real.

## Entrega esperada

Ao final, o Antigravity deve entregar:

* relatórios gerados;
* caminho local dos arquivos;
* links GitHub reais, se houver commit/push;
* lista de clientes concluídos;
* lista de clientes com pendência;
* lista de clientes com erro;
* resumo curto do que foi feito;
* status do precheck, se houver.

## Regra de prioridade

Sempre priorizar:

1. resultado final;
2. segurança dos dados;
3. automação;
4. economia de tokens;
5. redução de mensagens intermediárias;
6. clareza na entrega.

Nunca priorizar a narração do processo acima da entrega dos relatórios.

## Aplicação obrigatória

Aplicar esta regra em todos os fluxos do WidePay:

* levantamento preliminar;
* checagem de cobertura;
* consulta de carnês;
* consulta de cobranças;
* geração de relatórios;
* scripts CDP;
* scripts em segundo plano;
* extrações automatizadas;
* relatórios individuais;
* relatórios em lote;
* relatórios de todos os clientes.

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
* Fonte encontrada no WidePay: carnê, cobrança ou boleto avulso;
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

---

# REGRA — NÃO ACESSAR CONFIGURAÇÕES/CONTATOS DO WIDEPAY PARA RELATÓRIOS

O Antigravity/Codex não deve acessar a área:

`https://www.widepay.com/conta/configuracoes/contatos`

nem a seção:

`Configurações > Contatos`

para fazer levantamento financeiro dos clientes do loteamento.

Essa página contém contatos de transferências, dados bancários, favoritos, contatos seguros e outras informações sensíveis que não são necessárias para gerar relatórios financeiros dos lotes.

## Fontes permitidas para relatórios financeiros

Para relatórios WidePay, usar somente as áreas financeiras:

1. Carnês:
   `https://www.widepay.com/conta/recebimentos/carnes`

2. Cobranças/boletos:
   `https://www.widepay.com/conta/recebimentos`

3. Dados visíveis dentro dos próprios carnês, parcelas, cobranças e boletos.

## Comportamento obrigatório

Quando o usuário pedir para verificar clientes, fazer preliminar, conferir A a E, gerar relatórios ou procurar clientes faltando:

1. Não entrar em Configurações > Contatos.
2. Não usar contatos de Transferências.
3. Não usar contatos bancários como lista de clientes.
4. Não acessar dados de transferência, favoritos ou contatos seguros.
5. Buscar clientes pelos registros financeiros do WidePay:
   * carnês;
   * cobranças;
   * boletos;
   * parcelas;
   * referências de pagamento.
6. Usar contratos locais apenas como apoio complementar.
7. Se precisar de algum dado da área de contatos, pedir autorização antes e explicar exatamente por que precisa.

## Regra de segurança

Não consultar, extrair, registrar, copiar, salvar ou usar dados de contatos bancários, transferências, favoritos ou contatos seguros.

O objetivo do projeto é gerar relatórios financeiros dos clientes/lotes com base em carnês, cobranças e boletos do WidePay, não acessar áreas sensíveis de configuração da conta.

---

# REGRA — RESUMO OPERACIONAL LEVE E CONTROLE DE EXECUÇÃO

O Antigravity/Codex deve manter o processo controlado sem consumir tokens desnecessariamente.

O objetivo não é ficar enviando arquivos grandes, logs extensos ou regras completas toda vez.
O objetivo é manter um resumo claro, curto e atualizado do que foi feito, do que falta fazer e dos arquivos criados, para que o usuário consiga acompanhar o processo sem perder tempo.

## Comportamento obrigatório

Sempre que uma etapa importante for executada, criar ou atualizar um arquivo leve de controle, por exemplo:

`07_DADOS_TEMPORARIOS/RESUMO_EXECUCAO_ATUAL.md`

Esse arquivo deve funcionar como um log resumido/checkpoint da execução atual.

## O resumo deve conter somente o essencial

Registrar de forma curta:

1. Data e hora da execução;
2. Comando recebido do usuário;
3. Objetivo da etapa;
4. O que foi feito;
5. Fonte usada:
   * WidePay;
   * contrato local;
   * cache temporário;
   * arquivo já existente;
6. Clientes/lotes processados;
7. Arquivos criados ou alterados;
8. Arquivos apenas consultados;
9. Caminhos locais importantes;
10. O que está pronto;
11. O que está parcial;
12. O que está pendente;
13. Erros ou alertas importantes;
14. Próxima ação recomendada.

## Formato ideal do resumo

Usar formato curto, como:

```md
# RESUMO DA EXECUÇÃO ATUAL

Data/hora:
Comando do usuário:
Objetivo:

## Feito
- ...

## Clientes processados
| Cliente | Lote | Status | Arquivo |
|---|---|---|---|

## Arquivos criados/alterados
| Arquivo | Tipo | Caminho | Status |
|---|---|---|---|

## Pendências
- ...

## Próximo passo recomendado
- ...
```

## Evitar consumo desnecessário de tokens

Não enviar arquivos inteiros no chat sem necessidade.
Não colar logs extensos.
Não repetir regra-base inteira.
Não listar conteúdo completo de arquivos grandes.
Não mandar código inteiro se o usuário não pediu.

Quando precisar informar o andamento, mandar no chat apenas:
* resumo do que foi feito;
* caminhos dos arquivos;
* status;
* pendências;
* próximo passo.

## Regras resumidas

Criar também um resumo curto das regras principais do projeto, por exemplo:

`05_PROMPTS_E_REGRAS/RESUMO_REGRAS_OPERACIONAIS_WIDEPAY.md`

Esse arquivo deve resumir as regras mais importantes para consulta rápida, sem substituir a regra-base completa.

Deve conter, de forma curta:
1. WidePay é fonte principal;
2. Contratos locais são apenas apoio;
3. Não acessar Configurações > Contatos;
4. Não confundir iniciais de nomes com quadras;
5. Login com autopreenchimento seguro;
6. Não criar timers repetidos;
7. Não gerar arquivos finais sem aprovação;
8. Não alterar nada no WidePay;
9. Não usar contratos como lista principal;
10. Não inventar valores;
11. Somar todos os carnês e boletos antes de informar total pago geral;
12. Registrar arquivos locais x GitHub.

## Quando o usuário pedir status

Se o usuário perguntar “o que foi feito?”, “cadê os arquivos?”, “funcionou?”, “o que falta?” ou “me mostre o andamento”, responder com base no `RESUMO_EXECUCAO_ATUAL.md`, sem reler tudo desnecessariamente.

## Quando criar arquivos finais

Ao gerar relatórios, planilhas ou documentos finais, atualizar o resumo com:
* nome do cliente;
* lote;
* tipo de arquivo;
* caminho local;
* se foi ou não enviado ao GitHub;
* commit, se houver;
* se está pronto, parcial ou pendente.

## Controle GitHub

Sempre separar:

### Arquivos apenas locais
* caminho local;
* motivo de ainda não terem commit/push.

### Arquivos enviados ao GitHub
* caminho local;
* link GitHub real;
* commit;
* branch;
* status do push.

## Objetivo final

Manter o processo rápido, rastreável e eficiente.
O Antigravity/Codex deve entregar os relatórios e resultados ao usuário, sem transformar cada etapa em leitura longa de arquivos, logs enormes ou explicações técnicas desnecessárias.



