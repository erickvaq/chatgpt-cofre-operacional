# PROMPT — CODEX: ponte para Antigravity / Chat Fácil

## Contexto correto
A conversa `AUTOCHAT e Regras V8` é uma conversa dentro do Codex. Ela será usada como central operacional do Codex para dois tipos de trabalho:

1. Regras, memórias, salvamento seguro, backups e GitHub.
2. Orquestração da evolução da extensão Chat Fácil usando o Antigravity como ambiente principal de programação.

O Antigravity será usado para programar porque o usuário tem mais capacidade/tokens na conta Google/Gemini. O Codex deve atuar como ponte/orquestrador: preparar instruções, ler arquivos no GitHub, chamar/preparar o Antigravity quando possível, receber resultados, subir arquivos ao GitHub e devolver links para o ChatGPT analisar.

## Objetivo desta etapa
Preparar e executar a comunicação Codex → Antigravity para a etapa `Chat Fácil`, sem jogar trabalho manual desnecessário para o usuário.

## Entrada principal
Leia primeiro o prompt já salvo no GitHub:

`prompts/prompt_03_antigravity_chatfacil_mockups_backup.txt`

Esse prompt define a estrutura, mockups, documentação e protocolo de backup da extensão Chat Fácil.

## Regras obrigatórias

1. Antes de agir, declarar qual trilho está ativo: `Chat Fácil / Antigravity`.
2. Não alterar regras/memórias persistentes nesta etapa, salvo instrução explícita.
3. Não confundir `AUTOCHAT e Regras V8` com uma conversa comum do ChatGPT; ela é a central operacional dentro do Codex.
4. Usar o Antigravity para programação, mockups, documentação técnica e evolução da extensão.
5. Usar GitHub como ponte/cofre: todo arquivo importante deve ser enviado para `erickvaq/chatgpt-cofre-operacional`.
6. Não entregar apenas texto no chat se houver arquivos criados; criar arquivos reais e links GitHub quando possível.
7. Não apagar arquivos antigos, backups, README ou versões funcionais.
8. Se não conseguir controlar/abrir o Antigravity, preparar pacote local ou prompt pronto, explicar o bloqueio exato e devolver próximo passo objetivo.
9. Se conseguir executar, criar/atualizar a estrutura exigida:
   - `ferramentas/chat-facil/`
   - `ferramentas/chat-facil/mockups/`
   - `backups/extensoes/chat-facil/`
   - `backups/extensoes/chat-facil/INDEX.md`
10. Fazer commit/push quando autenticado.

## Entrega esperada
Ao final, entregar relatório com:

- trilho executado;
- arquivos criados/modificados;
- caminhos locais;
- links GitHub;
- commit;
- status do push;
- bloqueios reais, se houver;
- pendências;
- próximo passo único.

## Critério de sucesso
O ChatGPT deve conseguir abrir os links GitHub devolvidos, revisar os mockups/documentação da extensão Chat Fácil e orientar a próxima etapa sem o usuário precisar copiar manualmente prompts entre Codex e Antigravity.