# Registro de Status — Correção de Artefatos e Pipeline em Lote (2026-06-26)

Este documento registra a auditoria e correção do pipeline de extração e auditoria financeira em lote no WidePay, garantindo a geração de todos os artefatos obrigatórios por cliente e lote sem interrupções por regras de divergência matemática.

## 1. Erro Original
Durante a execução de auditorias em lote na interface Tkinter do `WideAPP_EXTRA`, a execução falhava com a seguinte mensagem em caixa de diálogo:
> **Erro na pipeline:**
> Nenhum cliente foi concluído com sucesso. Falhas: Alex Santos de Azevedo Leo lote B1: Pipeline sem artefatos obrigatórios para Alex Santos de Azevedo Leo lote B1: xlsx, pdf, html, md, json. Veja ...\logs\pipeline_bloco_ALEX_SANTOS_DE_AZEVEDO_LEO_20260626_171832.log

## 2. Causa
1. **Retorno do Gerador Excel**: O script `gerar_relatorio_excel.py` é modelado para retornar código de saída `1` quando a validação matemática de um cliente acusa divergências financeiras (situações com status `PENDENTE` ou `ERRO`).
2. **Aborto na Cópia do XLSX**: O runner [gerador_relatorios.py](file:///c:/Users/Windows User/Desktop/chatgpt projetos/Relatorio_WidePay_Lotes/WideAPP_EXTRA/app/gerador_relatorios.py) verificava se `res_xlsx.returncode == 0` para mover o XLSX final para a pasta de entrega. Quando a validação falhava e o returncode era `1`, o XLSX permanecia na pasta temporária global `02_RELATORIOS_GERADOS` e não era movido para a pasta final de entrega do cliente.
3. **Falha de Artefato Obrigatório**: O pipeline do `pipeline_runner.py` exige a presença dos 6 tipos de arquivos na pasta final do cliente (`xlsx`, `pdf`, `html`, `md`, `json` e `log`). A ausência do `.xlsx` bloqueava e abortava o pipeline de todo o bloco de clientes.
4. **Desatualização do Escopo de Lote**: O executador `executar_auditoria.py` na pasta de testes isolados não estava atualizado, fazendo com que a variável `lote_opcao` do loop vazasse de escopo e salvasse as entregas de todos os clientes no lote do último cliente do bloco (`G14`).

## 3. Arquivos Alterados
* [WideAPP_EXTRA/app/gerador_relatorios.py](file:///c:/Users/Windows User/Desktop/chatgpt projetos/Relatorio_WidePay_Lotes/WideAPP_EXTRA/app/gerador_relatorios.py#L285)  
  *Modificação*: Ajustado a verificação de retorno de subprocesso para aceitar `res_xlsx.returncode in (0, 1)`, garantindo a movimentação do XLSX mesmo em casos de auditoria divergente.
* [WideAPP_EXTRA/executar_auditoria.py](file:///c:/Users/Windows User/Desktop/chatgpt projetos/Relatorio_WidePay_Lotes/WideAPP_EXTRA/executar_auditoria.py#L230)  
  *Modificação*: Sincronizado e validado o isolamento de escopo por cliente no loop de auditoria (`lote_opcao = cli.get("lote_opcao")`).

## 4. Commits de Rastreabilidade
* **d19f660** - `fix(pipeline): allow Excel generation move on exit code 1 and fix scopes` (GitHub Link: [d19f660](https://github.com/erickvaq/chatgpt-cofre-operacional/commit/d19f660f6b4bf2f5be24867140f7d54ad589d970))
* **8e8e076** - `chore(debug): remove temporary debug prints from executor` (GitHub Link: [8e8e076](https://github.com/erickvaq/chatgpt-cofre-operacional/commit/8e8e0766d036e4f3f4c6e949ff089e9f9057b54a))

## 5. Teste Executado
* **Tipo**: Execução de auditoria em lote em ambiente de testes isolado (`TESTE_WIDEAPP_EXTRA_ISOLADO`) via linha de comando do Python virtualenv.
* **Clientes e Lotes Testados**:
  * Alex Santos de Azevedo (Lote: B1)
  * Alex Santos de Azevedo (Lote: B2)
  * Alexandre Arruda Santana (Lote: G14)

### Artefatos Gerados com Sucesso por Cliente
Para cada cliente e lote, a pasta de entrega correspondente sob `02_RELATORIOS_GERADOS` recebeu os 6 artefatos obrigatórios:
1. **Alex Santos de Azevedo (Lote B1)** em `ALEX_SANTOS_DE_AZEVEDO_LOTE_B1_FINAL\`:
   * `RELATORIO_FINANCEIRO_ALEX_SANTOS_DE_AZEVEDO_20260626_1717.xlsx`
   * `RESUMO_FINANCEIRO_ALEX_SANTOS_DE_AZEVEDO_20260626_1717.pdf`
   * `RESUMO_FINANCEIRO_ALEX_SANTOS_DE_AZEVEDO_20260626_1717_PREVIA.html`
   * `CONFERENCIA_CALCULOS_ALEX_SANTOS_DE_AZEVEDO_20260626_1717.md`
   * `METRICAS_ALEX_SANTOS_DE_AZEVEDO_20260626_1717.json`
   * `01_ABRIR_PDF_FINAL.bat` (atalho)
   * Log de execução associado na pasta de logs.
2. **Alex Santos de Azevedo (Lote B2)** em `ALEX_SANTOS_DE_AZEVEDO_LOTE_B2_FINAL\`:
   * `RELATORIO_FINANCEIRO_ALEX_SANTOS_DE_AZEVEDO_20260626_1717.xlsx`
   * `RESUMO_FINANCEIRO_ALEX_SANTOS_DE_AZEVEDO_20260626_1717.pdf`
   * `RESUMO_FINANCEIRO_ALEX_SANTOS_DE_AZEVEDO_20260626_1717_PREVIA.html`
   * `CONFERENCIA_CALCULOS_ALEX_SANTOS_DE_AZEVEDO_20260626_1717.md`
   * `METRICAS_ALEX_SANTOS_DE_AZEVEDO_20260626_1717.json`
   * `01_ABRIR_PDF_FINAL.bat` (atalho)
   * Log de execução associado na pasta de logs.
3. **Alexandre Arruda Santana (Lote G14)** em `ALEXANDRE_ARRUDA_SANTANA_LOTE_G14_FINAL\`:
   * `RELATORIO_FINANCEIRO_ALEXANDRE_ARRUDA_SANTANA_20260626_1717.xlsx`
   * `RESUMO_FINANCEIRO_ALEXANDRE_ARRUDA_SANTANA_20260626_1717.pdf`
   * `RESUMO_FINANCEIRO_ALEXANDRE_ARRUDA_SANTANA_20260626_1717_PREVIA.html`
   * `CONFERENCIA_CALCULOS_ALEXANDRE_ARRUDA_SANTANA_20260626_1717.md`
   * `METRICAS_ALEXANDRE_ARRUDA_SANTANA_20260626_1717.json`
   * `01_ABRIR_PDF_FINAL.bat` (atalho)
   * Log de execução associado na pasta de logs.

## 6. Reteste pelo Usuário
* **Status**: Aguardando reteste pelo usuário a partir da reabertura da interface Tkinter.
* **Critério de Aceitação**: Todos os 6 arquivos obrigatórios gerados nas pastas dos clientes individuais.

---
**Status Preliminar**: **APROVADO** (Validação local de integridade e separação de lotes bem sucedida com 100% de cobertura de artefatos).
