@echo off
chcp 65001 > nul
title WideAPP_EXTRA - Interface Gráfica
echo ===================================================
echo EXECUTANDO PRECHECK DE REGRAS PERSISTENTES...
echo ===================================================

python 00_SISTEMA_PRECHECK\precheck_regras.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERRO CRITICO] O precheck de regras falhou! Execução bloqueada.
    echo Por favor, verifique se o arquivo REGRAS_PERSISTENTES_DO_PROJETO.md existe e contem as 13 regras.
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ===================================================
echo INICIANDO A INTERFACE GRAFICA (WideAPP_EXTRA)...
echo ===================================================
echo.

cd /d "%~dp0WideAPP_EXTRA"
".venv\Scripts\python.exe" "main.py"
set "EXIT_CODE=%ERRORLEVEL%"

echo.
if not "%EXIT_CODE%"=="0" (
    echo [ERRO] A interface finalizou com codigo %EXIT_CODE%.
) else (
    echo [OK] Interface fechada com sucesso.
)
echo.
pause
exit /b %EXIT_CODE%
