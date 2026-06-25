# -*- coding: utf-8 -*-
import os
import sys
import json
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import asyncio
import time
import websockets
import argparse
import re
import unicodedata
from pathlib import Path

# Ajustar sys.path para carregar o precheck
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "00_SISTEMA_PRECHECK"))

try:
    from precheck_regras import executar_precheck
    executar_precheck("consultar_widepay_cdp.py")
except ImportError as e:
    print(f"ERRO: Nao foi possivel carregar o precheck de regras: {e}")
    sys.exit(1)

try:
    from config_widepay_cdp import CDP_HOST, CDP_PORT, CDP_BASE_URL, WIDEPAY_CARNES_URL
except ImportError:
    CDP_HOST = "localhost"
    CDP_PORT = 9444
    CDP_BASE_URL = f"http://{CDP_HOST}:{CDP_PORT}"
    WIDEPAY_CARNES_URL = "https://www.widepay.com/conta/recebimentos/carnes"

# Argumentos
parser = argparse.ArgumentParser(description="Consulta real do WidePay via CDP")
parser.add_argument("--cliente", required=True, help="Nome do cliente a ser pesquisado")
parser.add_argument("--rapido", action="store_true", help="Usa cache ou executa de forma otimizada")
args = parser.parse_args()
CLIENTE_ALVO = args.cliente

CDP_HOST_PORT = f"{CDP_HOST}:{CDP_PORT}"
JSON_OUTPUT_DIR = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "WIDEPAY_CONSULTAS"
os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
JSON_OUTPUT_FILE = JSON_OUTPUT_DIR / f"WIDEPAY_{CLIENTE_ALVO.replace(' ', '_').upper()}.json"


def normalizar_busca(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-zA-Z0-9]+", " ", texto).lower().strip()
    return texto


def gerar_termos_busca_cliente(cliente):
    base = normalizar_busca(cliente)
    if not base:
        return ["edmilson"]

    termos = {base}
    tokens = base.split()
    if "edmilson" in tokens:
        termos.add("edimson")
    if "edimson" in tokens:
        termos.add("edmilson")
    if base == "edmilson":
        termos.add("edimson")
    if base == "edimson":
        termos.add("edmilson")
    return sorted(termos, key=len, reverse=True)

async def cdp_command(ws_url, method, params=None):
    if params is None:
        params = {}
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": method,
            "params": params
        }
        await ws.send(json.dumps(msg))
        
        # Espera resposta correspondente
        while True:
            resp_str = await ws.recv()
            resp = json.loads(resp_str)
            if resp.get("id") == 1:
                return resp

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

