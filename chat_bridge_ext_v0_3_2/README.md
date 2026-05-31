# ChatFÁCIL / Chat Bridge v0.3.2 - Workspace v0.3.2

Extensão local para Google Chrome (Manifest V3) que gerencia pontes operacionais e filas de estados para integração assistida entre o ChatGPT, Codex Desktop (aplicativo Windows) e Antigravity.

Esta versão implementa a arquitetura de **Roteamento de Fila de Estado Síncrono e Assistido** e adiciona suporte pleno ao **Modo Codex Desktop Assistido** sem depender de Codex CLI, Native Messaging ou automação visual invasiva nesta etapa.

---

## 1. Tipos de Destino Suportados

A extensão gerencia e suporta três categorias de destinos:
* **`WEB_TAB`**: Abas de navegação normais do Chrome (ChatGPT, Claude, Gemini, Antigravity) controladas de forma assíncrona por troca de mensagens (`chrome.tabs.sendMessage`).
* **`WINDOWS_APP_ASSISTED`**: Aplicativos desktop nativos e assistidos do Windows (Codex Desktop), sem associação com abas Chrome. A extensão gerencia a sincronização de estados de forma manual e segura via área de transferência e inputs assistidos.
* **`LOCAL_BRIDGE_FUTURE`**: Marcação técnica e documentação reservada para a próxima etapa (integração futura com Native Messaging Host, fila JSON local e execução automática via Script Host integrado).

---

## 2. O que há de novo na v0.3.2 (Modo Codex Desktop Assistido)

Quando o destino selecionado é o **Codex Desktop**:
* **Sem Controle de Aba Direto**: A extensão detecta o tipo de destino e desativa tentativas de mandar mensagens de controle via Chrome DOM ou `tabId`.
* **Cópia Inteligente p/ Área de Transferência**: O botão **Copiar para Codex** copia automaticamente o prompt selecionado ou o composer inteiro formatado com um clique.
* **Alerta Visual**: Exibição imediata de feedback visual instrutivo: *"Prompt copiado para o Codex. Cole manualmente no aplicativo Codex."*
* **Fila de Estados Críticos**: O fluxo de estados gerencia a integridade da operação bloqueando novos envios ou interrupções acidentais.
* **Modal Inteligente de Resposta (Shadow DOM)**: Um modal elegante com isolamento total (Shadow DOM) abre no navegador para que o usuário cole o resultado retornado pelo Codex Desktop.
* **Auditoria de Retorno no ChatGPT**: A resposta colada é enviada de volta ao ChatGPT com o cabeçalho estructurado:
  ```text
  ---
  [Auditoria Chat Bridge] Resposta recebida do Codex para auditoria
  Origem: Codex Desktop (WINDOWS_APP_ASSISTED)
  Horário: [Data e Hora do Usuário]

  [Conteúdo da Resposta]
  ---
  ```
  O estado então transita para `AGUARDANDO_AUDITORIA_CHATGPT` para que o usuário faça a revisão e aprovação final.

---

## 3. Estados de Fila de Auditoria Adicionados

Os novos estados garantem controle sequencial estrito e evitam a sobreposição de tarefas ativas na ponte:
* **`IDLE`**: Fila livre para novas capturas ou envios.
* **`COPIADO_PARA_CODEX`**: Prompt capturado do ChatGPT e copiado com sucesso para a área de transferência.
* **`AGUARDANDO_COLAGEM_MANUAL`**: Estado intermediário assistido onde o prompt está sendo colado no Codex Desktop.
* **`AGUARDANDO_RESPOSTA_CODEX`**: Codex Desktop processando a instrução, aguardando que o usuário traga o resultado.
* **`RESPOSTA_CODEX_COLADA`**: Resposta colada com sucesso no Modal da extensão, pronta para retornar à aba Fonte.
* **`AGUARDANDO_AUDITORIA_CHATGPT`**: Resposta colada no composer do ChatGPT, aguardando revisão final humana antes do envio.

---

## 4. Botões no Painel Flutuante (ChatGPT)

O painel de Shadow DOM no ChatGPT apresenta um painel segregado para o **Codex Desktop**:
* 📋 **Copiar para Codex ➔**: Copia o prompt formatado e cria o payload ativo.
* ✓ **Marcar como colado**: Transiciona a fila para aguardar o processamento.
* 📥 **Colar resposta**: Abre a caixa de diálogo modal isolada para colar a resposta do Codex.
* 🚀 **Enviar p/ Auditoria ChatGPT**: Insere o bloco formatado de auditoria no ChatGPT.
* 🗑️ **Limpar fila Codex**: Apaga o payload e libera a fila (exige confirmação visual).

---

## 5. Arquivos e Estrutura

* `background.js`: Gerenciador de inicialização do storage e listener de abas fechadas. Tratamento seguro para `WINDOWS_APP_ASSISTED` para que o fechamento de outras abas não invalide o payload ativo do Codex.
* `content.js`: Menu flutuante dinâmico injetado em Shadow DOM no ChatGPT, com estilos modernos de glassmorphism, suporte completo a modal inteligente de resposta e botões de fluxo de auditoria.
* `popup.js` / `popup.html` / `popup.css`: Interface de controle popup da extensão atualizada para refletir visualmente os novos estados da fila e reatividade dos leds.

---

## 6. Como Testar Localmente

1. Abra `chrome://extensions/`.
2. Habilite o **Modo do desenvolvedor**.
3. Clique em **Carregar sem compactação**.
4. Selecione a pasta deste workspace:
   `C:\Users\Windows User\Desktop\chatgpt projetos\CHAT_BRIDGE_CODEX_ANTIGRAVITY\WORKSPACE_CHATBRIDGE_V0_3_2\chat_bridge_ext_v0_3_2`
5. Acesse o ChatGPT no Chrome e use o painel flutuante de controle na lateral direita para conduzir a auditoria assistida do Codex Desktop.
