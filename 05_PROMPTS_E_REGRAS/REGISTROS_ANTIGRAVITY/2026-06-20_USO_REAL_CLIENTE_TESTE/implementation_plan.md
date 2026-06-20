# Plano de Implementação — Atualização de Padrão (Sem BAT)

Este plano descreve as etapas para atualizar as regras persistentes, memória operacional do Codex e o histórico de processos para o novo padrão de entregas sem a geração automática de arquivos `.bat` auxiliares.

## User Review Required

> [!IMPORTANT]
> A partir desta alteração, nenhuma entrega visual padrão gerará arquivos `.bat` de abertura rápida. O padrão de conferência será abrir a pasta final no Explorer e verificar o HTML/PDF.

## Proposed Changes

### Documentação de Regras, Memórias e Histórico

#### [MODIFY] [REGRAS_PERSISTENTES_DO_PROJETO.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md)
Remover a geração de arquivos `.bat` automáticos e estabelecer a abertura da pasta no Explorer nas Regras 9, 12, 16, 24 e 25.

#### [MODIFY] [MEMORIA_OPERACIONAL_DO_CODEX.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/MEMORIA_OPERACIONAL_DO_CODEX.md)
Atualizar a memória para desativar `.bat` por padrão em entregas de clientes.

#### [MODIFY] [HISTORICO_DE_PROCESSOS_VALIDOS.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/HISTORICO_DE_PROCESSOS_VALIDOS.md)
Registrar a Etapa 3 e o padrão `PADRAO_ENTREGA_CLIENTE_SEM_BAT`.

### Backups

#### [NEW] [REGRAS_PERSISTENTES_DO_PROJETO_2026-06-20_V4.md.bak](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/backups/REGRAS_PERSISTENTES_DO_PROJETO_2026-06-20_V4.md.bak)
#### [NEW] [MEMORIA_OPERACIONAL_DO_CODEX_2026-06-20_V3.md.bak](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/backups/MEMORIA_OPERACIONAL_DO_CODEX_2026-06-20_V3.md.bak)
#### [NEW] [HISTORICO_DE_PROCESSOS_VALIDOS_2026-06-20_V4.md.bak](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/backups/HISTORICO_DE_PROCESSOS_VALIDOS_2026-06-20_V4.md.bak)

### Sincronização dos Registros do Antigravity

#### [NEW] [implementation_plan.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/2026-06-20_USO_REAL_CLIENTE_TESTE/implementation_plan.md)
#### [NEW] [task.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/2026-06-20_USO_REAL_CLIENTE_TESTE/task.md)
#### [NEW] [walkthrough.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/2026-06-20_USO_REAL_CLIENTE_TESTE/walkthrough.md)

## Verification Plan

### Automated Tests
- Executar `python 00_SISTEMA_PRECHECK\precheck_regras.py` para atestar a validade estrutural e de contagem do arquivo de regras persistentes.

### Manual Verification
- Validar `git status` antes do commit.
- Confirmar sucesso do push para a branch `main` no repositório remoto.
