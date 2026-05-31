# Plano Tecnico ChatFacil v0.3.2

## Objetivo

Transformar a extensao em uma ponte operacional entre ChatGPT, Codex e Antigravity, com roteamento claro de origem, fila, destino, resposta e auditoria.

## Base

- A base de desenvolvimento e a `v0.3.1`.
- A versao funcional de seguranca e a `v0.2.5`.
- A pasta ativa do Chrome continua como backup funcional e nao deve ser mexida neste passo.

## Fluxo principal

`Fonte -> Fila -> Destino -> Status -> Resposta -> Auditoria`

## Papéis

- ChatGPT: fonte principal, preparo de prompts, auditoria e decisao final.
- ChatFácil / Chat Bridge: ponte visual, menu flutuante, fila, status e roteador.
- Codex: executor local para arquivos, backups, GitHub, relatorios e validacoes.
- Antigravity: executor de programacao, ajustes de interface, testes e evolucao da extensao.

## MVP funcional

1. Painel flutuante organizado.
2. Seleção explicita de origem e destino.
3. Botões separados para Codex e Antigravity.
4. Estado global em `chrome.storage`.
5. Bloqueio de envio duplicado.
6. Um payload ativo por vez.
7. Captura manual ou assistida de resposta.
8. Botao para copiar resposta de volta ao ChatGPT.
9. Sem envio destrutivo automatico.
10. Sem GitHub automatico.

## Estados visuais

- `livre`
- `preparado`
- `enviado`
- `executando`
- `resposta capturada`
- `aguardando auditoria`
- `auditado`
- `bloqueado`
- `erro`

## Regras de roteamento

- Nao colar texto na propria janela errada.
- Nao enviar resposta ao destino errado.
- Nao aceitar novo comando enquanto existir payload ativo.
- Registrar origem, destino, horario, tipo de conteudo e status.
- Bloquear envio duplicado.

## Requisitos tecnicos

- Manifest V3.
- `chrome.storage` para estado.
- `chrome.runtime` messaging para troca entre partes.
- CSS isolado para o painel flutuante.
- Permissoes minimas.
- Sem codigo remoto executavel.

## Estrutura sugerida

- `manifest.json`
- `background.js`
- `content.js`
- `popup.html`
- `popup.js`
- `popup.css`
- `README.md`

## Riscos

- Misturar origem e destino dentro da propria aba.
- Permitir dois payloads simultaneos.
- Converter resposta em envio automatico sem auditoria.
- Tentar substituir a pasta ativa antes da validacao.

## Critério de aceite do MVP

- O usuario escolhe fonte e destino.
- O sistema envia um único payload por vez.
- O sistema bloqueia duplicidade.
- O sistema consegue capturar uma resposta e devolver para auditoria.
- Nenhum arquivo da pasta ativa foi alterado durante a preparacao.
