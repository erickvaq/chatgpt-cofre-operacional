# Prompt para Antigravity - v0.3.2

Cole este texto no Antigravity para iniciar a evolucao v0.3.2.

Trabalhe somente nesta pasta:

`C:\Users\Windows User\Desktop\chatgpt projetos\CHAT_BRIDGE_CODEX_ANTIGRAVITY\WORKSPACE_CHATBRIDGE_V0_3_2\chat_bridge_ext_v0_3_2`

Nao mexa na pasta ativa do Chrome:

`C:\Users\Windows User\Documents\Chrome_Extensoes\ChatBridge`

Nao apague `v0.2.5`, backups ou prototipos. Use `v0.3.1` como base principal. Nao use GitHub automatico. Nao use codigo remoto executavel. Nao refaca do zero.

Objetivo:

Construir a v0.3.2 como ponte operacional entre ChatGPT, Codex e Antigravity, corrigindo o problema atual de copiar e colar na propria janela errada e organizando o fluxo interno:

`Fonte -> Fila -> Destino -> Status -> Resposta -> Auditoria`

MVP inicial:

1. Painel flutuante organizado.
2. Selecao explicita de origem e destino.
3. Botões separados para Codex e Antigravity.
4. Estado global em `chrome.storage`.
5. Bloqueio de envio duplicado.
6. Um payload ativo por vez.
7. Captura manual ou assistida de resposta.
8. Botao para copiar resposta de volta ao ChatGPT.
9. Sem envio destrutivo automatico.
10. Sem GitHub automatico.

Regras:

- Manifest V3.
- Permissoes minimas.
- Message passing.
- CSS isolado para o painel.
- Registrar origem, destino, horario, tipo e status.
- Nao colar na janela errada.
- Nao enviar resposta ao destino errado.
- Nao publicar, sobrescrever ou excluir sem confirmacao.

Ao final, entregue:

- arquivos alterados;
- resumo do fluxo implementado;
- riscos;
- testes feitos;
- o que ficou pendente.

# Prompt para colar no Antigravity
