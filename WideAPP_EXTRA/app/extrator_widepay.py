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

from app.coletor_tabelas_paginadas import COLETOR_TABELAS_PAGINADAS_JS, validar_coleta_paginada

# Configuração e inicialização importáveis
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

async def cdp_command(ws_url, method, params=None):
    if params is None:
        params = {}
    async with websockets.connect(ws_url, max_size=None) as ws:
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
        return ["edmilson", "edimson", "edjinson"]
    termos = {base}
    tokens = base.split()
    
    # Trata variações e erros comuns de digitação para Edmilson
    if any(t in tokens for t in ["edmilson", "edimson", "edjinson"]):
        termos.add("edmilson")
        termos.add("edimson")
        termos.add("edjinson")
        
    return sorted(termos, key=len, reverse=True)


TOKENS_IGNORADOS_BUSCA = {
    "a", "e", "de", "da", "do", "das", "dos",
    "leo", "leonardo", "copia", "contrato", "agua", "viva", "leandro",
    "meirelles", "lote", "quadra", "par", "wp", "pdf", "docx", "txt",
}


def extrair_tokens_busca_cliente(cliente):
    base = normalizar_busca(cliente)
    tokens = []
    for token in base.split():
        if token in TOKENS_IGNORADOS_BUSCA:
            continue
        if re.match(r"^[a-z]\d+[a-z]?$", token):
            continue
        tokens.append(token)
    return tokens


def gerar_termos_busca_cliente(cliente):
    tokens = extrair_tokens_busca_cliente(cliente)
    if not tokens:
        return ["edmilson", "edimson", "edjinson"]

    termos = []

    def adicionar(termo):
        termo = normalizar_busca(termo)
        if termo and termo not in termos:
            termos.append(termo)

    primeiro_nome = tokens[0]
    adicionar(primeiro_nome)

    if len(tokens) >= 2:
        adicionar(" ".join(tokens[:2]))

    adicionar(" ".join(tokens))

    if primeiro_nome in {"edmilson", "edimson", "edjinson"}:
        for alias in ("edmilson", "edimson", "edjinson"):
            adicionar(alias)

    return termos

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

