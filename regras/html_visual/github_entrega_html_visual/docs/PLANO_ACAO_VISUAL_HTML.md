# Plano de Acao Visual/HTML

Fonte analisada:
- DOCX original: `C:\Users\Windows User\Desktop\💡CRIA✨REGRAS🧠GÊNIO!!!.docx`
- Texto extraido: `C:\Users\Windows User\Documents\Codex\2026-05-30\sim-se-o-codex-est-com\conversa-extraida.txt`

## Diagnostico curto

O problema real nao e o canvas. O canvas estava correto quando mostrava a pagina HTML renderizada como experiencia visual. A falha veio de uma correcao de memoria que tentou evitar codigo bruto, mas acabou criando uma leitura perigosa: "se codigo aparece, evite canvas". Isso enfraqueceu justamente a parte boa: entregar a pagina visual primeiro.

O ajuste correto e positivo:

1. Preservar canvas/preview quando ele mostra a pagina renderizada.
2. Tratar codigo aberto por padrao como problema de exibicao, nao como motivo para abandonar a visualizacao.
3. Manter codigo HTML/CSS/JS como opcao secundaria: botao, aba, arquivo, download, bloco recolhido/dropdown ou pedido explicito.
4. Interpretar "visual" em pedido de HTML como interface HTML renderizada/interativa, nao como imagem gerada.
5. Testar em conversa limpa com pedido de pagina visual renderizada.

## O que a conversa mostrou

- O teste de pagina sobre extensao Chrome criou uma pagina HTML no canvas e orientou usar "Previa", mas tambem deixou codigo aparecer no fluxo antes da resposta final. Isso foi classificado como "passou parcialmente".
- A resposta seguinte sugeriu "nao use canvas se ele abrir codigo", mas isso piorou a regra porque podia fazer a IA abandonar o canvas/previsualizacao.
- A correcao conceitual certa apareceu depois: "use canvas/preview como objetivo principal; se aparecer codigo, nao trate codigo como entrega final, mude para preview ou entregue miniatura/arquivo visual".
- A lista de memorias indicada na conversa tinha ao menos tres memorias visuais semelhantes: uma corrigida boa, uma ampla util e uma intermediaria antiga que podia causar conflito.
- O proximo ajuste deve ser consolidar a regra visual existente, nao criar outra memoria solta.

## Regra aprimorada recomendada

Quando o usuario pedir pagina visual, HTML visual, orientacao visual, print anotado, mockup, guia de interface, canvas, painel, dashboard, guia navegavel, previa interativa, interface local ou artefato visual semelhante, entregar como foco principal a pagina visual renderizada, previa/canvas visual, imagem, miniatura funcional, painel visual ou arquivo visual abrivel/baixavel. O canvas e correto quando mostra a pagina visual e nao deve ser evitado, removido, anulado ou substituido por codigo. Nao confundir "nao mostrar codigo bruto" com "nao usar canvas". Se HTML/CSS/JS/codigo aparecer por padrao, tratar como problema de exibicao, nao como motivo para abandonar a visualizacao: usar ou orientar o botao "Previa", mostrar a pagina renderizada, entregar miniatura/imagem, arquivo visual abrivel ou painel visual, sem expandir nem repetir codigo na conversa. Codigo bruto so deve aparecer quando o usuario pedir explicitamente. Preservar o comportamento bom anterior: visual renderizado primeiro, codigo/download em botoes nativos como "Previa", "Canvas", "Baixar" ou "Codigo", explicacao curta depois.

## Refinamento anti-conflito imagem x HTML

Quando o pedido envolver HTML, pagina HTML, HTML visual, painel, dashboard, guia navegavel, previa interativa, interface local, canvas com HTML ou artefato funcional, a palavra "visual" deve ser interpretada como interface HTML renderizada/interativa. A entrega correta deve ser canvas/previa visual, pagina renderizada, arquivo HTML abrivel/baixavel, painel interativo ou botao/link para abrir em nova aba/tela cheia. Nao usar geracao de imagem como entrega principal para pedido de HTML. O codigo HTML/CSS/JS pode existir de forma secundaria, minimizada, encurtada, recolhida em dropdown/aba/botao ou acessivel por "Codigo", desde que nao domine a resposta e que a visualizacao renderizada venha primeiro. Geracao de imagem deve ser foco principal somente quando o usuario pedir explicitamente imagem, foto, ilustracao, arte, mockup estatico, miniatura estatica ou print anotado, ou como fallback declarado se a renderizacao HTML nao estiver disponivel.

## Plano de acao

### Fase 1 - Congelar o estado atual

Objetivo: parar de gerar novas memorias conflitantes.

- Nao apagar memorias automaticamente.
- Nao criar nova memoria visual enquanto a lista atual nao for vista.
- Confirmar se o cartao "Memoria atualizada" apareceu quando a regra foi salva.
- Abrir Gerenciar memorias e copiar/observar somente as memorias relacionadas a visual, HTML, canvas, preview e codigo bruto.

### Fase 2 - Identificar a regra-alvo

Objetivo: saber qual memoria existente deve ser consolidada.

