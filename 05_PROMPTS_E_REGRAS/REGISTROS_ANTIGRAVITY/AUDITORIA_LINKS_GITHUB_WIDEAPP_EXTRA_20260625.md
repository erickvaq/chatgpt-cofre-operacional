# Auditoria GitHub - WideAPP_EXTRA aplicacao independente

## Objetivo

Publicar os arquivos leves criados para registrar que `WideAPP_EXTRA` e aplicacao independente do projeto `Relatorio_WidePay_Lotes`, nao apenas pasta de scripts do Antigravity.

## Repositorio

- Repositorio: `erickvaq/chatgpt-cofre-operacional`
- Branch: `main`
- Remoto local verificado: `origin`

## Links publicos de auditoria

- `WideAPP_EXTRA/README.md`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/README.md

- `WideAPP_EXTRA/ARQUITETURA_APLICACAO_INDEPENDENTE.md`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/WideAPP_EXTRA/ARQUITETURA_APLICACAO_INDEPENDENTE.md

- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/HANDOFF_WIDEAPP_EXTRA_APLICACAO_INDEPENDENTE_20260625.md`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/HANDOFF_WIDEAPP_EXTRA_APLICACAO_INDEPENDENTE_20260625.md

- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/LINKS_WIDEAPP_EXTRA_APLICACAO_INDEPENDENTE_20260625.md`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/LINKS_WIDEAPP_EXTRA_APLICACAO_INDEPENDENTE_20260625.md

- `.agents/skills/widepay-publicacao-segura/SKILL.md`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/.agents/skills/widepay-publicacao-segura/SKILL.md

- `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/REGRA_PUBLICACAO_GITHUB_DRIVE_PUBLICA_20260625.md`  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/REGRA_PUBLICACAO_GITHUB_DRIVE_PUBLICA_20260625.md

- Este indice de auditoria  
  https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/AUDITORIA_LINKS_GITHUB_WIDEAPP_EXTRA_20260625.md

## Checagem de publicabilidade

Comando executado antes da publicacao:

```powershell
rg -n -i "(token|senha|password|cookie|secret|api[_-]?key|sk-[a-zA-Z0-9]|Bearer\s+|Authorization:)" <arquivos alvo>
```

Resultado: encontrou apenas termos descritivos dentro de regras/documentacao, sem valor de segredo, token real, cookie real ou credencial.

## Status

Preparado para commit e push em 2026-06-25.
