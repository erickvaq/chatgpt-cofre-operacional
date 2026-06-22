# REGRAS PERSISTENTES DO PROJETO — Relatorio_WidePay_Lotes
# Atualizado em: 16/06/2026
---

## REGRA PRIORITÁRIA — Fonte principal de instruções do projeto

Antes de executar qualquer rotina de relatório, PDF, HTML, DOCX, importação, conferência financeira, busca de cliente, painel, .bat, .lnk ou arquivo final, o agente deve carregar automaticamente as regras persistentes deste arquivo por meio do precheck.

As regras deste arquivo têm prioridade operacional dentro do projeto Relatorio_WidePay_Lotes.

O usuário não deve precisar lembrar manualmente o agente de ler este arquivo.

Se houver conflito entre resposta anterior do agente e este arquivo, prevalece este arquivo.

Se houver conflito entre dados de cliente, carnê, WidePay, print ou relatório anterior, o agente deve parar e pedir confirmação antes de gerar arquivo final.

---

## REGRA 1 — Visualização de PDFs

**Nunca criar link clicável direto para arquivo `.pdf` dentro do Antigravity.**

Quando o link do PDF é clicável dentro do chat/painel do Antigravity,
o arquivo abre como texto bruto mostrando `%PDF-1.4` — isso está errado.

### Procedimento correto ao gerar ou referenciar um PDF:

1. Abrir o PDF externamente via PowerShell:
   ```
   Start-Process "C:\caminho\completo\arquivo.pdf"
   ```
   Ou via script bat:
   ```
   ABRIR_PDF.bat "nome_do_arquivo.pdf"
   ```

2. Mostrar o caminho completo do PDF em **texto puro** (não como link):
   ```
   C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes\02_RELATORIOS_GERADOS\arquivo.pdf
   ```

3. Gerar sempre uma **prévia HTML** com o mesmo conteúdo do PDF,
   salvar em `02_RELATORIOS_GERADOS` com sufixo `_PREVIA.html`,
   e abrir no navegador via:
   ```
   Start-Process "C:\caminho\completo\arquivo_PREVIA.html"
   ```

4. Se houver ferramenta local disponível (ex: Pillow, ghostscript, etc.),
   gerar também uma prévia PNG da primeira página do PDF.
   **Não instalar dependência nova sem autorização do usuário.**

---

## REGRA 2 — Idioma

O usuário sempre se comunica em **português**.
O agente deve sempre responder em português.

O conversor de voz do usuário pode transcrever "WidePay" como:
- "webplay", "web pay", "webpay"

O agente deve interpretar e corrigir automaticamente para "WidePay".

---

## REGRA 3 — Nunca alterar dados no WidePay

O agente só lê e organiza informações.
Nunca cancelar, excluir, baixar em massa ou modificar cobranças no WidePay.

---

## REGRA 4 — Login manual

O login no WidePay deve ser feito manualmente pelo usuário.
O agente não armazena senhas em nenhum arquivo.

---

## REGRA 5 — Prints do usuario sao fonte prioritaria de validacao

Quando o usuario enviar prints (capturas de tela) de cobrancas/parcelas,
essa informacao e tratada como fonte prioritaria.

Porem, se houver divergencia entre:
- o print do usuario
- os dados do WidePay
- o script Python
- o PDF gerado
- ou um relatorio anterior

**Parar imediatamente e perguntar ao usuario qual fonte deve prevalecer.**

Nao assumir automaticamente que o print e correto se houver conflito detectado.
Nao assumir que o sistema WidePay e correto se o usuario afirmar o contrario.
Sempre documentar a fonte usada no relatorio de conferencia.

---

## REGRA 6 — Auditar antes de gerar PDF final

Antes de gerar o PDF final de qualquer relatório:
1. Gerar arquivo de conferência `.md` em `07_DADOS_TEMPORARIOS`
2. Apresentar o cálculo ao usuário para validação
3. Só gerar o PDF após confirmação

---

## REGRA 7 — Conversão de documentos

- Pasta de entrada: `00_IMPORTAR_DOCUMENTOS`
- Pasta de saída: `01_DOCUMENTOS_CONVERTIDOS`
- Não alterar os arquivos originais
- Verificar ferramentas locais antes de instalar dependências novas
- Avisar o usuário antes de qualquer instalação de pacote

---

## REGRA 8 — Nao abrir pastas sem relacao com o projeto

