# Prompt para Antigravity - Chat Facil

Objetivo:
Criar a estrutura visual, mockups, documentacao e protocolo de backup da extensao Chat Facil no repositorio `erickvaq/chatgpt-cofre-operacional`.

## Caminhos obrigatorios

- `ferramentas/chat-facil/`
- `ferramentas/chat-facil/mockups/`
- `backups/extensoes/chat-facil/`
- `backups/extensoes/chat-facil/INDEX.md`

## Contexto

Chat Facil e uma extensao local de Chrome/Edge usada para acelerar fluxos dentro do ChatGPT: capturar mensagens, transferir texto entre abas/conversas, repetir capturas, auxiliar backups e reduzir copiar/colar manual.

## Tarefa

1. Abrir ou clonar o repositorio.
2. Preservar arquivos antigos, README, backups e versoes funcionais.
3. Criar mockups HTML/CSS simples em `ferramentas/chat-facil/mockups/`, representando:
   - popup principal;
   - selecao de origem/destino;
   - captura de ultimas mensagens;
   - envio para outra aba;
   - status/LED: amarelo = texto preparado, vermelho = enviado/processando, verde = resposta concluida/pronta;
   - area de log/historico;
   - aviso de que a extensao e opcional e depende do ambiente atual.
4. Atualizar:
   - `ferramentas/chat-facil/README.md`
   - `ferramentas/chat-facil/REGRA_CHAT_FACIL.md`
   - `ferramentas/chat-facil/FUNCOES_ATUALIZADAS.md`
   - `ferramentas/chat-facil/CHANGELOG.md`
   - `ferramentas/chat-facil/mockups/INDEX.md`
   - `backups/extensoes/chat-facil/INDEX.md`
5. Registrar que toda atualizacao futura da extensao deve gerar backup versionado em:
   `backups/extensoes/chat-facil/YYYY-MM-DD_HHhMM-BRT_vNN_resumo-curto/`
6. Nao alterar a extensao funcional se ela ja existir; criar mockups/documentacao separados.
7. Fazer `git status`, commit e push.
8. Entregar relatorio final com arquivos criados/modificados, funcoes documentadas, caminho do backup/documentacao, commit e status do push.

## Commit sugerido

`docs: adiciona estrutura e mockups da extensao Chat Facil`

