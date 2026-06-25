# Walkthrough - Login Session Automation & Bloco 1 Audit

We successfully implemented a robust login session automation using CDP to simulate focus and Enter keypress events, triggering Opera's native autofilled credentials. We then completed the read-only financial audit of the first three clients in Bloco 1.

## Changes Implemented

### Login Session Automation via CDP
1. **[consultar_widepay_cdp.py](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/03_SCRIPTS/consultar_widepay_cdp.py):**
   - Refactored the login detection logic to focus the password input and dispatch virtual `keyDown`/`keyUp` keyboard events for the `Enter` key (virtual code `13`) using CDP's `Input.dispatchKeyEvent`.
   - This method bypasses standard script limitations where programmatic clicks do not register autofilled values in frontend frameworks (like React).
   - Added automated redirection check to confirm dashboard load and error logs.

## Audit Results (Bloco 1 - 3 Clients)

### 1. Adailton Gomes De Jesus (Lote E22A)
* **Found in WidePay:** Yes
* **Carnes:** 
  - Carnê `45` (Lt E 22): Finalized (21/21 paid, received R$ 3,183.09, final venc. 20/06/2023)
  - Carnê `159` (ref `e22a 20-07 parcela 25 em diante R$140`): Cancelled (0 paid)
* **Cobranças/Boletos:** 
  - 2 active unpaid vencidos (ID `3461` and `3460` for late fees, total R$ 315)
  - 23 cancelled boletos under `"e22a 20-07..."`
* **Local folder:** Matches E22A (contains a physical copy of "DISTRATO").
* **Audit Diagnosis:** **Pendente.** The cancellation of carnê `159` and boletos matches the local contract distrato (cancellation). Outstanding late fees of R$ 315 from 2023 need verification.

### 2. Altamir Do Carmo Cerqueira (Lote G4)
* **Found in WidePay:** Yes
* **Carnes:**
  - Carnê `33` (Lt G-4): Finalized (5/5 paid, received R$ 2,500)
  - Carnê `93` (no reference): Finalized (2/2 paid, received R$ 1,000)
  - Carnê `31` (no reference): Cancelled (0 paid)
* **Cobranças/Boletos:**
  - 16 cancelled boletos of R$ 350
* **Local folder:** Matches G4 (contains "A VISTA" contract).
* **Audit Diagnosis:** **Pronto para relatório.** Paid R$ 3,500.00 in total, which matches the "A VISTA" full quittance plan. No outstanding active boletos.

### 3. Ana Carolina Nery Da S. Borgens (Lote E7)
* **Found in WidePay:** Yes
* **Carnes:**
  - Carnê `47` (no reference): Finalized (22/22 paid, received R$ 2,611.67)
  - Carnê `152` (ref `"e7 carne2 apart 25 R110"`): Finalized (11/11 paid, received R$ 1,298.27)
  - Carnê `185` (ref `"E7 apart.37"`): Finalized (4/4 paid, received R$ 500.87)
  - Carnê `234` (no reference): Active/Pendente (0/24 paid, total pending R$ 3,312.00, value per installment R$ 138)
* **Cobranças/Boletos:**
  - 5 active **Vencidos** from active carnê `234` (totaling R$ 690.00 in arrears)
  - 19 active **Aguardando** (totaling R$ 2,622.00 future)
  - 1 cancelled boleto (ID `5191`)
* **Local folder:** Matches E7.
* **Audit Diagnosis:** **Pendente.** Recent installment reajuste to R$ 138.00 and R$ 690.00 in active arrears (vencidos in 2026) must be audited and verified against the contract rules before producing a final report.
