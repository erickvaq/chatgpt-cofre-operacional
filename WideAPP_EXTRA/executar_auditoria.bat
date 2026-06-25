@echo off
chcp 65001 > nul
title AUDITORIA FINANCEIRA WIDEPAY
echo ========================================================
echo   INICIANDO APLICACAO DE AUDITORIA FINANCEIRA WIDEPAY  
echo ========================================================
echo.

if "%~1" == "" (
    echo Opcoes de uso:
    echo   executar_auditoria.bat --cliente "Nome do Cliente" [--lote "Lote"]
    echo   executar_auditoria.bat --letra A [--letra-fim D]
    echo   executar_auditoria.bat --quadra F
    echo   executar_auditoria.bat --todos [--consolidado]
    echo.
    set /p "CLIENTE=Digite o nome do cliente para auditar (ou Ctrl+C para sair): "
    if not "!CLIENTE!" == "" (
        python executar_auditoria.py --cliente "!CLIENTE!" --consolidado
    )
) else (
    python executar_auditoria.py %*
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERRO] Ocorreu um problema durante a execucao da auditoria.
) else (
    echo.
    echo [SUCESSO] Auditoria concluida. Relatorios disponiveis em 02_RELATORIOS_GERADOS.
)
echo.
pause
