# 04 - Diagnóstico de Dados e Persistência (Versão Sanitizada)

## Caminhos das Bases Oficiais
* **JSON Indexado**: `WideAPP_EXTRA/data/clientes_indexados.json`
* **JSON de Cache do WidePay**: `WideAPP_EXTRA/data/widepay_boletos_cache.json`
* **Planilha XLSX Consolidada**: `BANCO_DADOS_WIDEAPP_EXTRA.xlsx`

## Contagem de Registros Persistidos
* **Registros no `clientes_indexados.json`**: 93 registros.
* **Cobranças/Carnês no Cache WidePay**: Lançamentos brutos em cache local.

## Emmanuel Félix da Costa Filho (Confirmação de Estrutura e Independência)
* **Quantidade de Linhas no JSON**: **2 linhas independentes** (G2 e G18).
* **Registro G2**:
  * `lote`: `"G2"`
  * `chave_lote_canonica`: `"G2"`
  * `lote_canonico`: `"G2"`
  * `chave_saneamento`: `"emmanuel felix da costa filho|G2"`
  * `valor_base_parcela`: `99.0`
  * `valor_total_contratado`: `4950.0`
  * `valor_total_pago`: `6313.03`
  * `ultima_parcela_paga`: `"g2 g18 30/09 apartir de 25 R198"` (referente às parcelas de G2)
* **Registro G18**:
  * `lote`: `"G18"`
  * `chave_lote_canonica`: `"G18"`
  * `lote_canonico`: `"G18"`
  * `chave_saneamento`: `"emmanuel felix da costa filho|G18"`
  * `valor_base_parcela`: `99.0`
  * `valor_total_contratado`: `4950.0`
  * `valor_total_pago`: `5977.07`
  * `ultima_parcela_paga`: `"g2 g18 30/09 apartir de 25 R198"` (referente às parcelas de G18)

## Rodrigo Monteiro de Melo (Confirmação de Descontaminação)
* **Quantidade de Linhas no JSON**: **2 linhas independentes** (F19 e G1/G19).
* **Registro F19**:
  * `lote`: `"F19"`
  * `chave_lote_canonica`: `"F19"`
  * `chave_saneamento`: `"rodrigo monteiro de melo|F19"`
* **Registro G1/G19**:
  * `lote`: `"G1/G19"`
  * `chave_lote_canonica`: `"G1/G19"`
  * `chave_saneamento`: `"rodrigo monteiro de melo|G1/G19"`
* **Interseção de Eventos (`_evento_id`)**: **ZERO interseções** entre F19 e G1/G19.

## Confirmação de Carregamento na Interface
* Ambos os registros independentes de Emmanuel (G2 e G18) e de Rodrigo (F19 e G1/G19) são lidos do JSON e populam `self.registros` e a aba Ativ. Recentes como entidades autônomas.
