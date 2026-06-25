# REGRAS PERSISTENTES DO PROJETO - Relatorio_WidePay_Lotes
# Atualizado em: 2026-06-25
---

## REGRA ZERO - WidePay primeiro, contratos depois

Esta regra tem prioridade acima de todas as outras regras do projeto.

Antes de qualquer consulta, levantamento, auditoria, relatorio, busca de cliente, checagem de cobertura, conferencia A a E, letra especifica, cliente especifico, lote, carne, cobranca ou PDF, a ordem obrigatoria e:

## REGRA OBRIGATORIA - Abrir WidePay real antes de qualquer consulta

Antes de qualquer busca de cliente, relatorio, auditoria, letra, lote, pendencia, pagamento, parcela, carne, cobranca, PDF, HTML ou XLSX, o fluxo deve:

1. Abrir o Opera dedicado do projeto;
2. Conectar ao CDP `localhost:9444`;
3. Carregar o site real do WidePay;
4. Acessar a area financeira;
5. Consultar Carnes;
6. Consultar Cobrancas/Boletos.

Bloqueio:
- proibido continuar o fluxo usando contratos, pastas locais, arquivos antigos, JSONs antigos ou relatorios anteriores antes de tentar abrir o WidePay real;
- se o Opera/CDP nao estiver aberto, abrir automaticamente o Opera dedicado;
- se o WidePay nao carregar, parar e informar `WIDEPAY REAL NAO ABERTO - EXECUCAO BLOQUEADA. Nao vou consultar arquivos locais antes de abrir o WidePay.`

Comportamento esperado:
- a primeira acao pratica deve ser `Abrindo Opera dedicado e carregando WidePay real...`;
- se ja estiver logado, continuar;
- se o login estiver preenchido pelo navegador, clicar em Entrar;
- se o login estiver vazio, houver captcha, 2FA ou erro, aguardar intervencao manual;
- so depois consultar Carnes e Cobrancas/Boletos;
- so depois consultar contratos locais.

Erro critico:
- `ERRO CRITICO: WidePay real nao foi aberto. Fluxo bloqueado antes de consultar arquivos locais.`

1. WidePay primeiro
- consultar Carnes;
- consultar Cobrancas/Boletos;
- identificar clientes com evidencia financeira;
- identificar carnes ativos, finalizados, pagos, pendentes e cancelados;
- consolidar registros repetidos do mesmo cliente/lote.

2. Contratos e arquivos locais depois
- usar contratos locais apenas como apoio;
- confirmar lote;
- confirmar nome completo;
- conferir contrato fisico;
- complementar dados ausentes;
- nunca usar pasta local como fonte principal da lista oficial.

Bloqueio obrigatorio:
- proibido fechar lista oficial de clientes, pendentes, ativos ou relatorios comecando por arquivos locais.
- se o WidePay ainda nao foi consultado, qualquer resultado baseado em arquivos locais deve ser marcado obrigatoriamente como `LISTA LOCAL PRELIMINAR - PENDENTE DE VALIDACAO WIDEPAY`.

Erro critico:
- ERRO CRITICO: fluxo local-first bloqueado. A fonte principal e WidePay. Consulte Carnes e Cobrancas/Boletos antes de usar contratos locais.

Excecao permitida:
- so pode comecar por arquivos locais se o usuario pedir explicitamente algo como "procure so nos contratos", "faça uma busca local", "nao acesse o WidePay agora" ou "levante apenas o que existe no disco".
- mesmo nesses casos, o resultado deve sair marcado como `PRELIMINAR - NAO VALIDADO NO WIDEPAY`.

---

## REGRA UNIVERSAL - Fluxo padrao universal para relatorios WidePay

Esta regra vale para qualquer:
- cliente especifico;
- letra unica;
- intervalo de letras;
- grupo de clientes;
- lote;
- todos os clientes;
- relatorio financeiro individual;
- relatorio financeiro consolidado;
- levantamento;
- auditoria;
- conferencia;
- lista de pendencias;
- lista de pagamentos, parcelas, carnes, cobrancas ou boletos.

Fluxo obrigatorio:

1. Precheck e skills
- carregar `widepay-core-operacional`;
- carregar `widepay-relatorio-pdf` quando houver HTML, PDF, relatorio visual ou conferencia financeira;
- carregar `widepay-abertura-externa` quando houver abertura de arquivo ou pasta;
- rodar `python 00_SISTEMA_PRECHECK\precheck_regras.py`;
- se o precheck falhar, parar a execucao.

2. WidePay primeiro
- abrir o Opera dedicado e conectar ao CDP `localhost:9444`;
- consultar Carnes;
- consultar Cobrancas/Boletos;
- identificar clientes com evidencia financeira;
- consolidar registros repetidos do mesmo cliente/lote;
- nunca começar por contratos locais;
- nunca fechar lista oficial por arquivos locais;
- nunca acessar `Configuracoes > Contatos`.

3. Bloqueio e marcacao
- se o WidePay nao consultar, marcar `WIDEPAY NAO CONSULTADO - EXECUCAO OFICIAL BLOQUEADA`;
- se houver busca local por excecao, marcar `LISTA LOCAL PRELIMINAR - PENDENTE DE VALIDACAO WIDEPAY`.

