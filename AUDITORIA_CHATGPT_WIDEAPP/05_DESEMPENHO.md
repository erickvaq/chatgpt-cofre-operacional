# 05 - Medição Objetiva de Desempenho

## Tempos de Importação dos Módulos Principais
* **`app.widepay_boletos_cache`**: `1.0780` segundos.
* **`app.indexador_clientes`**: `0.0109` segundos.
* **`app.interface`**: `0.3288` segundos.

## Tempos de Carregamento de Arquivos em Disco
* **Leitura do `clientes_indexados.json` (92 registros)**: `0.0104` segundos.
* **Leitura da Planilha XLSX (`BANCO_DADOS_WIDEAPP_EXTRA.xlsx`)**: `0.0295` segundos.

## Renderização e Dados da Aba Ativ. Recentes
* **Tempo de Iteração e Montagem do Grid de Pagamentos Recentes**: `0.0001` segundos.

## Re-leituras de Disco na Inicialização e Troca de Aba
* **Frequência de Leitura no Start**: O `clientes_indexados.json` é lido exatamente **1 vez** durante a inicialização do app.
* **Frequência de Leitura ao Clicar em Ativ. Recentes**: **0 releituras de disco**. O grid consome diretamente os dados já carregados em memória no atributo `self.registros`.

## Diagnóstico da Thread Principal
* A montagem do grid consome os dados pré-indexados em memória (estruturados em `pagamentos_recentes_5m`). Não há releitura ou varredura de arquivos no disco durante o clique da aba Ativ. Recentes.
