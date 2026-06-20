# Passo a Passo da Execução — Correção do Teste Prático (Uso Real V2)

## 1. Precheck das Regras do Projeto
*   **Comando:** `python 00_SISTEMA_PRECHECK\precheck_regras.py`
*   **Resultado:** `REGRAS PERSISTENTES CARREGADAS COM SUCESSO - 25 regras encontradas.`
*   **Confirmação:** A REGRA 25 está carregada de forma ativa pela engine.

## 2. Geração da Entrega V2
Criado o arquivo de conferência V2 `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_CLIENTE_TESTE_USO_REAL_2026-06-20_V2.md`.
Executado o script `03_SCRIPTS/gerar_teste_uso_real_v2.py` para gerar na mesma pasta:
*   HTML de teste: `02_RELATORIOS_GERADOS\CLIENTE_TESTE_USO_REAL_2026-06-20_V2_FINAL\RESUMO_FINANCEIRO_CLIENTE_TESTE_USO_REAL_2026-06-20_V2_PREVIA.html`
*   PDF de teste: `02_RELATORIOS_GERADOS\CLIENTE_TESTE_USO_REAL_2026-06-20_V2_FINAL\RESUMO_FINANCEIRO_CLIENTE_TESTE_USO_REAL_2026-06-20_V2.pdf`
*   Scripts Batch (`01_ABRIR_PDF_FINAL.bat` e `02_ABRIR_PREVIA_HTML.bat`) para abertura externa automática.

## 3. Validação de Abertura e Tamanho de Arquivos
*   Abertura externa do PDF confirmada via `Start-Process` no PowerShell.
*   Tamanho de todos os arquivos conferidos localmente (tamanhos corretos e não-nulos).

## 4. Cópia de Artefatos do Antigravity
Os arquivos `implementation_plan.md`, `task.md`, e `walkthrough.md` foram copiados para a pasta dedicada do projeto em `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/2026-06-20_USO_REAL_CLIENTE_TESTE/`.

## 5. Git Status, Commit e Push
*   Executado `git status` para auditoria.
*   Arquivos novos e modificados adicionados e enviados ao GitHub na branch `main`.