async def extrair_dados_clientes_bloco(ws_url, clientes_bloco, progress_callback=None):
    """Navega, executa pesquisa em branco e extrai dados de até 3 clientes simultaneamente."""
    await ensure_widepay_logged_in(ws_url)
    
    # Inicializar estado de progresso na janela do navegador
    await cdp_command(ws_url, "Runtime.evaluate", {
        "expression": "window.wideapp_progress = null",
        "returnByValue": True
    })
    
    extraction_done = False

    async def poll_progress_loop():
        while not extraction_done:
            try:
                eval_prog = await cdp_command(ws_url, "Runtime.evaluate", {
                    "expression": "window.wideapp_progress",
                    "returnByValue": True
                })
                prog = eval_prog.get("result", {}).get("result", {}).get("value")
                if prog and isinstance(prog, dict):
                    et = prog.get("etapa")
                    pg = prog.get("pagina", 1)
                    aceitos = prog.get("total_aceitos", 0)
                    if progress_callback:
                        if et == "carnes":
                            pct = 40 + min(pg * 1, 14)
                            msg = f"Coletando carnês — página {pg} (coletados: {aceitos})"
                            progress_callback("Coleta Carnes", pct, msg)
                        elif et == "cobrancas":
                            pct = 55 + min(pg * 2, 14)
                            msg = f"Coletando cobranças — página {pg} (coletados: {aceitos})"
                            progress_callback("Coleta Cobranças", pct, msg)
            except Exception:
                pass
            await asyncio.sleep(1)

    poll_task = asyncio.create_task(poll_progress_loop())
    # 1. Obter URL
    eval_loc = await cdp_command(ws_url, "Runtime.evaluate", {"expression": "window.location.href", "returnByValue": True})
    current_url = eval_loc.get("result", {}).get("result", {}).get("value", "")
    
    # 2. Navegar para Carnes
    if "recebimentos/carnes" not in current_url:
        print("Navegando para a pagina de carnes...")
        await cdp_command(ws_url, "Page.navigate", {"url": "https://www.widepay.com/conta/recebimentos/carnes"})
        await asyncio.sleep(4)
        
    print(f"Extração em Bloco (WidePay) iniciada para: {', '.join(c['nome'] for c in clientes_bloco)}")
    
    # Preparar payload JSON dos clientes para injetar no JavaScript
    clientes_js_payload = []
    for c in clientes_bloco:
        tokens_busca = extrair_tokens_busca_cliente(c["nome"])
        busca_simp = tokens_busca[0] if tokens_busca else "Edmilson"
        c_query_terms = gerar_termos_busca_cliente(busca_simp)
        clientes_js_payload.append({
            "nome": c["nome"],
            "query_terms": c_query_terms,
            "lote": c.get("lote") or "-",
            "quadra": c.get("quadra") or "-"
        })
        
    clientes_js_string = json.dumps(clientes_js_payload, ensure_ascii=False)
    coletor_paginado_js = COLETOR_TABELAS_PAGINADAS_JS
    
    js_extract_carnes = """
    async function() {
        %s
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

        var wideappRpp = await wideappSelecionarMaiorRegistrosPorPagina("Carnes");
        
        function marcadorPagina() {
            var totalWideapp = wideappInfoTotalTabela();
            if (totalWideapp && totalWideapp.texto) {
                return totalWideapp.texto;
            }
            var paginaWideapp = wideappInfoPagina();
            if (paginaWideapp && paginaWideapp.texto) {
                return paginaWideapp.texto;
            }
            var texto = document.body.innerText || '';
            var m = texto.match(/Página\\s+(\\d+)\\s+de\\s+(\\d+)/i) || texto.match(/Pagina\\s+(\\d+)\\s+de\\s+(\\d+)/i);
            if (m) {
                return m[1] + "/" + m[2];
            }
            var atual = document.querySelector('[aria-current="page"], .active, .current');
            if (atual) {
                return (atual.innerText || atual.textContent || atual.value || '').trim();
            }
            return String(window.location.href) + "|" + String(texto.length);
        }
        
        var clientesBloco = %s;
        var carnesPorCliente = {};
        clientesBloco.forEach(c => {
            carnesPorCliente[c.nome] = [];
        });
        
        var visitadas = [];
        var paginasWideapp = [];
        var totalAceitos = 0;
        var totalIgnorados = 0;
        var ignoradosLog = [];
        
        var searchInput = document.getElementById("jab-1036-field");
        if (searchInput) {
            var termoBusca = "";
            if (clientesBloco.length === 1) {
                var tokens = clientesBloco[0].nome.split(" ").filter(Boolean);
                termoBusca = tokens[0] || "";
            }
            searchInput.value = termoBusca;
            searchInput.dispatchEvent(new Event('input', { bubbles: true }));
            searchInput.dispatchEvent(new Event('change', { bubbles: true }));
            var searchBtn = document.getElementById("jab-1038");
            if (searchBtn) searchBtn.click();
            else searchInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
            await new Promise(r => setTimeout(r, 4500));
        }
        
        await wideappIrPrimeiraPagina();
        var page = 1;
        
        while (page <= 25) {
            var marcador = marcadorPagina() + "|bloco";
            if (visitadas.indexOf(marcador) !== -1) {
                break;
            }
            visitadas.push(marcador);

            var trs = Array.from(document.querySelectorAll('tr'));
            
            trs.forEach(tr => {
                var tds = tr.querySelectorAll('td');
                if (tds.length >= 16) {
                    var col_cliente = tds[2].innerText.trim();
                    var col_cliente_norm = wideappNormalizarBusca(col_cliente);
                    var col_referencia = tds[8].innerText.trim().toLowerCase();
                    
                    var matchedCliente = null;
                    for (var i = 0; i < clientesBloco.length; i++) {
                        var cli = clientesBloco[i];
                        
                        var matchName = false;
                        var cli_nome_norm = wideappNormalizarBusca(cli.nome);
                        if (col_cliente_norm.includes(cli_nome_norm)) {
                            matchName = true;
                        } else {
                            var tokens = cli_nome_norm.split(" ").filter(Boolean);
                            if (tokens.length >= 2) {
                                var primeiros = tokens[0] + " " + tokens[1];
                                if (col_cliente_norm.includes(primeiros)) {
                                    matchName = true;
                                }
                            }
                        }
                        
                        var primeiroNome = cli_nome_norm.split(" ")[0];
                        var loteAlvo = (cli.lote || "").trim().toLowerCase();
                        var matchLote = false;
                        if (loteAlvo && loteAlvo !== "-") {
                            var refNorm = col_referencia.replace(/[^a-z0-9]+/g, "");
                            var loteNorm = loteAlvo.replace(/[^a-z0-9]+/g, "");
                            if (refNorm.includes(loteNorm)) {
                                matchLote = true;
                            }
                        }
                        
                        if (!matchName && primeiroNome && col_cliente_norm.includes(primeiroNome) && matchLote) {
                            matchName = true;
                        }
                        
                        if (matchName) {
                            matchedCliente = cli;
                            break;
                        }
                    }
                    
                    if (!matchedCliente) {
                        totalIgnorados++;
                        if (ignoradosLog.indexOf(col_cliente) === -1) {
                            ignoradosLog.push(col_cliente);
                        }
                        return;
                    }
                    
                    var col_id = tds[1].innerText.trim();
                    var col_referencia_real = tds[8].innerText.trim();
                    var col_valor = tds[9].innerText.trim();
                    var col_parcelas = tds[10].innerText.trim();
                    var col_recebimentos = tds[11].innerText.trim();
                    var col_prox_venc = tds[12].innerText.trim();
                    var col_ult_venc = tds[13].innerText.trim();
                    var col_status = tds[15].innerText.trim();
                    
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
                    
                    var cli_lista = carnesPorCliente[matchedCliente.nome];
                    if (!cli_lista.some(c => c.carne === col_id)) {
                        cli_lista.push({
                            carne: col_id,
                            referencia: col_referencia_real,
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
                    totalAceitos++;
                }
            });

            window.wideapp_progress = {
                etapa: "carnes",
                pagina: page,
                total_aceitos: totalAceitos,
                total_ignorados: totalIgnorados
            };

            var totalPagina = wideappInfoTotalTabela();
            var infoPagina = wideappInfoPagina();
            paginasWideapp.push({
                termo: "bloco",
                pagina: infoPagina.atual || page,
                paginas: infoPagina.total,
                totalWidePay: totalPagina.total,
                faixa: totalPagina.texto,
                coletadosPagina: totalAceitos
            });
            
            var nextBtn = wideappBotaoPaginacao('next');
            if (nextBtn && !wideappDisabled(nextBtn)) {
                nextBtn.click();
                page++;
                await new Promise(r => setTimeout(r, 3500));
            } else {
                break;
            }
        }

        var totalInfoFinal = wideappInfoTotalTabela();
        var totalInformado = totalInfoFinal.total;
        paginasWideapp.forEach(function(p) {
            if (p.totalWidePay !== null && p.totalWidePay !== undefined) {
                totalInformado = Math.max(totalInformado || 0, p.totalWidePay);
            }
        });
        var metaColeta = wideappValidarMetaColeta({
            tela: "Carnes",
            filtro: "bloco",
            registrosPorPagina: wideappRpp,
            totalWidePay: { total: totalInformado, texto: totalInfoFinal.texto },
            paginas: paginasWideapp,
            totalColetadoUnico: totalAceitos,
            erros: []
        });
        
        return {
            carnes_por_cliente: carnesPorCliente,
            total_aceitos: totalAceitos,
            total_ignorados: totalIgnorados,
            clientes_ignorados: ignoradosLog,
            _wideapp_meta_coleta: metaColeta
        };
    }
    """ % (coletor_paginado_js, clientes_js_string)
    
    eval_extract_carnes = await cdp_command(ws_url, "Runtime.evaluate", {
        "expression": f"({js_extract_carnes})()",
        "awaitPromise": True,
        "returnByValue": True
    })
    raw_data_carnes = eval_extract_carnes.get("result", {}).get("result", {}).get("value", {}) or {}
    print(f"[Evidência] Extração em Bloco de Carnes WidePay concluída. "
          f"{raw_data_carnes.get('total_aceitos', 0)} registros aceitos, "
          f"{raw_data_carnes.get('total_ignorados', 0)} ignorados de outros clientes (ignorados: {raw_data_carnes.get('clientes_ignorados', [])})")
    validar_coleta_paginada("Carnes_Bloco", raw_data_carnes)
    
    # 3. Navegar para Cobranças
    print("Navegando para a pagina de cobrancas...")
    await cdp_command(ws_url, "Page.navigate", {"url": "https://www.widepay.com/conta/recebimentos"})
    await asyncio.sleep(4)
    
    print(f"Extração em Bloco (WidePay - Cobranças) iniciada...")
    
    js_extract_cobrancas = """
    async function() {
        %s
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

        var wideappRpp = await wideappSelecionarMaiorRegistrosPorPagina("Cobrancas/Boletos");
        
        function marcadorPagina() {
            var totalWideapp = wideappInfoTotalTabela();
            if (totalWideapp && totalWideapp.texto) {
                return totalWideapp.texto;
            }
            var paginaWideapp = wideappInfoPagina();
            if (paginaWideapp && paginaWideapp.texto) {
                return paginaWideapp.texto;
            }
            var texto = document.body.innerText || '';
            var m = texto.match(/Página\\s+(\\d+)\\s+de\\s+(\\d+)/i) || texto.match(/Pagina\\s+(\\d+)\\s+de\\s+(\\d+)/i);
            if (m) {
                return m[1] + "/" + m[2];
            }
            var atual = document.querySelector('[aria-current="page"], .active, .current');
            if (atual) {
                return (atual.innerText || atual.textContent || atual.value || '').trim();
            }
            return String(window.location.href) + "|" + String(texto.length);
        }

        var clientesBloco = %s;
        var cobrancasPorCliente = {};
        clientesBloco.forEach(c => {
            cobrancasPorCliente[c.nome] = [];
        });
        
        var visitadas = [];
        var paginasWideapp = [];
        var totalAceitos = 0;
        var totalIgnorados = 0;
        var ignoradosLog = [];
        var searchInput = document.getElementById("jab-1043-field") || document.querySelector('input[placeholder*="Pesquisar"], input[type="text"], input[type="search"]');
        if (searchInput) {
            var termoBusca = "";
            if (clientesBloco.length === 1) {
                var tokens = clientesBloco[0].nome.split(" ").filter(Boolean);
                termoBusca = tokens[0] || "";
            }
            searchInput.value = termoBusca;
            searchInput.dispatchEvent(new Event('input', { bubbles: true }));
            searchInput.dispatchEvent(new Event('change', { bubbles: true }));
            var searchBtn = document.getElementById("jab-1045") || Array.from(document.querySelectorAll('button')).find(btn => btn.innerText.includes("Buscar") || btn.className.includes("search"));
            if (searchBtn) searchBtn.click();
            else searchInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
            await new Promise(r => setTimeout(r, 4500));
        }
        
        await wideappIrPrimeiraPagina();
        var page = 1;
        
        while (page <= 25) {
            var marcador = marcadorPagina() + "|bloco";
            if (visitadas.indexOf(marcador) !== -1) {
                break;
            }
            visitadas.push(marcador);

            var trs = Array.from(document.querySelectorAll('tr'));
            
            trs.forEach(tr => {
                var tds = tr.querySelectorAll('td');
                if (tds.length >= 21) {
                    var col_cliente = tds[4].innerText.trim();
                    var col_cliente_norm = wideappNormalizarBusca(col_cliente);
                    var col_referencia = tds[10].innerText.trim().toLowerCase();
                    
                    var matchedCliente = null;
                    for (var i = 0; i < clientesBloco.length; i++) {
                        var cli = clientesBloco[i];
                        var matchName = false;
                        var cli_nome_norm = wideappNormalizarBusca(cli.nome);
                        if (col_cliente_norm.includes(cli_nome_norm)) {
                            matchName = true;
                        } else {
                            var tokens = cli_nome_norm.split(" ").filter(Boolean);
                            if (tokens.length >= 2) {
                                var primeiros = tokens[0] + " " + tokens[1];
                                if (col_cliente_norm.includes(primeiros)) {
                                    matchName = true;
                                }
                            }
                        }
                        
                        var primeiroNome = cli_nome_norm.split(" ")[0];
                        var loteAlvo = (cli.lote || "").trim().toLowerCase();
                        
                        var matchLote = false;
                        if (loteAlvo && loteAlvo !== "-") {
                            var refNorm = col_referencia.replace(/[^a-z0-9]+/g, "");
                            var loteNorm = loteAlvo.replace(/[^a-z0-9]+/g, "");
                            if (refNorm.includes(loteNorm)) {
                                matchLote = true;
                            }
                        }
                        
                        if (!matchName && primeiroNome && col_cliente_norm.includes(primeiroNome) && matchLote) {
                            matchName = true;
                        }
                        
                        if (matchName) {
                            matchedCliente = cli;
                            break;
                        }
                    }
                    
                    if (!matchedCliente) {
                        totalIgnorados++;
                        if (ignoradosLog.indexOf(col_cliente) === -1) {
                            ignoradosLog.push(col_cliente);
                        }
                        return;
                    }
                    
                    var col_id = tds[1].innerText.trim();
                    var col_forma = tds[3].innerText.trim();
                    var col_referencia_real = tds[10].innerText.trim();
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
                    
                    var desc_lower = col_referencia_real.toLowerCase();
                    var pertence_a_carne = desc_lower.includes("carne") || desc_lower.includes("carn");
                    var avulsa = !pertence_a_carne;
                    
                    var cli_lista = cobrancasPorCliente[matchedCliente.nome];
                    if (!cli_lista.some(c => c.id === col_id)) {
                        cli_lista.push({
                            id: col_id,
                            forma: col_forma,
                            cliente: col_cliente,
                            descricao: col_referencia_real,
                            valor_original: valor_original,
                            valor_recebido: valor_recebido,
                            vencimento: col_vencimento,
                            pagamento: col_pagamento,
                            status: col_status,
                            pertence_a_carne: pertence_a_carne,
                            avulsa: avulsa
                        });
                    }
                    totalAceitos++;
                }
            });

            window.wideapp_progress = {
                etapa: "cobrancas",
                pagina: page,
                total_aceitos: totalAceitos,
                total_ignorados: totalIgnorados
            };

            var totalPagina = wideappInfoTotalTabela();
            var infoPagina = wideappInfoPagina();
            paginasWideapp.push({
                termo: "bloco",
                pagina: infoPagina.atual || page,
                paginas: infoPagina.total,
                totalWidePay: totalPagina.total,
                faixa: totalPagina.texto,
                coletadosPagina: totalAceitos
            });
            
            var nextBtn = wideappBotaoPaginacao('next');
            if (nextBtn && !wideappDisabled(nextBtn)) {
                nextBtn.click();
                page++;
                await new Promise(r => setTimeout(r, 3500));
            } else {
                break;
            }
        }
        var totalInformado = null;
        paginasWideapp.forEach(function(p) {
            if (p.totalWidePay !== null && p.totalWidePay !== undefined) {
                totalInformado = Math.max(totalInformado || 0, p.totalWidePay);
            }
        });
        var metaColeta = wideappValidarMetaColeta({
            tela: "Cobrancas/Boletos",
            filtro: "bloco",
            registrosPorPagina: wideappRpp,
            totalWidePay: { total: totalInformado, texto: "" },
            paginas: paginasWideapp,
            totalColetadoUnico: totalAceitos,
            erros: []
        });
        return {
            cobrancas_por_cliente: cobrancasPorCliente,
            total_aceitos: totalAceitos,
            total_ignorados: totalIgnorados,
            clientes_ignorados: ignoradosLog,
            _wideapp_meta_coleta: metaColeta
        };
    }
    """ % (coletor_paginado_js, clientes_js_string)
    
    eval_extract_cobrancas = await cdp_command(ws_url, "Runtime.evaluate", {
        "expression": f"({js_extract_cobrancas})()",
        "awaitPromise": True,
        "returnByValue": True
    })
    raw_data_cobrancas_result = eval_extract_cobrancas.get("result", {}).get("result", {}).get("value", {}) or {}
    print(f"[Evidência] Extração em Bloco de Cobranças WidePay concluída. "
          f"{raw_data_cobrancas_result.get('total_aceitos', 0)} registros aceitos, "
          f"{raw_data_cobrancas_result.get('total_ignorados', 0)} ignorados de outros clientes (ignorados: {raw_data_cobrancas_result.get('clientes_ignorados', [])})")
    validar_coleta_paginada("Cobrancas_Bloco", raw_data_cobrancas_result)
    
    # 4. Processar e estruturar resultados individuais para cada cliente do bloco
    resultados_bloco = {}
    for c in clientes_bloco:
        c_nome = c["nome"]
        c_lote = c.get("lote") or "-"
        c_carnes = raw_data_carnes.get("carnes_por_cliente", {}).get(c_nome) or []
        c_cobrancas = raw_data_cobrancas_result.get("cobrancas_por_cliente", {}).get(c_nome) or []
        
        # Salvar o JSON brutas individuais
        JSON_OUTPUT_DIR = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "WIDEPAY_CONSULTAS"
        os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
        nome_slug = c_nome.replace(" ", "_").upper()
        caminho_json = JSON_OUTPUT_DIR / f"WIDEPAY_{nome_slug}.json"
        
        res_json = {
            "cliente": c_nome,
            "status_conexao": "LOGADO",
            "carnes": c_carnes,
            "cobrancas": c_cobrancas,
            "metadados_coleta_paginada": {
                "carnes": raw_data_carnes.get("_wideapp_meta_coleta") or {},
                "cobrancas": raw_data_cobrancas_result.get("_wideapp_meta_coleta") or {},
            }
        }
        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(res_json, f, indent=4, ensure_ascii=False)
            
        resultados_bloco[c_nome] = res_json
        print(f"Dados brutos extraidos e salvos para {c_nome} em {caminho_json}")
        
    extraction_done = True
    try:
        await poll_task
    except Exception:
        pass
            
    return resultados_bloco

async def extrair_dados_cliente(ws_url, cliente_nome, cliente_lote=None, cliente_quadra=None, progress_callback=None):
    """Envelopa a chamada individual para manter retrocompatibilidade."""
    res_bloco = await extrair_dados_clientes_bloco(
        ws_url,
        [{"nome": cliente_nome, "lote": cliente_lote, "quadra": cliente_quadra}],
        progress_callback=progress_callback
    )
    return res_bloco.get(cliente_nome) or {
        "cliente": cliente_nome,
        "status_conexao": "LOGADO",
        "carnes": [],
        "cobrancas": []
    }
