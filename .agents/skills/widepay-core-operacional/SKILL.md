---
name: widepay-core-operacional
description: Usar sempre que o pedido envolver WidePay, cliente, contrato, lote, quadra, parcelas, carnes, cobranca, busca de cliente ou conferencia financeira.
---
# Skill: widepay-core-operacional

Esta skill centraliza as regras de negocio, auditoria financeira, busca de clientes e seguranca do projeto `Relatorio_WidePay_Lotes`.

## 0. Regra Zero
**WidePay primeiro, contratos depois.**
Esta ordem tem prioridade acima de qualquer outro fluxo desta skill.

## 0.5 Regra Universal
Esta skill vale para qualquer cliente especifico, letra unica, intervalo de letras, grupo de clientes, lote, todos os clientes, relatorio individual, relatorio consolidado, levantamento, auditoria, conferencia, lista de pendencias, pagamentos, parcelas, carnes, cobrancas ou boletos.

## 0.6 Abertura obrigatoria do WidePay real
Antes de qualquer busca, relatorio, auditoria, letra, lote, pendencia, pagamento, parcela, carne, cobranca, PDF, HTML ou XLSX, a primeira acao pratica e abrir o Google Chrome dedicado e carregar o WidePay real.
Se o Chrome/CDP nao estiver aberto, o fluxo deve tentar abrir automaticamente o navegador dedicado.
Se o CDP ja tiver aba WidePay logada, nunca fechar nem reiniciar o Chrome.
Antes de declarar login necessario, conferir `localhost:9333/json` e validar as abas reais do WidePay.
Somente depois de entrar no WidePay real pode consultar Carnes e Cobrancas/Boletos.
Somente depois disso pode usar contratos locais como apoio.
Se o WidePay real nao abrir, bloquear o fluxo com `ERRO CRITICO: WidePay real nao foi aberto. Fluxo bloqueado antes de consultar arquivos locais.`

## 1. Prioridade
**Maxima operacional.** Depois da Regra Zero, da Regra Universal e da Abertura obrigatoria do WidePay real, esta skill sobrescreve orientacoes gerais de desenvolvimento e direciona o fluxo de checagem.

## 2. Quando usar
* Busca de dados cadastrais e financeiros de clientes do loteamento.
* Cruzamento de contratos fisicos locais com lancamentos do site WidePay.
* Geracao do relatorio de conferencia Markdown em `07_DADOS_TEMPORARIOS`.
* Processamento e normalizacao de nomes, quadras e lotes.
* Automacao de login e controle de perfil de navegacao.

## 3. Quando nao usar
* Abertura direta de arquivos gerados (usar `widepay-abertura-externa`).
* Customizacao visual de relatorios ou conversao final de PDF/HTML (usar `widepay-relatorio-pdf`).

## 4. Gatilhos de ativacao
Palavras-chave: `buscar cliente`, `auditar lote`, `WidePay`, `conferir parcelas`, `loteamento`, `quadra`, `verificar A a E`.

## 5. Ordem obrigatoria das fontes
1. **WidePay primeiro:** consultar Carnes, Cobrancas/Boletos, identificar clientes com evidencia financeira, localizar carnes ativos, finalizados, pagos, pendentes e cancelados, e consolidar registros repetidos do mesmo cliente/lote.
2. **Contratos locais depois:** usar contratos locais apenas como apoio, confirmar lote, confirmar nome completo, conferir contrato fisico e complementar dados ausentes.
3. **Lista preliminar quando faltar WidePay:** se o WidePay ainda nao foi consultado, qualquer lista baseada em arquivos locais deve receber a marca `LISTA LOCAL PRELIMINAR - PENDENTE DE VALIDACAO WIDEPAY`.
4. **Consulta segura:** chamar `ensure_widepay_logged_in()` para conectar ao Google Chrome dedicado (`localhost:9333`) e acessar apenas `Recebimentos > Carnes` e `Recebimentos > Cobrancas/Boletos`.
5. **Arquivo de conferencia:** salvar o log detalhado em `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_[CLIENTE].md`.
6. **Base estruturada e consolidado:** quando houver mais de um cliente, manter a base local em `07_DADOS_TEMPORARIOS` e garantir que o fluxo consolidado nasÃ§a do WidePay antes de qualquer apoio local.

## 5.1 Parcelas restantes somente pelo contrato
* WidePay confirma pagamentos, cobrancas, carnes e status financeiro.
* O total de parcelas do contrato vem somente do contrato fisico/local confirmado.
* Parcelas restantes = total de parcelas do contrato confirmado menos parcelas pagas confirmadas.
* Nunca usar parcelas geradas no WidePay como substituto do total do contrato.
* Se o contrato nao confirmar o total de parcelas, marcar `CONTRATO NAO CONFIRMADO - PARCELAS RESTANTES BLOQUEADAS` e bloquear XLS/XLSX/PDF/HTML final com numero de restantes.
* O total pago do terreno/lote deve somar carnÃªs pagos e cobranÃ§as/boletos recebidos do mesmo cliente.
* Alias e erros de digitacao comuns do nome do cliente podem ser aceitos quando a evidencia financeira e o contrato apontarem para o mesmo lote (ex.: `Edmilson` e `Edimson`).
* Todo relatorio de cliente deve consultar e listar todos os carnes e todas as cobrancas/boletos pagos ou em aberto localizados no WidePay.
* Se o navegador dedicado ja tiver usuario ou senha salvos, usar o autopreenchimento e tentar login automatico antes de pedir intervencao manual.

