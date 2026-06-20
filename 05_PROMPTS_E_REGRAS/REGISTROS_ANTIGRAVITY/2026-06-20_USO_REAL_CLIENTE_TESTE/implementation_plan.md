# Plano de Implementação — Configuração GitHub e Teste da REGRA 24

Este plano descreve as etapas para configurar o repositório remoto do GitHub, testar a geração sincronizada de entregas visuais em HTML e PDF (REGRA 24) e documentar o aprendizado em arquivos persistentes de regras do projeto.

## User Review Required

> [!IMPORTANT]
> A credencial/token do GitHub do usuário deve estar configurada localmente (ou o Windows Credential Manager deve gerenciar) para permitir que o comando `git push` ocorra com sucesso sem solicitar credenciais de forma interativa. Se for solicitada autenticação interativa, o agente irá parar e solicitar intervenção manual.

## Proposed Changes

### Configuração do Git e Entrega de Teste

#### [NEW] [gerar_teste_regra24.py](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/03_SCRIPTS/gerar_teste_regra24.py)
Criar um script Python para gerar programaticamente os arquivos HTML e PDF do teste de entrega visual no formato e pasta corretos, utilizando ReportLab para a conversão para PDF em conformidade com as bibliotecas locais.

#### [NEW] [TESTE_ENTREGA_VISUAL_2026-06-20_V1.html](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/02_RELATORIOS_GERADOS/TESTE_ENTREGA_VISUAL_2026-06-20_V1/TESTE_ENTREGA_VISUAL_2026-06-20_V1.html)
Arquivo HTML contendo o conteúdo do teste visual (data de criação, versão, descrição da regra).

#### [NEW] [TESTE_ENTREGA_VISUAL_2026-06-20_V1.pdf](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/02_RELATORIOS_GERADOS/TESTE_ENTREGA_VISUAL_2026-06-20_V1/TESTE_ENTREGA_VISUAL_2026-06-20_V1.pdf)
Arquivo PDF gerado a partir do conteúdo do teste visual.

### Documentação de Regras e Histórico

#### [MODIFY] [REGRAS_PERSISTENTES_DO_PROJETO.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md)
Adicionar os novos aprendizados do teste de entrega à REGRA 24 (como a necessidade de manter a estrutura de subpastas dedicadas, verificação de Git remotes e tratamento de erros do push).

#### [NEW] [HISTORICO_DE_PROCESSOS_VALIDOS.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/HISTORICO_DE_PROCESSOS_VALIDOS.md)
Criar o arquivo de histórico registrando as etapas executadas, caminhos de arquivo, comandos, links do GitHub e o padrão `PADRAO_ENTREGA_VISUAL_HTML_PDF_GITHUB`.

#### [NEW] [REGRAS_PERSISTENTES_DO_PROJETO.md.bak](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/05_PROMPTS_E_REGRAS/backups/REGRAS_PERSISTENTES_DO_PROJETO.md.bak)
Criar backup dos arquivos de regras antes de rodar o precheck final.

## Verification Plan

### Automated Tests
- Executar `python 00_SISTEMA_PRECHECK\precheck_regras.py` para garantir que o arquivo de regras editado continua válido e contém as 24 regras esperadas.

### Manual Verification
- O agente usará o comando `Start-Process` no PowerShell para abrir o PDF gerado no leitor padrão do Windows ou navegador, garantindo que o arquivo não seja exibido em texto bruto no chat do Antigravity.
- O agente confirmará a presença do repositório remoto no GitHub usando `git remote -v` e validará o sucesso do envio com `git push`.
