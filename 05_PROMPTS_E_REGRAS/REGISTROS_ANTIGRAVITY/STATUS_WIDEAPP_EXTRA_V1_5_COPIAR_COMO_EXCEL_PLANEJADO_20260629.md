# STATUS - WideAPP_EXTRA V1.5 copiar como Excel planejado

Data: 2026-06-29
Branch atual no momento do registro: `wideapp-v1.4-dev`

## Objetivo do registro

Separar explicitamente o escopo da V1.4 e da V1.5 para evitar mistura de entrega.

## V1.4 - escopo aprovado

Foco exclusivo:

* deixar a interface mais leve;
* melhorar abertura;
* melhorar movimentação e redimensionamento da janela;
* melhorar rolagem da aba `Ativ. Recentes`;
* reduzir travadas e artefatos visuais;
* preservar o visual e as funções atuais.

Na V1.4, **não implementar seleção/cópia estilo Excel**.

## V1.5 - pendência planejada

Planejar em etapa futura:

* selecionar célula, linha ou intervalo;
* copiar com `Ctrl+C`;
* copiar em formato tabulado;
* colar no Excel, Bloco de Notas e WhatsApp;
* botão direito com `Copiar seleção`;
* comportamento parecido com tabela operacional.

## Regra de segurança para V1.4

Se a otimização com Canvas comprometer qualquer comportamento já existente da aba `Ativ. Recentes`, a execução deve parar e avisar antes de avançar.

Comportamentos que devem ser preservados na V1.4:

* seleção de linha/cliente já existente;
* botão direito/contexto;
* duplo clique, se já funcionava;
* filtros;
* controle de quantidade de meses;
* meses dinâmicos até o mês atual;
* rolagem vertical/horizontal;
* cores dos status;
* valores e datas dentro dos quadrinhos;
* layout visual aprovado.

A seleção/cópia estilo Excel continua planejada **somente para a V1.5**.

## Observação técnica

A otimização de Canvas da V1.4 deve ser avaliada somente como melhoria de fluidez visual. Qualquer interação nova de tabela operacional deve ficar fora da V1.4 e entrar apenas no planejamento da V1.5.
