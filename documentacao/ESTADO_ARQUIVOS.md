# ESTADO DOS ARQUIVOS - ChatFácil / Chat Bridge v0.3.2

## ⚠️ REGRA CRÍTICA — RAIZ CARREGÁVEL

A pasta `chat_bridge_ext_v0_3_2/` deve conter **apenas** os arquivos da extensão.
**Proibido:** pastas `_*`, arquivos `.bak`, relatórios, handoffs, logs.
**Backups:** sempre em `CHAT_BRIDGE_CODEX_ANTIGRAVITY\backups\`.
**Antes de testar no Chrome:** `Get-ChildItem` + confirmar zero itens inválidos.

---

## Estado após Passo 5: Reorganização do Fluxo Principal (31/05/2026)

### Pasta ativa do Chrome
- Caminho: `C:\Users\Windows User\Documents\Chrome_Extensoes\ChatBridge`
- Status: **INTOCADA** (última modificação: 28/05/2026)
- Versão instalada: v0.2.5 funcional estável

### Base v0.3.1
- Caminho: `chat_bridge_ext_v0_3_1_instalador\chat_bridge_ext_v0_3_1`
- Status: **INTOCADA** (última modificação: 29/05/2026)

### Workspace v0.3.2 — Raiz carregável

| Arquivo | Status | Modificado em |
|---|---|---|
| `popup.html` | **Reescrito — Passo 5** | 31/05/2026 |
| `popup.js`   | **Reescrito — Passo 5** | 31/05/2026 |
| `popup.css`  | **Reescrito — Passo 5** | 31/05/2026 |
| `background.js` | Inalterado | 30/05/2026 |
| `content.js`    | Inalterado | 30/05/2026 |
| `manifest.json` | Inalterado | 29/05/2026 |
| `README.md`     | Inalterado | 30/05/2026 |
| `icon*.png`     | Inalterado | —           |

### Raiz: verificação de higiene

| Verificação | Resultado |
|---|---|
| Subpastas na raiz | **0** |
| Pastas com `_` | **0** |
| Arquivos `.bak` | **0** |
| Relatórios/handoffs | **0** |

### Backups em local correto (`backups\`)

| Pasta | Conteúdo |
|---|---|
| `2026-05-30_18-40-00_docs_pre_step3` | Documentos pré-Passo 3 |
| `backup_pre_nucleo_fix_2026-05-31_00-04-21` | popup.{html,js,css}.bak + AUDITORIA_V0_2_5.md |
| `pre_p0_p5_2026-05-31_01-27-26` | popup.{html,js,css}.bak pré-Passo 5 |

### Validações do Passo 6 (Git e GitHub)

| Validação / Arquivo | Status / node --check |
|---|---|
| `chat_bridge_ext_v0_3_2\background.js` | ✅ PASSOU |
| `chat_bridge_ext_v0_3_2\content.js`    | ✅ PASSOU |
| `chat_bridge_ext_v0_3_2\popup.js`      | ✅ PASSOU |
| Git Local Configurado | ✅ OK |
| GitHub Remote Associado | ✅ OK |
| Arquivo `.gitignore` Criado | ✅ OK |
| Arquivo `regras/REGRAS_IA_SINCRONIZACAO.md` Criado | ✅ OK |
| Pasta `documentacao/` Populada | ✅ OK |

