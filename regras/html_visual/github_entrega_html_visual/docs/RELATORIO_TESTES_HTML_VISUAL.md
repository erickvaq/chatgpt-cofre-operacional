# Relatorio dos testes HTML visual / canvas / imagem

Data: 2026-05-30

## Status geral

O fluxo de testes confirmou que existe conflito ou roteamento incorreto entre pedidos de HTML visual e geracao de imagem. Quando o pedido dizia "pagina HTML visual" e "canvas/previa", o ChatGPT gerou imagem estatica em vez de entregar HTML renderizado/interativo. Quando o pedido foi mais forte e disse explicitamente "ARQUIVO HTML", "nao gere imagem estatica" e "nao use gerador de imagem", ele criou HTML/canvas, mas abriu o codigo no canvas como conteudo visivel.

O print enviado pelo usuario tambem confirmou outro bloqueio operacional: o ChatGPT exibiu "Excesso de solicitacoes", limitando temporariamente o acesso as conversas. Portanto, novos testes no navegador devem esperar alguns minutos.

## Confirmado

- O cartao/botao "Memoria atualizada" apareceu em atualizacoes anteriores.
- A regra visual original foi consolidada com sucesso antes do bloqueio.
- O teste simples depois da consolidacao ainda gerou imagem estatica.
- O refinamento anti-imagem foi aplicado e tambem mostrou "Memoria atualizada".
- O reteste sem dica extra continuou gerando "Imagem gerada".
- O teste forte, com "ARQUIVO HTML" e "nao gere imagem estatica", criou HTML/canvas, mas exibiu codigo aberto no painel.
- O navegador/ChatGPT entrou em bloqueio temporario por excesso de solicitacoes.

## Evidencias locais

- Confirmacao da memoria refinada: `chatgpt-memory-refined-response.png`
- Primeiro teste gerando imagem: `chatgpt-visual-test-result.png`
- Reteste gerando imagem novamente: `chatgpt-visual-retest-result.png`
- Teste forte criando HTML/canvas, mas com codigo aberto: `chatgpt-strong-html-test-result.png`
- Refinamento anti-imagem confirmado: `chatgpt-html-refine-confirmation.png`
- Plano visual local: `plano-visual-html.html`
- Plano em Markdown: `PLANO_ACAO_VISUAL_HTML.md`
- Prompt final pronto: `PROMPT_CONSOLIDAR_REGRA_HTML_VISUAL.md`

## Diagnostico

Ha duas regras/rotas provaveis em conflito:

1. Rota de imagem: palavras como "visual", "guia visual", "pagina visual" e "previa" podem estar acionando geracao de imagem.
2. Rota de HTML/canvas: palavras como "arquivo HTML" puxam artefato/canvas, mas podem abrir primeiro em modo codigo.

O comportamento desejado fica no meio:

- Para HTML visual, "visual" deve significar interface HTML renderizada/interativa.
- A entrega principal deve ser preview/canvas/pagina renderizada/arquivo HTML abrivel.
- Imagem gerada so deve ser usada quando o usuario pedir imagem, arte, mockup estatico, print anotado ou quando for fallback declarado.
- Codigo pode existir, mas deve ficar minimizado, recolhido, encurtado, em dropdown/aba/botao, ou acessivel por "Codigo".

## Regra final recomendada

Quando o usuario pedir HTML visual, pagina HTML, pagina visual renderizada, canvas com HTML, painel, dashboard, guia navegavel, previa interativa, interface local ou artefato funcional semelhante, interpretar "visual" como interface HTML renderizada/interativa, nao como imagem estatica gerada. Entregar como foco principal canvas/previa visual, pagina renderizada, arquivo HTML abrivel/baixavel, painel interativo ou botao/link para abrir em nova aba/tela cheia. Nao substituir pedido de HTML visual por imagem gerada. Geracao de imagem deve ser foco principal somente quando o usuario pedir explicitamente imagem, foto, ilustracao, arte, mockup estatico, miniatura estatica ou print anotado, ou como fallback declarado se a renderizacao HTML nao estiver disponivel. O canvas e correto quando mostra a pagina visual e nao deve ser evitado, removido, anulado ou substituido por codigo. Se HTML/CSS/JS/codigo aparecer por padrao, tratar como problema de exibicao: usar ou orientar o botao "Previa", abrir em nova aba/tela cheia quando possivel e nao repetir codigo bruto. Codigo pode aparecer minimizado, encurtado, recolhido em dropdown/aba/botao ou acessivel por "Codigo"; codigo aberto e longo so deve aparecer quando o usuario pedir explicitamente.

## Teste recomendado quando o bloqueio passar

Use primeiro este teste, sem acrescentar outras instrucoes:

```text
Crie uma pagina HTML visual simples para explicar como carregar uma extensao local no Chrome. Quero a interface HTML renderizada em canvas/previa como entrega principal, com botao ou link para abrir em nova aba/tela cheia se possivel. Nao gere imagem estatica. O codigo HTML pode ficar minimizado/recolhido em dropdown, aba ou botao, mas nao aberto como conteudo principal.
```

Resultado esperado:

- HTML/renderizacao/canvas/preview primeiro.
- Botao/link para abrir em nova aba ou tela cheia, se a interface permitir.
- Codigo recolhido/minimizado se aparecer.
- Sem imagem estatica gerada como entrega principal.

## Proxima acao

Esperar o cooldown do ChatGPT. Depois abrir conversa limpa e aplicar o prompt em `PROMPT_CONSOLIDAR_REGRA_HTML_VISUAL.md`, caso a ultima tentativa nao tenha sido confirmada. Em seguida rodar o teste recomendado acima.

Nao tentar mais agora enquanto aparece "Excesso de solicitacoes".

