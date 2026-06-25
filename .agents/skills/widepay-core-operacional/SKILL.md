---
name: widepay-core-operacional
description: Usar sempre que o pedido envolver WidePay, cliente, contrato, lote, quadra, parcelas, carnes, cobranca, busca de cliente ou conferencia financeira.
---
# Skill: widepay-core-operacional

Esta skill centraliza as regras de negocio, auditoria financeira, busca de clientes e seguranca do projeto `Relatorio_WidePay_Lotes`.

## 0. Regra Zero
**WidePay primeiro, contratos depois.**
Esta ordem tem prioridade acima de qualquer outro fluxo desta skill.

## 1. Prioridade
**Maxima operacional.** Depois da Regra Zero, esta skill sobrescreve orientacoes gerais de desenvolvimento e direciona o fluxo de checagem.

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
4. **Consulta segura:** chamar `ensure_widepay_logged_in()` para conectar ao Opera dedicado (`localhost:9444`) e acessar apenas `Recebimentos > Carnes` e `Recebimentos > Cobrancas/Boletos`.
5. **Arquivo de conferencia:** salvar o log detalhado em `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_[CLIENTE].md`.

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
PRECHECK LOGIN WIDEPAY: perfil persistente Opera/CDP obrigatorio
ensure_widepay_logged_in(): iniciado
```

## 8. Erros proibidos
* **ERRO 1:** Confundir iniciais dos nomes dos clientes com a letra da quadra/lote (ex: "Alex" pertence ao escopo A a E, embora seu lote B2 esteja na Quadra B).
* **ERRO 2:** Acessar a pagina de configuracoes `Configuracoes > Contatos` ou transferencias.
* **ERRO 3:** Simular dados financeiros falsos ou preencher dados de quitacao quando o WidePay nao pode ser consultado.
* **ERRO 4:** Calcular o total pago geral considerando apenas o primeiro carne do cliente quando houver multiplos carnes ativos ou finalizados.
* **ERRO 5:** Tentar fechar lista oficial por arquivos locais antes da consulta WidePay.
* **ERRO 6:** fluxo local-first bloqueado.

## 9. Critérios de validação
* Normalizacao rigorosa de nomes (remover termos como "Contrato", "Copia", "Leo/Leo").
* WidePay define quem existe financeiramente; contratos locais apenas complementam depois da consulta.
* Cobertura A a E baseada estritamente nas iniciais reais dos nomes.
* Tabela de pendencias atualizada sem dados financeiros sensiveis expostos no GitHub publico.

## 10. Painel operacional publico
Quando o painel operacional publico for alterado, consolidado ou limpo, o fluxo deve seguir a versao publicada, rodar precheck, fazer commit, fazer push e conferir o GitHub normal e o raw antes de encerrar.
O painel nao deve manter restos como `19 x 21`, `Heron Souza Dias`, `cb8c5c8` ou fotografias antigas de auditoria quando o objetivo for versao limpa.

## 11. Precheck relacionado
* O script de validacao `precheck_regras.py` valida a presenca deste arquivo, da Regra Zero e das 9 regras numeradas em `REGRAS_PERSISTENTES_DO_PROJETO.md`.

## 12. Exemplos curtos de decisao
* *Cenario:* O usuario pede checagem do cliente "Alex Santos de Azevedo" (Lote B2).
* *Decisao:* A inicial do nome e "A". Executar auditoria, mas a confirmacao financeira deve comecar no WidePay antes de qualquer apoio local.
* *Cenario:* O script CDP falha ao conectar ou a pagina de login esta sem senha salva.
* *Decisao:* Interromper imediatamente, registrar `WIDEPAY NAO CONSULTADO - AGUARDANDO LOGIN MANUAL` e solicitar acao do usuario.
* *Cenario:* O usuario pede somente busca local nos contratos.
* *Decisao:* Permitir a leitura local, mas marcar o resultado como `PRELIMINAR - NAO VALIDADO NO WIDEPAY`.
