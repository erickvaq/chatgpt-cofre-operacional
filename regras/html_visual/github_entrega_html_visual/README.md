# Entrega GitHub: HTML visual, canvas, previa e memoria

## Objetivo

Registrar e organizar o diagnostico do problema em que pedidos de HTML visual passaram a ser tratados como geracao de imagem estatica ou como codigo aberto, em vez de entregar uma interface HTML renderizada/interativa.

## Estrutura

```text
github_entrega_html_visual/
├─ README.md
├─ MENSAGEM_PARA_GITHUB_OU_IA.md
├─ docs/
│  ├─ RELATORIO_TESTES_HTML_VISUAL.md
│  └─ PLANO_ACAO_VISUAL_HTML.md
├─ prompts/
│  └─ PROMPT_CONSOLIDAR_REGRA_HTML_VISUAL.md
├─ html/
│  └─ plano-visual-html.html
├─ issues/
│  └─ GITHUB_ISSUE_HTML_VISUAL_CANVAS.md
└─ evidencias/
   ├─ chatgpt-memory-refined-response.png
   ├─ chatgpt-html-refine-confirmation.png
   ├─ chatgpt-visual-test-result.png
   ├─ chatgpt-visual-retest-result.png
   └─ chatgpt-strong-html-test-result.png
```

## Leitura recomendada

1. Leia `docs/RELATORIO_TESTES_HTML_VISUAL.md` para entender o que foi testado e o resultado.
2. Leia `prompts/PROMPT_CONSOLIDAR_REGRA_HTML_VISUAL.md` para aplicar a regra final em conversa limpa do ChatGPT.
3. Leia `issues/GITHUB_ISSUE_HTML_VISUAL_CANVAS.md` se quiser abrir uma issue ou tarefa no GitHub.
4. Abra `html/plano-visual-html.html` para ver o painel local visual do plano.
5. Confira `evidencias/` para prints dos testes.

## Conclusao curta

Para pedidos de HTML visual, "visual" deve significar interface HTML renderizada/interativa, nao imagem gerada. A entrega principal deve ser canvas/previa, pagina renderizada, arquivo HTML abrivel, painel interativo ou botao para abrir em nova aba/tela cheia. Codigo pode ficar recolhido/minimizado/dropdown, mas nao deve dominar a resposta. Imagem gerada so deve ser usada quando o usuario pedir imagem ou como fallback declarado.

