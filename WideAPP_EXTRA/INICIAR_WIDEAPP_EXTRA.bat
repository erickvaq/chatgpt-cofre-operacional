@echo off
chcp 65001 > nul
setlocal
title WideAPP_EXTRA - Aplicacao Independente

set "APP_DIR=%~dp0"
set "PYTHON_EXE=%APP_DIR%.venv\Scripts\python.exe"
set "MAIN_PY=%APP_DIR%main.py"

echo ========================================================
echo   WideAPP_EXTRA - Auditoria e Relatorios WidePay
echo ========================================================
echo.

if not exist "%PYTHON_EXE%" (
    echo [ERRO] Python do ambiente virtual nao encontrado:
    echo %PYTHON_EXE%
    echo.
    echo Recrie ou valide o ambiente .venv antes de continuar.
    pause
    exit /b 1
)

if not exist "%MAIN_PY%" (
    echo [ERRO] Entrada principal nao encontrada:
    echo %MAIN_PY%
    pause
    exit /b 1
)

"%PYTHON_EXE%" "%MAIN_PY%" %*
set "EXIT_CODE=%ERRORLEVEL%"

echo.
if not "%EXIT_CODE%"=="0" (
    echo [ERRO] WideAPP_EXTRA finalizou com codigo %EXIT_CODE%.
) else (
    echo [OK] WideAPP_EXTRA finalizou com sucesso.
)
echo.
pause
exit /b %EXIT_CODE%
