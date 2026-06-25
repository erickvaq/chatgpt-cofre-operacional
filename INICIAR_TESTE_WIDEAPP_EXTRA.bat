@echo off
chcp 65001 > nul
setlocal
title WideAPP_EXTRA - Inicializador de Teste

echo ========================================================
echo   WideAPP_EXTRA - Inicializador de Teste Local
echo ========================================================
echo.

set "BASE_DIR=%~dp0"
set "APP_DIR=%BASE_DIR%WideAPP_EXTRA"
set "VENV_PYTHON=%APP_DIR%\.venv\Scripts\python.exe"

if not exist "%APP_DIR%" (
    echo [ERRO] A pasta WideAPP_EXTRA nao foi encontrada neste diretorio.
    echo Certifique-se de extrair todo o conteudo do ZIP mantendo a estrutura original.
    echo.
    pause
    exit /b 1
)

if exist "%VENV_PYTHON%" (
    echo [INFO] Utilizando ambiente virtual local (.venv)...
    cd /d "%APP_DIR%"
    "%VENV_PYTHON%" main.py
    set "EXIT_CODE=%ERRORLEVEL%"
) else (
    echo [AVISO] Ambiente virtual (.venv) nao encontrado em:
    echo %VENV_PYTHON%
    echo.
    echo Para executar o programa, voce precisa ter o Python 3.10+ instalado e:
    echo 1. Abrir o terminal PowerShell ou Prompt de Comando na pasta:
    echo    %APP_DIR%
    echo 2. Criar o ambiente virtual executando:
    echo    python -m venv .venv
    echo 3. Ativar o venv e instalar as dependencias:
    echo    .venv\Scripts\pip install -r requirements.txt
    echo.
    echo Se voce estiver rodando no diretorio original do projeto, verifique
    echo se a pasta .venv foi copiada.
    echo.
    pause
    exit /b 1
)

echo.
if not "%EXIT_CODE%"=="0" (
    echo [ERRO] A interface finalizou com codigo %EXIT_CODE%.
) else (
    echo [OK] Interface fechada com sucesso.
)
echo.
pause
exit /b %EXIT_CODE%