O agente só deve ler arquivos dentro da pasta do projeto:
`C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes`

Nao acessar outras pastas do Desktop ou do sistema sem solicitacao explicita.

---

## REGRA 9 — Entrega pratica de arquivos

Quando entregar PDF, HTML ou relatorio final, sempre criar uma forma pratica
de abertura: painel HTML, script .bat ou atalho .lnk.

Nao entregar apenas caminho em texto puro quando o usuario precisar visualizar
rapidamente.

Padrao de entrega apos gerar qualquer relatorio (PADRAO_ENTREGA_CLIENTE_SEM_BAT):
1. Abrir automaticamente via Start-Process (externo, nunca dentro do Antigravity) ou abrir a pasta no Explorer para conferência.
2. Criar ou atualizar o painel HTML de acesso rapido (ABRIR_RELATORIO_*.html) se for necessário.
3. Para relatórios e entregas de cliente, não criar arquivos `.bat` por padrão (seguir PADRAO_ENTREGA_CLIENTE_SEM_BAT). Só criar se houver pedido explícito ou necessidade técnica explicada antes.
4. Se atalhos .bat forem criados sob demanda, devem constar no relatório com caminho local, tamanho e link GitHub individual.
5. Nunca criar link clicavel direto para .pdf no chat — causa abertura como texto bruto

---

## REGRA 10 — Nunca sobrescrever arquivos finais sem autorizacao

**Nunca sobrescrever PDF, HTML, relatorio `.md`, `.txt`, planilha ou qualquer
arquivo final ja existente sem autorizacao explicita do usuario.**

### Ao gerar uma versao corrigida, sempre usar nome novo:

- Sufixo `_CORRIGIDO`
- Sufixo `_V2`, `_V3`...
- Sufixo `_CONFERIDO`
- Ou data/hora no nome: `_2026-06-16_1049`

Exemplo correto:
```
RESUMO_FINANCEIRO_CAMILA_FERROLHO_CORRIGIDO.pdf   <- versao corrigida
RESUMO_FINANCEIRO_CAMILA_FERROLHO.pdf             <- original preservado
```

### Se ja existir arquivo com mesmo nome, perguntar antes:

> "Este arquivo ja existe. Deseja substituir, criar copia corrigida ou criar backup?"

### Se for necessario substituir, criar backup primeiro:

```
BACKUP_2026-06-16_1049_RESUMO_FINANCEIRO_CAMILA_FERROLHO.pdf
```

### Arquivo principal sempre deve ser o corrigido mais recente.
Os botoes, atalhos .bat e .lnk devem sempre apontar para o arquivo corrigido.

---

## REGRA 11 — Registro historico e modelo de auditoria: caso Camila Ferrolho

**Importante:** O caso da cliente Camila Ferrolho serve como **modelo metodologico e de procedimento de auditoria** para o projeto. Os valores numericos deste caso **nunca devem ser usados como constantes fixas para outros clientes**. Cada cliente possui seus proprios dados de contrato e parcelas que devem ser auditados individualmente.

### O que aconteceu no caso modelo:
- O script original (`gerar_pdf_camila.py`) continha um erro de calculo ao definir `total_geral = 65` em vez de `100` (limite do contrato fisico).
- O script corrigido (`gerar_pdf_camila_v2.py`) foi salvo no mesmo caminho e sobrescreveu o original — o arquivo antigo com erro foi perdido.

### Consequencia do caso modelo:
- `RESUMO_FINANCEIRO_CAMILA_FERROLHO.pdf` existe mas ja e a versao corrigida.
- `RESUMO_FINANCEIRO_CAMILA_FERROLHO_CORRIGIDO.pdf` e uma copia identica ao anterior e e o arquivo principal correto.

### Resumo dos dados auditados da Camila Ferrolho (Referencia de Procedimento):
- Total do contrato: 100 parcelas (confirmado no contrato fisico)
- Parcelas pagas: 48 parcelas (confirmado no WidePay)
- Parcelas restantes: 52 parcelas (100 - 48 = 52)
- Progresso: 48% pago
- Valor pago (com juros): R$ 4.876,45
- Valor restante: R$ 5.148,00 (52 x R$ 99,00)
- Arquivo principal: `RESUMO_FINANCEIRO_CAMILA_FERROLHO_CORRIGIDO.pdf`

---

## REGRA 12 — Checklist obrigatorio antes da entrega final

