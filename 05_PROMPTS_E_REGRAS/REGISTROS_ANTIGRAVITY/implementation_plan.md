# Implementation Plan - Register and Implement Rule 31 (GitHub Operational Panel)

We will register a new rule (Rule 31) requiring a lightweight operational dashboard (`PAINEL_OPERACIONAL_WIDEPAY.md`) on GitHub to mirror project execution without publishing sensitive data.

## Proposed Changes

### Documentation and Rules
#### [MODIFY] [REGRAS_PERSISTENTES_DO_PROJETO.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md)
* Append `## REGRA 31 — ESPELHO OPERACIONAL LEVE NO GITHUB` detailing dashboard requirements, formatting tables, sensitive data bans, and git update flows.

#### [MODIFY] [REGRA-BASE — RELATÓRIOS FINANCEIROS WIDEPAY — PROCESSO EFICIENTE E REPLICÁVEL.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/REGRA-BASE%20%E2%80%94%20RELAT%C3%93RIOS%20FINANCEIROS%20WIDEPAY%20%E2%80%94%20PROCESSO%20EFICIENTE%20E%20REPLIC%C3%81VEL.md)
* Append Rule 31 details at the end.

#### [MODIFY] [precheck_regras.py](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/00_SISTEMA_PRECHECK/precheck_regras.py)
* Add a check validation for Rule 31 in `regras_criticas`.

#### [NEW] [PAINEL_OPERACIONAL_WIDEPAY.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md)
* Create the master operational dashboard detailing: execution metadata, clients status table, WidePay extraction summary, requested vs delivered checklist, local sensitive files register, committed files catalog, error lists, and recommended next steps.

### Git Versioning
* Copy current Antigravity logs (`implementation_plan.md`, `task.md`, `walkthrough.md`) to `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/` (Rule 25).
* Stage only:
  - `00_SISTEMA_PRECHECK/precheck_regras.py`
  - `05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md`
  - `05_PROMPTS_E_REGRAS/REGRA-BASE — RELATÓRIOS FINANCEIROS WIDEPAY — PROCESSO EFICIENTE E REPLICÁVEL.md`
  - `05_PROMPTS_E_REGRAS/RESUMO_REGRAS_OPERACIONAIS_WIDEPAY.md`
  - `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md`
  - `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/implementation_plan.md`
  - `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/task.md`
  - `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/walkthrough.md`
  - `07_DADOS_TEMPORARIOS/RESUMO_EXECUCAO_ATUAL.md`
  - `scratch/extrair_tudo_cobertura.py`
* Execute `git commit -m "Audit: Rule 31 and Painel Operacional 2026-06-24"`
* Execute `git push`

## Verification Plan
* Run `python 00_SISTEMA_PRECHECK/precheck_regras.py` standalone.
* Confirm git commit/push success on remote.
