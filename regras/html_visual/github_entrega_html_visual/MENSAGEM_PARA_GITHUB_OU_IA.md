# Mensagem para GitHub ou outra IA

Use esta mensagem para abrir uma issue, criar uma tarefa no GitHub ou orientar outro agente/IA que vai continuar o trabalho.

```text
Preciso que você continue este trabalho a partir do pacote organizado em pastas.

Contexto:
Estamos corrigindo uma regra/memória de comportamento para pedidos de HTML visual no ChatGPT. O problema detectado foi que pedidos como "crie uma página HTML visual", "quero prévia/canvas", "painel", "dashboard", "guia navegável" ou "interface local" às vezes acionam geração de imagem estática ou exibem código HTML aberto, em vez de entregar uma interface HTML renderizada/interativa.

Objetivo correto:
Quando o pedido envolver HTML visual, página HTML, painel, dashboard, guia navegável, canvas com HTML, prévia interativa ou interface local, "visual" deve significar interface HTML renderizada/interativa. A entrega principal deve ser canvas/prévia, página renderizada, arquivo HTML abrível/baixável, painel interativo ou botão/link para abrir em nova aba/tela cheia.

Não confundir:
- HTML visual não é imagem gerada.
- Canvas não é problema quando mostra a página renderizada.
- Código bruto não deve dominar a resposta.
- Código pode aparecer minimizado, encurtado, recolhido em dropdown/aba/botão ou acessível por "Código".
- Imagem gerada só deve ser foco principal quando o usuário pedir imagem, foto, ilustração, arte, mockup estático, miniatura estática ou print anotado.

Arquivos do pacote:
- docs/RELATORIO_TESTES_HTML_VISUAL.md: relatório completo dos testes e falhas.
- docs/PLANO_ACAO_VISUAL_HTML.md: plano de ação e regra aprimorada.
- prompts/PROMPT_CONSOLIDAR_REGRA_HTML_VISUAL.md: prompt final para aplicar em conversa limpa do ChatGPT.
- html/plano-visual-html.html: painel visual local do plano.
- issues/GITHUB_ISSUE_HTML_VISUAL_CANVAS.md: texto pronto para issue/tarefa no GitHub.
- evidencias/: prints dos testes e confirmações.

O que já foi feito:
1. A memória visual foi atualizada/consolidada em testes anteriores.
2. O botão/cartão "Memória atualizada" apareceu.
3. Foi testado um pedido de página HTML visual.
4. O ChatGPT gerou imagem estática quando deveria entregar HTML renderizado.
5. Foi testado um prompt mais forte pedindo arquivo HTML e proibindo imagem estática.
6. Nesse teste, ele criou HTML/canvas, mas exibiu código aberto demais.
7. Foi criado um refinamento final: HTML visual deve priorizar interface renderizada/interativa; imagem só quando explicitamente pedida; código pode ficar recolhido/minimizado.
8. O ChatGPT entrou temporariamente em "Excesso de solicitações", então novos testes devem aguardar cooldown.

O que você deve fazer agora:
1. Subir ou organizar este pacote no GitHub mantendo a estrutura de pastas.
2. Ler primeiro docs/RELATORIO_TESTES_HTML_VISUAL.md.
3. Usar prompts/PROMPT_CONSOLIDAR_REGRA_HTML_VISUAL.md em conversa limpa do ChatGPT quando o acesso voltar.
4. Confirmar se aparece o cartão/botão "Memória atualizada".
5. Testar com a frase final abaixo.
6. Registrar o resultado: passou, falhou por imagem, falhou por código aberto, falhou por não entregar prévia/canvas, ou falhou por resposta textual demais.

Teste final recomendado:
Crie uma página HTML visual simples para explicar como carregar uma extensão local no Chrome. Quero a interface HTML renderizada em canvas/prévia como entrega principal, com botão ou link para abrir em nova aba/tela cheia se possível. Não gere imagem estática. O código HTML pode ficar minimizado/recolhido em dropdown, aba ou botão, mas não aberto como conteúdo principal.

Resultado esperado:
- HTML renderizado, canvas/prévia ou arquivo HTML abrível como entrega principal.
- Botão/link para abrir em nova aba/tela cheia quando possível.
- Código recolhido/minimizado/dropdown se aparecer.
- Nenhuma imagem estática gerada como substituto do HTML.
- Explicação curta depois da entrega visual.

Importante:
Não crie nova memória duplicada se já existir memória equivalente. Atualize/consolide a existente. Não apague memórias sem autorização explícita. Não use regra dizendo "não use canvas"; a regra correta é usar canvas/prévia quando mostrar HTML renderizado.
```

