# REGRAS PERSISTENTES DO PROJETO - Relatorio_WidePay_Lotes
# Atualizado em: 2026-06-25
---

## REGRA PRIORITARIA - Fonte principal de instrucoes

Antes de qualquer relatorio, PDF, HTML, DOCX, importacao, conferencia, busca de cliente, painel, script ou entrega final, carregar estas regras via precheck.

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
6. gerar conferencia `.md` antes do PDF final;
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
