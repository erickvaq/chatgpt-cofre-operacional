---
name: widepay-abertura-externa
description: Usar sempre que o pedido envolver abrir PDF, DOCX, HTML, HTA, imagem, planilha, pasta, painel, prévia ou arquivo final.
---
# Skill: widepay-abertura-externa

Esta skill garante que todos os arquivos de auditoria e relatórios gerados sejam abertos de forma limpa e nativa no Windows, eliminando renderização inadequada no chat do Antigravity.

## 1. Prioridade
**Alta.** Previne erros visuais de renderização de arquivos binários e de formatação HTML/PDF.

## 2. Quando usar
* Abertura de relatórios financeiros PDF, HTML, planilhas Excel ou documentos Word.
* Execução e exibição do painel local clicável HTA do cliente.
* Abertura de pastas no Windows Explorer (como a pasta de relatórios `02_RELATORIOS_GERADOS`).

## 3. Quando não usar
* Geração do conteúdo ou cálculos do relatório (usar `widepay-relatorio-pdf`).
* Consultas ou login no WidePay (usar `widepay-core-operacional`).

## 4. Gatilhos de ativação
Palavras-chave: `abrir PDF`, `abrir pasta`, `abrir painel`, `executar HTA`, `visualizar planilha`, `abrir previa`.

## 5. Fluxo obrigatório
1. **Lançador de Segurança:** Sempre invocar o script lançador `ABRIR_ARQUIVO_EXTERNO.bat` ou o script PowerShell correspondente.
2. **Evitar Links Diretos:** Nunca gerar links Markdown `file:///` diretos para arquivos `.pdf` no chat, pois forçam o Antigravity a renderizá-los em modo texto.
3. **Chamada de Sistema:** Utilizar o comando PowerShell `Start-Process` ou chamar diretamente no terminal para desvincular do terminal da IDE.
4. **HTML HTA:** Executar painéis HTA usando `mshta.exe` explicitamente.
5. **Explorer Nao Bloqueante:** Chamar `explorer.exe` no Windows Explorer de modo assíncrono para liberar o console.

## 6. Rotinas e scripts relacionados
* `c:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes\ABRIR_ARQUIVO_EXTERNO.bat`
* `00_SISTEMA_ABERTURA_EXTERNA\abrir_arquivo_externo.ps1`

## 7. Logs obrigatórios
Ao abrir um arquivo:
```text
SKILL CARREGADA: widepay-abertura-externa
EXECUÇÃO EXTERNA: comando de abertura disparado no Windows
VISUALIZADOR PADRÃO: arquivo carregado no aplicativo externo associado
```

## 8. Erros proibidos
* **ERRO 1:** Clicar ou induzir o usuário a clicar em caminhos de arquivos PDF dentro da IDE (causa abertura textual corrompida).
* **ERRO 2:** Bloquear o terminal do Antigravity com processos síncronos de visualização (ex: travar o console com o visualizador de PDF aberto).
* **ERRO 3:** Abrir arquivos locais confidenciais externamente fora do escopo do projeto ou sem a correspondência do cliente auditado.

## 9. Critérios de validação
* Verificação física de que o arquivo a ser aberto de fato existe no caminho especificado antes de invocar o lançador.

## 10. Precheck relacionado
* Validado em conjunto com o precheck de rotinas de abertura externa do projeto.

## 11. Exemplos curtos de decisão
* *Cenário:* O usuário quer ver a planilha de loteamento `Pre AGUA VIVA.xlsx`.
* *Decisão:* Executar `ABRIR_ARQUIVO_EXTERNO.bat "C:\Users\Windows User\Desktop\AGUA VIVA\- CONTRATOS AGUA VIVA\Pre AGUA VIVA.xlsx"` e informar o caminho local como texto puro.
* *Cenário:* O usuário solicita ver a prévia HTML da Camila Ferrolho.
* *Decisão:* Executar `Start-Process` para abrir no navegador padrão do Windows.
