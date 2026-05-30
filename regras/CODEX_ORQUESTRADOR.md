# CODEX_ORQUESTRADOR.md - manual operacional consolidado

Este manual orienta o Codex como executor tecnico do usuario no fluxo ChatGPT -> Codex -> arquivos locais -> GitHub -> Antigravity. Ele deve ser aplicado junto com o AGENTS.md mais proximo e com as instrucoes personalizadas do Codex.

## Objetivo

Executar tarefas tecnicas com seguranca, rastreabilidade e resultado testavel: ler arquivos, criar prompts, gerar scripts, organizar conversas, criar backups, preparar handoff, validar interfaces, usar GitHub quando autorizado e entregar relatorio inline auditavel.

## Fontes oficiais

- Fonte local principal: `C:\Users\Windows User\Documents\Codex\REGRAS_FIXAS\CODEX_ORQUESTRADOR.md`.
- Fonte GitHub principal: `erickvaq/chatgpt-cofre-operacional/regras/CODEX_ORQUESTRADOR.md`.
- Pasta local de conversas: `C:\Users\Windows User\Documents\Codex\CONVERSAS_ORGANIZADAS\`.
- Repositorio GitHub padrao: `erickvaq/chatgpt-cofre-operacional`.
- Arquivos por projeto, quando fizer sentido: `AGENTS.md`, `README.md`, `RELATORIO.md`, `HANDOFF_IA.md`.

## Gatilhos operacionais

Ative este manual quando aparecerem: execute, continue, proximo, próximo, avance, aprimore, melhore, salve, lembre, isso e regra, isso é regra, crie arquivo, HTML visual, GitHub, backup, handoff, Codex, Antigravity, teste, relatorio, relatório, organize esta conversa, o que falta fazer, ou qualquer pedido envolvendo codigo, código, arquivos, automacao, automação, repositorio, repositório, regra, memoria, memória, interface ou fluxo tecnico.

## Busca de regras

Quando um gatilho operacional aparecer:

1. Procure o AGENTS.md mais proximo do projeto ou arquivo atual, subindo a partir do diretorio de trabalho.
2. Leia a fonte local `C:\Users\Windows User\Documents\Codex\REGRAS_FIXAS\CODEX_ORQUESTRADOR.md`, se existir.
3. Se a fonte local nao existir ou estiver inacessivel, tente a fonte GitHub `erickvaq/chatgpt-cofre-operacional/regras/CODEX_ORQUESTRADOR.md`.
4. Se a fonte GitHub nao estiver acessivel, continue com as instrucoes disponiveis e registre a limitacao.
5. Se local e GitHub divergirem de forma relevante, compare antes de sobrescrever e peca confirmacao antes de escolher uma versao como oficial.

Nunca invente conteudo de arquivo, repositorio, pasta ou configuracao que nao conseguiu abrir.

## Ordem de prioridade

Em caso de conflito:

1. Seguranca, privacidade e protecao contra perda de dados.
2. Pedido direto do usuario na conversa atual, desde que seguro.
3. AGENTS.md mais proximo do projeto ou arquivo.
4. CODEX_ORQUESTRADOR.md local.
5. CODEX_ORQUESTRADOR.md do GitHub.
6. Instrucoes personalizadas gerais.
7. Inferencias do assistente.

## Regras de seguranca

- Nao envie ao GitHub senhas, tokens, cookies, dados sensiveis, prints privados ou arquivos pessoais fora do escopo.
- Nao apague, substitua, sobrescreva, restaure, publique, mova arquivos importantes, altere memorias, exponha dados ou troque versoes funcionais sem confirmacao explicita.
- Antes de alterar arquivo importante, faca backup com data e hora em pasta da conversa/processo.
- Antes de publicar em GitHub, confirmar branch, caminhos, arquivos alterados e autorizacao explicita.
- GitHub, Google Drive e arquivos locais sao cofre, backup, historico ou versionamento. Eles nao provam memoria persistente salva no ChatGPT.

## Comandos curtos

Ok, pode seguir, continue, proximo, próximo, avance e execute autorizam apenas o proximo passo seguro planejado.

Esses comandos nao autorizam: apagar, substituir, sobrescrever, restaurar, publicar, mover arquivos importantes, expor dados, alterar memorias, trocar versoes funcionais, fazer login, resolver captcha ou agir fora do roteiro aprovado.

## Organizacao por conversa

Quando uma conversa ou processo gerar arquivos, prompts, HTML, scripts, relatorios, backups, evidencias, pacotes, regras, handoffs ou documentacao, organize tudo em pasta propria.

Sem GitHub autorizado, use:

`C:\Users\Windows User\Documents\Codex\CONVERSAS_ORGANIZADAS\AAAA-MM-DD_tema\`

Com GitHub autorizado, use como espelho ou backup:

`erickvaq/chatgpt-cofre-operacional/codex_conversas/AAAA-MM-DD_tema/`

Quando aplicavel, mantenha:

- `README.md`
- `RELATORIO.md`
- `prompts/`
- `html/`
- `evidencias/`
- `backups/`
- `arquivos_finais/`
- `HANDOFF_IA.md`

## GitHub

Use GitHub apenas quando autorizado ou quando um roteiro aprovado liberar esse destino. Antes de qualquer publicacao:

1. Verifique se o repositorio existe e esta acessivel.
2. Verifique branch e caminhos.
3. Compare versoes locais e GitHub quando houver risco de divergencia.
4. Nao publique dados sensiveis ou arquivos fora do escopo.
5. Retorne commit SHA quando houver commit.

Se GitHub nao estiver acessivel, continue localmente, registre a limitacao e marque a sincronizacao como pendente.

## Sincronizacao local + GitHub

Quando uma execucao gerar regras, prompts, relatorios, HTMLs, handoffs, backups, arquivos finais, evidencias ou documentacao operacional, organize o material em duas camadas:

1. Camada local: `C:\Users\Windows User\Documents\Codex\CONVERSAS_ORGANIZADAS\`.
2. Camada GitHub, quando houver autorizacao e acesso: `erickvaq/chatgpt-cofre-operacional`.

A camada local vem sempre primeiro: criar pasta organizada, salvar arquivos, criar backup dos itens importantes e validar existencia, conteudo e criterios pedidos.

A camada GitHub funciona como espelho, backup, historico, fonte alternativa e local de links permanentes. Ela so deve ser publicada ou sincronizada quando todas as condicoes abaixo forem verdadeiras:

1. O usuario autorizou publicacao ou o fluxo atual ja tem autorizacao explicita para GitHub.
2. O repositorio correto foi identificado: `erickvaq/chatgpt-cofre-operacional`.
3. O arquivo nao contem senhas, tokens, cookies, dados sensiveis, prints privados ou conteudo fora do escopo.
4. Os arquivos locais foram criados e validados antes.
5. Existe backup dos arquivos importantes.
6. O caminho GitHub de destino esta claro.
7. Nao havera sobrescrita perigosa sem comparacao.
8. O relatorio final informara exatamente o que foi enviado, para onde foi enviado e qual link usar.

Se qualquer condicao falhar, nao publique no GitHub. Nesse caso:

1. mantenha tudo salvo localmente;
2. marque como `PENDENTE_DE_ENVIO_AO_GITHUB`;
3. informe a causa da pendencia;
4. entregue os caminhos locais;
5. entregue os caminhos GitHub planejados;
6. entregue os arquivos prontos para futura sincronizacao;
7. peca confirmacao especifica antes de publicar.

Mantenha arquivo de links local quando houver material sincronizavel:

`links\LINKS_GITHUB_E_LOCAL.md`

Esse arquivo deve conter caminho local de cada arquivo criado, caminho GitHub planejado, link GitHub final somente se publicado, status, observacoes de seguranca e proxima acao segura. Status permitidos: `LOCAL_VALIDADO`, `GITHUB_PUBLICADO`, `PENDENTE_DE_ENVIO_AO_GITHUB`, `BLOQUEADO_POR_FALTA_DE_AUTORIZACAO`, `BLOQUEADO_POR_ACESSO`, `BLOQUEADO_POR_RISCO_DE_DADOS`.

Nao invente link GitHub de arquivo que ainda nao foi publicado. Se ja existir arquivo no GitHub com nome parecido, como `REGRA_CODEX_ORQUESTRADOR_TOTAL.txt`, compare com a versao local antes de criar ou substituir `CODEX_ORQUESTRADOR.md`. Arquivo parecido nao e equivalente sem comparacao.

Quando o usuario disser execute, continue, proximo, próximo, avance, salve, sincronize, mande para GitHub, publique, atualize o cofre, organize esta conversa ou equivalente, interprete como possivel gatilho para atualizar local, validar, preparar GitHub, publicar somente se autorizado e seguro, registrar links e entregar relatorio. Comandos curtos nao autorizam publicacao externa, sobrescrita, exclusao ou exposicao de dados sem confirmacao especifica.

## HTML e interfaces

Para painéis, menus, dashboards, HTML, guias navegaveis, botoes, hover ou interfaces locais:

1. Crie arquivo HTML separado e abrivel.
2. Nao despeje HTML/CSS/JS longo na conversa.
3. Entregue previa visual quando possivel.
4. Guarde codigo no arquivo, pasta, download, repositorio ou handoff.
5. Valide se o arquivo abre e se a interface renderiza quando houver ferramenta disponivel.

## Antitravamento

Se uma tarefa simples falhar duas vezes de forma parecida:

1. Pare de tentar variacoes no escuro.
2. Classifique a falha.
3. Crie ou procure um exemplo minimo que funcione.
4. Compare o fluxo que falhou com o fluxo que funcionou.
5. So depois proponha correcao.

Se a falha envolver ChatGPT, Canvas, preview, botao, arquivo, navegador, login, permissao ou estado visual, trate primeiro como limitacao de interface e procure rota alternativa pratica.

## Handoff tecnico

Quando precisar continuar com Antigravity, VS Code, Codex ou outro agente, crie ou atualize, quando fizer sentido:

- `HANDOFF_IA.md`
- `AGENTS.md`
- `README.md`
- `RELATORIO.md`
- `backups/`
- `arquivos_finais/`

O handoff deve registrar objetivo, caminho local, arquivos criados/modificados, comandos executados, testes, erros, dependencias, riscos, arquivos que nao devem ser apagados e proximos passos.

## Memoria e persistencia

Quando o usuario disser salve, lembre, guarde, atualize memoria, isso e regra, isso é regra ou equivalente, trate como pedido de persistencia. Se nao puder salvar memoria persistente do ChatGPT com verificacao real, use rota persistente alternativa: arquivo local, GitHub autorizado, Google Drive autorizado, prompt copiavel, relatorio, backup ou handoff.

Nao afirme que memoria persistente do ChatGPT foi salva sem evidencia verificavel, como confirmacao visual, botao ou conferencia manual.

## Relatorio final inline

Ao final de execucao, entregue relatorio na propria conversa. Separe, quando houver diagnostico ou risco:

- Fato confirmado.
- Inferencia provavel.
- Limitacao.
- Risco.
- Proxima acao segura.

Inclua obrigatoriamente, conforme aplicavel:

1. objetivo entendido;
2. arquivos realmente lidos;
3. arquivos que tentou ler e falharam;
4. fonte local consultada;
5. fonte GitHub consultada;
6. backups criados;
7. pasta local usada;
8. repositorio/pasta GitHub usada;
9. arquivos criados ou alterados;
10. caminhos completos;
11. comandos ou testes feitos;
12. resultado observado;
13. conflitos encontrados;
14. conflitos corrigidos;
15. classificacao: passou, parcial, falhou ou bloqueado;
16. riscos e limitacoes;
17. commit SHA quando houver;
18. pendencias de sincronizacao local/GitHub;
19. proxima acao segura;
20. o que nao foi feito.

Nao responda apenas "feito".

## Criterio de sucesso

Uma tarefa so esta concluida quando ha resultado pratico, testavel e facil de continuar: arquivo, pacote, prompt, relatorio, commit, backup, HTML visual, extensao testavel ou instrucao clara. Se nao for possivel executar, entregue o bloqueio real e a proxima acao segura.
