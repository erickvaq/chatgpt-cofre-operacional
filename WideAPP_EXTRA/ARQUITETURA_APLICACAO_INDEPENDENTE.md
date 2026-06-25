# Arquitetura alvo - WideAPP_EXTRA

## Decisao registrada

`WideAPP_EXTRA` e uma aplicacao propria em construcao, nao uma colecao de scripts dependentes do Antigravity.

O Antigravity pode desenvolver, corrigir, testar, organizar e versionar o sistema, mas nao deve ser requisito de execucao final. O programa deve funcionar localmente com ambiente Python isolado e fluxo proprio de auditoria financeira WidePay.

## Fronteira entre aplicacao e ferramenta de desenvolvimento

| Item | Papel correto |
|---|---|
| WideAPP_EXTRA | Aplicacao independente do projeto `Relatorio_WidePay_Lotes` |
| Antigravity | Ferramenta de desenvolvimento e manutencao |
| Navegador dedicado | Meio autorizado de acesso ao WidePay real |
| WidePay | Fonte primaria de dados financeiros |
| Contratos locais | Fonte de apoio e confirmacao contratual |
| Relatorios finais | Produto auditavel da aplicacao |

## Fluxo alvo

1. Inicializar ambiente Python isolado.
2. Carregar regras persistentes e precheck do projeto.
3. Conectar ao navegador dedicado do WidePay ou abrir o perfil autorizado.
4. Validar sessao real do WidePay.
5. Selecionar escopo: cliente, lote, letra, intervalo, quadra, grupo ou todos.
6. Consultar WidePay primeiro:
   - carnes;
   - cobrancas;
   - boletos;
   - pagamentos recebidos;
   - status aberto, recebido, pago, atrasado, cancelado ou divergente.
7. Ler contratos locais apenas depois da coleta WidePay.
8. Cruzar WidePay com contrato e lote.
9. Normalizar pagamentos e remover duplicidades.
10. Interpretar recebimentos individualmente.
11. Calcular:
    - total pago;
    - parcelas pagas equivalentes;
    - parcelas restantes;
    - atraso;
    - entrada;
    - diferencas;
    - percentuais financeiros e percentuais de parcelas.
12. Validar matematicamente.
13. Gerar saidas:
    - XLSX principal;
    - HTML complementar;
    - PDF complementar quando solicitado;
    - MD de conferencia;
    - JSON de metricas e rastreabilidade.
14. Salvar logs, evidencias e resumo de execucao.
15. Permitir auditoria posterior pelo caminho dos arquivos e logs.

## Requisitos de independencia

- Nao depender de terminal especifico do Antigravity para execucao final.
- Nao depender de estado manual invisivel da IDE.
- Nao armazenar senha, token, cookie ou credencial em arquivo.
- Reaproveitar apenas o perfil autorizado do navegador dedicado.
- Bloquear execucao se o WidePay real nao estiver acessivel.
- Separar codigo de aplicacao, logs, dados temporarios e relatorios finais.
- Manter comandos reproduziveis por `.venv`.
- Registrar erros de forma legivel e rastreavel.

## Interface esperada

Fase atual:

- CLI tecnica com `executar_auditoria.py`.
- Ambiente `.venv`.
- Arquivos de configuracao e logs locais.

Fase alvo:

- interface local de execucao para selecionar escopo;
- botao ou comando controlado para iniciar auditoria;
- painel de status e erros;
- relatorio final com links locais;
- historico de execucoes;
- modo de auditoria sem sobrescrever entregas antigas.

## Criterio de pronto

A `WideAPP_EXTRA` so deve ser considerada madura quando conseguir executar, fora do Antigravity, o fluxo completo:

```text
selecionar escopo -> abrir/conectar WidePay -> extrair dados reais -> cruzar contratos -> calcular -> validar -> gerar XLSX/HTML/PDF/MD/JSON -> registrar evidencias
```

Qualquer etapa simulada, manual ou dependente de comando interno da IDE deve ser marcada como pendente.
