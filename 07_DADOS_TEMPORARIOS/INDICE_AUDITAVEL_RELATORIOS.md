# ÍNDICE DE AUDITORIA E CONTROLE DE RELATÓRIOS SANITIZADOS

Este índice rastreia os relatórios e auditorias financeiras gerados pelo projeto `Relatorio_WidePay_Lotes`, servindo como controle operacional público sem expor dados financeiros sensíveis (valores monetários, parcelas) ou informações pessoais (CPF, e-mails, telefones) dos clientes.

---

## 1. Diretriz de Privacidade Operacional
* **Classificação do Repositório:** Público
* **Política de Segurança:** Todos os relatórios financeiros detalhados (PDFs, HTMLs de prévia e Markdowns de conferência de valores) são mantidos **exclusivamente local**. No GitHub, são versionados apenas os metadados e status sanitizados para controle de andamento.

---

## 2. Registro de Auditorias Executadas

### Bloco 1 (Auditado e Gerado em 25/06/2026)

#### A. Adailton G. J.
* **Lote/Quadra:** E22A (Quadra E)
* **Status de Auditoria:** **Concluído**
* **Status Financeiro Resumido:** Ativo com pendências de cobranças avulsas de atraso vencidas. Carnê de parcelamento de lote finalizado no WidePay.
* **Arquivos Gerados Localmente:**
  * **PDF:** `02_RELATORIOS_GERADOS/ADAILTON_GOMES_DE_JESUS_E22A_AGUA_VIVA_LEANDRO_MEIRELLES_V3_FINAL/RESUMO_FINANCEIRO_ADAILTON_GOMES_DE_JESUS_E22A_AGUA_VIVA_LEANDRO_MEIRELLES_CORRIGIDO_V3.pdf`
  * **HTML Prévia:** `02_RELATORIOS_GERADOS/RESUMO_FINANCEIRO_ADAILTON_GOMES_DE_JESUS_E22A_AGUA_VIVA_LEANDRO_MEIRELLES_CORRIGIDO_V3_PREVIA.html`
  * **Markdown de Conferência:** `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_ADAILTON_GOMES_DE_JESUS_E22A_AGUA_VIVA_LEANDRO_MEIRELLES.md`
  * **Atalho BAT:** `02_RELATORIOS_GERADOS/ADAILTON_GOMES_DE_JESUS_E22A_AGUA_VIVA_LEANDRO_MEIRELLES_V3_FINAL/01_ABRIR_PDF_FINAL.bat`
* **Envio ao GitHub:** Não enviado (Contém valores monetários de parcelas e descrição de histórico financeiro do lote).
* **Versão Sanitizada no GitHub:** Registrado neste Índice e no Painel Operacional.

#### B. Altamir C. C.
* **Lote/Quadra:** G4 (Quadra G)
* **Status de Auditoria:** **Concluído**
* **Status Financeiro Resumido:** Ativo, **quitado** no WidePay (todas as obrigações e parcelas geradas foram pagas).
* **Arquivos Gerados Localmente:**
  * **PDF:** `02_RELATORIOS_GERADOS/CONTRATO_ALTAMIR_DO_CARMO_CERQUEIRA_G4_AGUA_VIVA_LEANDRO_MEIRELLES_V3_FINAL/RESUMO_FINANCEIRO_CONTRATO_ALTAMIR_DO_CARMO_CERQUEIRA_G4_AGUA_VIVA_LEANDRO_MEIRELLES_CORRIGIDO_V3.pdf`
  * **HTML Prévia:** `02_RELATORIOS_GERADOS/RESUMO_FINANCEIRO_CONTRATO_ALTAMIR_DO_CARMO_CERQUEIRA_G4_AGUA_VIVA_LEANDRO_MEIRELLES_CORRIGIDO_V3_PREVIA.html`
  * **Markdown de Conferência:** `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_CONTRATO_ALTAMIR_DO_CARMO_CERQUEIRA_G4_AGUA_VIVA_LEANDRO_MEIRELLES.md`
  * **Atalho BAT:** `02_RELATORIOS_GERADOS/CONTRATO_ALTAMIR_DO_CARMO_CERQUEIRA_G4_AGUA_VIVA_LEANDRO_MEIRELLES_V3_FINAL/01_ABRIR_PDF_FINAL.bat`
* **Envio ao GitHub:** Não enviado (Contém valores monetários de parcelas e histórico de amortização de boletos).
* **Versão Sanitizada no GitHub:** Registrado neste Índice e no Painel Operacional.

#### C. Ana Carolina N. S. B.
* **Lote/Quadra:** E7 (Quadra E)
* **Status de Auditoria:** **Concluído**
* **Status Financeiro Resumido:** Ativa com carnê em andamento no WidePay. Possui parcelas em aberto vencidas e vincendas.
* **Arquivos Gerados Localmente:**
  * **PDF:** `02_RELATORIOS_GERADOS/ANA_CAROLINA_NERY_DA_S__BORGENS_V3_FINAL/RESUMO_FINANCEIRO_ANA_CAROLINA_NERY_DA_S__BORGENS_CORRIGIDO_V3.pdf`
  * **HTML Prévia:** `02_RELATORIOS_GERADOS/RESUMO_FINANCEIRO_ANA_CAROLINA_NERY_DA_S__BORGENS_CORRIGIDO_V3_PREVIA.html`
  * **Markdown de Conferência:** `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_ANA_CAROLINA_NERY_DA_S_BORGENS.md`
  * **Atalho BAT:** `02_RELATORIOS_GERADOS/ANA_CAROLINA_NERY_DA_S__BORGENS_V3_FINAL/01_ABRIR_PDF_FINAL.bat`
* **Envio ao GitHub:** Não enviado (Contém histórico detalhado de parcelamento e valores monetários vencidos/a vencer).
* **Versão Sanitizada no GitHub:** Registrado neste Índice e no Painel Operacional.

---

## 3. Status Consolidado do Bloco 1

* **Total de Clientes do Bloco:** 3
* **Relatórios PDF/HTML gerados localmente:** 3 (100% concluídos)
* **Precheck de Regras:** Aprovado em todos os testes locais.
* **Próximo Bloco de Auditoria:** Bloco 2 (Aguardando liberação).

---

## 4. Registro de Incidente e Contencao

| Evento | Arquivos afetados | Classificacao | Contencao | GitHub |
|---|---|---|---|---|
| Conferencia gerada com cache/JSON antigo sem consulta atual ao WidePay | `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_ADALBERTO_OLIVEIRA_A3_AGUA_VIVA_LEANDRO_MEIRELLES.md`, `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/WIDEPAY_ADALBERTO_OLIVEIRA.json`, `07_DADOS_TEMPORARIOS/WIDEPAY_CONSULTAS/WIDEPAY_ADALBERTO_OLIVEIRA_A3_AGUA_VIVA_LEANDRO_MEIRELLES.json` | Nao aprovado / invalido / pendente | Arquivos completos mantidos localmente por conter dados sensiveis | Painel sanitizado atualizado no GitHub |
| Conferencia do Adalberto bloqueada ate consulta atual no WidePay | `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_ADALBERTO_OLIVEIRA_A3_AGUA_VIVA_LEANDRO_MEIRELLES.md` | Nao aprovado | Entrega final bloqueada ate validacao atual | Registro sanitizado no painel e no indice |
