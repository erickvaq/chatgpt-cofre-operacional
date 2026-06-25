# -*- coding: utf-8 -*-
import os
import json
import asyncio
import sys
import websockets
import urllib.request
import urllib.parse
import re
import unicodedata
from pathlib import Path

# Configuração e inicialização importáveis
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

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
        while True:
            resp_str = await ws.recv()
            resp = json.loads(resp_str)
            if resp.get("id") == 1:
                return resp

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

async def ensure_widepay_logged_in(ws_url):
    print("Verificando se o WidePay requer login...")
    
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
    
    # Se a senha estiver preenchida e o botão estiver habilitado, clica automaticamente.
    # Erro antigo na tela nao impede nova tentativa quando o navegador manteve autofill valido.
    if info.get("isPasswordFilled") and info.get("isSubmitEnabled") and not info.get("hasCaptcha") and not info.get("has2FA"):
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
                print(f"Erro detectado após tentativa de login: {info_now}")
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
    raise RuntimeError(f"Login automatico impossivel porque: {motivo_str}. Por favor, faca login manualmente.")

async def extrair_dados_cliente(ws_url, cliente_nome):
    """Navega, pesquisa e extrai carnes e cobrancas do WidePay para o cliente_nome."""
    await ensure_widepay_logged_in(ws_url)
    
    # 1. Obter URL
    eval_loc = await cdp_command(ws_url, "Runtime.evaluate", {"expression": "window.location.href", "returnByValue": True})
    current_url = eval_loc.get("result", {}).get("result", {}).get("value", "")
    
    # 2. Navegar para Carnes
    if "recebimentos/carnes" not in current_url:
        print("Navegando para a pagina de carnes...")
        await cdp_command(ws_url, "Page.navigate", {"url": "https://www.widepay.com/conta/recebimentos/carnes"})
        await asyncio.sleep(4)
        
    print(f"Pesquisando Carnes para '{cliente_nome}'...")
    
    # Normalizar busca do nome
    palavras = cliente_nome.split()
    filtro = []
    for p in palavras:
        p_lower = p.lower()
        if p_lower in ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "agua", "viva", "leandro", "meirelles", "lote", "quadra", "par"]:
            break
        if re.match(r'^[a-zA-Z]\d+$', p):
            continue
        filtro.append(p)
    busca_simplificada = " ".join(filtro) if filtro else "Edmilson"
    termo_busca_carnes_js = json.dumps(busca_simplificada, ensure_ascii=False)
    termos_busca_cobrancas_js = json.dumps(gerar_termos_busca_cliente(busca_simplificada), ensure_ascii=False)
    
    js_extract_carnes = """
    async function() {
        // Garantir que todos os status estejam marcados
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
    """ % (termo_busca_carnes_js, cliente_nome, termo_busca_carnes_js)
    
    eval_extract_carnes = await cdp_command(ws_url, "Runtime.evaluate", {
        "expression": f"({js_extract_carnes})()",
        "awaitPromise": True,
        "returnByValue": True
    })
    raw_data_carnes = eval_extract_carnes.get("result", {}).get("result", {}).get("value", {}) or {}
    
    # 3. Navegar para Cobranças
    print("Navegando para a pagina de cobrancas...")
    await cdp_command(ws_url, "Page.navigate", {"url": "https://www.widepay.com/conta/recebimentos"})
    await asyncio.sleep(4)
    
    print(f"Pesquisando Cobranças/Boletos para '{cliente_nome}'...")
    
    js_extract_cobrancas = """
    async function() {
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
    raw_data_cobrancas = eval_extract_cobrancas.get("result", {}).get("result", {}).get("value", []) or []
    
    nome_final = raw_data_carnes.get("nome_encontrado") or cliente_nome
    
    # Salvar evidência bruta JSON
    JSON_OUTPUT_DIR = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "WIDEPAY_CONSULTAS"
    os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
    nome_slug = nome_final.replace(" ", "_").upper()
    caminho_json = JSON_OUTPUT_DIR / f"WIDEPAY_{nome_slug}.json"
    
    resultado_json = {
        "cliente": nome_final,
        "status_conexao": "LOGADO",
        "carnes": raw_data_carnes.get("carnes") or [],
        "cobrancas": raw_data_cobrancas
    }
    
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(resultado_json, f, indent=4, ensure_ascii=False)
        
    print(f"Dados brutos extraidos do WidePay salvos em {caminho_json}")
    return resultado_json
