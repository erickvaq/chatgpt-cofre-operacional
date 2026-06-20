# Passo a Passo da Execução — Atualização de Padrão (Sem BAT)

## 1. Backups dos arquivos de regras
Foram criadas cópias de segurança exatas dos arquivos originais antes de qualquer modificação, salvas em `05_PROMPTS_E_REGRAS/backups/`:
*   `05_PROMPTS_E_REGRAS/backups/REGRAS_PERSISTENTES_DO_PROJETO_2026-06-20_V4.md.bak`
*   `05_PROMPTS_E_REGRAS/backups/MEMORIA_OPERACIONAL_DO_CODEX_2026-06-20_V3.md.bak`
*   `05_PROMPTS_E_REGRAS/backups/HISTORICO_DE_PROCESSOS_VALIDOS_2026-06-20_V4.md.bak`

## 2. Modificação das Regras Persistentes do Projeto
O arquivo `05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md` foi atualizado nas Regras 9, 12, 16, 24 e 25 para estabelecer o `PADRAO_ENTREGA_CLIENTE_SEM_BAT`. A partir de agora, arquivos `.bat` não são gerados automaticamente para entregas de clientes; em vez disso, o padrão de conferência é abrir a pasta final de entrega no Explorer.

## 3. Atualização da Memória Operacional do Codex
O arquivo `05_PROMPTS_E_REGRAS/MEMORIA_OPERACIONAL_DO_CODEX.md` foi alterado para refletir o novo comportamento, impedindo a geração automática de arquivos `.bat` por padrão em entregas visuais.

## 4. Registro no Histórico de Processos Válidos
O arquivo `05_PROMPTS_E_REGRAS/HISTORICO_DE_PROCESSOS_VALIDOS.md` foi complementado com o histórico da Etapa 3 e com a especificação formal do procedimento `PADRAO_ENTREGA_CLIENTE_SEM_BAT`.

## 5. Cópia de Artefatos do Antigravity
Copiar os arquivos de logs operacionais do Antigravity (`implementation_plan.md`, `task.md` e `walkthrough.md`) para o repositório em `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/2026-06-20_USO_REAL_CLIENTE_TESTE/` antes do commit para subir ao repositório GitHub.

## 6. Precheck, Commit e Push
*   Executado o precheck para validar as novas regras.
*   Executado o `git commit` com a mensagem apropriada.
*   Executado o `git push` confirmando o envio bem-sucedido para a branch `main`.