## 5.2 Interpretacao individual de pagamentos WidePay
* A regra e universal e nunca pode usar Edmilson, R$ 99,00 ou 100 parcelas como padrao global.
* Cada recebimento com status `Recebido` deve ser interpretado separadamente.
* Total pago do terreno/lote = soma dos valores recebidos no WidePay com status `Recebido` pertencentes ao cliente/lote correto.
* Parcelas pagas equivalentes = parcelas quitadas por carnes recebidos + parcelas quitadas por boletos avulsos/cobrancas recebidas.
* A interpretacao deve priorizar descricao original, referencias/competencias, vencimento, pagamento, valor original/base e valor base da parcela do contrato.
* Valor recebido serve como confirmacao financeira e pode conter juros, multa ou acrescimos; nao usar sozinho para dividir parcelas.
* Se a descricao indicar meses/referencias, ela prevalece sobre divisao por valor.
* Se nao houver referencia clara, marcar `REFERENCIA NAO IDENTIFICADA` e nao inventar parcela.
* Relatorio final deve conter a tabela `Pagamentos Recebidos Interpretados`.

## 6. Rotinas e scripts relacionados
* `python 03_SCRIPTS\buscar_cliente.py <nome>`
* `python 03_SCRIPTS\consultar_widepay_cdp.py --cliente <nome>`
* `python 03_SCRIPTS\gerar_conferencia_cliente.py`

## 7. Logs obrigatorios
Ao iniciar a execucao, imprimir no console:
```text
SKILL CARREGADA: widepay-core-operacional
REGRA ZERO: WIDEPAY PRIMEIRO
PRECHECK SKILLS: aprovado
PRECHECK LOGIN WIDEPAY: perfil persistente Chrome/CDP obrigatorio
ensure_widepay_logged_in(): iniciado
```

## 8. Erros proibidos
* **ERRO 1:** Confundir iniciais dos nomes dos clientes com a letra da quadra/lote (ex: "Alex" pertence ao escopo A a E, embora seu lote B2 esteja na Quadra B).
* **ERRO 2:** Acessar a pagina de configuracoes `Configuracoes > Contatos` ou transferencias.
* **ERRO 3:** Simular dados financeiros falsos ou preencher dados de quitacao quando o WidePay nao pode ser consultado.
* **ERRO 4:** Calcular o total pago geral considerando apenas o primeiro carne do cliente quando houver multiplos carnes ativos ou finalizados.
* **ERRO 5:** Tentar fechar lista oficial por arquivos locais antes da consulta WidePay.
* **ERRO 6:** fluxo local-first bloqueado.
* **ERRO 7:** WidePay real nao foi aberto.
* **ERRO 8:** Calcular parcelas restantes usando parcelas geradas no WidePay em vez do total do contrato confirmado.
* **ERRO 9:** Ignorar alias ou erro de digitacao comum do cliente e deixar de contabilizar boletos pagos do mesmo lote.
* **ERRO 10:** Gerar relatorio de cliente omitindo cobrancas/boletos pagos ou em aberto encontrados no WidePay.
* **ERRO 11:** Pedir login manual sem antes tentar usar usuario/senha ja salvos no navegador dedicado.
* **ERRO 12:** Gerar relatorio final sem interpretar individualmente todos os recebimentos `Recebido` do WidePay.
* **ERRO 13:** Usar regra fixa de outro cliente para calcular parcelas pagas equivalentes.

## 9. CritÃ©rios de validaÃ§Ã£o
* Normalizacao rigorosa de nomes (remover termos como "Contrato", "Copia", "Leo/Leo").
* WidePay define quem existe financeiramente; contratos locais apenas complementam depois da consulta.
* Parcelas restantes devem ser compativeis somente com o contrato confirmado.
* Total pago do terreno/lote inclui carnÃªs pagos e cobrancas/boletos recebidos do mesmo cliente.
* Cobertura A a E baseada estritamente nas iniciais reais dos nomes.
* Tabela de pendencias atualizada incluindo a rastreabilidade do arquivo completo.

## 10. Painel operacional publico
Quando o painel operacional publico for alterado, consolidado ou limpo, o fluxo deve seguir a versao publicada, rodar precheck, fazer commit, fazer push e conferir o GitHub normal e o raw antes de encerrar.
O painel nao deve manter restos como `19 x 21`, `Heron Souza Dias`, `cb8c5c8` ou fotografias antigas de auditoria quando o objetivo for versao limpa.

## 11. Precheck relacionado
* O script de validacao `precheck_regras.py` valida a presenca deste arquivo, da Regra Zero e das 10 regras numeradas em `REGRAS_PERSISTENTES_DO_PROJETO.md`.

## 12. Exemplos curtos de decisao
* *Cenario:* O usuario pede checagem do cliente "Alex Santos de Azevedo" (Lote B2).
* *Decisao:* A inicial do nome e "A". Executar auditoria, mas a confirmacao financeira deve comecar no WidePay antes de qualquer apoio local.
* *Cenario:* O script CDP falha ao conectar ou a pagina de login esta sem senha salva.
* *Decisao:* Interromper imediatamente, registrar `WIDEPAY NAO CONSULTADO - AGUARDANDO LOGIN MANUAL` e solicitar acao do usuario.
* *Cenario:* O usuario pede somente busca local nos contratos.
* *Decisao:* Permitir a leitura local, mas marcar o resultado como `PRELIMINAR - NAO VALIDADO NO WIDEPAY`.
