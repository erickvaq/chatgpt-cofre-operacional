# -*- coding: utf-8 -*-
"""Interface visual Tkinter da WideAPP_EXTRA."""

import threading
import tkinter as tk
from tkinter import messagebox, ttk

from app import config
from app import indexador_clientes
from app import pesquisa_clientes
from app import seletor_clientes
from app import drive_uploader
from app import pipeline_runner
from app.abridor_arquivos import abrir_pasta, abrir


COLUNAS = [
    ("cliente", "Cliente", 220),
    ("lote", "Lote", 70),
    ("quadra", "Quadra", 70),
    ("status", "Status", 170),
    ("contrato", "Contrato", 120),
    ("origem", "Origem", 130),
    ("parcelas_pagas_identificadas", "Parcelas", 90),
    ("ultimo_vencimento_pago", "Ult. vencimento", 110),
    ("valor_ultimo_pagamento", "Ult. valor", 90),
    ("observacoes", "Observacoes", 220),
]


class WideAppInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("WideAPP_EXTRA - Clientes, lotes e relatorios")
        self.root.geometry("1280x760")
        self.registros = indexador_clientes.carregar_cache()
        self.filtrados = []
        self.selecionados = set()
        self.ultimo_arquivo = None
        self.ultima_pasta = config.OUTPUT_DIR
        self.ultimos = {"xlsx": [], "pdf": [], "html": [], "md": [], "json": [], "log": []}
        self.ultimo_grupo = "SELECIONADOS"
        self._montar()
        self.aplicar_filtro()

    def _montar(self):
        topo = ttk.Frame(self.root, padding=8)
        topo.pack(fill="x")
        ttk.Button(topo, text="Atualizar lista de clientes e contratos", command=self.atualizar_async).pack(side="left")
        ttk.Label(topo, text="Pesquisar cliente").pack(side="left", padx=(12, 4))
        self.busca_var = tk.StringVar()
        busca = ttk.Entry(topo, textvariable=self.busca_var, width=36)
        busca.pack(side="left")
        busca.bind("<KeyRelease>", lambda _e: self.aplicar_filtro())
        ttk.Label(topo, text="Status").pack(side="left", padx=(12, 4))
        self.status_var = tk.StringVar(value="Todos")
        status_box = ttk.Combobox(
            topo,
            textvariable=self.status_var,
            values=["Todos", "Pendente validacao WidePay", "Sem contrato confirmado", "Ativo", "Com divergencia"],
            width=26,
            state="readonly",
        )
        status_box.pack(side="left")
        status_box.bind("<<ComboboxSelected>>", lambda _e: self.aplicar_filtro())

        botoes = ttk.Frame(self.root, padding=(8, 0, 8, 8))
        botoes.pack(fill="x")
        ttk.Button(botoes, text="Selecionar todos", command=self.selecionar_todos).pack(side="left")
        ttk.Button(botoes, text="Limpar selecao", command=self.limpar_selecao).pack(side="left", padx=4)
        ttk.Button(botoes, text="Gerar relatorio dos selecionados", command=self.gerar_selecionados).pack(side="left", padx=12)
        ttk.Button(botoes, text="Gerar relatorio de todos os clientes ativos", command=self.gerar_todos_ativos).pack(side="left")
        ttk.Button(botoes, text="Abrir pasta local", command=self.abrir_pasta_execucao).pack(side="right")
        ttk.Button(botoes, text="Abrir pasta no Drive", command=self.abrir_drive).pack(side="right", padx=4)
        ttk.Button(botoes, text="Abrir XLSX", command=self.abrir_ultimo).pack(side="right", padx=4)
        ttk.Button(botoes, text="Abrir PDF", command=lambda: self.abrir_tipo("pdf")).pack(side="right", padx=4)
        ttk.Button(botoes, text="Abrir HTML", command=lambda: self.abrir_tipo("html")).pack(side="right", padx=4)

        meio = ttk.Frame(self.root, padding=8)
        meio.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(meio, columns=[c[0] for c in COLUNAS], show="headings", selectmode="extended")
        for key, label, width in COLUNAS:
            self.tree.heading(key, text=label)
            self.tree.column(key, width=width, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", lambda _e: self.sincronizar_selecao_tree())
        scroll = ttk.Scrollbar(meio, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)

        rodape = ttk.PanedWindow(self.root, orient="horizontal")
        rodape.pack(fill="both", expand=False, padx=8, pady=(0, 8))
        logs_frame = ttk.LabelFrame(rodape, text="Logs/status")
        links_frame = ttk.LabelFrame(rodape, text="Links Google Drive")
        rodape.add(logs_frame, weight=3)
        rodape.add(links_frame, weight=2)
        self.logs = tk.Text(logs_frame, height=8, wrap="word")
        self.logs.pack(fill="both", expand=True)
        self.links = tk.Text(links_frame, height=8, wrap="word")
        self.links.pack(fill="both", expand=True)
        self.log("Interface iniciada.")
        if not self.registros:
            self.log("Cache vazio. Clique em Atualizar lista de clientes e contratos.")

    def log(self, msg):
        self.logs.insert("end", msg + "\n")
        self.logs.see("end")
        self.root.update_idletasks()

    def atualizar_async(self):
        self.log("Atualizacao iniciada...")
        threading.Thread(target=self._atualizar, daemon=True).start()

    def _atualizar(self):
        result = indexador_clientes.indexar_clientes(validar_widepay=True, log_callback=self.log)
        self.registros = result["registros"]
        self.root.after(0, self.aplicar_filtro)
        self.log(f"Clientes/lotes indexados: {len(self.registros)}")

    def aplicar_filtro(self):
        self.filtrados = pesquisa_clientes.filtrar(self.registros, self.busca_var.get(), self.status_var.get())
        self.tree.delete(*self.tree.get_children())
        for idx, item in enumerate(self.filtrados):
            values = [item.get(key, "") for key, _label, _width in COLUNAS]
            iid = str(idx)
            self.tree.insert("", "end", iid=iid, values=values)
            if self._chave(item) in self.selecionados:
                self.tree.selection_add(iid)
        self.log(f"Filtro aplicado: {len(self.filtrados)} resultado(s).")

    def _chave(self, item):
        return f"{item.get('cliente')}|{item.get('lote')}|{item.get('pasta_local')}"

    def sincronizar_selecao_tree(self):
        self.selecionados = set()
        for iid in self.tree.selection():
            item = self.filtrados[int(iid)]
            self.selecionados.add(self._chave(item))
        self.log(f"Selecionados: {len(self.selecionados)}")

    def selecionar_todos(self):
        for iid in self.tree.get_children():
            self.tree.selection_add(iid)
        self.sincronizar_selecao_tree()

    def limpar_selecao(self):
        self.tree.selection_remove(self.tree.selection())
        self.selecionados.clear()
        self.log("Selecao limpa.")

    def _selecionados_registros(self):
        chaves = set(self.selecionados)
        return [item for item in self.registros if self._chave(item) in chaves]

    def gerar_todos_ativos(self):
        registros = [r for r in self.registros if r.get("contrato") == "Encontrado"]
        self._gerar(registros, "TODOS_ATIVOS")

    def gerar_selecionados(self):
        registros = self._selecionados_registros()
        self._gerar(registros, "SELECIONADOS")

    def _gerar(self, registros, grupo):
        if not registros:
            messagebox.showwarning("WideAPP_EXTRA", "Nenhum cliente selecionado.")
            return
        resumo = seletor_clientes.resumir_selecao(registros)
        if not messagebox.askyesno("Confirmar selecao", resumo + "\n\nExecutar pipeline financeiro completo agora?"):
            self.log("Geracao cancelada pelo usuario.")
            return
        self.ultimo_grupo = grupo
        threading.Thread(target=self._gerar_thread, args=(registros, grupo), daemon=True).start()

    def _gerar_thread(self, registros, grupo):
        try:
            resultado = pipeline_runner.executar_lote(registros, grupo=grupo, log_callback=self.log)
        except Exception as exc:
            self.log(f"ERRO_PIPELINE: {exc}")
            messagebox.showerror("WideAPP_EXTRA", str(exc))
            return
        self.ultimos = {"xlsx": [], "pdf": [], "html": [], "md": [], "json": [], "log": []}
        for res in resultado["resultados"]:
            for tipo, paths in res["arquivos"].items():
                self.ultimos.setdefault(tipo, []).extend(paths)
        if resultado.get("consolidado"):
            self.ultimos.setdefault("xlsx", []).insert(0, resultado["consolidado"])
        if self.ultimos.get("xlsx"):
            self.ultimo_arquivo = self.ultimos["xlsx"][0]
        if self.ultimos.get("pdf"):
            self.ultima_pasta = self.ultimos["pdf"][0].parent
        elif self.ultimos.get("xlsx"):
            self.ultima_pasta = self.ultimos["xlsx"][0].parent
        self.links.delete("1.0", "end")
        for item in resultado["drive"]:
            self.links.insert("end", f"{item.get('cliente')} {item.get('lote')}: {item.get('status')} {item.get('link')}\n")
        self.log(f"Pipeline concluido. Manifesto Drive: {config.LINKS_DRIVE_MD}")
        if resultado["ignorados"]:
            self.log(f"Ignorados sem contrato confirmado: {len(resultado['ignorados'])}")

    def abrir_ultimo(self):
        if not self.ultimos.get("xlsx"):
            messagebox.showinfo("WideAPP_EXTRA", "Nenhum XLSX gerado nesta sessao.")
            return
        abrir(self.ultimos["xlsx"][0])

    def abrir_tipo(self, tipo):
        if not self.ultimos.get(tipo):
            messagebox.showinfo("WideAPP_EXTRA", f"Nenhum arquivo {tipo.upper()} gerado nesta sessao.")
            return
        abrir(self.ultimos[tipo][0])

    def abrir_pasta_execucao(self):
        abrir_pasta(self.ultima_pasta)

    def abrir_drive(self):
        destino = drive_uploader.abrir_destino_drive(self.ultimo_grupo)
        if not destino:
            messagebox.showinfo("WideAPP_EXTRA", "Destino Drive nao configurado.")
            return
        if hasattr(destino, "exists"):
            abrir_pasta(destino)
        else:
            self.links.insert("end", f"Destino Drive remoto: {destino}\n")


def abrir_interface():
    config.ensure_dirs()
    root = tk.Tk()
    WideAppInterface(root)
    root.mainloop()


def smoke_test():
    config.ensure_dirs()
    registros = indexador_clientes.carregar_cache()
    root = tk.Tk()
    root.withdraw()
    app = WideAppInterface(root)
    assert hasattr(app, "tree")
    root.destroy()
    return len(registros)