Manter:
- A memoria nova/corrigida que diz que a previa visual/canvas e correta e nao deve ser removida.
- A memoria visual ampla sobre prints, imagem, mockup e artefato funcional, se ela nao conflitar.

Nao apagar sem autorizacao:
- Memoria intermediaria antiga que fala em nao abrir/expandir codigo, porque ela pode conter trechos uteis.
- Memoria temporaria de teste.

Marcar como possivel conflito:
- Qualquer regra que diga ou induza "nao use canvas".
- Qualquer regra que faca a IA substituir preview por codigo.
- Qualquer regra que transforme "nao mostrar codigo bruto" em "evitar canvas".

### Fase 3 - Aplicar a regra sem duplicar

Objetivo: atualizar/consolidar a regra visual existente.

Prompt seguro para usar em conversa limpa do ChatGPT:

```text
Atualize/consolide a memoria visual existente sobre orientacao visual, HTML, canvas, previas, paineis, interfaces locais e codigo bruto. Nao crie memoria nova se ja existir memoria equivalente. Nao apague memorias.

Versao final desejada:
Quando o usuario pedir pagina visual, HTML visual, orientacao visual, print anotado, mockup, guia de interface, canvas, painel, dashboard, guia navegavel, previa interativa, interface local ou artefato visual semelhante, entregar como foco principal a pagina visual renderizada, previa/canvas visual, imagem, miniatura funcional, painel visual ou arquivo visual abrivel/baixavel. O canvas e correto quando mostra a pagina visual e nao deve ser evitado, removido, anulado ou substituido por codigo. Nao confundir "nao mostrar codigo bruto" com "nao usar canvas". Se HTML/CSS/JS/codigo aparecer por padrao, tratar como problema de exibicao, nao como motivo para abandonar a visualizacao: usar ou orientar o botao "Previa", mostrar a pagina renderizada, entregar miniatura/imagem, arquivo visual abrivel ou painel visual, sem expandir nem repetir codigo na conversa. Codigo bruto so deve aparecer quando o usuario pedir explicitamente. Preservar o comportamento bom anterior: visual renderizado primeiro, codigo/download em botoes nativos como "Previa", "Canvas", "Baixar" ou "Codigo", explicacao curta depois.

Depois responda curto com:
1. se apareceu o cartao/botao "Memoria atualizada";
2. se a acao foi consolidacao de memoria existente ou se nao foi possivel confirmar;
3. qual teste devo fazer em conversa limpa;
4. se nao conseguir ver o texto exato em Gerenciar memorias, diga exatamente: "Nao consegui confirmar o texto exato da memoria final salva/consolidada."
```

### Fase 4 - Testar comportamento visual

Teste principal:

```text
Crie uma pagina HTML visual simples para explicar como carregar uma extensao local no Chrome. Quero a pagina visual renderizada em canvas/previa como entrega principal. Nao quero codigo HTML aberto na conversa, salvo se eu pedir.
```

Resultado esperado:
- A primeira entrega util deve ser pagina visual renderizada, canvas visual, preview visual, painel interativo ou arquivo HTML abrivel.
- Codigo HTML/CSS/JS nao deve aparecer como conteudo principal; pode ficar recolhido, minimizado, encurtado ou em dropdown/botao.
- Imagem estatica gerada nao deve substituir o HTML visual.
- Se a interface abrir em modo Codigo, a resposta deve orientar o botao "Previa" e nao repetir o codigo.
- A resposta final deve ser curta e dizer onde ver preview, baixar, abrir em nova aba/tela cheia ou abrir codigo por botoes nativos.

Teste de permissao para codigo:

```text
Agora mostre o codigo HTML completo desse arquivo.
```

Resultado esperado:
- Agora o codigo pode aparecer, porque foi pedido explicitamente.

### Fase 5 - Aprimorar a entrega HTML daqui para frente

Contrato de entrega visual:

1. Entrega principal: preview/canvas visual, screenshot, miniatura funcional, arquivo HTML aberto ou link local.
2. Entrega secundaria: codigo, download, explicacao tecnica.
3. Resposta curta: o que foi entregue e qual botao usar.
4. Falha de preview: nao abandonar visual; criar alternativa visual abrivel.

Para Codex/local:
- Criar arquivo HTML funcional na pasta do trabalho.
- Abrir/verificar em navegador.
- Se possivel, salvar screenshot de confirmacao.
- Entregar link do arquivo HTML e screenshot/descricao objetiva.

Para ChatGPT/canvas:
- Pedir pagina renderizada/canvas/preview como entrega principal.
- Se abrir codigo, orientar "Previa" sem repetir o codigo.
- Nao pedir "nao use canvas", porque isso reativa o erro conceitual.

## Proxima acao recomendada

Aplicar a regra em uma conversa limpa somente depois de confirmar a memoria-alvo em Gerenciar memorias. Se o cartao "Memoria atualizada" aparecer, considerar persistencia confirmada visualmente. Depois rodar o teste principal em nova conversa limpa e registrar se a entrega principal foi pagina visual renderizada ou codigo.
