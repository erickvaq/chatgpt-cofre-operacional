# Passo a Passo da Execução — Validação da REGRA 25 e GitHub

## 1. Precheck das Regras do Projeto
*   **Comando:** `python 00_SISTEMA_PRECHECK\precheck_regras.py`
*   **Resultado:** `REGRAS PERSISTENTES CARREGADAS COM SUCESSO - 25 regras encontradas.`
*   **Confirmação:** A nova REGRA 25 foi carregada de forma ativa pela engine.

## 2. Geração dos Arquivos de Teste da REGRA 25
Executado o script `03_SCRIPTS/gerar_teste_regra25.py` para gerar:
*   HTML de teste: `02_RELATORIOS_GERADOS\TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1\TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1.html`
*   PDF de teste: `02_RELATORIOS_GERADOS\TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1\TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1.pdf`
*   Scripts Batch (`01_ABRIR_PDF_FINAL.bat` e `02_ABRIR_PREVIA_HTML.bat`) para abertura externa automática.

## 3. Criação do Arquivo de Auditoria
Criado o arquivo de auditoria `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/TESTE_REGRA25_GITHUB_ARTEFATOS_2026-06-20_V1.md` contendo as informações descritivas do teste de controle.

## 4. Validação e Abertura Externa do PDF
*   Tamanhos e existências dos arquivos foram verificados localmente com sucesso.
*   O PDF foi aberto e conferido externamente via `Start-Process`.

## 5. Git Status, Commit e Push
*   Executado `git status` para auditoria do stage.
*   Arquivos criados adicionados (`git add`) e commitados com a mensagem: `teste: valida REGRA 25 artefatos com links GitHub 2026-06-20 V1` (SHA: `5691f6a`).
*   Envio confirmado ao GitHub via `git push origin main` com sucesso.

## 6. Correção Fina de Links Individuais
*   O arquivo de auditoria foi atualizado para incluir a tabela detalhada de conferência de links individuais para todos os arquivos criados ou modificados.
*   Todos os links de arquivos individuais foram conferidos e confirmados como ativos no GitHub.
*   Novo commit e push foram efetuados para subir os arquivos atualizados de auditoria e registros do Antigravity.

