# -*- coding: utf-8 -*-
"""Coletor central para tabelas paginadas do WidePay.

REGRA — COLETA WIDEPAY COM REGISTROS POR PAGINA, PAGINACAO COMPLETA
E VALIDACAO TOTAL.
"""

ERRO_COLETA_INCOMPLETA = "COLETA_INCOMPLETA_PAGINACAO_OU_REGISTROS_POR_PAGINA_WIDEPAY"


COLETOR_TABELAS_PAGINADAS_JS = r"""
function wideappNormalizarBusca(texto) {
    if (!texto) return "";
    return texto.toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-z0-9]+/g, " ")
        .trim();
}

async function wideappSleep(ms) {
    await new Promise(r => setTimeout(r, ms));
}

function wideappTexto(el) {
    return ((el && (el.innerText || el.textContent || el.value)) || '').toString().trim();
}

function wideappDisabled(el) {
    if (!el) return true;
    var cls = (el.className || '').toString().toLowerCase();
    return !!el.disabled || cls.includes('disabled') || el.getAttribute('aria-disabled') === 'true';
}

async function wideappSelecionarMaiorRegistrosPorPagina(tela) {
    var resultado = {
        tela: tela,
        tentativa: true,
        encontrado: false,
        valorSelecionado: null,
        valoresDisponiveis: [],
        erro: null
    };

    function valorNumero(txt) {
        var m = String(txt || '').match(/\d+/);
        return m ? parseInt(m[0], 10) : null;
    }

    // ── Digita '500' no campo e confirma com Enter + clique no botão ──────────
    // O campo começa em 25 (padrão do WidePay) e NÃO aceita só .value = '500';
    // é necessário simular digitação real para o framework reagir.
    async function aplicar500(inputRpp, botaoConfirma) {
        resultado.encontrado = true;
        resultado.valoresDisponiveis = [500];
        resultado.valorSelecionado = 500;

        // 1. Focar e selecionar todo o conteúdo atual
        inputRpp.focus();
        inputRpp.click();
        try { inputRpp.select(); } catch(e) {}
        await wideappSleep(150);

        // 2. Apagar conteúdo existente com Backspace (até 10 chars)
        for (var d = 0; d < 10; d++) {
            inputRpp.dispatchEvent(new KeyboardEvent('keydown',  { key: 'Backspace', code: 'Backspace', keyCode: 8, which: 8, bubbles: true }));
            inputRpp.dispatchEvent(new KeyboardEvent('keypress', { key: 'Backspace', code: 'Backspace', keyCode: 8, which: 8, bubbles: true }));
            inputRpp.dispatchEvent(new KeyboardEvent('keyup',    { key: 'Backspace', code: 'Backspace', keyCode: 8, which: 8, bubbles: true }));
        }

        // 3. Inserir '500' usando execCommand (simula digitação real, ativa watchers)
        inputRpp.value = '';
        var digitado = false;
        try {
            digitado = document.execCommand('insertText', false, '500');
        } catch(e) {}

        // 4. Fallback direto caso execCommand não funcione
        if (!digitado || inputRpp.value !== '500') {
            inputRpp.value = '500';
            inputRpp.dispatchEvent(new Event('input',  { bubbles: true }));
            inputRpp.dispatchEvent(new Event('change', { bubbles: true }));
        }
        await wideappSleep(200);

        // 5. Enter no campo (keydown + keypress + keyup)
        ['keydown', 'keypress', 'keyup'].forEach(function(tipo) {
            inputRpp.dispatchEvent(new KeyboardEvent(tipo, {
                key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
            }));
        });
        await wideappSleep(500);

        // 6. Clicar no botão de confirmação (ícone de banco de dados ao lado)
        if (botaoConfirma) {
            try { botaoConfirma.focus(); botaoConfirma.click(); } catch(e) {}
        }

        // 7. Aguardar tabela recarregar com 500 registros
        await wideappSleep(4500);
    }

    var botoes    = Array.from(document.querySelectorAll('button, a, [role="button"]'));
    var inputsText = Array.from(document.querySelectorAll('input[type="text"], input:not([type])'));

    // ── Estratégia 1: botão localizado por title / aria-label / texto ─────────
    var botaoRpp = botoes.find(function(el) {
        var aria  = (el.getAttribute('aria-label') || '').toLowerCase();
        var title = (el.getAttribute('title')      || '').toLowerCase();
        var txt   = wideappTexto(el).toLowerCase();
        return /registros\s*por|registro\s*por/i.test(aria + ' ' + title + ' ' + txt);
    });

    // ── Estratégia 2: botão com ícone fa-database / fa-server / fa-hdd ────────
    if (!botaoRpp) {
        botaoRpp = botoes.find(function(el) {
            return !!(el.querySelector(
                'i.fa-database, i.fa-server, i.fa-hdd-o, i.fa-hdd, ' +
                'i.fa-filter, i.glyphicon-th-list, i.glyphicon-list-alt'
            ));
        });
    }

    if (botaoRpp) {
        // Tentar input dentro do mesmo .input-group ou container pai imediato
        var container = botaoRpp.closest('.input-group') || botaoRpp.parentElement;
        var inputRpp  = container ? container.querySelector('input[type="text"], input:not([type])') : null;

        // Se não achou no container direto, buscar input imediatamente anterior no DOM
        if (!inputRpp) {
            var prev = botaoRpp.previousElementSibling;
            while (prev) {
                if (prev.tagName === 'INPUT') { inputRpp = prev; break; }
                var found = prev.querySelector('input[type="text"], input:not([type])');
                if (found) { inputRpp = found; break; }
                prev = prev.previousElementSibling;
            }
        }

        if (inputRpp) {
            await aplicar500(inputRpp, botaoRpp);
            return resultado;
        }
    }

    // ── Estratégia 3: input numérico em input-group com botão adjacente ───────
    // Padrão visual WidePay: [↺] [25] [🗄]  — campo começa em 25
    var inputAchado = null;
    var botaoAchado = null;
    for (var i = 0; i < inputsText.length; i++) {
        var inp = inputsText[i];
        var grp = inp.closest('.input-group') || inp.parentElement;
        if (!grp) continue;
        var btns = Array.from(grp.querySelectorAll('button, a[role="button"]'));
        if (btns.length === 0) continue;
        // Só aceita se o valor atual for numérico (1–9999) ou campo vazio
        var numVal = valorNumero((inp.value || '').trim());
        if (numVal !== null && (numVal < 1 || numVal > 9999)) continue;
        inputAchado = inp;
        botaoAchado = btns[btns.length - 1]; // último botão = confirmar (🗄)
        break;
    }
    if (inputAchado) {
        await aplicar500(inputAchado, botaoAchado);
        return resultado;
    }

    // ── Estratégia 4: <select> tradicional de registros por página ────────────
    var selects    = Array.from(document.querySelectorAll('select'));
    var selectAlvo = selects.find(function(sel) {
        var texto  = wideappTexto(sel.parentElement) + ' ' + wideappTexto(sel.closest('label'));
        var opcoes = Array.from(sel.options || []).map(function(o) { return valorNumero(o.text || o.value); }).filter(Boolean);
        return opcoes.length && (/registro|pagina|página|por pagina|por página/i.test(texto) || Math.max.apply(null, opcoes) >= 50);
    });

    if (selectAlvo) {
        var opcoesValidas = Array.from(selectAlvo.options || [])
            .map(function(o) { return { option: o, valor: valorNumero(o.text || o.value) }; })
            .filter(function(o) { return o.valor; });
        if (opcoesValidas.length) {
            opcoesValidas.sort(function(a, b) { return b.valor - a.valor; });
            var escolhido = opcoesValidas[0];
            resultado.encontrado = true;
            resultado.valoresDisponiveis = opcoesValidas.map(function(o) { return o.valor; });
            resultado.valorSelecionado   = escolhido.valor;
            if (selectAlvo.value !== escolhido.option.value) {
                selectAlvo.value = escolhido.option.value;
                selectAlvo.dispatchEvent(new Event('input',  { bubbles: true }));
                selectAlvo.dispatchEvent(new Event('change', { bubbles: true }));
                await wideappSleep(3000);
            }
            return resultado;
        }
    }

    // ── Estratégia 5: dropdown numérico (botão que abre lista de valores) ─────
    if (botaoRpp && !wideappDisabled(botaoRpp)) {
        resultado.encontrado = true;
        try { botaoRpp.click(); await wideappSleep(800); } catch(e) { resultado.erro = String(e); }
    }
    var botoesOpcoes = Array.from(document.querySelectorAll(
        'button, a, [role="button"], .dropdown-menu *, .dropdown-item'
    ));
    var opcoesBotoes = botoesOpcoes
        .map(function(el) {
            return { el: el, valor: valorNumero(wideappTexto(el) || el.getAttribute('aria-label') || el.getAttribute('title')) };
        })
        .filter(function(item) { return item.valor && item.valor >= 10 && item.valor <= 500; });
    if (opcoesBotoes.length) {
        opcoesBotoes.sort(function(a, b) { return b.valor - a.valor; });
        resultado.encontrado = true;
        resultado.valoresDisponiveis = opcoesBotoes.map(function(o) { return o.valor; });
        resultado.valorSelecionado   = opcoesBotoes[0].valor;
        try { opcoesBotoes[0].el.click(); await wideappSleep(3000); } catch(e) { resultado.erro = String(e); }
        return resultado;
    }

    if (botaoRpp) {
        resultado.valorSelecionado = resultado.valorSelecionado || 0;
        resultado.erro = resultado.erro || 'Botao Registros por pagina localizado, mas opcoes numericas nao foram identificadas';
        return resultado;
    }

    resultado.erro = 'Controle Registros por pagina nao localizado na tela ' + tela;
    return resultado;
}

function wideappInfoTotalTabela() {
    var texto = document.body.innerText || '';
    var m = texto.match(/Exibindo\s+(\d+)\s+a\s+(\d+)\s+de\s+(\d+)\s+registros/i);
    if (m) {
        return {
            texto: m[0],
            inicio: parseInt(m[1], 10),
            fim: parseInt(m[2], 10),
            total: parseInt(m[3], 10)
        };
    }
    if (/Nenhum registro encontrado/i.test(texto) || /Nenhum carn[êe] encontrado/i.test(texto)) {
        return { texto: 'Nenhum registro encontrado', inicio: 0, fim: 0, total: 0 };
    }
    return { texto: '', inicio: null, fim: null, total: null };
}

function wideappInfoPagina() {
    var texto = document.body.innerText || '';
    var m = texto.match(/P[áa]gina\s+(\d+)\s+de\s+(\d+)/i);
    if (m) {
        return { atual: parseInt(m[1], 10), total: parseInt(m[2], 10), texto: m[0] };
    }
    return { atual: null, total: null, texto: '' };
}

function wideappBotaoPaginacao(tipo) {
    var botoes = Array.from(document.querySelectorAll('button, a, [role="button"]')).filter(function(el) {
        return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    });
    var porAlias = botoes.find(function(el) {
        var alias = (el.getAttribute('jab-alias') || '').toLowerCase();
        if (tipo === 'first') return alias === 'first';
        if (tipo === 'prev') return alias === 'prev';
        if (tipo === 'next') return alias === 'next';
        if (tipo === 'last') return alias === 'last';
        return false;
    });
    if (porAlias) return porAlias;
    return botoes.find(function(el) {
        var txt = wideappTexto(el).toLowerCase();
        var id = (el.id || '').toLowerCase();
        var cls = (el.className || '').toString().toLowerCase();
        var aria = (el.getAttribute('aria-label') || '').toLowerCase();
        var title = (el.getAttribute('title') || '').toLowerCase();
        var temPrimeiro = !!el.querySelector('i.fa-angle-double-left, i.fa-step-backward, i.fa-fast-backward');
        var temAnterior = !!el.querySelector('i.fa-angle-left, i.fa-chevron-left');
        var temProximo = !!el.querySelector('i.fa-angle-right, i.fa-chevron-right, i.fa-step-forward, i.fa-fast-forward');
        var temUltimo = !!el.querySelector('i.fa-angle-double-right, i.fa-step-forward, i.fa-fast-forward');
        if (tipo === 'first') return id.includes('first') || cls.includes('first') || aria.includes('primeira') || title.includes('primeira') || txt.includes('<<') || txt.includes('|<') || temPrimeiro;
        if (tipo === 'prev') return id.includes('prev') || id.includes('anterior') || cls.includes('prev') || aria.includes('anterior') || title.includes('anterior') || txt.includes('<') || temAnterior;
        if (tipo === 'next') return id.includes('next') || id.includes('proximo') || cls.includes('next') || aria.includes('proximo') || aria.includes('próximo') || title.includes('proximo') || title.includes('próximo') || txt.includes('>') || txt.includes('>>') || temProximo;
        if (tipo === 'last') return id.includes('last') || cls.includes('last') || aria.includes('ultima') || title.includes('ultima') || txt.includes('>|') || temUltimo;
        return false;
    });
}

async function wideappIrPrimeiraPagina() {
    var firstBtn = wideappBotaoPaginacao('first');
    if (firstBtn && !wideappDisabled(firstBtn)) {
        firstBtn.click();
        await wideappSleep(2500);
        return true;
    }
    var prevBtn = wideappBotaoPaginacao('prev');
    var moveu = false;
    var limite = 0;
    while (prevBtn && !wideappDisabled(prevBtn) && limite < 50) {
        prevBtn.click();
        moveu = true;
        limite++;
        await wideappSleep(1500);
        prevBtn = wideappBotaoPaginacao('prev');
    }
    return moveu;
}

function wideappChaveDedup(registro, campos) {
    return campos.map(c => String(registro[c] || '').trim().toLowerCase()).join('|');
}

function wideappValidarMetaColeta(meta) {
    meta.erros = meta.erros || [];
    if (!meta.registrosPorPagina || !meta.registrosPorPagina.tentativa) {
        meta.erros.push('Nao houve tentativa de aumentar registros por pagina');
    }
    if (!meta.registrosPorPagina || !meta.registrosPorPagina.encontrado || !meta.registrosPorPagina.valorSelecionado) {
        meta.erros.push('Registros por pagina nao foi localizado/selecionado');
    }
    if (meta.totalWidePay && meta.totalWidePay.total === 0 && meta.totalColetadoUnico === 0 && meta.registrosPorPagina && meta.registrosPorPagina.encontrado) {
        meta.erros = meta.erros.filter(e => e !== 'Registros por pagina nao foi localizado/selecionado');
    }
    if (!meta.totalWidePay || meta.totalWidePay.total === null || meta.totalWidePay.total === undefined) {
        meta.erros.push('Total exibido pelo WidePay nao foi identificado');
    }
    if (!meta.paginas || !meta.paginas.length) {
        meta.erros.push('Nenhuma pagina foi registrada na coleta');
    }
    if (meta.totalWidePay && meta.totalWidePay.total !== null && meta.totalColetadoUnico < meta.totalWidePay.total) {
        meta.erros.push('Total coletado menor que total exibido pelo WidePay');
    }
    if (meta.totalWidePay && meta.totalWidePay.total !== null && meta.totalColetadoUnico >= meta.totalWidePay.total) {
        meta.erros = meta.erros.filter(e => e !== 'Registros por pagina nao foi localizado/selecionado');
    }
    meta.valida = meta.erros.length === 0;
    meta.erroCodigo = meta.valida ? null : 'COLETA_INCOMPLETA_PAGINACAO_OU_REGISTROS_POR_PAGINA_WIDEPAY';
    return meta;
}
"""


def validar_coleta_paginada(nome, resultado):
    meta = (resultado or {}).get("_wideapp_meta_coleta") or {}
    erros = list(meta.get("erros") or [])
    if not meta:
        erros.append("Metadados de coleta paginada ausentes")
    if not meta.get("valida"):
        erros.append("Metadados de coleta paginada nao aprovados")
    if erros:
        detalhe = "; ".join(dict.fromkeys(erros))
        paginas = meta.get("paginas") or []
        resumo_paginas = ", ".join(
            f"{p.get('termo', '-')}:p{p.get('pagina', '?')}/{p.get('paginas', '?')}:{p.get('coletadosPagina', '?')}:{p.get('faixa', '')}"
            for p in paginas[:12]
        )
        rpp = meta.get("registrosPorPagina") or {}
        raise RuntimeError(
            f"{ERRO_COLETA_INCOMPLETA}: {nome}: {detalhe}; "
            f"rpp={rpp}; total={meta.get('totalWidePay')}; coletado={meta.get('totalColetadoUnico')}; paginas=[{resumo_paginas}]"
        )
    return True