Antes de entregar qualquer relatorio final (PDF, HTML, DOCX ou planilha), confirmar obrigatoriamente cada item abaixo:

| # | Verificacao | OK? |
|---|--------------------------------------------------------------------|-----|
| 1 | Li o arquivo REGRAS_PERSISTENTES_DO_PROJETO.md antes de comecar | [ ] |
| 2 | Gerei relatorio de conferencia `.md` em `07_DADOS_TEMPORARIOS` | [ ] |
| 3 | O usuario aprovou os calculos antes do PDF final | [ ] |
| 4 | O PDF final NAO sobrescreveu arquivo anterior sem autorizacao | [ ] |
| 5 | O PDF corrigido tem nome novo (`_CORRIGIDO`, `_V2` ou com data) | [ ] |
| 6 | Existe previa HTML do relatorio em `02_RELATORIOS_GERADOS` | [ ] |
| 7 | Pasta final aberta no Windows Explorer para conferência (sem BAT por padrão) | [ ] |
| 8 | Nenhum link direto para `.pdf` foi criado no chat do Antigravity | [ ] |
| 9 | Botoes e atalhos apontam para o arquivo corrigido mais recente | [ ] |
| 10| O PDF foi aberto externamente via Start-Process (nao como texto) | [ ] |

**Se qualquer item estiver sem OK, nao entregar o relatorio final ainda.**
Resolver o item pendente primeiro e registrar no relatorio de conferencia.

---

## REGRA 13 — Leitura automatica obrigatoria das regras (Prioritaria)

O usuario nao deve precisar mandar manualmente o agente ler este arquivo. 

Antes de qualquer processamento de relatorio, PDF, DOCX, HTML, importacao, conferencia financeira, busca de cliente, painel, `.bat`, `.lnk` ou geracao de arquivo final, as regras persistentes devem ser carregadas e verificadas automaticamente atraves do script:
`00_SISTEMA_PRECHECK\precheck_regras.py`

Se o precheck nao for executado com sucesso ou se for detectada a falta de alguma regra obrigatoria ou inconsistencias de numeracao, o script em execucao deve parar imediatamente e avisar:
`ERRO: regras persistentes nao foram carregadas. Execucao bloqueada.`

Nenhum arquivo final de entrega ou processamento pode rodar sem essa verificacao.

---

## REGRA 14 — Comando simples para buscar cliente e painel visual clicavel

O usuario nao deve precisar lembrar caminhos de arquivos complexos, scripts especificos ou copiar e colar caminhos do terminal para monitorar o andamento de um cliente.

Sempre que precisar consultar a situacao de um loteamento/cliente:
1. Deve ser utilizado o comando simplificado `BUSCAR_CLIENTE.bat` na raiz do projeto.
2. Esse comando executara o precheck das regras e acionara o script de busca `buscar_cliente.py`.
3. O sistema devera apresentar o resumo financeiro no terminal e gerar e abrir automaticamente um painel visual local clicavel (.hta) na pasta `07_DADOS_TEMPORARIOS\PAINEIS_CLIENTES\`.
4. Esse painel HTA devera conter o resumo do cliente e botoes de acao rapida para abrir o PDF final corrigido, a previa HTML, o painel do cliente, a pasta de relatorios gerados ou a conferencia .md, alem de permitir copiar o caminho do PDF para a area de transferencia.
5. Os arquivos devem ser abertos em aplicacoes externas nativas do Windows, impedindo que PDFs abram como texto bruto dentro do Antigravity.

---

## REGRA 15 — Entrega clicavel de arquivos criados

Sempre que o agente criar, modificar ou entregar arquivos do projeto, deve fornecer uma forma clicavel e pratica de acesso, usando painel HTA, arquivo BAT, atalho LNK ou link file:/// em Markdown. O usuario nao deve precisar copiar e colar caminhos para abrir arquivos.

É proibido entregar link Markdown direto para `.pdf` quando houver risco de abrir como texto bruto no Antigravity. PDF deve ser aberto por HTA, BAT, LNK, Start-Process, previa HTML ou visualizador externo.

---

## REGRA 16 — Abertura externa obrigatoria e organizacao de arquivos finais

Links `file:///` em Markdown dentro do Antigravity nao sao solucao confiavel para abrir arquivos finais. PDF, DOCX, HTML, HTA, planilhas e imagens devem ser abertos por lancador externo, HTA, BAT, LNK, PowerShell `Start-Process` ou aplicativo padrao do Windows.

