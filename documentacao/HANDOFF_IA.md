# HANDOFF IA - ChatFácil / Chat Bridge v0.3.2

## ⚠️ REGRA CRÍTICA — RAIZ CARREGÁVEL DA EXTENSÃO

> A pasta `chat_bridge_ext_v0_3_2/` é a raiz carregável no Chrome. Ela deve conter **somente** os arquivos da extensão:
> `manifest.json`, `background.js`, `content.js`, `popup.html`, `popup.js`, `popup.css`, ícones e `README.md`.
>
> **Proibido dentro da raiz:** pastas com `_`, arquivos `.bak`, relatórios, handoffs, logs, planejamentos.
>
> **Destino correto para backups:** `CHAT_BRIDGE_CODEX_ANTIGRAVITY\backups\`
>
> **Antes de pedir teste no Chrome:** rodar `Get-ChildItem` na raiz e confirmar zero itens inválidos.

---

## Passo 5 — Reorganização do Fluxo Principal (31/05/2026)

### O que foi feito

#### P0 — Filtro ChatGPT no dropdown
- O botão "+ Adicionar" agora lista **apenas abas com URL** `chatgpt.com` ou `chat.openai.com`.
- WhatsApp, YouTube, Google, outros sites: não aparecem mais.
- Se não houver aba ChatGPT aberta, uma mensagem orienta o usuário.
- A função `isChatGptUrl()` filtra antes de renderizar o dropdown.

#### P1 — Grupo verde [Colar | Enviar | Auto]
- **Colar no destino** (`pasteToDestBtn`): captura últimas N mensagens da fonte e cola no campo do destino, **sem enviar**. O usuário pode revisar antes.
- **Enviar** (`submitDestination`): aciona o botão de envio no destino (o que já estava no campo).
- **Auto** (`autoSendBtn`): colar + enviar no destino automaticamente.

#### P2 — Grupo azul [Trazer | Enviar | Auto]
- **Trazer resposta** (`pullDestinationResponse`): captura resposta do destino e cola na aba ativa (fonte).
- **Enviar** (`submitSourceBtn`): aciona envio na aba ativa/fonte.
- **Auto Retorno** (`autoReturnBtn`): traz + cola + envia na fonte automaticamente.
- Identidade visual azul (`btn-blue`, `btn-blue-dark`, `btn-blue-auto`).

#### P3 — Padrão "últimas mensagens" = 1
- O input `recentCount` inicia em `1` (era `3`).
- Persiste no storage e pode ser alterado pelo usuário.

#### P4 — Atalhos de teclado sob cada botão
- 6 caixinhas `.sc-input` abaixo dos dois grupos de 3 botões.
- Clique na caixinha → modo captura ("▶ tecle...").
- Apertar tecla ou combo → atalho salvo automaticamente, sem botão "Salvar".
- Atalhos persistem no `chrome.storage.local` (chave `shortcuts`).
- Ao pressionar o atalho globalmente (fora das caixinhas), a função correspondente é executada.
- Conflito de atalho detectado e avisado.

#### P5 — Botão "Manter no topo"
- Botão `📌 Topo` no cabeçalho.
- Em modo popup normal: exibe aviso explicando que precisa da janela fixa (botão ⧉ Fixar) e lista alternativas (PowerToys, Native Messaging).
- Na janela fixa (`?mode=window`): usa `chrome.windows.update({ alwaysOnTop: true })` — funciona se a API suportar para o tipo de janela atual. Em caso de falha, exibe aviso detalhado.
- Estado visual alterna entre `📌 Topo: on` (âmbar) e `📌 Topo` (neutro).
- Estado persiste no storage.

#### P6 — Preservado
- Capturar print e enviar: ✅
- Itens capturados (seção expandível): ✅
- Limpar tudo: ✅
- Redimensionar / minimizar / maximizar janela: ✅
- Janela separada via botão ⧉ Fixar: ✅
- Modo assistido Codex/Antigravity: ✅
- LEDs de estado e fila: ✅

### Arquivos alterados (somente workspace v0.3.2)
- `popup.html` — reescrito
- `popup.js` — reescrito
- `popup.css` — reescrito

### Arquivos não alterados
- `background.js` — PASSOU no `node --check`
- `content.js` — PASSOU no `node --check`
- `manifest.json` — inalterado
- `README.md` — inalterado

### Backups criados
- `backups\pre_p0_p5_2026-05-31_01-27-26\` — .bak dos 3 arquivos alterados

### Proteções confirmadas
- Pasta ativa do Chrome: **intocada** (28/05/2026)
- Base v0.3.1: **intocada** (29/05/2026)
- GitHub / commit / ZIP / cópia para ativa: **nenhum**

---

## Avaliação técnica — "Manter no topo"

### O que foi implementado
Botão visual com alternância de estado. Na janela fixa, tenta `chrome.windows.update({ alwaysOnTop })`.

### Limitações conhecidas
| Método | Status |
|---|---|
| `chrome.windows.update` no popup padrão | ❌ Não suportado (popup fecha ao clicar fora) |
| `chrome.windows.update` na janela fixa (`?mode=window`) | ⚠️ Depende do OS e versão do Chrome |
| PowerToys "Always on Top" (Win+Ctrl+T) | ✅ Externo, não depende da extensão |
| Native Messaging Host | ✅ Possível, mas requer .exe local registrado |
| App auxiliar Electron | ✅ Possível, mas fora do escopo desta fase |

### Recomendação prática
Usar a janela fixa (⧉ Fixar) e pressionar **Win+Ctrl+T** com PowerToys instalado. É o caminho mais simples sem infraestrutura adicional.

---

## Passo 6 — Sincronização Segura com GitHub e Regras Operacionais (31/05/2026)

### O que foi feito
- **Configuração Git Local:** O diretório local `CHAT_BRIDGE_CODEX_ANTIGRAVITY` foi inicializado e associado ao repositório remoto `https://github.com/erickvaq/chatgpt-cofre-operacional.git`.
- **Restauração de Arquivos Remotos:** Os arquivos e diretórios originais do repositório remoto foram baixados e restaurados no diretório local, garantindo zero perda de histórico e sem conflitos de mesclagem.
- **Estruturação Organizada:**
  - `chat_bridge_ext_v0_3_2/` na raiz do repositório contendo apenas os arquivos limpos e aprovados da extensão.
  - `documentacao/` contendo relatórios, planos e histórico de handoffs.
  - `regras/REGRAS_IA_SINCRONIZACAO.md` definindo as diretrizes operacionais de segurança permanentes para IAs.
- **Configuração de Segurança:** Criado um `.gitignore` robusto na raiz que impede o vazamento de chaves, credenciais, backups locais, ZIPs e pastas temporárias.
- **Validação de Sintaxe:** Verificado com `node --check` e todos os arquivos JavaScript passaram com sucesso.

---

## Próxima ação segura

1. Confirmar a sincronização dos arquivos no GitHub através de `git push origin main`.
2. Continuar a validação operacional e testes manuais da extensão no ambiente Chrome carregado sem compactação.