async def ensure_widepay_logged_in(ws_url):
    print("Verificando se o WidePay requer login...")
    
    # Obter URL atual
    eval_loc = await cdp_command(ws_url, "Runtime.evaluate", {"expression": "window.location.href", "returnByValue": True})
    current_url = eval_loc.get("result", {}).get("result", {}).get("value", "")
    
    is_login_page = "login" in current_url or "acessar" in current_url
    if not is_login_page:
        eval_body = await cdp_command(ws_url, "Runtime.evaluate", {"expression": "document.body.innerText", "returnByValue": True})
        body_text = eval_body.get("result", {}).get("result", {}).get("value", "")
        if "Entrar" in body_text and "Esqueci minha senha" in body_text:
            is_login_page = True
            
    if not is_login_page:
        print("WidePay ja esta logado. Continuando fluxo...")
        return True

    print("\nTela de login detectada. Tentando preenchimento automatico do navegador dedicado via CDP...")
    
    # Foca no campo de senha para forcar o preenchimento/autofill do Chrome
    js_focus = """
    (function() {
        var emailField = document.querySelector('input[type="text"], input[type="email"], input[name="autenticacao"], input[name="email"], input[name="login"]');
        var passwordField = document.querySelector('input[type="password"], input[name="senha"]');
        if (emailField) {
            emailField.focus();
            emailField.click();
        }
        if (passwordField) {
            passwordField.focus();
            passwordField.click();
            return "focused";
        }
        return "not_found";
    })()
    """
    await cdp_command(ws_url, "Runtime.evaluate", {"expression": js_focus, "returnByValue": True})
    await asyncio.sleep(1.5) # Delay para garantir o autofill do Chrome

    js_check = """
    (function() {
        var passwordField = document.querySelector('input[type="password"], input[name*="senha"]');
        var isPasswordFilled = false;
        if (passwordField) {
            isPasswordFilled = (passwordField.value.length > 0 || passwordField.matches(':-webkit-autofill'));
        }
        
        var botoes = Array.from(document.querySelectorAll('button, input[type="submit"], [role="button"], a'));
        var submitBtn = botoes.find(function(btn) {
            var txt = (btn.innerText || btn.value || btn.textContent || '').toLowerCase().trim();
            return txt === 'acessar' || txt === 'entrar' || txt === 'entrar na conta';
        }) || document.querySelector('button[type="submit"], input[type="submit"]');
        
        var isSubmitEnabled = false;
        if (submitBtn) {
            isSubmitEnabled = !submitBtn.disabled && !submitBtn.className.includes("disabled");
        }
        
        var bodyTextLower = document.body.innerText.toLowerCase();
        
        // Detectar CAPTCHA visível/ativo
        var hasCaptcha = false;
        if (bodyTextLower.includes("digite os caracteres") || bodyTextLower.includes("resolva o captcha") || bodyTextLower.includes("prove que você não é um robô")) {
            hasCaptcha = true;
        }
        // Verificar se há iframes de desafio reCAPTCHA ativos/visíveis (bframe)
        var bframes = Array.from(document.querySelectorAll('iframe[src*="recaptcha/api2/bframe"]'));
        bframes.forEach(function(iframe) {
            var style = window.getComputedStyle(iframe);
            if (style.display !== 'none' && style.visibility !== 'hidden') {
                hasCaptcha = true;
            }
        });
        // Verificar se há widget visível (não invisible) do checkbox reCAPTCHA
        var anchors = Array.from(document.querySelectorAll('iframe[src*="recaptcha/api2/anchor"]'));
        anchors.forEach(function(iframe) {
            var src = iframe.src || '';
            if (!src.includes('size=invisible')) {
                var style = window.getComputedStyle(iframe);
                if (style.display !== 'none' && style.visibility !== 'hidden') {
                    hasCaptcha = true;
                }
            }
        });

        var has2FA = bodyTextLower.includes("duas etapas") || bodyTextLower.includes("autenticação por aplicativo") || bodyTextLower.includes("segundo fator") || bodyTextLower.includes("código de segurança") || bodyTextLower.includes("autenticador") || !!document.querySelector('input[name*="token"], input[name*="code"], input[name*="2fa"]');
        var hasError = bodyTextLower.includes("erro na") || bodyTextLower.includes("incorreta") || bodyTextLower.includes("inválido") || bodyTextLower.includes("usuario ou senha incorretos");
        
        return {
            isPasswordFilled: isPasswordFilled,
            isSubmitEnabled: isSubmitEnabled,
            hasCaptcha: hasCaptcha,
            has2FA: has2FA,
            hasError: hasError
        };
    })()
    """
    eval_res = await cdp_command(ws_url, "Runtime.evaluate", {"expression": js_check, "returnByValue": True})
    info = eval_res.get("result", {}).get("result", {}).get("value", {}) or {}
    print(f"Estado dos inputs de login: {info}")
    
    # Se a senha estiver preenchida e o botão estiver habilitado, e sem erros/captcha/2fa, clica automaticamente
    if info.get("isPasswordFilled") and info.get("isSubmitEnabled") and not info.get("hasCaptcha") and not info.get("has2FA") and not info.get("hasError"):
        print("Senha salva e preenchida detectada. Clicando em 'Acessar'...")
        js_click = """
        (function() {
            var botoes = Array.from(document.querySelectorAll('button, input[type="submit"], [role="button"], a'));
            var submitBtn = botoes.find(function(btn) {
                var txt = (btn.innerText || btn.value || btn.textContent || '').toLowerCase().trim();
                return txt === 'acessar' || txt === 'entrar' || txt === 'entrar na conta';
            }) || document.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.click();
                return "clicked";
            }
            return "not_found";
        })()
        """
        await cdp_command(ws_url, "Runtime.evaluate", {"expression": js_click, "returnByValue": True})
        
        # Enviar Enter via CDP Input também, por segurança
        await cdp_command(ws_url, "Input.dispatchKeyEvent", {
            "type": "keyDown",
            "windowsVirtualKeyCode": 13,
            "unmodifiedText": "\r",
            "text": "\r"
        })
        await asyncio.sleep(0.1)
        await cdp_command(ws_url, "Input.dispatchKeyEvent", {
            "type": "keyUp",
            "windowsVirtualKeyCode": 13
        })
        
        # Aguardar navegação
        print("Aguardando 10 segundos para navegacao e processamento do login...")
        for i in range(10):
            await asyncio.sleep(1)
            eval_loc_now = await cdp_command(ws_url, "Runtime.evaluate", {"expression": "window.location.href", "returnByValue": True})
            url_now = eval_loc_now.get("result", {}).get("result", {}).get("value", "")
            if "login" not in url_now and "acessar" not in url_now:
                print(f"Login realizado com sucesso! URL atual: {url_now}")
                return True
                
            # Verifica se apareceu algum erro ou captcha/2fa durante a navegação
            eval_res_now = await cdp_command(ws_url, "Runtime.evaluate", {"expression": js_check, "returnByValue": True})
            info_now = eval_res_now.get("result", {}).get("result", {}).get("value", {}) or {}
            if info_now.get("hasCaptcha") or info_now.get("has2FA") or info_now.get("hasError"):
                print(f"Erro detectado apos tentativa de login: {info_now}")
                break

    # Se falhar ou não puder clicar, gera motivos detalhados
    motivos = []
    if not info.get("isPasswordFilled"):
        motivos.append("campo de senha vazio")
    if not info.get("isSubmitEnabled"):
        motivos.append("botao Acessar desabilitado")
    if info.get("hasCaptcha"):
        motivos.append("desafio CAPTCHA detectado")
    if info.get("has2FA"):
        motivos.append("autenticacao em duas etapas (2FA) detectada")
    if info.get("hasError"):
        motivos.append("erro de usuario/senha incorretos exibido")
    if not motivos:
        motivos.append("navegacao nao mudou apos o clique (continua na tela de login)")
        
    motivo_str = ", ".join(motivos)
    print(f"\n[INTERVENCAO HUMANA NECESSARIA] Login automatico impossivel porque: {motivo_str}.")
    print("Por favor, resolva manualmente no navegador dedicado.")
    sys.exit(2)

