# GitHub Issue: HTML visual deve renderizar interface, nao gerar imagem estatica

## Resumo

Quando o usuario pede HTML visual, pagina HTML visual, painel, dashboard, guia navegavel, canvas, previa interativa ou interface local, a entrega esperada deve ser uma interface HTML renderizada/interativa. O sistema nao deve interpretar automaticamente a palavra "visual" como pedido de geracao de imagem estatica.

## Problema observado

Em testes recentes, pedidos de "pagina HTML visual" com "canvas/previa como entrega principal" acionaram geracao de imagem estatica. Isso e incorreto para esse tipo de pedido, porque o objetivo era ver a pagina HTML funcionando, com preview/canvas, arquivo abrivel ou botao para abrir em nova aba/tela cheia.

Em outro teste, quando o prompt foi reforcado com "ARQUIVO HTML" e "nao gere imagem estatica", o sistema criou HTML/canvas, mas abriu o codigo de forma muito visivel. Isso tambem nao e o ideal: o codigo pode existir, mas deve ficar secundario, recolhido, minimizado, encurtado, em dropdown, aba ou botao "Codigo".

## Comportamento esperado

- Se o pedido envolver HTML, pagina HTML, HTML visual, painel, dashboard, guia navegavel, canvas com HTML, previa interativa, interface local ou artefato funcional, a entrega principal deve ser HTML real/renderizado/interativo.
- "Visual" nesse contexto deve significar interface HTML renderizada/interativa, nao imagem gerada.
- A entrega ideal deve usar canvas/previa visual, pagina renderizada, arquivo HTML abrivel/baixavel, painel interativo ou botao/link para abrir em nova aba/tela cheia.
- Codigo HTML/CSS/JS pode aparecer apenas como secundario: recolhido, minimizado, encurtado, em dropdown, aba, botao "Codigo" ou quando o usuario pedir explicitamente.
- Geracao de imagem deve ser foco principal somente quando o usuario pedir explicitamente imagem, foto, ilustracao, arte, mockup estatico, miniatura estatica ou print anotado.
- Se o canvas abrir em modo codigo, isso deve ser tratado como problema de exibicao: orientar o botao "Previa", abrir em nova aba/tela cheia quando possivel ou entregar arquivo HTML abrivel.

## Regra proposta

Quando o usuario pedir HTML visual, pagina HTML, pagina visual renderizada, canvas com HTML, painel, dashboard, guia navegavel, previa interativa, interface local ou artefato funcional semelhante, interpretar "visual" como interface HTML renderizada/interativa, nao como imagem estatica gerada. Entregar como foco principal canvas/previa visual, pagina renderizada, arquivo HTML abrivel/baixavel, painel interativo ou botao/link para abrir em nova aba/tela cheia. Nao substituir pedido de HTML visual por imagem gerada. Geracao de imagem deve ser foco principal somente quando o usuario pedir explicitamente imagem, foto, ilustracao, arte, mockup estatico, miniatura estatica ou print anotado, ou como fallback declarado se a renderizacao HTML nao estiver disponivel. O canvas e correto quando mostra a pagina visual e nao deve ser evitado, removido, anulado ou substituido por codigo. Se HTML/CSS/JS/codigo aparecer por padrao, tratar como problema de exibicao: usar ou orientar o botao "Previa", abrir em nova aba/tela cheia quando possivel e nao repetir codigo bruto. Codigo pode aparecer minimizado, encurtado, recolhido em dropdown/aba/botao ou acessivel por "Codigo"; codigo aberto e longo so deve aparecer quando o usuario pedir explicitamente.

## Teste de reproducao

Use em uma conversa limpa:

```text
Crie uma pagina HTML visual simples para explicar como carregar uma extensao local no Chrome. Quero a interface HTML renderizada em canvas/previa como entrega principal, com botao ou link para abrir em nova aba/tela cheia se possivel. Nao gere imagem estatica. O codigo HTML pode ficar minimizado/recolhido em dropdown, aba ou botao, mas nao aberto como conteudo principal.
```

## Resultado esperado do teste

- HTML renderizado, preview/canvas ou arquivo HTML abrivel como entrega principal.
- Botao/link para abrir em nova aba/tela cheia quando a interface permitir.
- Codigo apenas recolhido/minimizado/dropdown/botao, nao dominando a resposta.
- Nenhuma imagem estatica gerada como substituto do HTML.

## Evidencias locais disponiveis

- `RELATORIO_TESTES_HTML_VISUAL.md`
- `PROMPT_CONSOLIDAR_REGRA_HTML_VISUAL.md`
- `PLANO_ACAO_VISUAL_HTML.md`
- `plano-visual-html.html`
- `chatgpt-visual-test-result.png`
- `chatgpt-visual-retest-result.png`
- `chatgpt-strong-html-test-result.png`

