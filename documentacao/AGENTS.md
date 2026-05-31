# AGENTS.md - Chat Bridge / ChatFacil v0.3.2

## Atualizacao de prioridade

Estas instrucoes valem como referencia atual para o passo 3 da evolucao v0.3.2. O conteudo historico abaixo permanece apenas como trilha.

## Regras atuais

- Nao mexer na pasta ativa do Chrome: `C:\Users\Windows User\Documents\Chrome_Extensoes\ChatBridge`
- Nao alterar a v0.2.5 funcional de seguranca.
- Usar a v0.3.1 como base principal.
- Programar apenas no workspace separado `WORKSPACE_CHATBRIDGE_V0_3_2`.
- Nao apagar backups, prototipos ou instaladores.
- Nao publicar no GitHub nem fazer commit neste passo.
- Nao usar codigo remoto executavel.
- Manter Manifest V3 e permissoes minimas.
- Atualizar `HANDOFF_IA.md`, `ESTADO_ARQUIVOS.md` e `RELATORIO_ANTIGRAVITY_V0_3_2.md` ao final do passo.
- **REGRA CRITICA — RAIZ CARREGAVEL**: A raiz carregavel da extensao Chrome (`chat_bridge_ext_v0_3_2/`) deve conter APENAS os arquivos usados diretamente pela extensao: `manifest.json`, `background.js`, `content.js`, `popup.html`, `popup.js`, `popup.css`, icones e `README.md`. Backups, relatorios, logs, arquivos `.bak`, handoffs, pastas temporarias e pastas iniciadas por `_` devem ficar FORA da raiz carregavel, em `backups/` na raiz do projeto. Antes de pedir teste no Chrome, validar a arvore da extensao com `Get-ChildItem` e confirmar ausencia de itens invalidos.

## Estrutura atual

- Pasta ativa do Chrome: `C:\Users\Windows User\Documents\Chrome_Extensoes\ChatBridge`
- Base v0.3.1: `C:\Users\Windows User\Desktop\chatgpt projetos\CHAT_BRIDGE_CODEX_ANTIGRAVITY\chat_bridge_ext_v0_3_1_instalador\chat_bridge_ext_v0_3_1`
- Workspace v0.3.2: `C:\Users\Windows User\Desktop\chatgpt projetos\CHAT_BRIDGE_CODEX_ANTIGRAVITY\WORKSPACE_CHATBRIDGE_V0_3_2\chat_bridge_ext_v0_3_2`
- Backup funcional: `C:\Users\Windows User\Desktop\chatgpt projetos\CHAT_BRIDGE_CODEX_ANTIGRAVITY\BACKUP_ESTADO_FUNCIONAL`
- Backup do prototipo: `C:\Users\Windows User\Desktop\chatgpt projetos\CHAT_BRIDGE_CODEX_ANTIGRAVITY\BACKUP_PROTOTIPO_ATUAL`

## Foco para a proxima programacao

- Roteador Fonte -> Fila -> Destino -> Status -> Resposta -> Auditoria.
- Seleção explicita de origem e destino.
- Bloqueio de envio duplicado e de novo envio durante execucao.
- Captura de resposta e retorno ao ChatGPT para auditoria.
- Sem envio automatico destrutivo.

# AGENTS.md - Chat Bridge

## Visao geral

Projeto local de extensao Chrome chamada Chat Bridge. O objetivo e enviar texto, mensagens recentes e prints entre conversas abertas do ChatGPT. Nao usar GitHub neste fluxo.

## Estrutura principal

- `chat_bridge_ext_v0_2_5_instalador/`: ultima versao funcional empacotada.
- `chat_bridge_ext_v0_3_0_instalador/`: prototipo atual em edicao.
- `C:\Users\Windows User\Documents\Chrome_Extensoes\ChatBridge`: pasta fixa carregada no Chrome, atualmente v0.2.5.
- `BACKUP_ESTADO_FUNCIONAL/`: copia da v0.2.5 funcional.
- `BACKUP_PROTOTIPO_ATUAL/`: copia do prototipo v0.3.0 no estado atual.

## Comandos uteis

Checar JS:

```powershell
node --check .\chat_bridge_ext_v0_3_0_instalador\chat_bridge_ext_v0_3_0\background.js
node --check .\chat_bridge_ext_v0_3_0_instalador\chat_bridge_ext_v0_3_0\content.js
node --check .\chat_bridge_ext_v0_3_0_instalador\chat_bridge_ext_v0_3_0\popup.js
```

Preparar pasta fixa da versao funcional:

```powershell
cmd /c ".\chat_bridge_ext_v0_2_5_instalador\INSTALAR_CHAT_BRIDGE.bat" --prepare-only
```

Instalacao manual no Chrome:

1. Abrir `chrome://extensions/`.
2. Ativar `Modo do desenvolvedor`.
3. Clicar `Carregar sem compactacao`.
4. Selecionar `C:\Users\Windows User\Documents\Chrome_Extensoes\ChatBridge`.

## Convencoes importantes

- Preservar a v0.2.5 funcional.
- Trabalhar a v0.3.0 no pacote separado antes de copiar para a pasta fixa.
- Popup e prioridade da v0.3.0.
- O botao `Enviar mensagem` deve ser explicito; nao enviar automaticamente ao apenas colar/anexar.
- PDF/DOCX ficam para fase futura.

## Regras de seguranca

- Nao apagar backups.
- Nao substituir a pasta fixa do Chrome com prototipo nao testado.
- Nao refazer do zero.
- Nao usar GitHub.
- Nao usar `git reset`, `git checkout --` ou comandos destrutivos.
- Antes de copiar v0.3.0 para a pasta fixa, testar e confirmar.

## Instrucao para continuar

Leia primeiro `HANDOFF_IA.md` e `ESTADO_ARQUIVOS.md`. Continue a partir de `chat_bridge_ext_v0_3_0_instalador`, mantendo `BACKUP_ESTADO_FUNCIONAL` intacto.
