# Handoff - WideAPP_EXTRA como aplicacao independente

## Objetivo

Registrar para o Antigravity e demais agentes que a `WideAPP_EXTRA` deve evoluir para uma aplicacao/programa independente, reutilizavel e auditavel do projeto `Relatorio_WidePay_Lotes`.

## Comando curto para o Antigravity

```text
Entenda a WideAPP_EXTRA como uma aplicacao propria, e nao como um conjunto de scripts dependentes do Antigravity.

O Antigravity deve servir apenas para desenvolver, corrigir e versionar o sistema. A aplicacao final precisa funcionar de forma independente, como um programa local capaz de acessar o WidePay, extrair dados financeiros, cruzar com contratos, aplicar as regras do projeto, validar os calculos e gerar os relatorios finais.

A meta e transformar o fluxo atual em um sistema autonomo de auditoria e geracao de relatorios WidePay, com modulos proprios, interface de execucao, ambiente Python isolado, logs, rastreabilidade, validacao matematica e geracao de XLSX, HTML, PDF, MD e JSON.

Nao tratar a WideAPP_EXTRA como script temporario. Tratar como o nucleo da futura aplicacao independente do projeto Relatorio_WidePay_Lotes.
```

## Diretrizes obrigatorias

- WidePay primeiro, contratos depois.
- Excel/XLSX e a entrega principal de relatorio financeiro.
- HTML e PDF sao complementares, salvo pedido explicito.
- O sistema deve consultar carnes, cobrancas, boletos e pagamentos recebidos.
- O sistema deve interpretar pagamentos individualmente, sem herdar constantes de outro cliente.
- Parcelas restantes devem vir do total de parcelas do contrato confirmado menos parcelas pagas confirmadas.
- O programa deve registrar logs, evidencias, arquivos de conferencia e metricas JSON.
- Nenhuma credencial deve ser lida, copiada, salva ou exposta.
- O navegador dedicado e o perfil autorizado podem ser usados como meio de acesso, mas nao como deposito de segredo no codigo.

## Proximas tarefas tecnicas seguras

1. Manter `WideAPP_EXTRA/README.md` como entrada curta do produto.
2. Manter `WideAPP_EXTRA/ARQUITETURA_APLICACAO_INDEPENDENTE.md` como contrato de arquitetura.
3. Separar claramente CLI atual de futura interface local.
4. Criar modulo de configuracao central sem credenciais.
5. Padronizar saidas em pastas por execucao.
6. Criar testes de unidade para normalizacao, calculo e validacao matematica.
7. Criar modo `--dry-run` ou `--validar` para conferir regras sem gerar entrega final.
8. Evitar sobrescrever relatorios existentes.

## Arquivos relacionados

- `WideAPP_EXTRA/README.md`
- `WideAPP_EXTRA/ARQUITETURA_APLICACAO_INDEPENDENTE.md`
- `WideAPP_EXTRA/executar_auditoria.py`
- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/STATUS_AMBIENTE_WIDEAPP_EXTRA.md`

## Status

Registrado localmente em 2026-06-25.

GitHub nao publicado nesta etapa.
