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
5. Quando o usuário pedir acesso direto, o PDF pode ser referenciado por link clicável no chat, mantendo também o caminho em texto puro e a opção de abertura externa.

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
| 8 | Se o usuário pediu acesso clicável, o PDF foi referenciado de forma direta e também em texto puro | [ ] |
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

Sempre que o agente criar, modificar ou entregar arquivos do projeto, deve fornecer uma forma clicavel e pratica de acesso, usando painel HTA, arquivo BAT, atalho LNK ou link clicavel do proprio arquivo quando solicitado. O usuario nao deve precisar copiar e colar caminhos para abrir arquivos.

Se o ambiente abrir PDF como texto bruto, o agente deve preferir HTA, BAT, LNK, Start-Process, previa HTML ou visualizador externo; quando o usuario pedir link clicavel do PDF, ele pode ser fornecido junto com o caminho em texto puro.

---

## REGRA 16 — Abertura externa obrigatoria e organizacao de arquivos finais

Links `file:///` em Markdown dentro do Antigravity podem ser usados como atalho clicavel quando o usuario pedir acesso direto; para prevenção de texto bruto, mantenha também o lancador externo, HTA, BAT, LNK, PowerShell `Start-Process` ou aplicativo padrao do Windows.

Abertura e atalhos na pasta de entrega (PADRAO_ENTREGA_CLIENTE_SEM_BAT):
1. O sistema deve criar uma pasta final limpa e dedicada para a entrega de cada cliente (ex: `02_RELATORIOS_GERADOS\CAMILA_FERROLHO_V3_FINAL\`).
2. Dentro dessa pasta devem residir unicamente os arquivos finais (PDF, HTML, DOCX) e arquivos auxiliares estritamente necessários.
3. Não criar arquivos `.bat` automaticamente por padrão para entregas de cliente, pois basta abrir a pasta final.
4. O padrão de conferência agora é abrir a pasta final no Windows Explorer usando o comando apropriado (ex: `explorer.exe "caminho_da_pasta"`).
5. Só criar `.bat` se solicitado explicitamente ou houver necessidade técnica real que deve ser justificada previamente.
6. Se um `.bat` for criado por exceção, ele deve usar caminhos relativos com `%~dp0` (ex: `cd /d "%~dp0" && start "" "nome_do_arquivo.pdf"`), possuir numeração e nomes claros (ex: `01_ABRIR_PDF_FINAL.bat`), e constar no relatório com caminho local, tamanho e link GitHub individual.
7. Links clicaveis do Antigravity podem abrir a pasta de entrega limpa ou o arquivo individual, conforme o pedido do usuario.

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
1. Consultar primeiro o WidePay (carnês, cobranças/boletos) para listar clientes ativos.
2. Cruzar nomes repetidos para evitar duplicidade.
3. Consolidar todos os registros do mesmo cliente/lote.
4. Classificar cada nome encontrado como: "Ativo confirmado", "Sem evidência financeira ativa" ou "Pendente de conferência".
5. Não excluir cliente apenas porque não encontrou contrato local. Manter na tabela com "Contrato local não encontrado — pendente de conferência."
6. Informar obrigatoriamente no final: total de nomes avaliados, total de clientes ativos confirmados, total de inativos/sem evidência e total de pendentes, bem como eventuais limites de consultas.

Esta checagem deve ser feita de forma automatizada e dinâmica, devendo ser executada mesmo sob comandos curtos.

---

## REGRA 27 — Login WidePay com Autopreenchimento Seguro do Navegador

Quando o WidePay abrir na tela de login, o Antigravity/Codex não deve encerrar o processo, não deve reiniciar a tarefa e não deve pedir para eu repetir o comando completo.

Antes de pedir minha intervenção manual, ele pode verificar apenas visualmente se o navegador dedicado já preencheu automaticamente os campos de login pelo próprio recurso de autofill/senha salva do navegador.

Essa verificação deve ser feita de forma segura, sem ler, copiar, exibir, extrair ou armazenar senha.

### Comportamento permitido

Se a tela de login estiver aberta e os campos já estiverem preenchidos automaticamente pelo navegador, o Antigravity/Codex pode:

1. Clicar no botão “Entrar”, “Acessar”, “Login” ou equivalente;
2. Pressionar Enter, se isso apenas confirmar o login já preenchido;
3. Aguardar o carregamento da área logada;
4. Confirmar que saiu da tela de login;
5. Continuar exatamente do ponto em que parou.

O agente pode reconhecer visualmente que o campo de senha está preenchido quando aparecer mascarado, por exemplo com bolinhas ou pontos, mas não pode tentar ler o conteúdo do campo.

### Restrições obrigatórias de segurança

O Antigravity/Codex não deve, em hipótese alguma:

1. Ler minha senha;
2. Copiar minha senha;
3. Exibir minha senha;
4. Salvar minha senha em arquivo, log, print, cache, script ou variável;
5. Digitar senha manualmente;
6. Alterar senha;
7. Acessar o gerenciador de senhas do navegador;
8. Usar DevTools para ler campos sensíveis;
9. Ler o atributo `value` de campo `password`;
10. Exportar, consultar ou manipular credenciais salvas;
11. Tentar burlar autenticação;
12. Prosseguir sozinho se aparecer captcha, 2FA, código por SMS/e-mail, confirmação sensível ou bloqueio de segurança.

### Se o navegador preencher automaticamente

Se o navegador já tiver preenchido os campos e faltar apenas confirmar o acesso, o Antigravity/Codex pode clicar em “Entrar” ou pressionar Enter.

Depois disso, deve aguardar a área logada carregar e continuar o processo exatamente do ponto atual, sem reiniciar a tarefa.

### Se o navegador não preencher automaticamente

Se os campos estiverem vazios, se o login salvo não aparecer, se houver captcha, 2FA, código por SMS/e-mail, confirmação sensível ou qualquer dúvida, o Antigravity/Codex deve parar e responder:

“O WidePay está na tela de login. O navegador não preencheu automaticamente os dados ou há confirmação manual necessária. Faça login manualmente na janela dedicada. Vou aguardar sua confirmação e depois continuo exatamente do ponto atual.”

### Respostas aceitas do usuário

Após o login manual, aceitar como autorização para continuar respostas como:

* “Logado”
* “Pode continuar”
* “Já entrei”
* “Pode seguir”
* “Continue”
* “Pronto”

### Objetivo da regra

Reduzir intervenção manual desnecessária quando o navegador dedicado já possui sessão ou preenchimento automático seguro, mantendo a proteção total das credenciais.

O Antigravity/Codex pode apenas confirmar o login já preenchido pelo navegador.

Se exigir senha manual, captcha, 2FA, código externo ou qualquer confirmação sensível, deve aguardar minha intervenção.

### Versão curta da regra

Se o WidePay abrir na tela de login e o navegador já preencher os campos automaticamente, pode clicar em “Entrar” e continuar. Não leia, copie, extraia, salve, exiba nem digite minha senha. Não use DevTools nem gerenciador de senhas. Se os campos estiverem vazios, houver captcha, 2FA, código externo ou qualquer dúvida, pare e aguarde meu login manual.

---


## REGRA 28 — Foco no resultado final: relatórios de todos os clientes com eficiência

O objetivo principal dos fluxos do WidePay não é narrar cada etapa, criar timers, fazer verificações repetidas ou consumir contexto explicando o processo.

O objetivo principal é:

**gerar e entregar os relatórios financeiros de todos os clientes solicitados, com segurança, conferência e o menor consumo possível de tempo, contexto e tokens.**

### Interpretação obrigatória da intenção do usuário

Quando o usuário pedir levantamento, conferência, extração ou relatório de clientes do WidePay, a IA deve interpretar que o usuário quer o **resultado final organizado**, e não acompanhamento passo a passo desnecessário.

A IA deve agir como executor operacional, tomando decisões simples e seguras sozinho, sem pedir confirmação para cada microetapa.

### Comportamento obrigatório

Sempre que possível, a IA deve:

1. Automatizar processos repetitivos.
2. Processar clientes em lote.
3. Reaproveitar sessão, navegador, scripts e dados já coletados.
4. Evitar repetir buscas ou extrações já feitas.
5. Evitar narrar esperas longas.
6. Evitar timers repetidos.
7. Evitar mensagens intermediárias sem valor.
8. Consolidar erros, pendências e dados parciais em um único resumo.
9. Continuar o fluxo até entregar os relatórios ou até encontrar bloqueio real.
10. Só pedir intervenção do usuário quando houver login, 2FA, erro crítico, dúvida de dados ou risco de alterar algo indevidamente.

### O que deve ser evitado

É proibido transformar a tarefa em uma sequência longa de mensagens como:

* “vou verificar”;
* “vou aguardar”;
* “vou tentar novamente”;
* “timer expirou”;
* “vou abrir outro timer”;
* “vou analisar mais um pouco”;
* “preciso confirmar cada cliente”;
* “vou fazer cliente por cliente manualmente sem necessidade”.

Essas mensagens gastam contexto e tokens sem aproximar o usuário do resultado final.

### Estratégia correta

Para relatórios de vários clientes, a IA deve trabalhar assim:

1. Identificar a lista de clientes.
2. Extrair dados do WidePay da forma mais automatizada possível.
3. Consultar carnês, cobranças, contatos e pagamentos sem repetir passos desnecessários.
4. Validar cobertura dos dados.
5. Gerar os relatórios finais no padrão do projeto.
6. Separar clientes concluídos, clientes com pendência e clientes com erro.
7. Apresentar ao usuário um resumo objetivo com os arquivos gerados.

### Quando houver demora ou travamento

Se uma extração demorar, a IA deve verificar o status real uma única vez e responder de forma objetiva:

“A extração está demorando. Verifiquei o status: [rodando/travado]. Última etapa: [etapa]. Último log relevante: [log]. Dados parciais disponíveis: [sim/não]. Deseja que eu aguarde mais uma vez, interrompa com segurança ou apresente os dados parciais?”

Não criar timers repetidos.
Não narrar espera infinita.
Não continuar consumindo contexto sem avanço real.

### Entrega esperada

Ao final, a IA deve entregar:

* relatórios gerados;
* caminho local dos arquivos;
* links GitHub reais, se houver commit/push;
* lista de clientes concluídos;
* lista de clientes com pendência;
* lista de clientes com erro;
* resumo curto do que foi feito;
* status do precheck, se houver.

### Regra de prioridade

Sempre priorizar:

1. resultado final;
2. segurança dos dados;
3. automação;
4. economia de tokens;
5. redução de mensagens intermediárias;
6. clareza na entrega.

Nunca priorizar a narração do processo acima da entrega dos relatórios.

### Aplicação obrigatória

Aplicar esta regra em todos os fluxos do WidePay:

* levantamento preliminar;
* checagem de cobertura;
* consulta de carnês;
* consulta de cobranças;
* consulta de contatos;
* geração de relatórios;
* scripts CDP;
* scripts em segundo plano;
* extrações automatizadas;
* relatórios individuais;
* relatórios em lote;
* relatórios de todos os clientes.

---

## REGRA 29 — NÃO ACESSAR CONFIGURAÇÕES/CONTATOS DO WIDEPAY PARA RELATÓRIOS

O Antigravity/Codex não deve acessar a área:

`https://www.widepay.com/conta/configuracoes/contatos`

nem a seção:

`Configurações > Contatos`

para fazer levantamento financeiro dos clientes do loteamento.

Essa página contém contatos de transferências, dados bancários, favoritos, contatos seguros e outras informações sensíveis que não são necessárias para gerar relatórios financeiros dos lotes.

### Fontes permitidas para relatórios financeiros

Para relatórios WidePay, usar somente as áreas financeiras:

1. Carnês:
   `https://www.widepay.com/conta/recebimentos/carnes`

2. Cobranças/boletos:
   `https://www.widepay.com/conta/recebimentos`

3. Dados visíveis dentro dos próprios carnês, parcelas, cobranças e boletos.

### Comportamento obrigatório

Quando o usuário pedir para verificar clientes, fazer preliminar, conferir A a E, gerar relatórios ou procurar clientes faltando:

1. Não entrar em Configurações > Contatos.
2. Não usar contatos de Transferências.
3. Não usar contatos bancários como lista de clientes.
4. Não acessar dados de transferência, favoritos ou contatos seguros.
5. Buscar clientes pelos registros financeiros do WidePay:
   * carnês;
   * cobranças;
   * boletos;
   * parcelas;
   * referências de pagamento.
6. Usar contratos locais apenas como apoio complementar.
7. Se precisar de algum dado da área de contatos, pedir autorização antes e explicar exatamente por que precisa.

### Regra de segurança

Não consultar, extrair, registrar, copiar, salvar ou usar dados de contatos bancários, transferências, favoritos ou contatos seguros.

O objetivo do projeto é gerar relatórios financeiros dos clientes/lotes com base em carnês, cobranças e boletos do WidePay, não acessar áreas sensíveis de configuração da conta.

---

## REGRA 30 — RESUMO OPERACIONAL LEVE E CONTROLE DE EXECUÇÃO

O Antigravity/Codex deve manter o processo controlado sem consumir tokens desnecessariamente.

O objetivo não é ficar enviando arquivos grandes, logs extensos ou regras completas toda vez.
O objetivo é manter um resumo claro, curto e atualizado do que foi feito, do que falta fazer e dos arquivos criados, para que o usuário consiga acompanhar o processo sem perder tempo.

### Comportamento obrigatório

Sempre que uma etapa importante for executada, criar ou atualizar um arquivo leve de controle:

`07_DADOS_TEMPORARIOS/RESUMO_EXECUCAO_ATUAL.md`

Esse arquivo deve funcionar como um log resumido/checkpoint da execução atual.

### O resumo deve conter somente o essencial

Registrar de forma curta:

1. Data e hora da execução;
2. Comando recebido do usuário;
3. Objetivo da etapa;
4. O que foi feito;
5. Fonte usada:
   * WidePay;
   * contrato local;
   * cache temporário;
   * arquivo já existente;
6. Clientes/lotes processados;
7. Arquivos criados ou alterados;
8. Arquivos apenas consultados;
9. Caminhos locais importantes;
10. O que está pronto;
11. O que está parcial;
12. O que está pendente;
13. Erros ou alertas importantes;
14. Próxima ação recomendada.

### Formato ideal do resumo

Usar formato curto, como:

```md
# RESUMO DA EXECUÇÃO ATUAL

Data/hora:
Comando do usuário:
Objetivo:

## Feito
- ...

## Clientes processados
| Cliente | Lote | Status | Arquivo |
|---|---|---|---|

## Arquivos criados/alterados
| Arquivo | Tipo | Caminho | Status |
|---|---|---|---|

## Pendências
- ...

## Próximo passo recomendado
- ...
```

### Evitar consumo desnecessário de tokens

Não enviar arquivos inteiros no chat sem necessidade.
Não colar logs extensos.
Não repetir regra-base inteira.
Não listar conteúdo completo de arquivos grandes.
Não mandar código inteiro se o usuário não pediu.

Quando precisar informar o andamento, mandar no chat apenas:
* resumo do que foi feito;
* caminhos dos arquivos;
* status;
* pendências;
* próximo passo.

### Regras resumidas

Criar também um resumo curto das regras principais do projeto:

`05_PROMPTS_E_REGRAS/RESUMO_REGRAS_OPERACIONAIS_WIDEPAY.md`

Esse arquivo deve resumir as regras mais importantes para consulta rápida, sem substituir a regra-base completa.

Deve conter, de forma curta:
1. WidePay é fonte principal;
2. Contratos locais são apenas apoio;
3. Não acessar Configurações > Contatos;
4. Não confundir iniciais de nomes com quadras;
5. Login com autopreenchimento seguro;
6. Não criar timers repetidos;
7. Não gerar arquivos finais sem aprovação;
8. Não alterar nada no WidePay;
9. Não usar contratos como lista principal;
10. Não inventar valores;
11. Somar todos os carnês e boletos antes de informar total pago geral;
12. Registrar arquivos locais x GitHub.

### Quando o usuário pedir status

Se o usuário perguntar “o que foi feito?”, “cadê os arquivos?”, “funcionou?”, “o que falta?” ou “me mostre o andamento”, responder com base no `RESUMO_EXECUCAO_ATUAL.md`, sem reler tudo desnecessariamente.

### Quando criar arquivos finais

Ao gerar relatórios, planilhas ou documentos finais, atualizar o resumo com:
* nome do cliente;
* lote;
* tipo de arquivo;
* caminho local;
* se foi ou não enviado ao GitHub;
* commit, se houver;
* se está pronto, parcial ou pendente.

### Controle GitHub

Sempre separar:

#### Arquivos apenas locais
* caminho local;
* motivo de ainda não terem commit/push.

#### Arquivos enviados ao GitHub
* caminho local;
* link GitHub real;
* commit;
* branch;
* status do push.

### Objetivo final

Manter o processo rápido, rastreável e eficiente.
Manter o processo rápido, rastreável e eficiente.
O Antigravity/Codex deve entregar os relatórios e resultados ao usuário, sem transformar cada etapa em leitura longa de arquivos, logs enormes ou explicações técnicas desnecessárias.

---

## REGRA 31 — ESPELHO OPERACIONAL LEVE NO GITHUB

### 1. Princípio principal

O GitHub deve funcionar como um painel de controle leve do projeto, não como uma duplicação pesada da pasta local.
O controle deve ser: leve, objetivo, rápido de atualizar, fácil de revisar, sem logs gigantes, sem excesso de texto, sem duplicação de dados sensíveis, sem interferir na execução principal e sem criar arquivos novos sem necessidade.
O objetivo final continua sendo entregar relatórios financeiros corretos dos clientes, não criar burocracia.

### 2. Arquivo principal obrigatório

Criar ou manter atualizado:
`05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md`
Esse será o arquivo principal para o ChatGPT revisar o andamento do projeto pelo GitHub. Ele deve conter apenas informações essenciais.

### 3. Conteúdo mínimo do painel

O painel deve informar:
1. Data da última atualização;
2. Último comando executado;
3. Estado atual do processo;
4. Último commit;
5. Branch atual;
6. Link GitHub do próprio painel;
7. Clientes já acessados;
8. Clientes com relatório gerado;
9. Clientes pendentes;
10. Clientes sem evidência financeira no WidePay;
11. Arquivos locais sensíveis não enviados ao GitHub;
12. Arquivos enviados ao GitHub;
13. Erros identificados;
14. Correções aplicadas;
15. Se a entrega atual está completa, parcial ou pendente;
16. Próximo passo recomendado.

### 4. Controle de clientes

Manter no painel uma tabela curta:
| Cliente | Inicial | Lote | Fonte WidePay | Status WidePay | Relatório | Arquivo local | GitHub | Pendência |
|---|---|---|---|---|---|---|---|---|

Status permitidos: `Acessado`, `Não acessado`, `Relatório gerado`, `Pendente`, `Sem evidência financeira`, `Erro`, `Revisar`, `Pronto`, `Parcial`.

### 5. Resumo do que foi extraído do WidePay

O painel deve conter uma seção chamada `RESUMO DA EXTRAÇÃO WIDEPAY`. Essa seção deve informar, de forma resumida e sem expor dados financeiros sensíveis:
* data da extração;
* áreas consultadas (Carnês e Cobranças/Boletos);
* clientes encontrados e não encontrados;
* clientes com carnê e com cobrança/boleto;
* clientes com dados parciais ou que precisam de conferência individual;
* erros ou limitações da extração;
* se a cobertura foi completa ou incompleta.

Não incluir valores financeiros detalhados no GitHub sem autorização. Se necessário, usar termos como: "há parcelas vencidas", "há carnês ativos", "dados financeiros sensíveis mantidos localmente".

### 6. Conferência do que foi pedido x entregue

O painel deve conter uma seção `PEDIDO DO USUÁRIO X ENTREGA` com a tabela:
| Pedido do usuário | Entregue? | Arquivo/resultado | Status | Pendência |
|---|---|---|---|---|

Isso é obrigatório para evitar que se declare concluído um pedido que foi apenas parcialmente entregue.

### 7. Arquivos locais sensíveis

Arquivos com dados financeiros ou pessoais de clientes não devem ser enviados ao GitHub sem autorização expressa (PDFs, HTMLs de relatórios, planilhas XLSX, contratos, JSONs do WidePay, caches). Registrar apenas a existência desses arquivos no painel usando:
`Não enviado — arquivo sensível` no campo de status do GitHub.

### 8. Arquivos permitidos no GitHub

Podem ser enviados ao GitHub: regras, scripts, precheck, auditorias sem dados financeiros pessoais, resumos operacionais, painel operacional, registros de processo, mapas técnicos e históricos de erros.

### 9. Não criar arquivos novos sem necessidade

Antes de criar um novo arquivo de controle, verificar se o `PAINEL_OPERACIONAL_WIDEPAY.md` já resolve. Evitar logs pequenos ou auditorias longas redundantes.

### 10. Erros críticos que não podem se repetir

Manter no painel uma seção `ERROS CRÍTICOS QUE NÃO PODEM SE REPETIR` com os itens:
1. Não confundir iniciais dos nomes com quadras;
2. `A a E` significa iniciais dos nomes dos clientes, não quadras;
3. Não usar contratos locais como fonte principal;
4. Não acessar `Configurações > Contatos`;
5. Usar apenas `Carnês` e `Cobranças/Boletos` no WidePay;
6. Não criar timers repetidos;
7. Não gerar arquivos finais sem autorização;
8. Não enviar dados financeiros sensíveis ao GitHub sem autorização;
9. Não calcular total pago geral usando apenas um carnê quando houver vários;
10. Não inventar valores, datas, parcelas, clientes ou lotes.

### 11. Fluxo após cada etapa importante

Depois de concluir uma etapa importante:
1. Atualizar o `PAINEL_OPERACIONAL_WIDEPAY.md`;
2. Registrar apenas o essencial;
3. Separar arquivos locais sensíveis dos permitidos;
4. Fazer commit/push apenas dos arquivos não sensíveis;
5. Informar no chat os links e status atualizados.

### 12. Segurança obrigatória

Não enviar ao GitHub dados financeiros ou pessoais de clientes sem autorização expressa. Se o arquivo for sensível, registrar como `Não enviado — arquivo sensível`.

---

## REGRA 32 — RASTREABILIDADE GITHUB OBRIGATORIA DE TUDO O QUE FOR FEITO

### 1. Objetivo

Todo arquivo criado, alterado, consultado como evidencia, copiado, gerado, usado em teste, relatorio, erro, auditoria ou conferencia deve ter rastreabilidade no GitHub por meio de um arquivo completo publicado ou de um registro sanitizado no painel operacional.

### 2. Classificacao obrigatoria

1. Arquivo completo enviado ao GitHub quando nao houver dado sensivel ou quando houver autorizacao expressa.
2. Arquivo sensivel mantido localmente, mas registrado no painel ou indice sanitizado do GitHub.
3. Versao sanitizada enviada ao GitHub quando for possivel remover os dados financeiros sensiveis sem perder a utilidade operacional.

### 3. Painel obrigatorio

Manter sempre atualizado:
`05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md`

O painel deve registrar:
* nome do arquivo;
* caminho local;
* tipo;
* cliente ou lote relacionado;
* acao executada;
* motivo de nao envio completo;
* status;
* data e hora;
* proximo passo.

### 4. Regra de bloqueio

Se um arquivo foi criado, alterado ou usado e nao possui link GitHub completo ou registro sanitizado no painel ou indice, a etapa permanece incompleta.

### 5. Regra de erro

Todo erro de conferencia, cache antigo, JSON desatualizado, arquivo invalido ou consulta sem validacao atual deve ser registrado no painel com:
* causa;
* arquivos afetados;
* decisao de contecao;
* status final;
* proximo passo seguro.





