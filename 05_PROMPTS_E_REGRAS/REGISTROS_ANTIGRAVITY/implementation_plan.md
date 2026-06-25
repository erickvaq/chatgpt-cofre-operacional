# Plan - Session Login Automation via CDP and Audit of Bloco 1 & Letter A Clients

We will process all clients whose names begin with the letter **A** in a read-only local manner. This covers updating existing reports, auditing pending clients from existing JSON logs, resolving ambiguities, and generating final local PDF/HTML reports, with sanitized tracking updated on GitHub.

## User Review Required

> [!WARNING]
> **Identity and Lot Ambiguity - Alexandre (G14):**
> * **WidePay Search Results:** Searching "Alexandre" returned records for two distinct individuals: **Everton Alexandre Jesus Santos Sena** (associated with Carnês 170, 112, and 7) and **Alexandre Arruda Santana** (associated with one paid Boleto ID 3665 and several canceled Boletos IDs 3666–3688).
> * **Contract Review:** The physical contract in the G14 folder is for **Alexandre Arruda Santana** (CPF 016.520.388-92).
> * **Action Plan:** We will generate the G14 report containing *only* Alexandre Arruda Santana's financial records (the single R$ 100 payment, with the remaining 23 installments canceled in WidePay). We will discard the carnês belonging to Everton Alexandre.

> [!NOTE]
> **Lot Discrepancy - Antonio Dias Mota (E15, E16, E17):**
> * **WidePay Search Results:** Antonio Dias Mota has active and finished carnês registered under **E15, E16, E17** (R$ 290 installments) and also **E18** (R$ 99 installments).
> * **Action Plan:** The local contract is only for E15, E16, and E17. However, to match the financial reality of WidePay, we will audit and consolidate all financial items (including E18) under his report, explicitly highlighting this discrepancy.

## Proposed Changes

### Scripts & Data Compilations

#### [NEW] Local Conference Markdowns (`07_DADOS_TEMPORARIOS/`)
Generate calculation summaries using existing JSON logs (using `--usar-json` to bypass new requests, keeping execution offline as requested):
* `CONFERENCIA_CALCULOS_ADALBERTO_OLIVEIRA.md`
* `CONFERENCIA_CALCULOS_CONTRATO_ALEX_SANTOS_DE_AZEVEDO_LEO.md`
* `CONFERENCIA_CALCULOS_ALEXANDRE.md` (Sanitized to Alexandre Arruda Santana)
* `CONFERENCIA_CALCULOS_ANTONIO_DIAS_MOTA.md`

#### [NEW] Local Reports (`02_RELATORIOS_GERADOS/`)
Generate final V3 PDFs and HTML Previews:
* `ADALBERTO_OLIVEIRA_V3_FINAL/`
* `ALEX_SANTOS_DE_AZEVEDO_V3_FINAL/`
* `ALEXANDRE_ARRUDA_SANTANA_G14_V3_FINAL/`
* `ANTONIO_DIAS_MOTA_V3_FINAL/`

#### [MODIFY] [PAINEL_OPERACIONAL_WIDEPAY.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md)
Update dashboard statuses for "A" clients:
* **Adalberto Oliveira**, **Alex Santos de Azevedo**, **Alexandre Arruda Santana**, and **Antonio Dias Mota** will transition from "Pendente / Não gerado" to:
  * **Status WidePay:** Consultado
  * **Relatório:** Gerado local (V3)
  * **Arquivo local:** Sim
  * **GitHub:** Não enviado — arquivo sensível
  * **Pendência:** Aguardando validação do usuário
* Update the execution progress tables to reflect the new state.

#### [MODIFY] [INDICE_AUDITAVEL_RELATORIOS.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/07_DADOS_TEMPORARIOS/INDICE_AUDITAVEL_RELATORIOS.md)
* Append the metadata blocks for the newly generated local reports (Adalberto, Alex, Alexandre, Antonio) including file paths and verification hash lists.

## Verification Plan

### Automated Tests
* Run `python 00_SISTEMA_PRECHECK/precheck_regras.py` to ensure all edits to Markdown and dashboard registries comply with project constraints (no financial values on Git, strict file path formatting, Heron exclusion, rule compliance).

### Manual Verification
* Visually check the generated PDF and HTML outputs locally for formatting or calculation anomalies before updating the dashboard.
* Confirm that no local PDF, HTML, or JSON file containing financial values is staged or committed to Git.
