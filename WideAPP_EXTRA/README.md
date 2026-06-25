# WideAPP_EXTRA

`WideAPP_EXTRA` deve ser tratada como o nucleo da futura aplicacao independente do projeto `Relatorio_WidePay_Lotes`.

Ela nao e apenas uma pasta de scripts para execucao manual pelo Antigravity. O Antigravity deve servir como apoio de desenvolvimento, organizacao, correcao, teste e versionamento. A aplicacao final precisa executar por conta propria o fluxo completo de auditoria e geracao de relatorios financeiros WidePay.

## Objetivo

Transformar o fluxo atual em um programa local, reutilizavel e auditavel, capaz de:

- abrir ou conectar ao navegador dedicado do projeto;
- acessar o WidePay com o perfil autorizado ja configurado;
- consultar clientes, carnes, cobrancas, boletos e pagamentos recebidos;
- extrair dados reais diretamente do WidePay;
- cruzar dados do WidePay com contratos locais;
- aplicar as regras financeiras do projeto;
- identificar pagamentos confirmados, boletos avulsos, atrasos, entradas e diferencas;
- calcular total pago, parcelas pagas equivalentes e parcelas restantes;
- validar matematicamente os resultados;
- gerar relatorios em XLSX, HTML, PDF, MD e JSON;
- salvar logs, evidencias e arquivos de conferencia;
- permitir auditoria posterior de tudo que foi feito.

## Principio operacional

WidePay primeiro, contratos depois.

O programa deve usar o WidePay real como fonte primaria de pagamentos, carnes, cobrancas e boletos. Contratos locais entram depois como apoio para confirmar lote, total de parcelas, valor do contrato e regras financeiras aplicaveis.

## Forma esperada de uso

A meta e que o usuario consiga escolher um cliente, lote, letra, quadra, grupo ou conjunto de clientes e executar o fluxo completo com seguranca, controle e rastreabilidade, sem depender de comandos manuais internos do Antigravity.

Exemplos de escopo de execucao:

```powershell
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\executar_auditoria.py --cliente "NOME DO CLIENTE" --lote F05
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\executar_auditoria.py --letra A --letra-fim E --consolidado
WideAPP_EXTRA\.venv\Scripts\python.exe WideAPP_EXTRA\executar_auditoria.py --todos --consolidado
```

Esses comandos ainda representam a interface tecnica atual. A evolucao desejada e uma aplicacao propria com entrada controlada, logs claros, validacao e relatorios finais.

## Modulos internos esperados

- `login_navegador`: conexao segura com navegador dedicado e sessao WidePay.
- `extrator_widepay`: captura real de carnes, cobrancas, boletos e pagamentos.
- `leitor_contratos`: leitura e identificacao de contratos locais.
- `normalizador_pagamentos`: normalizacao, deduplicacao e interpretacao de pagamentos.
- `calculadora_financeira`: totais, parcelas equivalentes, restantes e percentuais.
- `validador_matematico`: bloqueios, alertas e conciliacao matematica.
- `gerador_relatorios`: XLSX principal, HTML/PDF complementares, MD e JSON.
- `rastreabilidade`: logs, evidencias, arquivos de conferencia e auditoria posterior.

## Regra para agentes

Nao tratar `WideAPP_EXTRA` como script temporario. Tratar como aplicacao/produto local em evolucao, com arquitetura propria, ambiente Python isolado, interface de execucao, logs, validacao matematica e rastreabilidade.