4. Contratos locais depois
- usar contratos locais apenas como apoio;
- confirmar lote;
- confirmar nome completo;
- conferir contrato fisico;
- complementar dados ausentes;
- nunca usar pasta local como fonte principal da lista oficial.

5. Base estruturada
- criar ou atualizar base local em `07_DADOS_TEMPORARIOS`;
- separar dados do WidePay, contrato local, inferencias, pendencias e divergencias;
- nunca inventar valor, data, parcela ou pagamento.

6. Conferencia e entregas
- gerar conferencia em Markdown (`.md`) antes do PDF final individual;
- para mais de um cliente, gerar tambem planilha consolidada `.xlsx`;
- gerar HTML + PDF no padrao visual aprovado;
- abrir PDF externamente; nao abrir como texto bruto;
- atualizar o painel publico somente com resumo curto;
- nao enviar dados sensiveis ao GitHub sem autorizacao.

7. Resposta obrigatoria
- informar escopo, precheck, WidePay consultado, carnes, cobrancas/boletos, arquivos gerados, painel e pendencias.

---

## REGRA PRIORITARIA - Fonte principal de instrucoes

Antes de qualquer relatorio, PDF, HTML, DOCX, importacao, conferencia, busca de cliente, painel, script ou entrega final, carregar estas regras via precheck.

A REGRA ZERO vem antes de qualquer outra secao.

Ordem de prioridade:
1. seguranca dos dados;
2. resultado final correto;
3. consulta real ao WidePay;
4. conferencia antes do PDF;
5. economia de tokens;
6. rastreabilidade suficiente;
7. clareza para o usuario.

Se houver conflito entre print do usuario, WidePay, contrato local, script ou relatorio anterior, parar e pedir confirmacao antes de gerar arquivo final.

---

## REGRA 1 - WidePay, contratos e conflito de fontes

WidePay e a fonte principal financeira do projeto.
Contratos locais sao apoio complementar.
Prints do usuario podem validar a leitura, mas nao podem ser usados para forcar conclusao quando houver conflito com WidePay, contrato, script ou relatorio anterior.

Se houver divergencia relevante:
- parar;
- registrar a fonte de cada dado;
- pedir confirmacao explicita do usuario.

Todos os arquivos e consultas devem permanecer dentro da pasta do projeto, salvo leitura controlada de fontes externas autorizadas.

---

## REGRA 2 - Seguranca WidePay e login

WidePay e somente leitura.
Nunca alterar, cancelar, excluir, baixar em massa, editar boleto, editar carne, editar cobranca, alterar cadastro ou mudar valor.

Usar somente as areas financeiras:
- Carnes;
- Cobrancas/Boletos.

Nao acessar:
- `Configuracoes > Contatos`;
- contatos bancarios;
- transferencias;
- favoritos;
- contatos seguros;
- qualquer area nao financeira como fonte de cliente.

Login:
- nunca ler, copiar, salvar, exibir, extrair ou digitar senha;
- se o navegador dedicado preencher automaticamente, pode apenas clicar em Entrar ou pressionar Enter;
- se campos estiverem vazios, houver captcha, 2FA, codigo externo ou qualquer duvida, parar e aguardar login manual.

Navegador:
- usar Opera GX dedicado com perfil persistente do projeto;
- porta CDP principal: `9444`;
- nao usar o Chrome principal do usuario;
- nao encerrar o navegador do usuario;
- se o CDP falhar, marcar WidePay como nao consultado e nao inventar dados.

---

## REGRA 3 - Fluxo por cliente

Para cada cliente:
1. identificar nome e lote;
2. consultar todos os carnes e cobrancas/boletos relacionados;
3. cruzar com contrato local quando existir;
4. recalcular tudo do zero;
5. nunca copiar numeros de um cliente para outro;
6. gerar conferencia em Markdown (`.md`) antes do PDF final;
7. gerar PDF/HTML final somente apos validacao do usuario, quando exigida.

Para pedidos como `A a E`, interpretar como iniciais reais dos nomes dos clientes, nao como quadras.
Consolidar nomes repetidos.
Separar conclusao, pendencia, sem evidencia financeira e erro.
Nao excluir cliente apenas por falta de contrato local.

---

## REGRA 4 - Relatorios em lote e consolidado

Quando o usuario pedir lista geral, todos os clientes, atrasos de todos ou relatorio consolidado:
- gerar conferência consolidada em modo somente leitura;
- preferir JSONs locais recentes em `07_DADOS_TEMPORARIOS\WIDEPAY_CONSULTAS` para economizar tempo e creditos;
- consultar o WidePay real novamente somente quando o usuario pedir atualizacao real, quando nao houver JSON confiavel ou quando houver divergencia relevante;
- nunca alterar WidePay;
- registrar boletos avulsos como possivel regularizacao de parcelas atrasadas quando a descricao informal permitir inferencia;
- marcar toda inferencia de data como inferencia e preservar a descricao original.

