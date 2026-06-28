# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time
import urllib.request
import urllib.parse
import json
from pathlib import Path

# Ajustar caminhos do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR / "00_SISTEMA_PRECHECK"))

try:
    from config_widepay_cdp import CDP_HOST, CDP_PORT, CDP_BASE_URL, WIDEPAY_CARNES_URL, BROWSER_PREFERENCIAL
except ImportError:
    CDP_HOST = "localhost"
    CDP_PORT = 9333
    CDP_BASE_URL = f"http://{CDP_HOST}:{CDP_PORT}"
    WIDEPAY_CARNES_URL = "https://www.widepay.com/conta/recebimentos/carnes"
    BROWSER_PREFERENCIAL = "chrome"

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

def obter_abas():
    try:
        url = f"{CDP_BASE_URL}/json"
        with urllib.request.urlopen(url, timeout=3) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"Erro ao listar abas do Chrome: {e}")
        return []

def abrir_nova_aba(target_url):
    try:
        encoded_url = urllib.parse.quote(target_url, safe='')
        url = f"{CDP_BASE_URL}/json/new?{encoded_url}"
        req = urllib.request.Request(url, method='PUT')
        with urllib.request.urlopen(req, timeout=3) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"Erro ao abrir nova aba: {e}")
        return None

def _aba_widepay_valida(aba):
    url = (aba.get("url") or "").lower()
    if "widepay.com" not in url:
        return False
    if "/conta/acessar" in url or "/conta/login" in url:
        return False
    return True

def selecionar_aba_widepay(abas, preferir_valida=True):
    candidatos = [aba for aba in abas if aba.get("type") == "page" and "widepay.com" in (aba.get("url") or "")]
    if preferir_valida:
        for aba in candidatos:
            if _aba_widepay_valida(aba):
                return aba
    return candidatos[0] if candidatos else None

def validar_sessao_widepay(ws_url):
    async def _validar():
        import websockets
        async with websockets.connect(ws_url, max_size=None) as ws:
            async def cdp(method, params=None):
                nonlocal ws
                msg = {"id": 1, "method": method, "params": params or {}}
                await ws.send(json.dumps(msg))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get("id") == 1:
                        return resp

            loc = await cdp("Runtime.evaluate", {"expression": "window.location.href", "returnByValue": True})
            url = loc.get("result", {}).get("result", {}).get("value", "")
            body = await cdp("Runtime.evaluate", {"expression": "document.body.innerText", "returnByValue": True})
            texto = (body.get("result", {}).get("result", {}).get("value", "") or "").lower()
            erro = any(p in texto for p in ["usuario ou senha incorretos", "senha incorreta", "acessar conta", "esqueci minha senha"])
            login = "/conta/acessar" in url or "/conta/login" in url or "acessar conta" in texto
            return {
                "url": url,
                "texto": texto[:500],
                "login": login,
                "erro": erro,
                "valida": not login and not erro,
            }

    try:
        import asyncio
        return asyncio.run(_validar())
    except RuntimeError:
        # Já existe loop ativo em alguns ambientes; cria execução isolada simples.
        import asyncio as _asyncio
        loop = _asyncio.new_event_loop()
        try:
            return loop.run_until_complete(_validar())
        finally:
            loop.close()

def iniciar_navegador_wmi():
    browser_exe = localizar_chrome()
    if not browser_exe:
        print("Erro: Google Chrome nao encontrado no sistema.")
        return False

    perfil = ROOT_DIR / "08_NAVEGADOR_WIDEPAY" / f"ChromeProfile_{CDP_PORT}"
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
    
    cmd_line = f'"{browser_exe}" ' + " ".join(args)
    ps_cmd = f"Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{{ CommandLine = '{cmd_line}' }}"
    
    print("Iniciando Google Chrome dedicado via WMI...")
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

def garantir_navegador_conectado():
    """Garante que o navegador está aberto e com o CDP ativo. Retorna ws_url da aba WidePay."""
    ok, msg, data = testar_cdp()
    if not ok:
        print("Navegador nao respondendo na porta CDP. Tentando iniciar...")
        if not iniciar_navegador_wmi():
            raise RuntimeError("Nao foi possivel iniciar o Google Chrome via WMI.")
        
        # Aguardar inicialização
        for i in range(10):
            time.sleep(1.5)
            ok, msg, data = testar_cdp()
            if ok:
                break
        else:
            raise RuntimeError("CDP do Chrome nao respondeu apos inicializacao.")
            
    # Localizar aba WidePay ou abrir nova
    abas = obter_abas()
    wp_aba = None
    wp_aba = selecionar_aba_widepay(abas, preferir_valida=True)
            
    if not wp_aba:
        print("Aba do WidePay nao encontrada. Abrindo nova aba...")
        nova_aba = abrir_nova_aba(WIDEPAY_CARNES_URL)
        if not nova_aba:
            raise RuntimeError("Nao foi possivel abrir nova aba no WidePay.")
        time.sleep(3)
        abas = obter_abas()
        wp_aba = selecionar_aba_widepay(abas, preferir_valida=True)
                
    if not wp_aba:
        raise RuntimeError("Falha ao localizar aba do WidePay apos tentativa de criacao.")
        
    ws_url = wp_aba["webSocketDebuggerUrl"]
    print(f"Conexao CDP estabelecida com a aba: {wp_aba.get('title')} ({wp_aba.get('url')})")
    return ws_url
