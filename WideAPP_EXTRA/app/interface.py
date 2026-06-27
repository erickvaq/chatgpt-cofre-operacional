# -*- coding: utf-8 -*-
"""Interface visual Tkinter da WideAPP_EXTRA."""

import threading
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
from PIL import Image, ImageDraw, ImageTk, ImageFont

from app import config
from app import indexador_clientes
from app import pesquisa_clientes
from app import seletor_clientes
from app import drive_uploader
from app import pipeline_runner
from app.abridor_arquivos import abrir_pasta, abrir


COLUNAS = [
    ("cliente", "Cliente", 220),
    ("lote", "Lote / Quadra", 105),
    ("contrato_resumo", "Contrato", 140),
    ("parcelas_resumo", "Parcelas", 110),
    ("situacao_final", "Situacao", 140),
    ("ultima_atualizacao_widepay", "Atualizado em", 125),
    ("valor_total_contratado", "Valor Lote", 110),
    ("valor_total_pago", "Total pago", 100),
    ("observacoes", "Observacoes", 160),
]


class ConfirmacaoSelecaoDialogo:
    def __init__(self, parent, resumo_texto):
        self.result = False
        self.top = tk.Toplevel(parent)
        self.top.title("Confirmar seleção de clientes")
        self.top.geometry("640x500")
        self.top.configure(bg="#181818")
        self.top.transient(parent)
        self.top.grab_set()
        self.top.resizable(False, False)
        
        # Centralizar na tela parent
        self.top.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        x = px + (pw - 640) // 2
        y = py + (ph - 500) // 2
        self.top.geometry(f"640x500+{max(0, x)}+{max(0, y)}")

        # Estilo do Tema Dark
        fg_white = "#F3F3F3"
        bg_card = "#242424"
        bg_dark = "#181818"
        green_accent = "#00E676"
        green_dark = "#007A3E"
        
        # Header Label (Topo)
        header_frame = tk.Frame(self.top, bg=bg_dark, pady=10)
        header_frame.pack(side="top", fill="x")
        tk.Label(
            header_frame, 
            text="Confirmar seleção de clientes e lotes", 
            font=("Segoe UI", 12, "bold"), 
            bg=bg_dark, 
            fg=green_accent
        ).pack(anchor="w", padx=15)
        
        # Botões de Ação no rodapé (Base) - Empacota primeiro no rodapé para garantir que nunca sejam cortados
        btn_frame = tk.Frame(self.top, bg=bg_dark, pady=10)
        btn_frame.pack(side="bottom", fill="x")
        
        # Botão Sim (Accent.TButton)
        btn_yes = ttk.Button(btn_frame, text="Sim, executar", style="Accent.TButton", command=self.on_yes)
        btn_yes.pack(side="right", padx=(10, 20))
        
        # Botão Não
        btn_no = ttk.Button(btn_frame, text="Não, cancelar", command=self.on_no)
        btn_no.pack(side="right")
        
        # Label de pergunta final (Acima dos botões no rodapé)
        lbl_pergunta = tk.Label(
            self.top, 
            text="Deseja executar o pipeline financeiro completo agora?", 
            font=("Segoe UI", 10, "bold"), 
            bg=bg_dark, 
            fg=fg_white
        )
        lbl_pergunta.pack(side="bottom", pady=(0, 10))
        
        # Text com Scrollbar para exibir os clientes (Centro - Ocupa o espaço restante)
        container = tk.Frame(self.top, bg=bg_card, bd=1, relief="solid")
        container.pack(side="top", fill="both", expand=True, padx=15, pady=(5, 10))
        
        scroll_y = ttk.Scrollbar(container, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        self.text_widget = tk.Text(
            container, 
            wrap="word", 
            yscrollcommand=scroll_y.set,
            bg=bg_card, 
            fg=fg_white, 
            insertbackground=fg_white,
            selectbackground=green_dark, 
            selectforeground=fg_white, 
            font=("Segoe UI", 9),
            bd=0,
            padx=10,
            pady=10
        )
        self.text_widget.pack(side="left", fill="both", expand=True)
        scroll_y.config(command=self.text_widget.yview)
        
        # Inserir o resumo de clientes e desativar edição
        self.text_widget.insert("1.0", resumo_texto)
        self.text_widget.configure(state="disabled")
        
        self.top.protocol("WM_DELETE_WINDOW", self.on_no)
        self.top.wait_window()

    def on_yes(self):
        self.result = True
        self.top.destroy()

    def on_no(self):
        self.result = False
        self.top.destroy()


class WideAppInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("WideAPP_EXTRA - Clientes, lotes e relatorios")
        self.root.geometry("1280x720")
        self.root.minsize(1120, 650)
        
        # Configurar Estilos do Tema Dark + Accent Green
        style = ttk.Style(self.root)
        style.theme_use("clam")
        
        bg_dark = "#181818"      # Cinza escuro quase preto
        bg_card = "#242424"      # Cinza grafite intermediário
        bg_active = "#333333"    # Cinza ativo / hover
        fg_white = "#F3F3F3"     # Branco suave
        fg_gray = "#A0A0A0"      # Cinza claro
        green_accent = "#00E676" # Verde brilhante estilo Antigravity
        green_dark = "#007A3E"   # Verde escuro / highlight

        self.ui_bg = "#0F1A20"
        self.ui_panel = "#17252D"
        self.ui_panel_alt = "#1D3039"
        self.ui_border = "#2D4650"
        self.ui_text = "#F3F7F8"
        self.ui_muted = "#9FB1B8"
        self.ui_green = "#22C55E"
        self.ui_yellow = "#FFD600"
        self.ui_red = "#FF3B4F"
        self.ui_blue = "#2563EB"
        
        self.root.configure(bg=bg_dark)
        self.root.option_add("*TCombobox*Listbox.background", bg_card)
        self.root.option_add("*TCombobox*Listbox.foreground", fg_white)
        self.root.option_add("*TCombobox*Listbox.selectBackground", green_dark)
        self.root.option_add("*TCombobox*Listbox.selectForeground", fg_white)
        self.root.option_add("*TCombobox*Listbox.font", ("Segoe UI", 9))
        
        style.configure(".", background=bg_dark, foreground=fg_white, fieldbackground=bg_dark)
        style.configure("TFrame", background=bg_dark)
        style.configure("TLabel", background=bg_dark, foreground=fg_white, font=("Segoe UI", 9))
        
        style.configure("TButton", background=bg_card, foreground=fg_white, bordercolor=bg_active, font=("Segoe UI", 9, "bold"), padding=6)
        style.map("TButton",
            background=[("active", bg_active), ("disabled", "#222222")],
            foreground=[("active", green_accent), ("disabled", "#666666")]
        )
        
        style.configure("Accent.TButton", background=green_dark, foreground=fg_white, bordercolor=green_accent, font=("Segoe UI", 9, "bold"), padding=8)
        style.map("Accent.TButton",
            background=[("active", green_accent)],
            foreground=[("active", bg_dark)]
        )
        
        style.configure("TCombobox", fieldbackground=bg_card, background=bg_dark, foreground=fg_white, arrowcolor=green_accent, font=("Segoe UI", 9))
        style.map("TCombobox",
            fieldbackground=[("readonly", bg_card)],
            selectbackground=[("readonly", green_dark)],
            selectforeground=[("readonly", fg_white)]
        )
        
        style.configure("TEntry", fieldbackground=bg_card, foreground=fg_white, insertcolor=fg_white, font=("Segoe UI", 9))
        
        style.configure("Treeview", 
            background=bg_card, 
            foreground=fg_white, 
            fieldbackground=bg_card, 
            rowheight=26,
            font=("Segoe UI", 9)
        )
        style.configure("Treeview.Heading", 
            background=bg_dark, 
            foreground=green_accent, 
            font=("Segoe UI", 9, "bold")
        )
        style.map("Treeview",
            background=[("selected", green_dark)],
            foreground=[("selected", fg_white)]
        )
        
        style.configure("TProgressbar", thickness=12, troughcolor=bg_card, background=green_accent)
        style.configure("TLabelframe", background=bg_dark, foreground=green_accent, font=("Segoe UI", 9, "bold"), bordercolor=bg_active)
        style.configure("TLabelframe.Label", background=bg_dark, foreground=green_accent)
        style.configure("Toolbar.TButton", background=self.ui_panel_alt, foreground=self.ui_text, bordercolor=self.ui_border, font=("Segoe UI", 10, "bold"), padding=(14, 10))
        style.map("Toolbar.TButton",
            background=[("active", "#233A44"), ("disabled", "#1A2226")],
            foreground=[("active", self.ui_text), ("disabled", "#66737A")]
        )
        style.configure("Primary.Toolbar.TButton", background="#10B95B", foreground="#FFFFFF", bordercolor="#2DF27D", font=("Segoe UI", 10, "bold"), padding=(16, 10))
        style.map("Primary.Toolbar.TButton",
            background=[("active", "#22C55E"), ("disabled", "#1A2226")],
            foreground=[("active", "#06150B"), ("disabled", "#66737A")]
        )
        style.configure("Danger.Toolbar.TButton", background="#3A2630", foreground="#FFB4C0", bordercolor="#7F2D3B", font=("Segoe UI", 10, "bold"), padding=(14, 10))
        style.map("Danger.Toolbar.TButton",
            background=[("active", "#7F1D1D"), ("disabled", "#1A2226")],
            foreground=[("active", "#FFFFFF"), ("disabled", "#66737A")]
        )
        style.configure("Modern.TEntry", fieldbackground="#101B21", foreground=self.ui_text, insertcolor=self.ui_text, bordercolor=self.ui_border, font=("Segoe UI", 10), padding=7)
        style.configure("Modern.TCombobox", fieldbackground="#101B21", background=self.ui_panel, foreground=self.ui_text, arrowcolor=self.ui_text, bordercolor=self.ui_border, font=("Segoe UI", 10), padding=6)
        style.configure("Modern.Treeview", background="#16232A", foreground=self.ui_text, fieldbackground="#16232A", rowheight=31, bordercolor=self.ui_border, font=("Segoe UI", 10))
        style.configure("Modern.Treeview.Heading", background="#1C2B33", foreground=self.ui_text, font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Modern.Treeview",
            background=[("selected", "#0B7F45")],
            foreground=[("selected", "#FFFFFF")]
        )

        self.registros = indexador_clientes.carregar_cache()
        self.filtrados = []
        self.selecionados = set()
        self.imagens_barrinha = {}
        self.ultimo_arquivo = None
        self.ultima_pasta = config.OUTPUT_DIR
        self.ultimos = {"xlsx": [], "pdf": [], "html": [], "md": [], "json": [], "log": []}
        self.ultimo_grupo = "SELECIONADOS"
        self.xlsx_map = {}
        self._context_iid = None
        self.execucao_em_andamento = False
        self._montar()
        self.aplicar_filtro()
        self.atualizar_combo_xlsx()
        self._trazer_para_frente()

    def _trazer_para_frente(self):
        def _focus():
            try:
                self.root.deiconify()
                self.root.state("normal")
                self.root.lift()
                self.root.attributes("-topmost", True)
                self.root.focus_force()
                self.root.after(800, lambda: self.root.attributes("-topmost", False))
            except Exception:
                pass

        self.root.after(150, _focus)
        self.root.after(800, _focus)
        self.root.after(1600, _focus)

    def _montar(self):
        topo = ttk.Frame(self.root, padding=8)
        topo.pack(fill="x")
        ttk.Button(topo, text="Atualizar clientes", command=self.atualizar_async).pack(side="left")
        ttk.Button(topo, text="Atualizar informações da WidePay", command=self.atualizar_widepay_async).pack(side="left", padx=(6, 0))
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
            values=["Todos", "Pendente validacao WidePay", "APROVADO", "PENDENTE", "ERRO", "Sem contrato confirmado"],
            width=26,
            state="readonly",
        )
        status_box.pack(side="left")
        status_box.bind("<<ComboboxSelected>>", lambda _e: self.aplicar_filtro())

        botoes = ttk.Frame(self.root, padding=(8, 0, 8, 8))
        botoes.pack(fill="x")
        ttk.Button(botoes, text="Selecionar todos", command=self.selecionar_todos).pack(side="left")
        ttk.Button(botoes, text="Limpar selecao", command=self.limpar_selecao).pack(side="left", padx=4)
        self.btn_gerar_sel = ttk.Button(botoes, text="Gerar relatorio dos selecionados", command=self.gerar_selecionados, style="Accent.TButton")
        self.btn_gerar_sel.pack(side="left", padx=12)
        self.btn_gerar_todos = ttk.Button(botoes, text="Gerar relatorio de todos os clientes ativos", command=self.gerar_todos_ativos, style="Accent.TButton")
        self.btn_gerar_todos.pack(side="left")
        self.btn_parar = ttk.Button(botoes, text="Parar captura", command=self.parar_captura, state="disabled")
        self.btn_parar.pack(side="left", padx=(8, 0))
        
        # Frame para organizador de abridores
        abridores = ttk.Frame(botoes)
        abridores.pack(side="right")
        
        # Linha superior: botões
        botoes_linha = ttk.Frame(abridores)
        botoes_linha.pack(side="top", anchor="e")
        ttk.Button(botoes_linha, text="Abrir pasta local", command=self.abrir_pasta_execucao).pack(side="left", padx=2)
        ttk.Button(botoes_linha, text="Abrir pasta no Drive", command=self.abrir_drive).pack(side="left", padx=2)
        ttk.Button(botoes_linha, text="Abrir HTML", command=lambda: self.abrir_tipo("html")).pack(side="left", padx=2)
        ttk.Button(botoes_linha, text="Abrir PDF", command=lambda: self.abrir_tipo("pdf")).pack(side="left", padx=2)
        ttk.Button(botoes_linha, text="Abrir XLSX", command=self.abrir_ultimo).pack(side="left", padx=2)
        
        # Linha inferior: combobox de planilhas de largura 75 para visualização completa
        xlsx_linha = ttk.Frame(abridores)
        xlsx_linha.pack(side="top", fill="x", anchor="e", pady=(4, 0))
        ttk.Label(xlsx_linha, text="Planilhas recentes:").pack(side="left", padx=2)
        self.xlsx_combo = ttk.Combobox(xlsx_linha, state="readonly", width=75)
        self.xlsx_combo.pack(side="left", padx=2, fill="x", expand=True)
        self.xlsx_combo.bind("<<ComboboxSelected>>", self.abrir_xlsx_selecionado)

        meio = ttk.Frame(self.root, padding=8)
        meio.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(meio, columns=[c[0] for c in COLUNAS], show="tree headings", selectmode="extended")
        self.tree.heading("#0", text="STATUS")
        self.tree.column("#0", width=88, minwidth=72, anchor="center", stretch=False)
        for key, label, width in COLUNAS:
            self.tree.heading(key, text=label)
            self.tree.column(key, width=width, anchor="w" if key == "cliente" else "center")
        
        scroll_y = ttk.Scrollbar(meio, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(meio, orient="horizontal", command=self.tree.xview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tree.bind("<ButtonRelease-1>", lambda _e: self.sincronizar_selecao_tree())
        self.tree.bind("<Button-3>", self.mostrar_menu_contexto)
        self.tree.bind("<Double-1>", lambda _e: self.abrir_pasta_cliente_selecionado())
        self.tree.bind("<MouseWheel>", self._rolar_tree)
        self.tree.bind("<Shift-MouseWheel>", self._rolar_tree_horizontal)

        # Progresso da execução
        progresso_frame = ttk.Frame(self.root, padding=(8, 0, 8, 8))
        progresso_frame.pack(fill="x", expand=False)
        
        self.progress_label = ttk.Label(progresso_frame, text="Aguardando início...")
        self.progress_label.pack(side="top", fill="x", pady=(0, 4))
        
        self.progress = ttk.Progressbar(progresso_frame, orient="horizontal", mode="determinate")
        self.progress.pack(side="top", fill="x")

        rodape = ttk.PanedWindow(self.root, orient="horizontal")
        rodape.pack(fill="both", expand=False, padx=8, pady=(0, 8))
        
        logs_frame = ttk.LabelFrame(rodape, text="Logs/status")
        links_frame = ttk.LabelFrame(rodape, text="Links Google Drive")
        rodape.add(logs_frame, weight=3)
        rodape.add(links_frame, weight=2)
        
        logs_scroll = ttk.Scrollbar(logs_frame, orient="vertical")
        logs_scroll.pack(side="right", fill="y")
        self.logs = tk.Text(logs_frame, height=8, wrap="word", yscrollcommand=logs_scroll.set)
        self.logs.pack(fill="both", expand=True)
        self.logs.configure(bg="#242424", fg="#F3F3F3", insertbackground="#F3F3F3", selectbackground="#007A3E", selectforeground="#F3F3F3", font=("Consolas", 9))
        logs_scroll.config(command=self.logs.yview)
        
        links_scroll = ttk.Scrollbar(links_frame, orient="vertical")
        links_scroll.pack(side="right", fill="y")
        self.links = tk.Text(links_frame, height=8, wrap="word", yscrollcommand=links_scroll.set)
        self.links.pack(fill="both", expand=True)
        self.links.configure(bg="#242424", fg="#F3F3F3", insertbackground="#F3F3F3", selectbackground="#007A3E", selectforeground="#F3F3F3", font=("Consolas", 9))
        links_scroll.config(command=self.links.yview)
        self.log("Interface iniciada.")
        
        # Metadados de Diagnóstico de Inicialização
        import sys
        import subprocess
        from datetime import datetime
        
        main_path = Path(sys.argv[0]).resolve()
        interface_path = Path(__file__).resolve()
        
        try:
            mtime = datetime.fromtimestamp(interface_path.stat().st_mtime).strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            mtime = "Desconhecida"
            
        try:
            commit_version = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], 
                cwd=str(interface_path.parent), 
                text=True, 
                stderr=subprocess.DEVNULL
            ).strip()
        except Exception:
            commit_version = "Sem Git"
            
        self.log(f"[DIAGNOSTICO] Entrada: {main_path}")
        self.log(f"[DIAGNOSTICO] Modulo UI: {interface_path}")
        self.log(f"[DIAGNOSTICO] Modificacao UI: {mtime}")
        self.log(f"[DIAGNOSTICO] Versao Git: {commit_version}")
        self.log(f"[DIAGNOSTICO] Cache JSON: {config.CLIENTES_JSON}")
        
        if not self.registros:
            self.log("Cache vazio. Clique em Atualizar clientes.")

    def _label(self, parent, text, size=10, weight="normal", color=None, bg=None):
        return tk.Label(
            parent,
            text=text,
            bg=bg or self.ui_bg,
            fg=color or self.ui_text,
            font=("Segoe UI", size, weight),
        )

    def _panel(self, parent, padx=0, pady=0):
        frame = tk.Frame(parent, bg=self.ui_panel, highlightbackground=self.ui_border, highlightthickness=1, bd=0)
        if padx or pady:
            inner = tk.Frame(frame, bg=self.ui_panel)
            inner.pack(fill="both", expand=True, padx=padx, pady=pady)
            frame.inner = inner
        else:
            frame.inner = frame
        return frame

    def _opcoes_quadra_lote(self):
        opcoes = {"Todos"}
        for item in self.registros:
            quadra = str(item.get("quadra") or "").strip()
            lote = str(item.get("lote") or "").strip()
            if quadra and quadra != "-":
                opcoes.add(quadra)
            if lote and lote != "-":
                opcoes.add(lote)
        return ["Todos"] + sorted(opcao for opcao in opcoes if opcao != "Todos")

    def _montar(self):
        self.root.configure(bg=self.ui_bg)

        header = tk.Frame(self.root, bg=self.ui_bg)
        header.pack(fill="x", padx=22, pady=(16, 8))

        logo = tk.Canvas(header, width=50, height=50, bg=self.ui_bg, highlightthickness=0)
        logo.pack(side="left", padx=(0, 14))
        for y, color in ((8, "#67E85A"), (20, "#44C85D"), (32, "#2EA84E")):
            logo.create_polygon(8, y + 6, 25, y, 42, y + 6, 25, y + 16, fill=color, outline="")

        title_box = tk.Frame(header, bg=self.ui_bg)
        title_box.pack(side="left", fill="x", expand=True)
        self._label(title_box, "WideAPP_EXTRA - Clientes, lotes e relatorios", 20, "bold", self.ui_text).pack(anchor="w")
        self._label(title_box, "Gestao de clientes, lotes e relatorios", 11, "normal", self.ui_muted).pack(anchor="w", pady=(2, 0))

        status_box = tk.Frame(header, bg=self.ui_bg)
        status_box.pack(side="right")
        self.conexao_var = tk.StringVar(value="Conectado ao WidePay")
        tk.Label(status_box, textvariable=self.conexao_var, bg=self.ui_bg, fg=self.ui_text, font=("Segoe UI", 10)).pack(side="left", padx=(0, 22))
        ttk.Button(status_box, text="Configuracoes", style="Toolbar.TButton", command=lambda: self.log("Configuracoes ainda nao possuem painel dedicado.")).pack(side="left")

        toolbar = self._panel(self.root, padx=14, pady=12)
        toolbar.pack(fill="x", padx=22, pady=(6, 10))
        tb = toolbar.inner
        tb_actions = tk.Frame(tb, bg=self.ui_panel)
        tb_actions.pack(fill="x")
        tb_open = tk.Frame(tb, bg=self.ui_panel)
        tb_open.pack(fill="x", pady=(10, 0))

        ttk.Button(tb_actions, text="Atualizar clientes", style="Primary.Toolbar.TButton", command=self.atualizar_async).pack(side="left", padx=(0, 10), ipady=5)
        ttk.Button(tb_actions, text="Atualizar WidePay", style="Toolbar.TButton", command=self.atualizar_widepay_async).pack(side="left", padx=(0, 10), ipady=5)
        self.btn_gerar_sel = ttk.Button(tb_actions, text="Gerar relatorio selecionados", style="Toolbar.TButton", command=self.gerar_selecionados)
        self.btn_gerar_sel.pack(side="left", padx=(0, 10), ipady=5)
        self.btn_gerar_todos = ttk.Button(tb_actions, text="Gerar clientes ativos", style="Toolbar.TButton", command=self.gerar_todos_ativos)
        self.btn_gerar_todos.pack(side="left", padx=(0, 10), ipady=5)
        self.btn_parar = ttk.Button(tb_actions, text="Parar captura", style="Danger.Toolbar.TButton", command=self.parar_captura, state="disabled")
        self.btn_parar.pack(side="left", ipady=5)

        ttk.Button(tb_open, text="Abrir pasta local", style="Toolbar.TButton", command=self.abrir_pasta_execucao).pack(side="left", padx=(0, 8), ipady=5)
        ttk.Button(tb_open, text="Abrir Drive", style="Toolbar.TButton", command=self.abrir_drive).pack(side="left", padx=(0, 8), ipady=5)
        ttk.Button(tb_open, text="Abrir HTML", style="Toolbar.TButton", command=lambda: self.abrir_tipo("html")).pack(side="left", padx=(0, 8), ipady=5)
        ttk.Button(tb_open, text="Abrir PDF", style="Toolbar.TButton", command=lambda: self.abrir_tipo("pdf")).pack(side="left", padx=(0, 8), ipady=5)
        ttk.Button(tb_open, text="Abrir XLSX", style="Toolbar.TButton", command=self.abrir_ultimo).pack(side="left", ipady=5)
        recentes_box = tk.Frame(tb_open, bg=self.ui_panel)
        recentes_box.pack(side="right", fill="x", expand=True, padx=(16, 0))
        self._label(recentes_box, "Planilhas recentes", 9, "normal", self.ui_muted, self.ui_panel).pack(side="left", padx=(0, 8))
        self.xlsx_combo = ttk.Combobox(recentes_box, state="readonly", width=58, style="Modern.TCombobox")
        self.xlsx_combo.pack(side="left", fill="x", expand=True, ipady=4)
        self.xlsx_combo.bind("<<ComboboxSelected>>", self.abrir_xlsx_selecionado)

        filtros_panel = self._panel(self.root, padx=16, pady=14)
        filtros_panel.pack(fill="x", padx=22, pady=(0, 8))
        filtros = filtros_panel.inner
        busca_box = tk.Frame(filtros, bg=self.ui_panel)
        busca_box.pack(side="left", fill="x", expand=True, padx=(0, 16))
        self._label(busca_box, "Pesquisar cliente", 9, "normal", self.ui_muted, self.ui_panel).pack(anchor="w")
        self.busca_var = tk.StringVar()
        busca = ttk.Entry(busca_box, textvariable=self.busca_var, style="Modern.TEntry", width=42)
        busca.pack(fill="x", ipady=4, pady=(4, 0))
        busca.insert(0, "")
        busca.bind("<KeyRelease>", lambda _e: self.aplicar_filtro())

        status_filter_box = tk.Frame(filtros, bg=self.ui_panel)
        status_filter_box.pack(side="left", padx=(0, 16))
        self._label(status_filter_box, "Status", 9, "normal", self.ui_muted, self.ui_panel).pack(anchor="w")
        self.status_var = tk.StringVar(value="Todos")
        status_box = ttk.Combobox(
            status_filter_box,
            textvariable=self.status_var,
            values=["Todos", "Pendente validacao WidePay", "APROVADO", "PENDENTE", "ERRO", "Sem contrato confirmado"],
            width=26,
            state="readonly",
            style="Modern.TCombobox",
        )
        status_box.pack(ipady=4, pady=(4, 0))
        status_box.bind("<<ComboboxSelected>>", lambda _e: self.aplicar_filtro())

        quadra_box = tk.Frame(filtros, bg=self.ui_panel)
        quadra_box.pack(side="left", padx=(0, 16))
        self._label(quadra_box, "Quadra / Lote", 9, "normal", self.ui_muted, self.ui_panel).pack(anchor="w")
        self.quadra_lote_var = tk.StringVar(value="Todos")
        self.quadra_lote_combo = ttk.Combobox(
            quadra_box,
            textvariable=self.quadra_lote_var,
            values=self._opcoes_quadra_lote(),
            width=24,
            state="readonly",
            style="Modern.TCombobox",
        )
        self.quadra_lote_combo.pack(ipady=4, pady=(4, 0))
        self.quadra_lote_combo.bind("<<ComboboxSelected>>", lambda _e: self.aplicar_filtro())
        ttk.Button(filtros, text="Limpar filtros", style="Toolbar.TButton", command=self.limpar_filtros).pack(side="left", ipady=7, pady=(18, 0))

        tabela_panel = self._panel(self.root, padx=14, pady=10)
        tabela_panel.pack(fill="both", expand=True, padx=22, pady=(0, 8))
        tabela = tabela_panel.inner
        self.tree = ttk.Treeview(tabela, columns=[c[0] for c in COLUNAS], show="tree headings", selectmode="extended", style="Modern.Treeview")
        self.tree.heading("#0", text="STATUS")
        self.tree.column("#0", width=86, minwidth=72, anchor="center", stretch=False)
        for key, label, width in COLUNAS:
            self.tree.heading(key, text=label)
            anchor = "w" if key == "cliente" else "center"
            self.tree.column(key, width=width, anchor=anchor)

        scroll_y = ttk.Scrollbar(tabela, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(tabela, orient="horizontal", command=self.tree.xview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(side="top", fill="both", expand=True)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tree.bind("<ButtonRelease-1>", lambda _e: self.sincronizar_selecao_tree())
        self.tree.bind("<Button-3>", self.mostrar_menu_contexto)
        self.tree.bind("<Double-1>", lambda _e: self.abrir_pasta_cliente_selecionado())
        self.tree.bind("<MouseWheel>", self._rolar_tree)
        self.tree.bind("<Shift-MouseWheel>", self._rolar_tree_horizontal)

        tabela_footer = tk.Frame(tabela, bg=self.ui_panel)
        tabela_footer.pack(side="bottom", fill="x", pady=(8, 0))
        self._label(tabela_footer, "Legenda (parcelas em atraso):", 9, "normal", self.ui_text, self.ui_panel).pack(side="left")
        self._label(tabela_footer, "  0-3 verde", 9, "normal", self.ui_text, self.ui_panel).pack(side="left", padx=(10, 0))
        self._label(tabela_footer, "  4-5 amarelo", 9, "normal", self.ui_text, self.ui_panel).pack(side="left", padx=(14, 0))
        self._label(tabela_footer, "  6+ vermelho", 9, "normal", self.ui_text, self.ui_panel).pack(side="left", padx=(14, 0))
        self.paginacao_var = tk.StringVar(value="Exibindo 0 de 0 clientes")
        tk.Label(tabela_footer, textvariable=self.paginacao_var, bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9)).pack(side="right")

        progresso_frame = tk.Frame(self.root, bg=self.ui_bg)
        progresso_frame.pack(fill="x", padx=22, pady=(0, 8))
        self.progress_label = tk.Label(progresso_frame, text="Aguardando inicio...", bg=self.ui_bg, fg=self.ui_text, font=("Segoe UI", 9))
        self.progress_label.pack(side="top", fill="x", anchor="w", pady=(0, 5))
        self.progress = ttk.Progressbar(progresso_frame, orient="horizontal", mode="determinate")
        self.progress.pack(side="top", fill="x")

        inferior = ttk.PanedWindow(self.root, orient="horizontal")
        inferior.pack(fill="both", expand=False, padx=22, pady=(0, 6))

        logs_frame = self._panel(inferior, padx=14, pady=10)
        resumo_frame = self._panel(inferior, padx=14, pady=10)
        inferior.add(logs_frame, weight=3)
        inferior.add(resumo_frame, weight=3)

        logs_header = tk.Frame(logs_frame.inner, bg=self.ui_panel)
        logs_header.pack(fill="x")
        self._label(logs_header, "Log de execucao", 11, "bold", self.ui_text, self.ui_panel).pack(side="left")
        ttk.Button(logs_header, text="Limpar log", style="Toolbar.TButton", command=lambda: self.logs.delete("1.0", "end")).pack(side="right")
        self.logs = tk.Text(logs_frame.inner, height=5, wrap="word", bg=self.ui_panel, fg=self.ui_text, insertbackground=self.ui_text, selectbackground="#0B7F45", selectforeground="#FFFFFF", font=("Consolas", 9), bd=0)
        self.logs.pack(fill="both", expand=True, pady=(8, 0))

        resumo_header = tk.Frame(resumo_frame.inner, bg=self.ui_panel)
        resumo_header.pack(fill="x")
        self._label(resumo_header, "Resumo rapido", 11, "bold", self.ui_text, self.ui_panel).pack(side="left")
        self.resumo_atualizado_var = tk.StringVar(value="Atualizado agora")
        tk.Label(resumo_header, textvariable=self.resumo_atualizado_var, bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9)).pack(side="right")
        cards = tk.Frame(resumo_frame.inner, bg=self.ui_panel)
        cards.pack(fill="x", pady=(10, 0))
        self.metric_total_var = tk.StringVar(value="0")
        self.metric_atraso_var = tk.StringVar(value="0")
        self.metric_critico_var = tk.StringVar(value="0")
        self.metric_atualizados_var = tk.StringVar(value="0")
        self._criar_card_resumo(cards, self.metric_total_var, "Clientes ativos", self.ui_green).pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._criar_card_resumo(cards, self.metric_atraso_var, "Em atraso", self.ui_red).pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._criar_card_resumo(cards, self.metric_critico_var, "Atraso critico", self.ui_yellow).pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._criar_card_resumo(cards, self.metric_atualizados_var, "Atualizados hoje", self.ui_blue).pack(side="left", fill="both", expand=True)

        self.links = tk.Text(resumo_frame.inner, height=3, wrap="word", bg="#101B21", fg=self.ui_text, insertbackground=self.ui_text, selectbackground="#0B7F45", selectforeground="#FFFFFF", font=("Consolas", 8), bd=0)
        self.links.pack(fill="x", pady=(10, 0))

        statusbar = tk.Frame(self.root, bg="#0B151A")
        statusbar.pack(fill="x", side="bottom")
        self._label(statusbar, "Usuario: administrador", 8, "normal", self.ui_muted, "#0B151A").pack(side="left", padx=22, pady=7)
        self._label(statusbar, "Versao 2.0.3", 8, "normal", self.ui_muted, "#0B151A").pack(side="left", padx=(20, 0), pady=7)
        self._label(statusbar, "Ambiente: Producao", 8, "normal", self.ui_muted, "#0B151A").pack(side="left", padx=(20, 0), pady=7)
        self.status_ultima_atualizacao_var = tk.StringVar(value="Ultima atualizacao: nunca")
        tk.Label(statusbar, textvariable=self.status_ultima_atualizacao_var, bg="#0B151A", fg=self.ui_muted, font=("Segoe UI", 8)).pack(side="right", padx=22, pady=7)

        self.log("Interface iniciada.")
        self.log("SKILL CARREGADA: widepay-core-operacional")
        self._registrar_diagnostico_inicial()
        if not self.registros:
            self.log("Cache vazio. Clique em Atualizar clientes.")

    def _criar_card_resumo(self, parent, var, label, accent):
        card = tk.Frame(parent, bg="#14222A", highlightbackground=accent, highlightthickness=1, bd=0)
        tk.Label(card, textvariable=var, bg="#14222A", fg=self.ui_text, font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=14, pady=(12, 0))
        tk.Label(card, text=label, bg="#14222A", fg=self.ui_text, font=("Segoe UI", 10)).pack(anchor="w", padx=14)
        tk.Label(card, text="base atual", bg="#14222A", fg=self.ui_muted, font=("Segoe UI", 8)).pack(anchor="w", padx=14, pady=(2, 12))
        return card

    def _registrar_diagnostico_inicial(self):
        import sys
        import subprocess
        from datetime import datetime

        main_path = Path(sys.argv[0]).resolve()
        interface_path = Path(__file__).resolve()
        try:
            mtime = datetime.fromtimestamp(interface_path.stat().st_mtime).strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            mtime = "Desconhecida"
        try:
            commit_version = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=str(interface_path.parent),
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except Exception:
            commit_version = "Sem Git"

        self.log(f"[DIAGNOSTICO] Entrada: {main_path}")
        self.log(f"[DIAGNOSTICO] Modulo UI: {interface_path}")
        self.log(f"[DIAGNOSTICO] Modificacao UI: {mtime}")
        self.log(f"[DIAGNOSTICO] Versao Git: {commit_version}")
        self.log(f"[DIAGNOSTICO] Cache JSON: {config.CLIENTES_JSON}")

    def limpar_filtros(self):
        self.busca_var.set("")
        self.status_var.set("Todos")
        if hasattr(self, "quadra_lote_var"):
            self.quadra_lote_var.set("Todos")
        self.aplicar_filtro()

    def log(self, msg):
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, lambda m=msg: self.log(m))
            return
        self.logs.insert("end", msg + "\n")
        self.logs.see("end")
        self.root.update_idletasks()

    def atualizar_async(self):
        self.log("Atualizacao incremental de clientes iniciada...")
        threading.Thread(target=self._atualizar, daemon=True).start()

    def _atualizar(self):
        result = indexador_clientes.indexar_clientes(validar_widepay=True, log_callback=self.log)
        self.registros = result["registros"]
        self.root.after(0, self.aplicar_filtro)
        self.root.after(0, self.atualizar_combo_xlsx)
        self.log(f"Clientes/lotes atualizados incrementalmente: {len(self.registros)}")

    def _obter_imagem_barrinha_legacy(self, boletos_atrasados):
        """Gera e retorna uma imagem de barrinha colorida dinamicamente baseada nos boletos vencidos."""
        chave_cache = str(boletos_atrasados)
        if chave_cache in self.imagens_barrinha:
            return self.imagens_barrinha[chave_cache]

        # Se for nulo ou vazio (sem auditoria), cria imagem totalmente transparente para alinhar
        if boletos_atrasados in (None, ""):
            img = Image.new("RGBA", (32, 16), (0, 0, 0, 0))
            photo = ImageTk.PhotoImage(img)
            self.imagens_barrinha[chave_cache] = photo
            return photo

        try:
            vencidos = int(float(boletos_atrasados))
        except (ValueError, TypeError):
            # Fallback para transparente
            img = Image.new("RGBA", (32, 16), (0, 0, 0, 0))
            photo = ImageTk.PhotoImage(img)
            self.imagens_barrinha[chave_cache] = photo
            return photo

        # Definir cores baseadas nas regras de boletos vencidos
        if vencidos <= 3:
            fill_color = "#00C853"  # Verde premium
            text_color = "#FFFFFF"  # Texto branco
        elif vencidos < 6:
            fill_color = "#FFD600"  # Amarelo premium
            text_color = "#181818"  # Texto escuro para contraste
        else:
            fill_color = "#FF1744"  # Vermelho premium
            text_color = "#FFFFFF"  # Texto branco

        # Criar imagem RGBA
        img = Image.new("RGBA", (32, 16), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Desenhar retângulo com borda suavizada (raio = 3)
        draw.rounded_rectangle([1, 1, 30, 14], radius=3, fill=fill_color)
        
        # Carregar fonte do sistema
        try:
            font = ImageFont.truetype("arial.ttf", 10)
        except IOError:
            font = ImageFont.load_default()

        # Calcular e alinhar texto centralizado
        text_str = str(vencidos)
        if hasattr(draw, "textbbox"):
            bbox = draw.textbbox((0, 0), text_str, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        else:
            text_w, text_h = draw.textsize(text_str, font=font) if hasattr(draw, "textsize") else (6, 8)

        x = (32 - text_w) // 2
        y = (16 - text_h) // 2 - 1

        draw.text((x, y), text_str, fill=text_color, font=font)

        photo = ImageTk.PhotoImage(img)
        self.imagens_barrinha[chave_cache] = photo
        return photo

    def obter_imagem_barrinha(self, boletos_atrasados):
        """Gera o selo colorido do indicador recente de atraso."""
        qtd = indexador_clientes.inteiro(boletos_atrasados)
        cor_status = indexador_clientes.classificar_status_atraso(qtd)
        chave_cache = f"{cor_status}:{qtd}"
        if chave_cache in self.imagens_barrinha:
            return self.imagens_barrinha[chave_cache]

        if cor_status == "verde":
            fill_color = "#00C853"
            text_color = "#FFFFFF"
        elif cor_status == "amarelo":
            fill_color = "#FFD600"
            text_color = "#181818"
        else:
            fill_color = "#FF1744"
            text_color = "#FFFFFF"

        img = Image.new("RGBA", (42, 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([1, 1, 40, 18], radius=4, fill=fill_color)

        try:
            font = ImageFont.truetype("arial.ttf", 11)
        except IOError:
            font = ImageFont.load_default()

        text_str = str(qtd)
        if hasattr(draw, "textbbox"):
            bbox = draw.textbbox((0, 0), text_str, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        else:
            text_w, text_h = draw.textsize(text_str, font=font) if hasattr(draw, "textsize") else (6, 8)

        x = (42 - text_w) // 2
        y = (20 - text_h) // 2 - 1
        draw.text((x, y), text_str, fill=text_color, font=font)

        photo = ImageTk.PhotoImage(img)
        self.imagens_barrinha[chave_cache] = photo
        return photo

    def aplicar_filtro(self):
        self.filtrados = pesquisa_clientes.filtrar(self.registros, self.busca_var.get(), self.status_var.get())
        quadra_lote = self.quadra_lote_var.get() if hasattr(self, "quadra_lote_var") else "Todos"
        if quadra_lote and quadra_lote != "Todos":
            alvo = quadra_lote.strip().upper()
            self.filtrados = [
                item for item in self.filtrados
                if str(item.get("quadra") or "").strip().upper() == alvo
                or str(item.get("lote") or "").strip().upper() == alvo
            ]
        self.tree.delete(*self.tree.get_children())
        for idx, item in enumerate(self.filtrados):
            values = [self._valor_grade(item, key) for key, _label, _width in COLUNAS]
            iid = str(idx)
            
            vencidos = item.get("status_atraso_qtd", item.get("boletos_atrasados", 0))
            img_barrinha = self.obter_imagem_barrinha(vencidos)
            
            # A coluna #0 exibe apenas o ícone da barrinha na coluna STATUS.
            # O texto da coluna #0 fica vazio (""), e o nome do cliente vai no values.
            self.tree.insert("", "end", iid=iid, text="", image=img_barrinha, values=values)
            if self._chave(item) in self.selecionados:
                self.tree.selection_add(iid)
        self.atualizar_resumo_visual()
        self.log(f"Filtro aplicado: {len(self.filtrados)} resultado(s).")

    def atualizar_resumo_visual(self):
        total = len(self.filtrados)
        total_base = len(self.registros)
        atrasados = sum(1 for item in self.filtrados if indexador_clientes.inteiro(item.get("status_atraso_qtd", item.get("boletos_atrasados", 0))) > 0)
        criticos = sum(1 for item in self.filtrados if indexador_clientes.inteiro(item.get("status_atraso_qtd", item.get("boletos_atrasados", 0))) >= 6)
        atualizados = sum(1 for item in self.filtrados if item.get("ultima_atualizacao_widepay"))
        if hasattr(self, "metric_total_var"):
            self.metric_total_var.set(str(total))
            self.metric_atraso_var.set(str(atrasados))
            self.metric_critico_var.set(str(criticos))
            self.metric_atualizados_var.set(str(atualizados))
        if hasattr(self, "paginacao_var"):
            self.paginacao_var.set(f"Exibindo {total} de {total_base} clientes")
        if hasattr(self, "status_ultima_atualizacao_var"):
            self.status_ultima_atualizacao_var.set(f"Ultima atualizacao: {indexador_clientes.formatar_data_hora(self._ultima_atualizacao_lista())}")

    def _ultima_atualizacao_lista(self):
        datas = [item.get("ultima_atualizacao_widepay") or item.get("data_atualizacao") for item in self.registros]
        datas = [d for d in datas if d]
        return sorted(datas)[-1] if datas else ""

    def _chave(self, item):
        return f"{item.get('cliente')}|{item.get('lote')}|{item.get('pasta_local')}"

    def _valor_grade(self, item, key):
        valor = item.get(key, "")
        if key == "cliente":
            return indexador_clientes.limpar_nome_cliente(str(valor))
        if key == "lote":
            lote_can = item.get("chave_lote_canonica") or indexador_clientes.chave_lote_canonica(item)
            lote = str(lote_can or item.get("lote") or "-").strip() or "-"
            quadra = str((lote_can[:1] if lote_can else item.get("quadra")) or "-").strip() or "-"
            return f"{lote} / {quadra}"
        if key == "contrato_resumo":
            return indexador_clientes.deduzir_resumo_contrato(item)
        if key == "parcelas_resumo":
            return indexador_clientes.deduzir_resumo_parcelas(item)
        if key == "situacao_final":
            return item.get("situacao_final") or indexador_clientes.deduzir_situacao_final(item)
        if key == "ultima_atualizacao_widepay":
            return indexador_clientes.formatar_data_hora(item.get("ultima_atualizacao_widepay") or item.get("data_atualizacao"))
        if key in ("valor_total_pago", "valor_total_contratado"):
            return indexador_clientes.formatar_moeda(valor)
        return valor

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

    def _registro_contexto_ou_primeiro(self):
        if self._context_iid is not None and str(self._context_iid) in self.tree.get_children():
            try:
                return self.filtrados[int(self._context_iid)]
            except Exception:
                pass
        registros = self._selecionados_registros()
        return registros[0] if registros else None

    def _rolar_tree(self, event):
        self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def _rolar_tree_horizontal(self, event):
        self.tree.xview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def gerar_todos_ativos(self):
        registros = [r for r in self.registros if r.get("contrato") == "Encontrado"]
        self._gerar(registros, "TODOS_ATIVOS")

    def gerar_selecionados(self):
        registros = self._selecionados_registros()
        self._gerar(registros, "SELECIONADOS")

    def _gerar(self, registros, grupo):
        if self.execucao_em_andamento:
            messagebox.showinfo("WideAPP_EXTRA", "Ja existe uma captura em andamento.")
            return
        if not registros:
            messagebox.showwarning("WideAPP_EXTRA", "Nenhum cliente selecionado.")
            return
        resumo = seletor_clientes.resumir_selecao(registros)
        dialogo = ConfirmacaoSelecaoDialogo(self.root, resumo)
        if not dialogo.result:
            self.log("Geracao cancelada pelo usuario.")
            return
        self.ultimo_grupo = grupo
        threading.Thread(target=self._gerar_thread, args=(registros, grupo), daemon=True).start()

    def parar_captura(self):
        if not self.execucao_em_andamento:
            self.log("Parada ignorada: nenhuma captura em andamento.")
            return
        interrompeu = pipeline_runner.solicitar_cancelamento(log_callback=self.log)
        self.root.after(0, lambda: self.progress_label.configure(text="Cancelamento solicitado..."))
        if interrompeu:
            self.log("Cancelamento enviado para a captura atual.")
        else:
            self.log("Cancelamento registrado. A captura sera interrompida assim que a etapa atual responder.")

    def _marcar_execucao_iniciada(self):
        self.execucao_em_andamento = True
        self.btn_gerar_sel.configure(state="disabled")
        self.btn_gerar_todos.configure(state="disabled")
        self.btn_parar.configure(state="normal")

    def _marcar_execucao_finalizada(self):
        self.execucao_em_andamento = False
        self.btn_gerar_sel.configure(state="normal")
        self.btn_gerar_todos.configure(state="normal")
        self.btn_parar.configure(state="disabled")

    def _gerar_thread(self, registros, grupo):
        self.root.after(0, self._marcar_execucao_iniciada)
        self.root.after(0, lambda: self.progress.configure(value=0))
        self.root.after(0, lambda: self.progress_label.configure(text="Iniciando execução da pipeline..."))
        self.log("Processando cliente...")
        self.log("Pipeline em execucao...")
        try:
            resultado = pipeline_runner.executar_lote(
                registros,
                grupo=grupo,
                log_callback=self.log,
                progress_callback=self.atualizar_progresso
            )
            self.log("CODIGO SAIDA: 0")
            self.log("Relatorio gerado com sucesso.")
            self.root.after(0, self.atualizar_combo_xlsx)
        except Exception as exc:
            self.log(f"ERRO_PIPELINE: {exc}")
            self.root.after(0, lambda: self.progress_label.configure(text=f"Erro na pipeline: {exc}"))
            self.root.after(0, self._marcar_execucao_finalizada)
            self.root.after(0, lambda: messagebox.showerror("WideAPP_EXTRA", f"Erro na pipeline:\n{exc}"))
            return

        if resultado.get("cancelado"):
            self.log("CAPTURA_CANCELADA: execucao interrompida pelo usuario.")
            self.root.after(0, lambda: self.progress_label.configure(text="Captura interrompida pelo usuario."))

        falhas = resultado.get("falhas") or []
        if falhas and not resultado.get("cancelado"):
            resumo_falhas = "\n".join(
                f"- {item.get('cliente')} lote {item.get('lote')}: {item.get('erro')}"
                for item in falhas[:5]
            )
            self.log(f"FALHAS_PARCIAIS: {len(falhas)} cliente(s)")
            self.root.after(
                0,
                lambda: messagebox.showwarning(
                    "WideAPP_EXTRA",
                    f"Relatorios gerados para {len(resultado.get('resultados', []))} cliente(s), "
                    f"mas {len(falhas)} falharam:\n{resumo_falhas}"
                )
            )

        self.ultimos = {"xlsx": [], "pdf": [], "html": [], "md": [], "json": [], "log": []}
        for res in resultado["resultados"]:
            for tipo, paths in res["arquivos"].items():
                self.ultimos.setdefault(tipo, []).extend(paths)

            # Atualiza registro em memoria com os resultados da pipeline
            c_name_norm = res.get("cliente", "").strip().lower()
            c_lote_norm = res.get("lote", "").strip().lower()
            for r in self.registros:
                r_name = r.get("cliente", "").strip().lower()
                r_lote = r.get("lote", "").strip().lower()
                if r_name == c_name_norm and r_lote == c_lote_norm:
                    json_paths = res["arquivos"].get("json", [])
                    if json_paths:
                        try:
                            import json
                            with open(json_paths[0], "r", encoding="utf-8") as jf:
                                metrics = json.load(jf)
                            atualizado = indexador_clientes.aplicar_metricas_registro(r, metrics)
                            r.clear()
                            r.update(atualizado)
                        except Exception as je:
                            self.log(f"Erro ao ler JSON de metricas: {je}")
                    else:
                        r["observacoes"] = "Relatorio gerado sem JSON de metricas"

        # Salvar cache local atualizado
        try:
            indexador_clientes.salvar_cache(self.registros)
            self.log("Cache local atualizado com sucesso.")
        except Exception as se:
            self.log(f"Erro ao salvar cache local: {se}")

        # Atualiza a tabela na UI
        self.root.after(0, self.aplicar_filtro)

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
        if resultado.get("cancelado"):
            self.log("Captura encerrada sem consolidado/upload final por solicitacao do usuario.")
        else:
            self.log(f"Pipeline concluido. Manifesto Drive: {config.LINKS_DRIVE_MD}")
        if resultado["ignorados"]:
            self.log(f"Ignorados sem contrato confirmado: {len(resultado['ignorados'])}")

        self.root.after(0, self._marcar_execucao_finalizada)

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
        if self.ultima_pasta and Path(self.ultima_pasta).exists():
            abrir_pasta(self.ultima_pasta)
            self.log(f"Pasta local aberta: {self.ultima_pasta}")
        else:
            messagebox.showinfo("WideAPP_EXTRA", f"Pasta local nao encontrada: {self.ultima_pasta}")

    def abrir_drive(self):
        destino = drive_uploader.abrir_destino_drive(self.ultimo_grupo)
        if not destino:
            messagebox.showinfo("WideAPP_EXTRA", "Destino Drive nao configurado.")
            return
        if hasattr(destino, "exists"):
            if destino.exists():
                abrir_pasta(destino)
                self.log(f"Pasta Drive aberta: {destino}")
            else:
                messagebox.showinfo("WideAPP_EXTRA", f"Pasta Drive nao encontrada: {destino}")
        else:
            self.links.insert("end", f"Destino Drive remoto: {destino}\n")

    def atualizar_progresso(self, pct, tempo_restante_segundos):
        def _update():
            self.progress["value"] = pct
            if pct >= 100.0:
                self.progress_label.configure(text="Execução concluída com sucesso! (100%)")
            else:
                tempo_str = f"{int(tempo_restante_segundos)}s" if tempo_restante_segundos > 0 else "calculando..."
                self.progress_label.configure(text=f"Processando pipeline... {pct:.1f}% concluído. Tempo restante estimado: {tempo_str}")
            self.root.update_idletasks()
        self.root.after(0, _update)

    def obter_xlsx_recentes(self):
        from pathlib import Path
        arquivos = []
        if config.OUTPUT_DIR.exists():
            for p in config.OUTPUT_DIR.rglob("*.xlsx"):
                if p.is_file() and not p.name.startswith("~$"):
                    arquivos.append(p)
        planilhas_dir = config.ROOT_DIR / "03_PLANILHAS"
        if planilhas_dir.exists():
            for p in planilhas_dir.rglob("*.xlsx"):
                if p.is_file() and not p.name.startswith("~$"):
                    arquivos.append(p)
        drive_dir = Path(config.DRIVE_LOCAL_DIR)
        if drive_dir.exists():
            for p in drive_dir.rglob("*.xlsx"):
                if p.is_file() and not p.name.startswith("~$"):
                    arquivos.append(p)
        unicos = {}
        for p in arquivos:
            try:
                resolvido = p.resolve()
                unicos[resolvido] = p
            except Exception:
                unicos[p] = p
        lista_ordenada = list(unicos.values())
        lista_ordenada.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
        return lista_ordenada

    def atualizar_combo_xlsx(self):
        try:
            self.xlsx_map = {}
            items = []
            from datetime import datetime
            xlsx_files = self.obter_xlsx_recentes()
            for p in xlsx_files[:40]:
                try:
                    mtime = p.stat().st_mtime
                    dt_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                except Exception:
                    dt_str = "Desconhecido"
                
                nome_arq = p.stem
                friendly_name = nome_arq
                if nome_arq.startswith("RELATORIO_FINANCEIRO_CLIENTE_"):
                    partes = nome_arq.replace("RELATORIO_FINANCEIRO_CLIENTE_", "")
                    if "_LOTE_" in partes:
                        subpartes = partes.split("_LOTE_")
                        nome_cliente = subpartes[0].replace("_", " ").title()
                        lote_e_data = subpartes[1]
                        lote_name = lote_e_data.split("_")[0] if "_" in lote_e_data else lote_e_data
                        friendly_name = f"{nome_cliente} - Lote {lote_name}"
                
                display_name = f"{dt_str} - {friendly_name}"
                items.append(display_name)
                self.xlsx_map[display_name] = p
            if hasattr(self, "xlsx_combo"):
                self.xlsx_combo.configure(values=items)
                if items:
                    self.xlsx_combo.set("Selecione para abrir...")
                else:
                    self.xlsx_combo.set("Nenhuma planilha encontrada")
        except Exception as e:
            self.log(f"Erro ao atualizar dropdown de planilhas: {e}")

    def abrir_xlsx_selecionado(self, event=None):
        if not hasattr(self, "xlsx_combo"):
            return
        selected = self.xlsx_combo.get()
        path = self.xlsx_map.get(selected)
        if path and path.exists():
            self.log(f"Abrindo planilha selecionada: {path.name}")
            abrir(path)

    def mostrar_menu_contexto(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self._context_iid = row_id
            if row_id not in self.tree.selection():
                self.tree.selection_set(row_id)
            self.sincronizar_selecao_tree()
            
            menu = tk.Menu(self.root, tearoff=0, bg="#242424", fg="#F3F3F3", activebackground="#007A3E", activeforeground="#F3F3F3")
            menu.add_command(label="Gerar relatório do(s) selecionado(s)", command=self.gerar_selecionados)
            menu.add_command(label="Abrir pasta do cliente no Explorer", command=self.abrir_pasta_cliente_selecionado)
            menu.add_command(label="Abrir planilha recente do cliente", command=self.abrir_planilha_cliente_selecionado)
            menu.add_separator()
            menu.add_command(label="Atualizar clientes", command=self.atualizar_async)
            menu.add_command(label="Atualizar informações da WidePay (selecionados)", command=self.atualizar_widepay_selecionados_async)
            
            menu.post(event.x_root, event.y_root)

    def abrir_pasta_cliente_selecionado(self):
        reg = self._registro_contexto_ou_primeiro()
        if not reg:
            messagebox.showinfo("WideAPP_EXTRA", "Nenhum cliente selecionado.")
            return
        pasta = reg.get("pasta_local")
        if pasta and Path(pasta).exists():
            self.log(f"SKILL CARREGADA: widepay-abertura-externa")
            self.log(f"EXECUÇÃO EXTERNA: abrir pasta do cliente {reg.get('cliente')}")
            abrir_pasta(pasta)
            self.log(f"VISUALIZADOR PADRÃO: pasta aberta no Explorer")
        else:
            messagebox.showwarning("WideAPP_EXTRA", f"Pasta do cliente nao encontrada: {pasta}")

    def abrir_planilha_cliente_selecionado(self):
        reg = self._registro_contexto_ou_primeiro()
        if not reg:
            messagebox.showinfo("WideAPP_EXTRA", "Nenhum cliente selecionado.")
            return
        cliente = reg.get("cliente", "")
        lote = reg.get("lote", "")
        slug_c = indexador_clientes.slug_busca(cliente).upper().replace(" ", "_")
        
        pasta_relatorios = config.OUTPUT_DIR
        encontrado = None
        if pasta_relatorios.exists():
            arquivos = []
            for p in pasta_relatorios.rglob("*.xlsx"):
                if p.is_file() and not p.name.startswith("~$"):
                    name_upper = p.name.upper()
                    if slug_c in name_upper or (lote and lote.upper() in name_upper):
                        arquivos.append(p)
            if arquivos:
                arquivos.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
                encontrado = arquivos[0]
                
        if encontrado:
            self.log(f"SKILL CARREGADA: widepay-abertura-externa")
            self.log(f"EXECUÇÃO EXTERNA: abrindo planilha recente do cliente {cliente}: {encontrado.name}")
            abrir(encontrado)
            self.log(f"VISUALIZADOR PADRÃO: planilha aberta no Excel")
        else:
            messagebox.showwarning("WideAPP_EXTRA", f"Nenhum relatorio XLSX encontrado para {cliente} no diretorio {pasta_relatorios}")

    def atualizar_widepay_async(self):
        registros = [r for r in self.registros if r.get("contrato") == "Encontrado"]
        if not registros:
            messagebox.showinfo("WideAPP_EXTRA", "Nenhum cliente com contrato confirmado para atualizar do WidePay.")
            return
        if not messagebox.askyesno("Atualizar WidePay", f"Deseja baixar e atualizar as informacoes de pagamentos do WidePay para os {len(registros)} clientes confirmados? Isso sincronizara nomes e parcelas pagas."):
            return
        self.ultimo_grupo = "WIDEPAY_ATUALIZACAO"
        threading.Thread(target=self._gerar_thread, args=(registros, "WIDEPAY_ATUALIZACAO"), daemon=True).start()

    def atualizar_widepay_selecionados_async(self):
        registros = self._selecionados_registros()
        confirmados = [r for r in registros if r.get("contrato") == "Encontrado"]
        if not confirmados:
            messagebox.showinfo("WideAPP_EXTRA", "Nenhum cliente selecionado com contrato confirmado.")
            return
        if not messagebox.askyesno("Atualizar WidePay", f"Deseja baixar e atualizar as informacoes de pagamentos do WidePay para os {len(confirmados)} clientes selecionados?"):
            return
        self.ultimo_grupo = "WIDEPAY_SELECIONADOS"
        threading.Thread(target=self._gerar_thread, args=(confirmados, "WIDEPAY_SELECIONADOS"), daemon=True).start()


def abrir_interface():
    config.ensure_dirs()
    root = tk.Tk()
    root.deiconify()
    root.lift()
    root.attributes("-topmost", True)
    root.after(250, lambda: root.attributes("-topmost", False))
    root.after(300, root.focus_force)
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