O consolidado deve listar por cliente/lote:
- carne;
- referencia;
- parcela vencida;
- status;
- valor;
- boleto avulso relacionado;
- data inferida;
- valor pago em avulso;
- observacao.

---

## REGRA 5 - Entrega visual e arquivos finais

Toda entrega visual final deve sair em par:
- `.html` para previa visual/interativa;
- `.pdf` para conferencia, impressao e envio.

Regras da entrega:
- os dois arquivos devem ficar na mesma pasta final;
- nomear com assunto ou cliente, tipo, data e versao;
- nunca sobrescrever versao antiga;
- se `V1` existir, criar `V2`, depois `V3` e assim por diante;
- abrir a pasta final no Windows Explorer para conferencia;
- abrir o PDF externamente quando necessario;
- nao abrir PDF como texto bruto dentro do editor.

Se o usuario pedir acesso clicavel, o PDF pode ser referenciado por link clicavel no chat, mantendo tambem o caminho em texto puro e a opcao de abertura externa.

Nao criar `.bat` por padrao. Criar apenas se o usuario pedir ou houver necessidade tecnica real.
Quando criar `.bat`, usar caminhos relativos com `%~dp0`.

---

## REGRA 6 - GitHub e rastreabilidade

GitHub e um espelho operacional leve, nao uma copia pesada da pasta local.

Pode ir completo para o GitHub:
- regras;
- scripts;
- precheck;
- painel operacional;
- resumos operacionais sem dado sensivel;
- evidencias sanitizadas.

Fica local e deve ser registrado de forma sanitizada no painel:
- PDFs financeiros;
- HTMLs financeiros;
- planilhas;
- contratos;
- JSONs do WidePay;
- caches;
- logs com dado sensivel.

Nao enviar ao GitHub sem autorizacao:
- dados financeiros detalhados;
- contratos sensiveis;
- cookies;
- tokens;
- senhas;
- caches;
- qualquer dado pessoal indevido.

Nunca inventar link GitHub.
So informar link depois de commit e push confirmados.

---

## REGRA 7 - Painel operacional WidePay

Manter sempre atualizado:
`05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md`

O painel e o controle principal e deve conter apenas o essencial:
- data da ultima atualizacao;
- ultimo comando;
- estado atual;
- ultimo commit;
- branch;
- clientes acessados;
- clientes concluidos;
- clientes pendentes;
- clientes sem evidencia financeira;
- arquivos criados ou alterados;
- arquivos sensiveis nao enviados;
- erros criticos;
- proximo passo recomendado.

Nao criar varios arquivos pequenos de controle se o painel ja resolver.
Erros, bloqueios e contencao devem ser registrados no painel de forma curta e objetiva.

---

## REGRA 8 - Economia operacional, skills e precheck

Economia operacional:
- evitar timers repetidos;
- evitar mensagens intermediarias sem avancos;
- evitar planos longos quando o pedido for simples;
- nao reler arquivos grandes sem necessidade;
- nao colar logs extensos no chat;
- responder com resumo curto: feito, pendente, arquivos, erros e proximo passo.

Skills WidePay a acionar automaticamente quando o pedido envolver o dominio:
- `widepay-core-operacional`;
- `widepay-relatorio-pdf`;
- `widepay-abertura-externa`.

Precheck:
- rodar `00_SISTEMA_PRECHECK\precheck_regras.py` antes de tarefas relevantes;
- o precheck deve validar a estrutura e os pontos criticos sem depender de quantidade fixa de regras.

Modelo Camila:
- serve apenas como modelo visual e metodologico;
- nao usar numeros ou constantes da Camila em outros clientes;
- sempre recalcular do zero para cada cliente novo.

---

## REGRA 9 - Painel operacional publico sempre limpo e verificado

O arquivo `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md` e o painel publico oficial usado para revisar o estado do projeto.

Sempre que o Antigravity alterar, consolidar, limpar ou atualizar esse painel, deve:
1. atualizar o painel local;
2. remover conteudo legado que possa confundir a revisao;
3. rodar precheck;
4. fazer commit;
5. fazer push;
6. conferir o conteudo publicado no GitHub apos o push;
7. so entao declarar a tarefa concluida.

Marcadores proibidos quando o painel estiver em modo limpo:
- `19 x 21`;
- `Heron Souza Dias`;
- `cb8c5c8`;
- `RESUMO DA EXTRAÇÃO WIDEPAY`;
- tabelas antigas de clientes A a E;
- auditoria antiga;
- pendencias antigas ja substituidas;
- commits antigos apresentados como estado atual;
- qualquer informacao que contradiga o estado final informado no chat.

Pos-push obrigatorio:
- conferir o arquivo publicado no GitHub normal;
- conferir o raw, quando possivel;
- so declarar conclusao se o painel publico realmente mostrar a versao nova.

Se o painel local estiver correto, mas o painel publico ainda mostrar conteudo antigo, cache, branch errada ou versao divergente, nao responder `concluido`.

Resposta obrigatoria nesse caso:
`O painel local foi atualizado, mas o painel público ainda não reflete a versão limpa. Vou corrigir sincronização, branch, commit ou push antes de declarar concluído.`
