# Plan - Session Login Automation via CDP and Audit of Bloco 1 (3 Clients)

We will modify the WidePay query integration to handle the login page dynamically by leveraging the saved password in the dedicated Opera browser's persistent profile (port 9444). We will trigger autofill using element focus and click events, click the login button, and confirm successful navigation to the dashboard. Subsequently, we will audit the first 3 clients in a read-only manner.

## User Review Required

> [!IMPORTANT]
> **Autofill Trigger:**
> The script will attempt to trigger the browser's native autofill by simulating user click/focus on the email and password fields. If Opera successfully fills the fields, it will click "Acessar". If no saved password is found or autofill fails, the script will prompt for manual login and pause.
> **No Sensitive Data Exposure:**
> The automation does not read, copy, print, or store the password. It operates completely through browser events.

## Proposed Changes

### Scripts

#### [MODIFY] [consultar_widepay_cdp.py](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/03_SCRIPTS/consultar_widepay_cdp.py)
* Implement `ensure_widepay_logged_in(ws_url)` function:
  - Check if the current URL points to a login/access page.
  - If yes, query inputs to check visibility.
  - Simulate focus and click events on the `usuario` / `email` and `senha` / `password` inputs to trigger Opera's native autofill.
  - Wait 1-2 seconds.
  - If the password input receives autofill value (which might be verified by checking if the browser allows submitting or if value length > 0), click the submit button.
  - Confirm the page navigates away from the login URL to the authenticated page.
  - If it fails, raise a login required exception/exit with code 2 for manual login.

### Execution Scope (Bloco 1)
* Run read-only query on the 3 clients:
  1. **Adailton Gomes De Jesus** (lote **E22A**)
  2. **Altamir Do Carmo Cerqueira** (lote **G4**)
  3. **Ana Carolina Nery Da S. Borgens** (lote **E7**)

## Verification Plan

### Manual Verification
* Run `python 03_SCRIPTS/consultar_widepay_cdp.py --cliente "Adailton Gomes De Jesus"` and observe if the Opera browser automatically processes the login screen and navigates to the carnês page, or if it halts correctly when credentials aren't populated.
* Verify the console output for each of the 3 clients in the block, confirming carnês, avulsos, and status details.
