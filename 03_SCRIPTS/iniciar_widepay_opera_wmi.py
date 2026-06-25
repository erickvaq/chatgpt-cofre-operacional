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

def iniciar_opera_wmi(opera_path):
    perfil = ROOT_DIR / "08_NAVEGADOR_WIDEPAY" / f"OperaProfile_{CDP_PORT}"
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
    
    cmd_line = f'"{opera_path}" ' + " ".join(args)
    ps_cmd = f"Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{{ CommandLine = '{cmd_line}' }}"
    
    print(f"Spawning Opera GX via WMI...")
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
        if testar_login_necessario():
            print("STATUS: login necessario (WidePay aberto no Opera dedicado; faça login sem reiniciar o navegador)")
            sys.exit(2)

    print("Abrindo Opera dedicado sem fechar sessoes existentes...")
    
    opera_exe = localizar_opera()
    if not opera_exe:
        print("STATUS: falha de navegador (Opera nao encontrado no sistema)")
        sys.exit(1)
        
    if not iniciar_opera_wmi(opera_exe):
        print("STATUS: falha de navegador (Nao foi possivel iniciar o processo via WMI)")
        sys.exit(1)
        
    print("Aguardando inicializacao do Opera...")
    for i in range(5):
        time.sleep(2)
        ok, msg, data = testar_cdp()
        if ok:
            if testar_login_necessario():
                print("STATUS: login necessario (Faça login no WidePay na janela do Opera)")
                sys.exit(2)
            else:
                print("STATUS: CDP OK")
                sys.exit(0)
                
    print("STATUS: falha de porta (CDP nao respondeu apos inicializacao)")
    sys.exit(3)

if __name__ == "__main__":
    main()