async def main_async():
    print(f"Conectando ao navegador em {CDP_HOST}:{CDP_PORT}...")
    abas = obter_abas()
    if not abas:
        print("Abrindo navegador dedicado e carregando WidePay real...")
        script_inicio = ROOT_DIR / "03_SCRIPTS" / "iniciar_widepay_opera_wmi.py"
        tentativa = subprocess.run([sys.executable, str(script_inicio)], capture_output=True, text=True)
        if tentativa.stdout:
            print(tentativa.stdout, end="" if tentativa.stdout.endswith("\n") else "\n")
        if tentativa.stderr:
            print(tentativa.stderr, end="" if tentativa.stderr.endswith("\n") else "\n")
        if tentativa.returncode == 2:
            print("WIDEPAY REAL NAO ABERTO - EXECUCAO BLOQUEADA. Login manual necessario no navegador dedicado.")
            sys.exit(2)
        if tentativa.returncode not in (0, 2):
            print("WIDEPAY REAL NAO ABERTO - EXECUCAO BLOQUEADA. Falha ao abrir o Opera dedicado.")
            sys.exit(1)
        time.sleep(3)
        abas = obter_abas()
        if not abas:
            print("WIDEPAY REAL NAO ABERTO - EXECUCAO BLOQUEADA. Nao vou consultar arquivos locais antes de abrir o WidePay.")
            sys.exit(1)
        
    wp_aba = None
    for aba in abas:
        if aba.get("type") == "page" and "widepay.com" in aba.get("url", ""):
            wp_aba = aba
            break
            
    if not wp_aba:
        print("Aba do WidePay nao encontrada. Abrindo nova aba...")
        nova_aba = abrir_nova_aba("https://www.widepay.com/conta/recebimentos/carnes")
        if not nova_aba:
            print("Nao foi possivel abrir aba do WidePay.")
            sys.exit(1)
        await asyncio.sleep(3)
        abas = obter_abas()
        for aba in abas:
            if aba.get("type") == "page" and "widepay.com" in aba.get("url", ""):
                wp_aba = aba
                break
                
    if not wp_aba:
        print("Erro: Nao foi possivel localizar a aba do WidePay.")
        sys.exit(1)
        
    ws_url = wp_aba["webSocketDebuggerUrl"]
    print(f"Conectado com sucesso Ã  aba: {wp_aba.get('title')} ({wp_aba.get('url')})")
    
    # Executa a funcao de login obrigatoria
    await ensure_widepay_logged_in(ws_url)
    
    # Obter URL atualizada apos o login
    eval_location = await cdp_command(ws_url, "Runtime.evaluate", {"expression": "window.location.href", "returnByValue": True})
    current_url = eval_location.get("result", {}).get("result", {}).get("value", "")    # 2. ExtraÃ§Ã£o de CarnÃªs
    if "recebimentos/carnes" not in current_url:
        print("Navegando para a pagina de carnes...")
        await cdp_command(ws_url, "Page.navigate", {"url": "https://www.widepay.com/conta/recebimentos/carnes"})
        await asyncio.sleep(4)
        
    print(f"Executando pesquisa e extraÃ§Ã£o de CarnÃªs para '{CLIENTE_ALVO}'...")
    
    # Simplificar o nome para busca no WidePay (remover lixo do nome da pasta)
    palavras = CLIENTE_ALVO.split()
    filtro = []
    for p in palavras:
        p_lower = p.lower()
        if p_lower in ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "agua", "viva", "leandro", "meirelles", "lote", "quadra", "par"]:
            break
        # Filtrar termos de lote/quadra como E7, F14, G7, etc.
        if re.match(r'^[a-zA-Z]\d+$', p):
            continue
        filtro.append(p)
    busca_simplificada = " ".join(filtro) if filtro else "Ana Carolina"
    termo_busca_carnes_js = json.dumps(busca_simplificada, ensure_ascii=False)
    termos_busca_cobrancas_js = json.dumps(gerar_termos_busca_cliente(busca_simplificada), ensure_ascii=False)
    
    js_extract_carnes = """
    async function() {
        // 1. Garantir que todos os status estejam marcados
        var statusIds = ["jab-1083-field", "jab-1084-field", "jab-1085-field", "jab-1086-field"];
        var changed = false;
        statusIds.forEach(id => {
            var el = document.getElementById(id);
            if (el && !el.checked) {
                el.checked = true;
                el.dispatchEvent(new Event('change', { bubbles: true }));
                changed = true;
            }
        });
        
        var applyBtn = document.getElementById("jab-1088");
        if (applyBtn && changed) {
            applyBtn.click();
            await new Promise(r => setTimeout(r, 4000));
        }
        
        // 2. Pesquisar o cliente
        var searchInput = document.getElementById("jab-1036-field");
        if (searchInput) {
            searchInput.value = %s;
            searchInput.dispatchEvent(new Event('input', { bubbles: true }));
            searchInput.dispatchEvent(new Event('change', { bubbles: true }));
            
            var searchBtn = document.getElementById("jab-1038");
            if (searchBtn) {
                searchBtn.click();
            } else {
                searchInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
            }
            await new Promise(r => setTimeout(r, 4000));
        }
        
        // 3. Loop de extraÃ§Ã£o de todas as pÃ¡ginas
        var carnes = [];
        var nomeEncontrado = "%s";
        var page = 1;
        
        while (page <= 10) {
            var trs = Array.from(document.querySelectorAll('tr'));
            var query = %s.toLowerCase();
            
            var foundRows = trs.filter(tr => {
                var text = tr.innerText.toLowerCase();
                return text.includes(query);
            });
            
            foundRows.forEach(tr => {
                var tds = tr.querySelectorAll('td');
                if (tds.length >= 16) {
                    var col_id = tds[1].innerText.trim();
                    var col_cliente = tds[2].innerText.trim();
                    var col_referencia = tds[8].innerText.trim();
                    var col_valor = tds[9].innerText.trim();
                    var col_parcelas = tds[10].innerText.trim();
                    var col_recebimentos = tds[11].innerText.trim();
                    var col_prox_venc = tds[12].innerText.trim();
                    var col_ult_venc = tds[13].innerText.trim();
                    var col_status = tds[15].innerText.trim();
                    
                    nomeEncontrado = col_cliente;
                    
                    var pagas = 0;
                    var total_geradas = parseInt(col_parcelas) || 24;
                    var total_recebido = 0.0;
                    
                    var rec_match = col_recebimentos.match(/(\\d+)\\/(\\d+)\\s+R\\$\\s*([\\d\\.,]+)/);
                    if (rec_match) {
                        pagas = parseInt(rec_match[1]);
                        total_geradas = parseInt(rec_match[2]);
                        total_recebido = parseFloat(rec_match[3].replace(/\\./g, '').replace(',', '.'));
                    } else {
                        var parts = col_recebimentos.split('/');
                        if (parts.length >= 2) {
                            pagas = parseInt(parts[0].trim()) || 0;
                            var right_parts = parts[1].split('R$');
                            total_geradas = parseInt(right_parts[0].trim()) || total_geradas;
                            if (right_parts.length >= 2) {
                                total_recebido = parseFloat(right_parts[1].replace(/\\./g, '').replace(',', '.')) || 0.0;
                            }
                        }
                    }
                    
                    var valor_parcela = parseFloat(col_valor.replace(/\\./g, '').replace(',', '.')) || 0.0;
                    var parcelas_restantes = total_geradas - pagas;
                    var total_pendente = parcelas_restantes * valor_parcela;
                    
                    if (!carnes.some(c => c.carne === col_id)) {
                        carnes.push({
                            carne: col_id,
                            referencia: col_referencia,
                            valor_parcela: valor_parcela,
                            parcelas_geradas: total_geradas,
                            parcelas_pagas: pagas,
                            parcelas_restantes: parcelas_restantes,
                            total_recebido: total_recebido,
                            total_pendente: total_pendente,
                            proximo_vencimento: col_prox_venc,
                            ultimo_vencimento: col_ult_venc,
                            status: col_status
                        });
                    }
                }
            });
            
            var nextBtn = document.getElementById("jab-1023");
            if (nextBtn && !nextBtn.disabled && !nextBtn.className.includes("disabled")) {
                nextBtn.click();
                page++;
                await new Promise(r => setTimeout(r, 4000));
            } else {
                break;
            }
        }
        
        return {
            nome_encontrado: nomeEncontrado,
            carnes: carnes
        };
    }
    """ % (termo_busca_carnes_js, CLIENTE_ALVO, termo_busca_carnes_js)
    
    eval_extract_carnes = await cdp_command(ws_url, "Runtime.evaluate", {
        "expression": f"({js_extract_carnes})()",
        "awaitPromise": True,
        "returnByValue": True
    })
    
    raw_data_carnes = eval_extract_carnes.get("result", {}).get("result", {}).get("value", {})
    if not raw_data_carnes:
        print("Erro: A extraÃ§Ã£o de carnÃªs via JS retornou vazia.")
        raw_data_carnes = {"nome_encontrado": CLIENTE_ALVO, "carnes": []}
        
    # 3. Navegar para a pÃ¡gina de CobranÃ§as
    print("Navegando para a pagina de cobrancas...")
    await cdp_command(ws_url, "Page.navigate", {"url": "https://www.widepay.com/conta/recebimentos"})
    await asyncio.sleep(4)
    
    print(f"Executando pesquisa e extraÃ§Ã£o de CobranÃ§as/Boletos para '{CLIENTE_ALVO}'...")
    
    js_extract_cobrancas = """
    async function() {
        // 1. Garantir que os status estejam marcados
        var labels = Array.from(document.querySelectorAll('label'));
        var changed = false;
        ["Aguardando", "Cancelado", "Recebido", "Vencido"].forEach(status => {
            var label = labels.find(l => l.innerText.trim() === status);
            if (label) {
                var checkbox = document.getElementById(label.getAttribute('for')) || label.querySelector('input[type="checkbox"]');
                if (checkbox && !checkbox.checked) {
                    checkbox.checked = true;
                    checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                    changed = true;
                }
            }
        });
        
        var statusIds = ["jab-1098-field", "jab-1099-field", "jab-1103-field", "jab-1106-field"];
        statusIds.forEach(id => {
            var el = document.getElementById(id);
            if (el && !el.checked) {
                el.checked = true;
                el.dispatchEvent(new Event('change', { bubbles: true }));
                changed = true;
            }
        });
        
        var applyBtn = document.getElementById("jab-1110") || Array.from(document.querySelectorAll('button')).find(btn => btn.innerText.includes("Aplicar"));
        if (applyBtn && changed) {
            applyBtn.click();
            await new Promise(r => setTimeout(r, 4000));
        }
        
        // 2. Pesquisar cada alias do cliente separadamente
        var queryTerms = %s;
        var cobrancas = [];
        var searchInput = document.getElementById("jab-1043-field") || document.querySelector('input[placeholder*="Pesquisar"], input[type="text"], input[type="search"]');
        for (var termIndex = 0; termIndex < queryTerms.length; termIndex++) {
            var termoAtual = queryTerms[termIndex];
            if (!searchInput || !termoAtual) {
                continue;
            }
            searchInput.value = termoAtual;
            searchInput.dispatchEvent(new Event('input', { bubbles: true }));
            searchInput.dispatchEvent(new Event('change', { bubbles: true }));
            
            var searchBtn = document.getElementById("jab-1045") || Array.from(document.querySelectorAll('button')).find(btn => btn.innerText.includes("Buscar") || btn.className.includes("search"));
            if (searchBtn) {
                searchBtn.click();
            } else {
                searchInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
            }
            await new Promise(r => setTimeout(r, 4000));
            
            // 3. Loop de extracao das cobrancas do termo atual
            var page = 1;
            while (page <= 10) {
                var trs = Array.from(document.querySelectorAll('tr'));
                var foundRows = trs.filter(tr => {
                    var text = tr.innerText.toLowerCase();
                    return text.includes((termoAtual || '').toLowerCase());
                });
                
                foundRows.forEach(tr => {
                    var tds = tr.querySelectorAll('td');
                    if (tds.length >= 21) {
                        var col_id = tds[1].innerText.trim();
                        var col_forma = tds[3].innerText.trim();
                        var col_cliente = tds[4].innerText.trim();
                        var col_referencia = tds[10].innerText.trim();
                        var col_valor = tds[11].innerText.trim();
                        var col_recebido = tds[12].innerText.trim();
                        var col_vencimento = tds[14].innerText.trim();
                        var col_pagamento = tds[15].innerText.trim();
                        var col_status = tds[20].innerText.trim();
                        
                        var valor_original = parseFloat(col_valor.replace(/\\./g, '').replace(',', '.')) || 0.0;
                        var valor_recebido = 0.0;
                        if (col_recebido && col_recebido !== "-") {
                            valor_recebido = parseFloat(col_recebido.replace(/\\./g, '').replace(',', '.')) || 0.0;
                        }
                        
                        var desc_lower = col_referencia.toLowerCase();
                        var pertence_a_carne = desc_lower.includes("carne") || desc_lower.includes("carn");
                        var avulsa = !pertence_a_carne;
                        
                        if (!cobrancas.some(c => c.id === col_id)) {
                            cobrancas.push({
                                id: col_id,
                                forma: col_forma,
                                cliente: col_cliente,
                                descricao: col_referencia,
                                valor_original: valor_original,
                                valor_recebido: valor_recebido,
                                vencimento: col_vencimento,
                                pagamento: col_pagamento,
                                status: col_status,
                                pertence_a_carne: pertence_a_carne,
                                avulsa: avulsa
                            });
                        }
                    }
                });
                
                var nextBtn = Array.from(document.querySelectorAll('button, a')).find(el => {
                    var txt = el.innerText || '';
                    var cls = el.className || '';
                    var id = el.id || '';
                    return (id.includes('next') || cls.includes('next') || txt.includes('Pr') || txt.includes('>') || el.querySelector('i.fa-angle-right') || el.querySelector('i.fa-chevron-right'));
                });
                
                if (nextBtn && !nextBtn.disabled && !nextBtn.className.includes("disabled")) {
                    nextBtn.click();
                    page++;
                    await new Promise(r => setTimeout(r, 4000));
                } else {
                    break;
                }
            }
        }
        return cobrancas;
    }
    """ % (termos_busca_cobrancas_js)
    
    eval_extract_cobrancas = await cdp_command(ws_url, "Runtime.evaluate", {
        "expression": f"({js_extract_cobrancas})()",
        "awaitPromise": True,
        "returnByValue": True
    })
    
    raw_data_cobrancas = eval_extract_cobrancas.get("result", {}).get("result", {}).get("value", [])
    if not raw_data_cobrancas:
        print("Erro: A extraÃ§Ã£o de cobranÃ§as via JS retornou vazia.")
        raw_data_cobrancas = []
        
    # 4. ClassificaÃ§Ã£o, De-duplicidade e ConsolidaÃ§Ã£o
    carnes_lista = raw_data_carnes.get("carnes") or []
    cobrancas_lista = []
    boletos_avulsos = []
    possiveis_duplicidades = []
    
    cobrancas_unicas = []
    for cob in raw_data_cobrancas:
        # Check for duplicate
        is_duplicate = False
        for existing in cobrancas_unicas:
            # Same ID or same characteristics (desc, due date, original, received, status)
            if (existing["id"] == cob["id"] and cob["id"]) or (
                existing["descricao"] == cob["descricao"] and 
                existing["vencimento"] == cob["vencimento"] and 
                abs(existing["valor_original"] - cob["valor_original"]) < 0.01 and 
                abs(existing["valor_recebido"] - cob["valor_recebido"]) < 0.01 and 
                existing["status"] == cob["status"]
            ):
                is_duplicate = True
                break
        
        # Apply Python classification heuristic to prevent false avulsas
        desc_lower = cob["descricao"].lower()
        pertence_a_carne = "carne" in desc_lower or "carnÃª" in desc_lower
        
        if not pertence_a_carne:
            for c in carnes_lista:
                if c["status"].lower() != "cancelado":
                    if abs(cob["valor_original"] - float(c["valor_parcela"])) < 0.01:
                        ref_lower = c["referencia"].lower()
                        if not cob["descricao"].strip() or (ref_lower and ref_lower in desc_lower):
                            if not any(word in desc_lower for word in ["atraso", "atrazos", "ref atraso", "atr", "mÃªs", "mes"]):
                                pertence_a_carne = True
                                break
                                
        cob["pertence_a_carne"] = pertence_a_carne
        cob["avulsa"] = not pertence_a_carne
        cob["duplicidade"] = is_duplicate
        cobrancas_lista.append(cob)
        
        if is_duplicate:
            possiveis_duplicidades.append(cob)
        else:
            cobrancas_unicas.append(cob)
            if cob["avulsa"]:
                boletos_avulsos.append(cob)
                
    # 5. Calcular Totais
    # Totais Carnes
    total_pago_carnes = 0.0
    total_pendente_carnes = 0.0
    total_pagas_carnes = 0
    total_geradas_carnes = 0
    
    for c in carnes_lista:
        if c["status"].lower() != "cancelado":
            total_pago_carnes += float(c["total_recebido"])
            total_pendente_carnes += float(c["total_pendente"])
            total_pagas_carnes += int(c["parcelas_pagas"])
            total_geradas_carnes += int(c["parcelas_geradas"])
            
    totais_carnes = {
        "total_pago": round(total_pago_carnes, 2),
        "total_pendente": round(total_pendente_carnes, 2),
        "parcelas_pagas": total_pagas_carnes,
        "parcelas_geradas": total_geradas_carnes
    }
    
    # Totais Cobrancas Avulsas
    total_pago_avulsas = 0.0
    total_pendente_avulsas = 0.0
    
    for cob in boletos_avulsos:
        if cob["status"] == "Recebido":
            total_pago_avulsas += cob["valor_recebido"]
        elif cob["status"] in ["Aguardando", "Vencido"]:
            total_pendente_avulsas += cob["valor_original"]
            
    totais_cobrancas_avulsas = {
        "total_pago": round(total_pago_avulsas, 2),
        "total_pendente": round(total_pendente_avulsas, 2)
    }
    
    # Totais Consolidados
    totais_consolidados = {
        "total_pago_consolidado": round(total_pago_carnes + total_pago_avulsas, 2),
        "total_pendente_consolidado": round(total_pendente_carnes + total_pendente_avulsas, 2)
    }
    
    status_final = "CONECTADO" if (carnes_lista or cobrancas_lista) else "PENDENTE"
    nome_final = raw_data_carnes.get("nome_encontrado") or CLIENTE_ALVO
    
    resultado_json = {
        "cliente": nome_final,
        "status_conexao": "LOGADO",
        "status_geral": status_final,
        "carnes": carnes_lista,
        "cobrancas": cobrancas_lista,
        "boletos_avulsos": boletos_avulsos,
        "possiveis_duplicidades": possiveis_duplicidades,
        "totais_carnes": totais_carnes,
        "totais_cobrancas_avulsas": totais_cobrancas_avulsas,
        "totais_consolidados": totais_consolidados
    }
    
    with open(JSON_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultado_json, f, indent=4, ensure_ascii=False)
        
    print(f"JSON de consulta salvo em: {JSON_OUTPUT_FILE}")
    print(f"Total de carnÃªs extraÃ­dos: {len(carnes_lista)}")
    print(f"Total de cobranÃ§as extraÃ­das: {len(cobrancas_lista)}")
    print(f"Total de cobranÃ§as avulsas: {len(boletos_avulsos)}")
    print(f"Total de possÃ­veis duplicidades: {len(possiveis_duplicidades)}")
    
    if status_final == "CONECTADO":
        print(f"\nSTATUS FINAL: CLIENTE ENCONTRADO E DADOS EXTRAIDOS")
        sys.exit(0)
    else:
        print(f"\nSTATUS FINAL: CONECTADO MAS CLIENTE NAO ENCONTRADO / SEM DADOS")
        sys.exit(0)

def main():
    try:
        asyncio.run(main_async())
    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        print(f"Erro na execucao do script de consulta: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
