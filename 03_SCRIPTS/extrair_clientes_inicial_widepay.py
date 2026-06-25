# -*- coding: utf-8 -*-
import argparse
import asyncio
import json
import sys
import urllib.request
from pathlib import Path

import websockets

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "00_SISTEMA_PRECHECK"))

from precheck_regras import executar_precheck

executar_precheck("extrair_clientes_inicial_widepay.py")

try:
    from config_widepay_cdp import CDP_BASE_URL
except ImportError:
    CDP_BASE_URL = "http://localhost:9444"


def obter_aba_widepay():
    with urllib.request.urlopen(f"{CDP_BASE_URL}/json", timeout=5) as r:
        abas = json.loads(r.read().decode("utf-8"))
    for aba in abas:
        if aba.get("type") == "page" and "widepay.com" in aba.get("url", ""):
            return aba
    return None


async def cdp_command(ws_url, method, params=None):
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({"id": 1, "method": method, "params": params or {}}))
        while True:
            resp = json.loads(await ws.recv())
            if resp.get("id") == 1:
                return resp


async def extrair_tabela(ws_url, url, col_cliente, col_ref, max_paginas):
    await cdp_command(ws_url, "Page.navigate", {"url": url})
    await asyncio.sleep(4)
    js = f"""
    async function() {{
        const rows = [];
        for (let page = 1; page <= {max_paginas}; page++) {{
            Array.from(document.querySelectorAll('tr')).forEach(tr => {{
                const tds = tr.querySelectorAll('td');
                if (tds.length > {max(col_cliente, col_ref)}) {{
                    const cliente = tds[{col_cliente}].innerText.trim();
                    const referencia = tds[{col_ref}].innerText.trim();
                    if (cliente && cliente.toLowerCase() !== 'cliente') {{
                        rows.push({{ cliente, referencia, texto: tr.innerText.trim() }});
                    }}
                }}
            }});
            const btns = Array.from(document.querySelectorAll('button, a'));
            const next = btns.find(el => {{
                const text = (el.innerText || '').trim().toLowerCase();
                const cls = el.className || '';
                const id = el.id || '';
                return (id.includes('next') || cls.includes('next') || text === '>' || text.includes('proximo') || text.includes('próximo'));
            }});
            if (!next || next.disabled || String(next.className || '').includes('disabled')) break;
            next.click();
            await new Promise(r => setTimeout(r, 2500));
        }}
        return rows;
    }}
    """
    result = await cdp_command(ws_url, "Runtime.evaluate", {
        "expression": f"({js})()",
        "awaitPromise": True,
        "returnByValue": True,
    })
    return result.get("result", {}).get("result", {}).get("value", []) or []


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inicial", required=True)
    args = parser.parse_args()
    inicial = args.inicial.strip().upper()[0]

    aba = obter_aba_widepay()
    if not aba:
        print("WIDEPAY REAL NAO ABERTO - EXECUCAO BLOQUEADA.")
        sys.exit(1)
    ws_url = aba["webSocketDebuggerUrl"]

    carnes = await extrair_tabela(ws_url, "https://www.widepay.com/conta/recebimentos/carnes", 2, 8, 20)
    cobrancas = await extrair_tabela(ws_url, "https://www.widepay.com/conta/recebimentos", 4, 10, 20)

    clientes = {}
    for origem, rows in (("carne", carnes), ("cobranca", cobrancas)):
        for row in rows:
            nome = row.get("cliente", "").strip()
            if nome.upper().startswith(inicial):
                item = clientes.setdefault(nome, {"cliente": nome, "fontes": set(), "referencias": []})
                item["fontes"].add(origem)
                if row.get("referencia"):
                    item["referencias"].append(row["referencia"])

    saida = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "WIDEPAY_CONSULTAS" / f"CLIENTES_INICIAL_{inicial}_WIDEPAY.json"
    saida.parent.mkdir(parents=True, exist_ok=True)
    serializado = []
    for item in sorted(clientes.values(), key=lambda x: x["cliente"].lower()):
        item["fontes"] = sorted(item["fontes"])
        item["referencias"] = sorted(set(item["referencias"]))
        serializado.append(item)
    saida.write_text(json.dumps(serializado, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Arquivo salvo: {saida}")
    print(f"Clientes com inicial {inicial}: {len(serializado)}")
    for item in serializado:
        print(f"- {item['cliente']} | fontes: {', '.join(item['fontes'])}")


if __name__ == "__main__":
    asyncio.run(main())