Abertura e atalhos na pasta de entrega (PADRAO_ENTREGA_CLIENTE_SEM_BAT):
1. O sistema deve criar uma pasta final limpa e dedicada para a entrega de cada cliente (ex: `02_RELATORIOS_GERADOS\CAMILA_FERROLHO_V3_FINAL\`).
2. Dentro dessa pasta devem residir unicamente os arquivos finais (PDF, HTML, DOCX) e arquivos auxiliares estritamente necessários.
3. Não criar arquivos `.bat` automaticamente por padrão para entregas de cliente, pois basta abrir a pasta final.
4. O padrão de conferência agora é abrir a pasta final no Windows Explorer usando o comando apropriado (ex: `explorer.exe "caminho_da_pasta"`).
5. Só criar `.bat` se solicitado explicitamente ou houver necessidade técnica real que deve ser justificada previamente.
6. Se um `.bat` for criado por exceção, ele deve usar caminhos relativos com `%~dp0` (ex: `cd /d "%~dp0" && start "" "nome_do_arquivo.pdf"`), possuir numeração e nomes claros (ex: `01_ABRIR_PDF_FINAL.bat`), e constar no relatório com caminho local, tamanho e link GitHub individual.
7. Links clicaveis do Antigravity devem abrir preferencialmente a pasta de entrega limpa em vez do arquivo individual diretamente.

---

## REGRA 17 — Padronizacao de escrita do cabecalho dos relatorios

O titulo principal de identificacao dos relatorios deve ser grafado como:
`RELATÓRIO FINANCEIRO`

E a localidade/subtitulo do loteamento deve ser grafada exatamente como:
`Loteamento Água Viva — Iaçú-BA`

Esta grafia e obrigatoria em todos os templates, scripts e geradores de relatorio do projeto, nao sendo aceitas variacoes como "Agua Viva", "Iacu-Ba", "Iaco-Ba" ou semelhantes.

---

## REGRA 18 — Skills operacionais do projeto

O projeto utiliza Skills customizadas do Antigravity estruturadas no plugin global `widepay-plugin` para executar rotinas de relatorio financeiro, abertura externa, busca de cliente e geracao de PDF.

As Skills principais sao:
- `widepay-core-operacional`: precheck, regras, busca de cliente, seguranca e fluxo financeiro.
- `widepay-relatorio-pdf`: geracao, revisao e padronizacao de relatorios financeiros em PDF/HTML.
- `widepay-abertura-externa`: abertura de arquivos finais no aplicativo correto do Windows.

As Skills devem ser acionadas automaticamente por pedidos simples do usuario, como: "Buscar Camila", "Quero o relatorio da Camila", "Abrir arquivo da Camila", "Gerar relatorio de cliente".

O usuario nao deve precisar explicar caminhos, regras ou comandos tecnicos.

O precheck deve continuar dinamico, sem depender de quantidade fixa de regras.

---

## REGRA 19 — Pasta de Contratos Externa Somente Leitura

A pasta contendo os contratos originais dos clientes (`C:\Users\Windows User\Desktop\AGUA VIVA`) e o site WidePay (`https://www.widepay.com/`) devem ser tratados como **estritamente somente leitura (read-only)**.
1. O agente nunca deve modificar, editar, renomear ou criar novos arquivos ou subpastas dentro desta pasta de contratos.
2. Todas as rotinas que utilizarem dados destes contratos devem apenas consultá-los de forma passiva.
3. Quaisquer novos arquivos de relatório (PDF, HTML, MD, BAT, atalhos LNK) ou backups gerados devem residir obrigatoriamente dentro da estrutura da pasta do projeto: `C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes`.

---

## REGRA 20 — Tratamento de múltiplos resultados na busca de clientes

Quando o usuário iniciar uma busca por nome de cliente através de `BUSCAR_CLIENTE.bat` ou pelo script correspondente:
1. Se houver mais de um cliente compatível mapeado nas pastas do projeto ou da Água Viva, o script de busca deve listar as opções numeradas de forma limpa e objetiva e solicitar ao usuário que selecione o cliente desejado.
2. Após a seleção, o fluxo deve proceder normalmente carregando os dados do cliente escolhido.

---

## REGRA CRÍTICA — Fluxo Genérico de Clientes e Modelo Metodológico (Caso Camila Ferrolho)

1. **WidePay é Somente Consulta e Não Pode Ser Simulado:** O site WidePay (https://www.widepay.com/) deve ser utilizado estritamente em modo somente leitura. É proibido criar, deletar ou modificar qualquer cobrança, boleto ou cadastro de cliente. O WidePay nunca deve ser simulado. O navegador preferencial para WidePay automático é o Opera dedicado na porta CDP `9444` (endpoint principal `localhost:9444`). O Chrome principal do usuário não deve ser fechado e não deve sofrer interferência. Se o CDP falhar, os dados financeiros ficam pendentes com a observação: "WIDEPAY NÃO CONSULTADO — AGUARDANDO LOGIN MANUAL, PRINTS OU EXPORTAÇÃO DO USUÁRIO".
2. **Pasta Água Viva é Somente Consulta:** A pasta externa `C:\Users\Windows User\Desktop\AGUA VIVA` é somente leitura. Contratos só podem ser localizados e copiados para dentro do projeto antes de serem editados ou convertidos.
3. **Escrita Restrita ao Projeto:** Todos os arquivos novos de relatórios (PDF, HTML, MD, BAT ou atalhos) devem ser criados e mantidos exclusivamente na pasta do projeto: `C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes`.
4. **Fluxo Genérico por Cliente:** O fluxo de geração de relatórios é genérico. O agente deve identificar o cliente pelo nome, copiar e converter seu contrato, cruzar com dados do WidePay e gerar a conferência.
5. **Conferência .md Antes do PDF:** Sempre gerar um relatório de conferência `.md` em `07_DADOS_TEMPORARIOS` antes de gerar o PDF/HTML final.
6. **PDF Final Após Validação:** O PDF final do relatório só deve ser gerado após o usuário validar e aprovar explicitamente os cálculos apresentados no arquivo de conferência `.md`.
7. **Modelo Camila é Apenas Visual/Metodológico:** O relatório Camila V4 (cabeçalho verde, título "RELATÓRIO FINANCEIRO", cards de resumo, tabelas de dados de contrato e WidePay, barra de progresso, rodapé) serve apenas como padrão visual e de método de conferência.
8. **Recalcular do Zero:** É proibido copiar dados ou números de um cliente para outro. Todos os cálculos de total do contrato, parcelas pagas, restantes, percentuais e saldos a pagar devem ser recalculados do zero para cada novo cliente.

---

## REGRA CRÍTICA — WidePay automático via Opera GX, WMI e CDP localhost:9444

O acesso automático ao WidePay na Antigravity IDE deve usar:
* navegador preferencial: Opera GX dedicado;
* porta CDP principal: `9444`;
* endpoint principal: `http://localhost:9444`;
* abertura via WMI / `Win32_Process`;
* perfil dedicado: `08_NAVEGADOR_WIDEPAY\OperaProfile_9444`.

Nunca usar como principal:
* `127.0.0.1`;
* porta `9222`;
* Chrome principal do usuário;
* terminal interno com `cmd /c` como método principal de abertura do navegador.

Motivo:
A Antigravity IDE pode executar comandos dentro de um Job Object do Windows. Quando o terminal termina, processos filhos podem ser encerrados. Por isso, o navegador dedicado deve ser iniciado via WMI, fora da árvore do terminal.

Regras:
1. WidePay é somente consulta.
2. Nunca alterar cadastro, boleto, carnê, cobrança ou valores.
3. Nunca salvar senha.
4. Login é manual quando necessário.
5. Nunca simular dados do WidePay.
6. Se CDP falhar, marcar dados financeiros como pendentes.
7. Se WidePay não for consultado de verdade, registrar: `WIDEPAY NÃO CONSULTADO — AGUARDANDO LOGIN, PRINTS OU EXPORTAÇÃO.`
8. Para qualquer cliente, pesquisar todos os carnês, não apenas o primeiro.
9. Verificar carnês ativos, finalizados, pagos, pendentes e cancelados.
10. Não gerar PDF final antes da conferência `.md` e aprovação do usuário.

---

## REGRA 21 — Consulta integrada de Carnês e Cobranças/Boletos

Todo relatório financeiro deve consultar carnês e cobranças/boletos do WidePay. É proibido gerar conferência final ou PDF considerando apenas carnês quando houver possibilidade de boletos/cobranças avulsas.

---

## REGRA 22 — Modo Econômico Obrigatório

Sempre que o pedido for apenas conferir, validar, comparar, procurar valor, confirmar item ou revisar resultado já gerado, usar modo econômico.
Isso significa:
1. Não abrir navegador;
2. Não usar browser subagent;
3. Não consultar WidePay novamente;
4. Não usar CDP se já existe JSON;
5. Não gerar PDF;
6. Não criar plano longo;
7. Não editar arquivos, salvo pedido explícito;
8. Ler somente os arquivos necessários;
9. Ler no máximo trechos pequenos;
10. Responder em no máximo 12 linhas.

---

## REGRA 23 - Relatorio Consolidado de Atrasos e Boletos Avulsos

Quando o usuario pedir explicitamente uma lista geral, todos os clientes, atrasos de todos, relatorio consolidado ou equivalente, o agente pode gerar uma conferencia consolidada de clientes/lotes do WidePay em modo somente leitura.

Este modo consolidado nao substitui o fluxo individual por cliente. Os relatorios individuais permanecem como modelo principal para analise detalhada, PDF final por cliente e validacao de contrato.

Regras do modo consolidado:
1. Preferir os JSONs locais recentes de `07_DADOS_TEMPORARIOS\WIDEPAY_CONSULTAS` para economizar tempo e creditos.
2. Consultar o WidePay real novamente apenas quando o usuario pedir atualizacao real, quando nao houver JSON confiavel ou quando houver divergencia relevante.
3. Nunca alterar cobrancas, carnes, boletos, status ou cadastros no WidePay.
4. Gerar arquivos novos com nome proprio, sem sobrescrever relatorios individuais.
5. Gerar primeiro conferencia em Markdown/HTML/CSV; PDF consolidado somente apos validacao do usuario.
6. Interpretar boletos avulsos como possiveis regularizacoes de parcelas atrasadas quando a descricao informal indicar uma data de referencia, por exemplo `ref 10/08/24 atraso`, `ref 10/08/2024`, `atraso 10/08/24` ou `mes 08/2024`.
7. Se o boleto avulso estiver recebido/pago e a data inferida corresponder a uma parcela vencida, classificar como `atraso pago por boleto avulso`.
8. Se nao houver boleto avulso pago correspondente, manter a parcela como `atraso em aberto/sem avulso pago`.
9. Toda data inferida de texto informal deve ser marcada como inferencia e deve preservar a descricao original usada.
10. O consolidado deve listar por cliente/lote: carne, referencia, parcela vencida, status, valor, boleto avulso relacionado, data inferida, valor pago em avulso e observacao.

---

## REGRA 24 - Entrega Visual Obrigatoria em HTML + PDF + GitHub

Sempre que o usuario pedir para gerar arquivo de visualizacao, relatorio, conferencia, painel, resumo financeiro, previa, documento visual ou entrega final, a entrega visual deve sair em pares: um arquivo `.html` e um arquivo `.pdf`.

Esta regra nao elimina as conferencias previas obrigatorias. Quando o conteudo envolver calculos financeiros, contrato, WidePay, parcelas, carnes, boletos ou valores, o agente deve primeiro gerar e validar a conferencia permitida pelas regras anteriores. O PDF/HTML final so deve ser tratado como entrega final depois das validacoes aplicaveis.

Regras de geracao:
1. Sempre gerar os dois formatos para entrega visual final: um `.html` para previa visual/interativa e um `.pdf` para conferencia, impressao e envio.
2. Os dois arquivos devem ficar na mesma pasta final de entrega.
3. Os nomes dos dois arquivos devem conter assunto ou cliente, tipo do documento, data de criacao e versao.
4. Padrao recomendado: `TIPO_ASSUNTO_YYYY-MM-DD_V1.html` e `TIPO_ASSUNTO_YYYY-MM-DD_V1.pdf`.
5. Nunca sobrescrever arquivo final antigo. Se `V1` existir, criar `V2`; se `V2` existir, criar `V3`, e assim por diante.
6. Depois de gerar o PDF e o HTML na mesma pasta final de entrega, abrir a pasta final no Windows Explorer (e abrir o PDF externamente se necessário) para conferência.
7. Nunca abrir PDF como texto bruto dentro do editor ou chat.
8. Depois de gerar HTML e PDF, confirmar obrigatoriamente: existencia dos dois arquivos, tamanho dos arquivos, PDF realmente criado e HTML abrivel.

Regras de GitHub:
1. Toda entrega visual final deve preparar envio para o GitHub do projeto quando os arquivos forem seguros para publicacao.
2. Antes de subir, verificar se a pasta atual e um repositorio Git, se existe `remote origin`, qual branch esta ativa e se os arquivos nao contem senha, token, cookie, dado sensivel indevido, cache de navegador ou informacao fora do escopo.
3. Se nao existir repositorio Git ou `remote origin`, parar a etapa GitHub e pedir o link do repositorio. Nao criar repositorio novo sem autorizacao.
4. Se a árvore do Git local estiver desalinhada com a do remote (ex: após inicialização limpa `git init`), realizar checkout da branch correta (ex: `main`), vincular upstream (`git branch --set-upstream-to=origin/main main`), executar reset misto (`git reset --mixed origin/main`) e recuperar arquivos (`git restore .`) para sincronizar a árvore sem alterar ou perder modificações locais.
5. Se faltar autenticacao, permissao, internet ou houver risco de expor dados, parar a etapa GitHub, explicar exatamente o motivo e manter a entrega local validada.
6. Quando GitHub estiver configurado e seguro, adicionar os arquivos HTML e PDF da entrega, criar commit com mensagem clara contendo data e versao, fazer push e confirmar o push.
7. Informar link GitHub somente depois de push confirmado. Nunca inventar link de arquivo ainda nao publicado.

Abertura e Atalhos na Pasta de Entrega (PADRAO_ENTREGA_CLIENTE_SEM_BAT):
1. Para entregas de cliente, relatórios financeiros, conferências visuais e entregas finais, não criar arquivos `.bat` automaticamente por padrão.
2. O padrão obrigatório é colocar o HTML e o PDF na mesma pasta final de entrega e abrir a pasta no Windows Explorer para conferência.
3. Só criar `.bat` se houver necessidade técnica real (explicada previamente) ou pedido explícito. Se criado, deve usar caminhos relativos com `%~dp0` e constar no relatório final com caminho local, tamanho e link GitHub individual.

Formato final obrigatorio para entregas visuais:

ENTREGA FINAL GERADA

1. HTML criado:
   Caminho local:

2. PDF criado:
   Caminho local:

3. PDF aberto para conferencia?
   Resposta:

4. Versao criada:
   Resposta:

5. Data de criacao:
   Resposta:

6. Arquivos enviados ao GitHub?
   Resposta:

7. Commit criado:
   Resposta:

8. Link do GitHub para conferir:
   Resposta:

9. Observacoes ou erros:
   Resposta:

---

## REGRA 25 — Memória Operacional e Registro Obrigatório de Artefatos no GitHub

Toda e qualquer criação, alteração ou citação de arquivos de relevância para o projeto (HTML, PDF, scripts, `.bat` sob demanda, regras, históricos, backups, etc.) ou de auditoria do Antigravity/Codex deve possuir caminho local do Windows e link correspondente no GitHub.

Regras operacionais de artefatos:
1. **Preservação de arquivos no projeto:** Todos os arquivos gerados devem ser mantidos na estrutura do projeto.
2. **Versionamento e Publicação:** Os arquivos devem ser rastreados no Git, com commits estruturados e enviados ao repositório remoto via `git push`.
3. **Links Reais:** Sempre retornar links reais correspondentes aos arquivos publicados no GitHub. É proibido simular ou inventar links de arquivos que não foram efetivamente enviados.
4. **Arquivos do Antigravity:** Os arquivos auxiliares de planejamento, tarefas e execução (`implementation_plan.md`, `task.md`, `walkthrough.md`) gerados em pastas temporárias do Antigravity (ex: `.gemini/antigravity-ide/brain/...`) devem ser copiados obrigatoriamente para `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/` antes de cada commit, versionados e enviados ao GitHub.
5. **Segurança de Dados:** Nunca registrar ou subir ao repositório senhas, tokens, cookies, credenciais ou chaves de API.

---

## REGRA 26 — Checagem de Cobertura Obrigatória no WidePay

Sempre que o usuário pedir para conferir clientes, fazer levantamento preliminar, revisar clientes por letras ou gerar relatórios por grupo de clientes, execute automaticamente uma checagem de cobertura no WidePay antes de concluir.

Objetivo:
Garantir que nenhum cliente ativo das iniciais solicitadas fique de fora.

Processo obrigatório:
1. Consultar primeiro o WidePay (contatos, carnês, cobranças/boletos) para listar clientes ativos.
2. Cruzar nomes repetidos para evitar duplicidade.
3. Consolidar todos os registros do mesmo cliente/lote.
4. Classificar cada nome encontrado como: "Ativo confirmado", "Sem evidência financeira ativa" ou "Pendente de conferência".
5. Não excluir cliente apenas porque não encontrou contrato local. Manter na tabela com "Contrato local não encontrado — pendente de conferência."
6. Informar obrigatoriamente no final: total de nomes avaliados, total de clientes ativos confirmados, total de inativos/sem evidência e total de pendentes, bem como eventuais limites de consultas.

Esta checagem deve ser feita de forma automatizada e dinâmica, devendo ser executada mesmo sob comandos curtos.

---

## REGRA 27 — Login Manual no WidePay sem encerrar o processo

Sempre que o Antigravity precisar acessar o WidePay e encontrar a tela de login, o processo não deve ser encerrado, cancelado nem reiniciado.

### Comportamento obrigatório
Quando aparecer a tela de login do WidePay, o Antigravity deve:
1. Abrir ou manter visível a janela/navegador dedicado do WidePay.
2. Informar claramente que o usuário precisa fazer login manualmente.
3. Pausar a execução e aguardar confirmação do usuário.
4. Aceitar como confirmação respostas como: "Logado", "Pode continuar", "Já entrei", "Pode seguir".
5. Não encerrar a tarefa.
6. Não reiniciar o levantamento do zero.
7. Não exigir que o usuário repita o comando completo.
8. Após a confirmação do login, continuar exatamente do ponto em que parou.

### Resposta padrão ao encontrar login
Quando o WidePay estiver na tela de login, responder:
"O WidePay está na tela de login. Faça login manualmente na janela do navegador dedicada. Vou aguardar sua confirmação. Quando estiver logado, responda 'Logado' ou 'Pode continuar' para eu seguir exatamente do ponto atual."

### Aplicação obrigatória
Aplicar esta regra em todos os fluxos do WidePay, incluindo:
- Levantamento preliminar;
- Checagem de cobertura;
- Conferência de cliente específico;
- Geração de relatórios;
- Consulta de carnês;
- Consulta de cobranças/boletos;
- Consulta de contatos.

### Objetivo
Esta regra deve evitar:
- perda de tempo;
- repetição de comandos;
- reinício desnecessário do processo;
- abandono da tarefa quando o login manual for necessário.

---

## REGRA 28 — Não criar timers repetidos nem esperas infinitas

Sempre que uma tarefa, script ou extração do WidePay demorar, o Antigravity não deve ficar criando timers repetidos de 30 ou 40 segundos nem enviando mensagens sucessivas de espera.

### Comportamento proibido
É proibido repetir ciclos como:
- “vou aguardar 30 segundos”;
- “timer expirou”;
- “vou aguardar mais 40 segundos”;
- “vou verificar de novo”;
- “estou esperando a extração terminar”;
- “vou agendar outro timer”.

Esse comportamento consome tempo, contexto e tokens sem entregar resultado útil.

### Comportamento obrigatório
Quando um script, extração ou automação demorar, o Antigravity deve:
1. Verificar o status real da tarefa uma única vez.
2. Informar objetivamente:
   - se está rodando;
   - se travou;
   - em qual etapa está;
   - último log relevante;
   - dados já extraídos, se houver.
3. Se parecer travado, interromper com segurança ou pedir autorização para interromper.
4. Não agendar novos timers repetidos.
5. Não narrar esperas longas.
6. Não continuar consumindo contexto com mensagens de espera.
7. Se houver dados parciais, apresentar os dados já coletados.
8. Se não houver avanço real, parar e pedir decisão do usuário.

### Padrão correto de resposta
Se a tarefa estiver demorando, responder apenas:
"A extração está demorando. Verifiquei o status: [rodando/travado]. Última etapa: [etapa]. Último log relevante: [log]. Deseja que eu aguarde mais uma vez, interrompa com segurança ou apresente os dados parciais?"

### Aplicação obrigatória
Aplicar esta regra em todos os fluxos do WidePay:
- levantamento preliminar;
- checagem de cobertura;
- consulta de carnês;
- consulta de cobranças;
- consulta de contatos;
- geração de relatórios;
- scripts CDP;
- scripts em segundo plano;
- qualquer extração automatizada.

### Objetivo
Evitar:
- gasto desnecessário de tokens;
- espera infinita;
- repetição de mensagens;
- travamento silencioso;
- perda de tempo;
- execução sem controle.



