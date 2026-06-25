# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time
import urllib.request
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "00_SISTEMA_PRECHECK"))

try:
    from precheck_regras import executar_precheck
    executar_precheck("iniciar_widepay_opera_wmi.py")
except ImportError as e:
    print(f"ERRO: Nao foi possivel carregar o precheck de regras: {e}")
    sys.exit(1)

try:
    from config_widepay_cdp import CDP_HOST, CDP_PORT, CDP_BASE_URL, WIDEPAY_CARNES_URL, BROWSER_PREFERENCIAL
except ImportError:
    CDP_HOST = "localhost"
    CDP_PORT = 9444
    CDP_BASE_URL = f"http://{CDP_HOST}:{CDP_PORT}"
    WIDEPAY_CARNES_URL = "https://www.widepay.com/conta/recebimentos/carnes"
    BROWSER_PREFERENCIAL = "opera_gx"

def localizar_opera():
    possiveis = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera GX\opera.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera\opera.exe"),
        r"C:\Users\Windows User\AppData\Local\Programs\Opera GX\opera.exe",
        r"C:\Users\Windows User\AppData\Local\Programs\Opera\opera.exe",
        r"C:\Program Files\Opera\opera.exe",
        r"C:\Program Files (x86)\Opera\opera.exe"
    ]
    for p in possiveis:
        if os.path.exists(p):
            return p
    return None

def localizar_chrome():
    possiveis = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for p in possiveis:
        if os.path.exists(p):
            return p
    return None

def testar_cdp():
    url = f"{CDP_BASE_URL}/json/version"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as r:
            data = json.loads(r.read().decode('utf-8'))
            if "webSocketDebuggerUrl" in data:
                return True, "CDP OK", data
    except Exception as e:
        return False, str(e), None
    return False, "Sem resposta do CDP", None

def testar_login_necessario():
    try:
        url = f"{CDP_BASE_URL}/json"
        with urllib.request.urlopen(url, timeout=3) as r:
            abas = json.loads(r.read().decode('utf-8'))
            for aba in abas:
                if "widepay.com" in aba.get("url", ""):
                    if "login" in aba["url"] or "acessar" in aba["url"]:
                        return True
    except Exception:
        pass
    return False

def widepay_ja_logado():
    try:
        url = f"{CDP_BASE_URL}/json"
        with urllib.request.urlopen(url, timeout=3) as r:
            abas = json.loads(r.read().decode("utf-8"))
            for aba in abas:
                aba_url = aba.get("url", "")
                titulo = aba.get("title", "")
                if "widepay.com" not in aba_url:
                    continue
                if "login" in aba_url or "acessar" in aba_url:
                    continue
                if "recebimentos" in aba_url or "Recebimentos" in titulo:
                    return True, aba
    except Exception as e:
        return False, {"erro": str(e)}
    return False, None

def iniciar_navegador_wmi(browser_path, browser_nome):
    prefixo = "ChromeProfile" if browser_nome.startswith("chrome") else "OperaProfile"
    perfil = ROOT_DIR / "08_NAVEGADOR_WIDEPAY" / f"{prefixo}_{CDP_PORT}"
    os.makedirs(perfil, exist_ok=True)
    
    args = [
        f"--remote-debugging-port={CDP_PORT}",
        "--remote-allow-origins=*",
        f'--user-data-dir="{perfil}"',
        "--no-first-run",
        "--no-default-browser-check",
        "--new-window",
        f'"{WIDEPAY_CARNES_URL}"'
    ]
    
    cmd_line = f'"{browser_path}" ' + " ".join(args)
    ps_cmd = f"Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{{ CommandLine = '{cmd_line}' }}"
    
    print(f"Spawning {browser_nome} via WMI...")
    result = subprocess.run(
        ["powershell", "-Command", ps_cmd],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    if result.returncode != 0:
        print(f"Erro ao disparar via WMI: {result.stderr}")
        return False
    return True

def main():
    ok, msg, data = testar_cdp()
    if ok:
        logado, aba = widepay_ja_logado()
        if logado:
            print(f"STATUS: WidePay ja aberto e logado ({aba.get('title')} - {aba.get('url')})")
            sys.exit(0)
        print("STATUS: CDP OK (navegador ja em execucao)")
        sys.exit(0)

    print(f"Abrindo navegador dedicado WidePay sem fechar sessoes existentes ({BROWSER_PREFERENCIAL})...")

    if BROWSER_PREFERENCIAL.startswith("chrome"):
        browser_exe = localizar_chrome()
        browser_nome = "chrome"
    else:
        browser_exe = localizar_opera()
        browser_nome = "opera"

    if not browser_exe:
        print(f"STATUS: falha de navegador ({browser_nome} nao encontrado no sistema)")
        sys.exit(1)
        
    if not iniciar_navegador_wmi(browser_exe, browser_nome):
        print("STATUS: falha de navegador (Nao foi possivel iniciar o processo via WMI)")
        sys.exit(1)
        
    print(f"Aguardando inicializacao do {browser_nome}...")
    for i in range(5):
        time.sleep(2)
        ok, msg, data = testar_cdp()
        if ok:
            print("STATUS: CDP OK")
            sys.exit(0)
                
    print("STATUS: falha de porta (CDP nao respondeu apos inicializacao)")
    sys.exit(3)

if __name__ == "__main__":
    main()
