# -*- coding: utf-8 -*-
"""Interface visual Tkinter da WideAPP_EXTRA."""

import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
from PIL import Image, ImageDraw, ImageTk, ImageFont

from app import config
from app import indexador_clientes
from app import pesquisa_clientes
from app import saneamento_clientes
from app import seletor_clientes
from app import drive_uploader
from app import pipeline_runner
from app.app_version import APP_VERSION, APP_VERSION_LABEL, APP_WINDOW_TITLE
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
        self.root.title(APP_WINDOW_TITLE)
        self.root.geometry("1500x900")
        self.root.minsize(1280, 760)
        self.app_version_var = tk.StringVar(value=APP_VERSION_LABEL)
        
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
        style.configure("Toolbar.TButton", background=self.ui_panel_alt, foreground=self.ui_text, bordercolor=self.ui_border, font=("Segoe UI", 9, "bold"), padding=(10, 4))
        style.map("Toolbar.TButton",
            background=[("active", "#233A44"), ("disabled", "#1A2226")],
            foreground=[("active", self.ui_text), ("disabled", "#66737A")]
        )
        style.configure("Primary.Toolbar.TButton", background="#10B95B", foreground="#FFFFFF", bordercolor="#2DF27D", font=("Segoe UI", 9, "bold"), padding=(12, 4))
        style.map("Primary.Toolbar.TButton",
            background=[("active", "#22C55E"), ("disabled", "#1A2226")],
            foreground=[("active", "#06150B"), ("disabled", "#66737A")]
        )
        style.configure("Danger.Toolbar.TButton", background="#3A2630", foreground="#FFB4C0", bordercolor="#7F2D3B", font=("Segoe UI", 9, "bold"), padding=(10, 4))
        style.map("Danger.Toolbar.TButton",
            background=[("active", "#7F1D1D"), ("disabled", "#1A2226")],
            foreground=[("active", "#FFFFFF"), ("disabled", "#66737A")]
        )
        style.configure("Info.Toolbar.TButton", background="#1D4ED8", foreground="#FFFFFF", bordercolor="#60A5FA", font=("Segoe UI", 9, "bold"), padding=(10, 4))
        style.map("Info.Toolbar.TButton",
            background=[("active", "#2563EB"), ("disabled", "#1A2226")],
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
        style.configure("TNotebook", background=self.ui_bg, borderwidth=0)
        style.configure("TNotebook.Tab", background="#102029", foreground=self.ui_text, padding=(14, 8), font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
            background=[("selected", self.ui_panel), ("active", "#1C2B33")],
            foreground=[("selected", "#FFFFFF"), ("active", "#FFFFFF")]
        )

        self.registros = indexador_clientes.carregar_cache()
        self.filtrados = []
        self.selecionados = set()
        self.sort_column = "cliente"
        self.sort_descending = False
        self.imagens_barrinha = {}
        self.ultimo_arquivo = None
        self.ultima_pasta = config.OUTPUT_DIR
        self.ultimos = {"xlsx": [], "pdf": [], "html": [], "md": [], "json": [], "log": []}
        self.ultimo_grupo = "SELECIONADOS"
        self.xlsx_map = {}
        self._context_iid = None
        self._context_tree = None
        self._tree_record_maps = {}
        self.execucao_em_andamento = False
        self.progress_status_var = tk.StringVar(value="Pronto")
        self.progress_etapa_var = tk.StringVar(value="Aguardando ação do usuário")
        self.progress_pct_var = tk.StringVar(value="0%")
        self.progress_reg_var = tk.StringVar(value="0")
        self.progress_cli_var = tk.StringVar(value="0")
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

    def _montar_painel_progresso(self, parent):
        progress_panel = self._panel(parent, padx=10, pady=8)
        self.progress_panel = progress_panel
        prog_inner = progress_panel.inner

        self._label(prog_inner, "Andamento da atualizacao", 10, "bold", self.ui_text, self.ui_panel).pack(anchor="w", pady=(0, 4))

        info_frame = tk.Frame(prog_inner, bg=self.ui_panel)
        info_frame.pack(fill="x", pady=(0, 4))

        tk.Label(info_frame, text="Status: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_status_val = tk.Label(info_frame, textvariable=self.progress_status_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_status_val.pack(side="left", padx=(0, 10))

        tk.Label(info_frame, text="Progresso: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_pct_val = tk.Label(info_frame, textvariable=self.progress_pct_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_pct_val.pack(side="left", padx=(0, 10))

        tk.Label(info_frame, text="Clientes: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_cli_val = tk.Label(info_frame, textvariable=self.progress_cli_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_cli_val.pack(side="left", padx=(0, 10))

        tk.Label(info_frame, text="Registros: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_reg_val = tk.Label(info_frame, textvariable=self.progress_reg_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_reg_val.pack(side="left", padx=(0, 10))

        etapa_frame = tk.Frame(prog_inner, bg=self.ui_panel)
        etapa_frame.pack(fill="x", pady=(0, 4))
        tk.Label(etapa_frame, text="Etapa: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_etapa_val = tk.Label(etapa_frame, textvariable=self.progress_etapa_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_etapa_val.pack(side="left")
        self.progress_label = self.lbl_etapa_val

        style = ttk.Style(self.root)
        style.configure("Big.Horizontal.TProgressbar", thickness=10, troughcolor="#0F1A20", background="#22C55E")
        self.progress = ttk.Progressbar(prog_inner, orient="horizontal", mode="determinate", style="Big.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(0, 4))

        log_label_frame = tk.Frame(prog_inner, bg=self.ui_panel)
        log_label_frame.pack(fill="x", pady=(4, 2))
        self._label(log_label_frame, "Log de andamento recente:", 9, "bold", self.ui_muted, self.ui_panel).pack(anchor="w")

        self.progress_mini_log = tk.Text(
            prog_inner,
            height=3,
            bg="#0F1A20",
            fg="#F3F7F8",
            font=("Consolas", 8),
            bd=0,
            highlightthickness=1,
            highlightbackground="#2D4650",
            padx=6,
            pady=3
        )
        self.progress_mini_log.pack(fill="x")
        self.progress_mini_log.configure(state="disabled")
        return progress_panel



    def _montar(self):
        self.root.configure(bg=self.ui_bg)

        header = tk.Frame(self.root, bg=self.ui_bg)
        self.header_frame = header
        header.pack(fill="x", padx=22, pady=(16, 8))

        status_box = tk.Frame(header, bg=self.ui_bg)
        self.header_status_box = status_box
        status_box.pack(side="right", anchor="ne")
        self.conexao_var = tk.StringVar(value="Conectado ao WidePay")
        conexao_row = tk.Frame(status_box, bg=self.ui_bg)
        conexao_row.pack(anchor="e", pady=(0, 6))
        tk.Label(conexao_row, textvariable=self.conexao_var, bg=self.ui_bg, fg=self.ui_text, font=("Segoe UI", 10)).pack(side="left", padx=(0, 22))
        ttk.Button(conexao_row, text="Configuracoes", style="Toolbar.TButton", command=lambda: self.log("Configuracoes ainda nao possuem painel dedicado.")).pack(side="left")
        # O painel de progresso definitivo e montado no fim do bloco legado abaixo.

        # Logo image loader using PIL
        try:
            from PIL import Image, ImageTk
            logo_path = Path(__file__).resolve().parent.parent / "widepay_icon_transparente_centralizado_ok.png"
            if not logo_path.exists():
                logo_path = Path(__file__).resolve().parent.parent / "assets" / "wideapp_extra_icon.png"
            if not logo_path.exists():
                logo_path = Path(__file__).resolve().parent / "assets" / "wideapp_extra_icon.png"
            if logo_path.exists():
                logo_img = Image.open(logo_path).resize((48, 48), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(header, image=self.logo_photo, bg=self.ui_bg)
                logo_label.pack(side="left", padx=(0, 14))
            else:
                # Fallback to polygon drawing if file is missing
                logo = tk.Canvas(header, width=50, height=50, bg=self.ui_bg, highlightthickness=0)
                logo.pack(side="left", padx=(0, 14))
                for y, color in ((8, "#67E85A"), (20, "#44C85D"), (32, "#2EA84E")):
                    logo.create_polygon(8, y + 6, 25, y, 42, y + 6, 25, y + 16, fill=color, outline="")
        except Exception:
            logo = tk.Canvas(header, width=50, height=50, bg=self.ui_bg, highlightthickness=0)
            logo.pack(side="left", padx=(0, 14))
            for y, color in ((8, "#67E85A"), (20, "#44C85D"), (32, "#2EA84E")):
                logo.create_polygon(8, y + 6, 25, y, 42, y + 6, 25, y + 16, fill=color, outline="")

        title_box = tk.Frame(header, bg=self.ui_bg)
        self.title_box = title_box
        title_box.pack(side="left", fill="both", expand=True, padx=(0, 16))

        title_row = tk.Frame(title_box, bg=self.ui_bg)
        title_row.pack(fill="x")
        self.title_label = self._label(title_row, "WideAPP_EXTRA - Clientes, lotes e relatorios", 20, "bold", self.ui_text)
        self.title_label.pack(side="left", anchor="w")
        self.version_badge = tk.Label(
            title_row,
            textvariable=self.app_version_var,
            bg="#132833",
            fg=self.ui_text,
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=4,
            highlightbackground=self.ui_border,
            highlightthickness=1,
        )
        self.version_badge.pack(side="left", padx=(12, 0), pady=(2, 0))

        self._label(title_box, "Gestao de clientes, lotes e relatorios", 11, "normal", self.ui_muted).pack(anchor="w", pady=(2, 0))

        toolbar = self._panel(title_box, padx=14, pady=10)
        self.toolbar_panel = toolbar
        toolbar.pack(fill="x", pady=(20, 0))
        tb = toolbar.inner
        
        tb_row1 = tk.Frame(tb, bg=self.ui_panel)
        tb_row1.pack(fill="x", pady=(2, 4))
        
        tb_row2 = tk.Frame(tb, bg=self.ui_panel)
        tb_row2.pack(fill="x", pady=(2, 2))

        self.btn_atualizar_cli = ttk.Button(tb_row1, text="Atualizar clientes", style="Primary.Toolbar.TButton", command=self.atualizar_async)
        self.btn_atualizar_cli.pack(side="left", padx=(0, 8), ipady=3)

        self.btn_visualizar_db = ttk.Button(tb_row1, text="Visualizar banco de dados", style="Info.Toolbar.TButton", command=self.visualizar_banco_dados)
        self.btn_visualizar_db.pack(side="left", padx=(0, 8), ipady=3)
        
        self.btn_atualizar_wp = ttk.Button(tb_row1, text="Atualizar WidePay", style="Toolbar.TButton", command=self.atualizar_widepay_async)
        self.btn_atualizar_wp.pack(side="left", padx=(0, 8), ipady=3)
        
        self.btn_parar = ttk.Button(tb_row1, text="Parar captura", style="Danger.Toolbar.TButton", command=self.parar_captura, state="disabled")
        self.btn_parar.pack(side="left", padx=(0, 8), ipady=3)

        self.btn_abrir_xlsx = ttk.Button(tb_row1, text="Abrir XLSX", style="Toolbar.TButton", command=self.abrir_ultimo)
        self.btn_abrir_xlsx.pack(side="left", padx=(0, 8), ipady=3)

        self.btn_abrir_pasta = ttk.Button(tb_row1, text="Abrir pasta local", style="Toolbar.TButton", command=self.abrir_pasta_execucao)
        self.btn_abrir_pasta.pack(side="left", padx=(0, 8), ipady=3)

        self.btn_abrir_drive = ttk.Button(tb_row1, text="Abrir Drive", style="Toolbar.TButton", command=self.abrir_drive)
        self.btn_abrir_drive.pack(side="left", ipady=3)

        self.btn_gerar_sel = ttk.Button(tb_row2, text="Gerar relatorio selecionados", style="Toolbar.TButton", command=self.gerar_selecionados)
        self.btn_gerar_sel.pack(side="left", padx=(0, 8), ipady=3)
        
        self.btn_gerar_todos = ttk.Button(tb_row2, text="Gerar clientes ativos", style="Toolbar.TButton", command=self.gerar_todos_ativos)
        self.btn_gerar_todos.pack(side="left", padx=(0, 8), ipady=3)

        self.btn_abrir_html = ttk.Button(tb_row2, text="Abrir HTML", style="Toolbar.TButton", command=lambda: self.abrir_tipo("html"))
        self.btn_abrir_html.pack(side="left", padx=(0, 8), ipady=3)

        self.btn_abrir_pdf = ttk.Button(tb_row2, text="Abrir PDF", style="Toolbar.TButton", command=lambda: self.abrir_tipo("pdf"))
        self.btn_abrir_pdf.pack(side="left", padx=(0, 16), ipady=3)

        recentes_box = tk.Frame(tb_row2, bg=self.ui_panel)
        recentes_box.pack(side="left", fill="x", expand=True)
        self._label(recentes_box, "Planilhas recentes", 9, "normal", self.ui_muted, self.ui_panel).pack(side="left", padx=(0, 8))
        self.xlsx_combo = ttk.Combobox(recentes_box, state="readonly", width=42, style="Modern.TCombobox")
        self.xlsx_combo.pack(side="left", fill="x", expand=True, ipady=3)
        self.xlsx_combo.bind("<<ComboboxSelected>>", self.abrir_xlsx_selecionado)

        # -------------------------------------------------------------
        # Painel de Andamento da Atualização (área fixa de progresso)
        # -------------------------------------------------------------
        progress_panel = self._panel(self.root, padx=10, pady=8)
        progress_panel.pack(anchor="e", padx=22, pady=(0, 6))
        prog_inner = progress_panel.inner
        
        self._label(prog_inner, "Andamento da atualização", 10, "bold", self.ui_text, self.ui_panel).pack(anchor="w", pady=(0, 4))
        
        info_frame = tk.Frame(prog_inner, bg=self.ui_panel)
        info_frame.pack(fill="x", pady=(0, 4))
        
        # Grid of status fields
        tk.Label(info_frame, text="Status: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_status_val = tk.Label(info_frame, textvariable=self.progress_status_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_status_val.pack(side="left", padx=(0, 10))
        
        tk.Label(info_frame, text="Progresso: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_pct_val = tk.Label(info_frame, textvariable=self.progress_pct_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_pct_val.pack(side="left", padx=(0, 10))

        tk.Label(info_frame, text="Clientes: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_cli_val = tk.Label(info_frame, textvariable=self.progress_cli_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_cli_val.pack(side="left", padx=(0, 10))

        tk.Label(info_frame, text="Registros: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_reg_val = tk.Label(info_frame, textvariable=self.progress_reg_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_reg_val.pack(side="left", padx=(0, 10))
        
        tk.Label(info_frame, text="Etapa: ", bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.lbl_etapa_val = tk.Label(info_frame, textvariable=self.progress_etapa_var, bg=self.ui_panel, fg=self.ui_text, font=("Segoe UI", 9))
        self.lbl_etapa_val.pack(side="left")
        self.progress_label = self.lbl_etapa_val

        # Custom high visibility style for progress bar
        style = ttk.Style(self.root)
        style.configure("Big.Horizontal.TProgressbar", thickness=10, troughcolor="#0F1A20", background="#22C55E")
        self.progress = ttk.Progressbar(prog_inner, orient="horizontal", mode="determinate", style="Big.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(0, 4))
        
        log_label_frame = tk.Frame(prog_inner, bg=self.ui_panel)
        log_label_frame.pack(fill="x", pady=(4, 2))
        self._label(log_label_frame, "Log de andamento recente:", 9, "bold", self.ui_muted, self.ui_panel).pack(anchor="w")
        
        self.progress_mini_log = tk.Text(
            prog_inner,
            height=3,
            bg="#0F1A20",
            fg="#F3F7F8",
            font=("Consolas", 8),
            bd=0,
            highlightthickness=1,
            highlightbackground="#2D4650",
            padx=6,
            pady=3
        )
        self.progress_mini_log.pack(fill="x")
        self.progress_mini_log.configure(state="disabled")
        progress_panel.destroy()
        self._montar_painel_progresso(status_box).pack(anchor="e")

        main_area = tk.Frame(self.root, bg=self.ui_bg)
        self.main_area = main_area
        main_area.pack(fill="both", expand=True, padx=22, pady=(0, 8))

        content_area = tk.Frame(main_area, bg=self.ui_bg)
        self.content_area = content_area
        content_area.pack(fill="both", expand=True)

        filtros_panel = self._panel(content_area, padx=16, pady=14)
        filtros_panel.pack(fill="x", pady=(0, 8))
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

        workspace_tabs = ttk.Notebook(content_area)
        self.workspace_tabs = workspace_tabs
        workspace_tabs.pack(fill="both", expand=True)

        clientes_tab = tk.Frame(workspace_tabs, bg=self.ui_bg)
        recentes_tab = tk.Frame(workspace_tabs, bg=self.ui_bg)
        quitados_tab = tk.Frame(workspace_tabs, bg=self.ui_bg)
        bloqueados_tab = tk.Frame(workspace_tabs, bg=self.ui_bg)
        banco_tab = tk.Frame(workspace_tabs, bg=self.ui_bg)
        logs_tab = tk.Frame(workspace_tabs, bg=self.ui_bg)
        resumo_tab = tk.Frame(workspace_tabs, bg=self.ui_bg)
        auditoria_tab = tk.Frame(workspace_tabs, bg=self.ui_bg)
        self.clientes_tab = clientes_tab
        self.recentes_tab = recentes_tab
        self.quitados_tab = quitados_tab
        self.bloqueados_tab = bloqueados_tab
        self.banco_tab = banco_tab
        self.logs_tab = logs_tab
        self.resumo_tab = resumo_tab
        self.auditoria_tab = auditoria_tab
        workspace_tabs.add(clientes_tab, text="Ativos")
        workspace_tabs.add(recentes_tab, text="Pagamentos Recentes")
        workspace_tabs.add(quitados_tab, text="Quitados")
        workspace_tabs.add(bloqueados_tab, text="Bloqueados / Removidos")
        workspace_tabs.add(banco_tab, text="Banco de dados")
        workspace_tabs.add(logs_tab, text="Logs")
        workspace_tabs.add(resumo_tab, text="Resumo / status")
        workspace_tabs.add(auditoria_tab, text="Auditoria")
        workspace_tabs.bind("<<NotebookTabChanged>>", lambda _e: self.atualizar_aba_auditoria())

        # Define display columns visually excluding observacoes by default
        display_cols = [c[0] for c in COLUNAS if c[0] != "observacoes"]
        try:
            import json
            config_path = config.DATA_DIR / "colunas_config.json"
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    saved_cols = json.load(f)
                valid_saved = [col for col in saved_cols if col in [c[0] for c in COLUNAS]]
                if valid_saved:
                    display_cols = valid_saved
        except Exception:
            pass
        self.display_cols = display_cols

        clientes_paned = ttk.PanedWindow(clientes_tab, orient="vertical")
        self.clientes_paned = clientes_paned
        clientes_paned.pack(fill="both", expand=True)

        tabela_panel = self._panel(clientes_paned, padx=14, pady=10)
        self.tabela_panel = tabela_panel
        tabela = tabela_panel.inner
        self.tree = ttk.Treeview(tabela, columns=[c[0] for c in COLUNAS], show="tree headings", selectmode="extended", style="Modern.Treeview")
        self.tree["displaycolumns"] = display_cols
        
        self.tree.heading("#0", text="STATUS")
        self.tree.column("#0", width=86, minwidth=72, anchor="center", stretch=False)
        for key, label, width in COLUNAS:
            self.tree.heading(key, text=label)
            anchor = "w" if key == "cliente" else "center"
            self.tree.column(key, width=width, anchor=anchor, stretch=True)

        scroll_y = ttk.Scrollbar(tabela, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(side="top", fill="both", expand=True)
        self.tree.configure(yscrollcommand=scroll_y.set)
        
        # Handlers for click to sort vs click-and-drag to reorder columns
        self.tree.bind("<ButtonPress-1>", self.on_tree_press)
        self.tree.bind("<B1-Motion>", self.on_tree_motion)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_release)
        
        self.tree.bind("<Button-3>", self.mostrar_menu_contexto)
        self.tree.bind("<Double-1>", lambda _e: self.abrir_pasta_cliente_selecionado())
        self.tree.bind("<MouseWheel>", self._rolar_tree)
        self.tree.bind("<<TreeviewSelect>>", lambda _e: self.sincronizar_selecao_tree(self.tree))

        self.tree_recentes = self._montar_grade_pagamentos_recentes(recentes_tab)
        self.tree_quitados = self._montar_grade_saneamento(quitados_tab)
        self.tree_bloqueados = self._montar_grade_saneamento(bloqueados_tab)

        tabela_footer = tk.Frame(tabela, bg=self.ui_panel)
        tabela_footer.pack(side="bottom", fill="x", pady=(8, 0))
        self._label(tabela_footer, "Legenda (parcelas em atraso):", 9, "normal", self.ui_text, self.ui_panel).pack(side="left")
        self._label(tabela_footer, "  0-3 verde", 9, "normal", self.ui_text, self.ui_panel).pack(side="left", padx=(10, 0))
        self._label(tabela_footer, "  4-5 amarelo", 9, "normal", self.ui_text, self.ui_panel).pack(side="left", padx=(14, 0))
        self._label(tabela_footer, "  6+ vermelho", 9, "normal", self.ui_text, self.ui_panel).pack(side="left", padx=(14, 0))
        self.paginacao_var = tk.StringVar(value="Exibindo 0 de 0 clientes")
        tk.Label(tabela_footer, textvariable=self.paginacao_var, bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9)).pack(side="right")



        inferior = ttk.PanedWindow(clientes_paned, orient="horizontal")
        self.inferior_paned = inferior

        logs_frame = self._panel(inferior, padx=14, pady=10)
        resumo_frame = self._panel(inferior, padx=14, pady=10)
        self.logs_frame = logs_frame
        self.resumo_frame = resumo_frame
        inferior.add(logs_frame, weight=3)
        inferior.add(resumo_frame, weight=3)

        logs_header = tk.Frame(logs_frame.inner, bg=self.ui_panel)
        logs_header.pack(fill="x")
        self._label(logs_header, "Log de execucao", 11, "bold", self.ui_text, self.ui_panel).pack(side="left")
        ttk.Button(logs_header, text="Limpar log", style="Toolbar.TButton", command=self._limpar_logs).pack(side="right")
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

        banco_panel = self._panel(banco_tab, padx=16, pady=14)
        banco_panel.pack(fill="both", expand=True, padx=8, pady=8)
        banco_inner = banco_panel.inner
        self._label(banco_inner, "Banco de dados", 14, "bold", self.ui_text, self.ui_panel).pack(anchor="w")
        try:
            from app import paths
            banco_path_text = str(paths.get_visual_database_path())
        except Exception:
            banco_path_text = "BANCO_DADOS_WIDEAPP_EXTRA.xlsx"
        self.banco_path_var = tk.StringVar(value=banco_path_text)
        tk.Label(banco_inner, textvariable=self.banco_path_var, bg=self.ui_panel, fg=self.ui_muted, font=("Consolas", 9), anchor="w").pack(fill="x", pady=(8, 12))
        ttk.Button(banco_inner, text="Visualizar banco de dados", style="Info.Toolbar.TButton", command=self.visualizar_banco_dados).pack(anchor="w", ipady=5)

        logs_tab_panel = self._panel(logs_tab, padx=14, pady=10)
        logs_tab_panel.pack(fill="both", expand=True, padx=8, pady=8)
        logs_tab_header = tk.Frame(logs_tab_panel.inner, bg=self.ui_panel)
        logs_tab_header.pack(fill="x")
        self._label(logs_tab_header, "Logs", 13, "bold", self.ui_text, self.ui_panel).pack(side="left")
        ttk.Button(logs_tab_header, text="Limpar log", style="Toolbar.TButton", command=self._limpar_logs).pack(side="right")
        logs_tab_scroll = ttk.Scrollbar(logs_tab_panel.inner, orient="vertical")
        logs_tab_scroll.pack(side="right", fill="y", pady=(8, 0))
        self.logs_tab_text = tk.Text(logs_tab_panel.inner, height=12, wrap="word", bg="#101B21", fg=self.ui_text, insertbackground=self.ui_text, selectbackground="#0B7F45", selectforeground="#FFFFFF", font=("Consolas", 9), bd=0, yscrollcommand=logs_tab_scroll.set)
        self.logs_tab_text.pack(fill="both", expand=True, pady=(8, 0))
        logs_tab_scroll.config(command=self.logs_tab_text.yview)

        resumo_tab_panel = self._panel(resumo_tab, padx=14, pady=10)
        resumo_tab_panel.pack(fill="both", expand=True, padx=8, pady=8)
        resumo_tab_header = tk.Frame(resumo_tab_panel.inner, bg=self.ui_panel)
        resumo_tab_header.pack(fill="x")
        self._label(resumo_tab_header, "Resumo e status", 13, "bold", self.ui_text, self.ui_panel).pack(side="left")
        tk.Label(resumo_tab_header, textvariable=self.resumo_atualizado_var, bg=self.ui_panel, fg=self.ui_muted, font=("Segoe UI", 9)).pack(side="right")
        cards_tab = tk.Frame(resumo_tab_panel.inner, bg=self.ui_panel)
        cards_tab.pack(fill="x", pady=(10, 0))
        self._criar_card_resumo(cards_tab, self.metric_total_var, "Clientes ativos", self.ui_green).pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._criar_card_resumo(cards_tab, self.metric_atraso_var, "Em atraso", self.ui_red).pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._criar_card_resumo(cards_tab, self.metric_critico_var, "Atraso critico", self.ui_yellow).pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._criar_card_resumo(cards_tab, self.metric_atualizados_var, "Atualizados hoje", self.ui_blue).pack(side="left", fill="both", expand=True)
        self.links_tab_text = tk.Text(resumo_tab_panel.inner, height=8, wrap="word", bg="#101B21", fg=self.ui_text, insertbackground=self.ui_text, selectbackground="#0B7F45", selectforeground="#FFFFFF", font=("Consolas", 9), bd=0)
        self.links_tab_text.pack(fill="both", expand=True, pady=(12, 0))

        auditoria_panel = self._panel(auditoria_tab, padx=16, pady=14)
        auditoria_panel.pack(fill="both", expand=True, padx=8, pady=8)
        self._label(auditoria_panel.inner, "Auditoria Financeira e de Conformidade", 14, "bold", self.ui_text, self.ui_panel).pack(anchor="w")
        
        auditoria_scroll = ttk.Scrollbar(auditoria_panel.inner, orient="vertical")
        auditoria_scroll.pack(side="right", fill="y", pady=(10, 0))
        
        self.auditoria_txt = tk.Text(
            auditoria_panel.inner,
            height=12,
            wrap="word",
            bg="#101B21",
            fg=self.ui_text,
            insertbackground=self.ui_text,
            selectbackground="#0B7F45",
            selectforeground="#FFFFFF",
            font=("Consolas", 9),
            bd=0,
            yscrollcommand=auditoria_scroll.set
        )
        self.auditoria_txt.pack(fill="both", expand=True, pady=(10, 0))
        auditoria_scroll.config(command=self.auditoria_txt.yview)
        self.atualizar_aba_auditoria()

        clientes_paned.add(tabela_panel, weight=5)
        clientes_paned.add(inferior, weight=2)

        statusbar = tk.Frame(self.root, bg="#0B151A")
        statusbar.pack(fill="x", side="bottom")
        self._label(statusbar, "Usuario: administrador", 8, "normal", self.ui_muted, "#0B151A").pack(side="left", padx=22, pady=7)
        self.status_version_label = tk.Label(
            statusbar,
            textvariable=self.app_version_var,
            bg="#0B151A",
            fg=self.ui_muted,
            font=("Segoe UI", 8),
        )
        self.status_version_label.pack(side="left", padx=(20, 0), pady=7)
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

    def _montar_grade_saneamento(self, parent):
        panel = self._panel(parent, padx=14, pady=10)
        panel.pack(fill="both", expand=True, padx=8, pady=8)
        tabela = panel.inner
        tree = ttk.Treeview(
            tabela,
            columns=[c[0] for c in COLUNAS],
            show="tree headings",
            selectmode="extended",
            style="Modern.Treeview",
        )
        tree["displaycolumns"] = getattr(self, "display_cols", [c[0] for c in COLUNAS if c[0] != "observacoes"])
        tree.heading("#0", text="STATUS")
        tree.column("#0", width=86, minwidth=72, anchor="center", stretch=False)
        for key, label, width in COLUNAS:
            tree.heading(key, text=label)
            anchor = "w" if key == "cliente" else "center"
            tree.column(key, width=width, anchor=anchor, stretch=True)
        scroll_y = ttk.Scrollbar(tabela, orient="vertical", command=tree.yview)
        scroll_y.pack(side="right", fill="y")
        tree.pack(side="top", fill="both", expand=True)
        tree.configure(yscrollcommand=scroll_y.set)
        tree.bind("<Button-3>", self.mostrar_menu_contexto)
        tree.bind("<<TreeviewSelect>>", lambda _e, current_tree=tree: self.sincronizar_selecao_tree(current_tree))
        footer = tk.Frame(tabela, bg=self.ui_panel)
        footer.pack(side="bottom", fill="x", pady=(8, 0))
        tk.Label(
            footer,
            text="Lista separada pela camada persistente de saneamento manual",
            bg=self.ui_panel,
            fg=self.ui_muted,
            font=("Segoe UI", 9),
        ).pack(side="left")
        return tree

    def _colunas_pagamentos_recentes(self):
        return indexador_clientes.janela_pagamentos_recentes()

    def _montar_grade_pagamentos_recentes(self, parent):
        panel = self._panel(parent, padx=14, pady=10)
        panel.pack(fill="both", expand=True, padx=8, pady=8)
        tabela = panel.inner
        colunas_mes = [mes["chave"] for mes in self._colunas_pagamentos_recentes()]
        tree = ttk.Treeview(
            tabela,
            columns=[c[0] for c in COLUNAS] + colunas_mes,
            show="tree headings",
            selectmode="extended",
            style="Modern.Treeview",
        )
        tree["displaycolumns"] = list(getattr(self, "display_cols", [c[0] for c in COLUNAS if c[0] != "observacoes"])) + colunas_mes
        tree.heading("#0", text="STATUS")
        tree.column("#0", width=86, minwidth=72, anchor="center", stretch=False)
        for key, label, width in COLUNAS:
            tree.heading(key, text=label)
            anchor = "w" if key == "cliente" else "center"
            tree.column(key, width=width, anchor=anchor, stretch=True)
        for mes in self._colunas_pagamentos_recentes():
            tree.heading(mes["chave"], text=mes["rotulo"])
            tree.column(mes["chave"], width=90, minwidth=76, anchor="center", stretch=False)
        scroll_y = ttk.Scrollbar(tabela, orient="vertical", command=tree.yview)
        scroll_y.pack(side="right", fill="y")
        tree.pack(side="top", fill="both", expand=True)
        tree.configure(yscrollcommand=scroll_y.set)
        tree.bind("<Button-3>", self.mostrar_menu_contexto)
        tree.bind("<Double-1>", lambda _e: self.abrir_pasta_cliente_selecionado())
        tree.bind("<MouseWheel>", self._rolar_tree)
        tree.bind("<<TreeviewSelect>>", lambda _e, current_tree=tree: self.sincronizar_selecao_tree(current_tree))
        return tree

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
        
        # Logs de diagnóstico obrigatórios para banco XLSX portátil
        from app import paths
        self.log(f"Pasta raiz do app: {paths.get_app_root()}")
        self.log(f"Banco visual XLSX: {paths.get_visual_database_path()}")
        self.log(f"Cache interno WidePay: {config.WIDEPAY_BOLETOS_CACHE_JSON}")

    def limpar_filtros(self):
        self.busca_var.set("")
        self.status_var.set("Todos")
        if hasattr(self, "quadra_lote_var"):
            self.quadra_lote_var.set("Todos")
        self.aplicar_filtro()

    def _limpar_logs(self):
        for widget_name in ("logs", "logs_tab_text"):
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.delete("1.0", "end")

    def _limpar_links_status(self):
        for widget_name in ("links", "links_tab_text"):
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.delete("1.0", "end")

    def _append_links_status(self, texto):
        for widget_name in ("links", "links_tab_text"):
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.insert("end", texto)
                widget.see("end")

    def log(self, msg):
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, lambda m=msg: self.log(m))
            return
        for widget_name in ("logs", "logs_tab_text"):
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.insert("end", msg + "\n")
                widget.see("end")
        self.root.update_idletasks()

    def _append_progress_log(self, linha):
        if not hasattr(self, "progress_mini_log"):
            return
        self.progress_mini_log.configure(state="normal")
        linhas = [x for x in self.progress_mini_log.get("1.0", "end").splitlines() if x.strip()]
        linhas.append(linha)
        linhas = linhas[-3:]
        self.progress_mini_log.delete("1.0", "end")
        self.progress_mini_log.insert("end", "\n".join(linhas) + ("\n" if linhas else ""))
        self.progress_mini_log.configure(state="disabled")

    def _recarregar_dados_apos_atualizacao(self):
        self.registros = indexador_clientes.carregar_cache()
        if hasattr(self, "quadra_lote_combo"):
            opcoes = self._opcoes_quadra_lote()
            atual = self.quadra_lote_var.get()
            self.quadra_lote_combo.configure(values=opcoes)
            if atual not in opcoes:
                self.quadra_lote_var.set("Todos")
        self.aplicar_filtro()
        self.atualizar_combo_xlsx()

    def atualizar_async(self):
        self.btn_atualizar_cli.configure(state="disabled")
        self.btn_atualizar_wp.configure(state="disabled")
        self.btn_gerar_sel.configure(state="disabled")
        self.btn_gerar_todos.configure(state="disabled")
        self.btn_abrir_xlsx.configure(state="disabled")
        self.btn_visualizar_db.configure(state="disabled")
        
        self.progress_status_var.set("Atualizando clientes")
        self.progress_etapa_var.set("Preparando atualização...")
        self.progress_pct_var.set("0%")
        self.progress_reg_var.set("0")
        self.progress_cli_var.set("0")
        self.progress["value"] = 0
        self.progress_label.configure(text="Preparando atualização...")
        
        # Habilitar e limpar mini log
        self.progress_mini_log.configure(state="normal")
        self.progress_mini_log.delete("1.0", "end")
        self.progress_mini_log.configure(state="disabled")
        self._append_progress_log("[0%] Iniciando atualização...")
        
        self.log("Atualizacao incremental de clientes iniciada...")
        threading.Thread(target=self._atualizar, daemon=True).start()

    def _atualizar(self):
        def progress_ui_callback(etapa, percentual, mensagem, detalhes=None):
            def _update():
                self.progress["value"] = percentual
                self.progress_pct_var.set(f"{percentual}%")
                self.progress_etapa_var.set(mensagem)
                self.progress_label.configure(text=mensagem)
                
                # Extrair registros coletados
                import re
                match_reg = re.search(r"coletados:\s*(\d+)", mensagem)
                if match_reg:
                    self.progress_reg_var.set(match_reg.group(1))
                
                # Extrair total de clientes
                match_idx = re.search(r"(\d+)\s+registros indexados", mensagem)
                if match_idx:
                    self.progress_cli_var.set(match_idx.group(1))
                elif percentual == 100:
                    self.progress_cli_var.set(str(len(self.registros)))
                
                self._append_progress_log(f"[{percentual}%] {mensagem}")
                
                self.log(f"[{percentual}%] {mensagem}")
            self.root.after(0, _update)

        try:
            result = indexador_clientes.indexar_clientes(
                validar_widepay=True,
                log_callback=self.log,
                progress_callback=progress_ui_callback
            )
            def _success_msg():
                self._recarregar_dados_apos_atualizacao()
                self.progress_status_var.set("Pronto")
                self.progress_etapa_var.set("Atualização concluída com sucesso — 100%")
                self.progress_label.configure(text="Atualização concluída com sucesso — 100%")
                self.progress_pct_var.set("100%")
                self.progress["value"] = 100
                self.progress_cli_var.set(str(len(self.registros)))
                self._append_progress_log(f"[100%] Banco e tabela atualizados com {len(self.registros)} registros.")
                self.log(f"Clientes/lotes atualizados incrementalmente: {len(self.registros)}")
                messagebox.showinfo(
                    "WideAPP_EXTRA",
                    f"Atualização concluída com sucesso!\n{len(self.registros)} clientes/lotes indexados."
                )
            self.root.after(0, _success_msg)
        except Exception as e:
            self.log(f"Erro durante atualização: {e}")
            
            def _error_msg():
                self.progress_status_var.set("Pronto")
                self.progress_etapa_var.set("Atualização falhou — veja o log")
                self.progress_label.configure(text="Atualização falhou — veja o log")
                self._append_progress_log("[erro] Atualização falhou; dados anteriores preservados.")
                messagebox.showerror(
                    "WideAPP_EXTRA",
                    f"Erro durante atualização de clientes:\n{e}\n\nOs dados anteriores foram preservados."
                )
            self.root.after(0, _error_msg)
        finally:
            def _restore_buttons():
                self.btn_atualizar_cli.configure(state="normal")
                self.btn_atualizar_wp.configure(state="normal")
                self.btn_gerar_sel.configure(state="normal")
                self.btn_gerar_todos.configure(state="normal")
                self.btn_abrir_xlsx.configure(state="normal")
                self.btn_visualizar_db.configure(state="normal")
            self.root.after(0, _restore_buttons)

    def on_tree_press(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "heading":
            col_id = self.tree.identify_column(event.x)
            self._drag_col = col_id
            self._drag_start_x = event.x
            self._drag_start_time = time.time()
            self._dragged = False
        else:
            self._drag_col = None

    def on_tree_motion(self, event):
        if hasattr(self, "_drag_col") and self._drag_col:
            if abs(event.x - self._drag_start_x) > 12:
                self._dragged = True

    def on_tree_release(self, event):
        if hasattr(self, "_drag_col") and self._drag_col:
            region = self.tree.identify_region(event.x, event.y)
            if getattr(self, "_dragged", False):
                if region == "heading":
                    dst_col = self.tree.identify_column(event.x)
                    if dst_col and dst_col != self._drag_col:
                        self.reordenar_colunas(self._drag_col, dst_col)
            else:
                elapsed = time.time() - self._drag_start_time
                if elapsed < 0.5:
                    col_id = self._drag_col
                    if col_id == "#0":
                        self.ordenar_por_coluna("#0")
                    else:
                        try:
                            visual_idx = int(col_id.replace("#", "")) - 1
                            display_cols = list(self.tree["displaycolumns"])
                            if not display_cols or display_cols == ["#all"]:
                                display_cols = [c[0] for c in COLUNAS if c[0] != "observacoes"]
                            if 0 <= visual_idx < len(display_cols):
                                col_name = display_cols[visual_idx]
                                self.ordenar_por_coluna(col_name)
                        except ValueError:
                            pass
            self._drag_col = None
        self.sincronizar_selecao_tree()

    def reordenar_colunas(self, src_visual, dst_visual):
        if src_visual == "#0" or dst_visual == "#0":
            return
            
        try:
            src_idx = int(src_visual.replace("#", "")) - 1
            dst_idx = int(dst_visual.replace("#", "")) - 1
        except ValueError:
            return
            
        display_cols = list(self.tree["displaycolumns"])
        if not display_cols or display_cols == ["#all"]:
            display_cols = [c[0] for c in COLUNAS if c[0] != "observacoes"]
            
        if 0 <= src_idx < len(display_cols) and 0 <= dst_idx < len(display_cols):
            col_name = display_cols.pop(src_idx)
            display_cols.insert(dst_idx, col_name)
            self.tree["displaycolumns"] = display_cols
            
            try:
                import json
                config_path = config.DATA_DIR / "colunas_config.json"
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(display_cols, f, indent=4, ensure_ascii=False)
            except Exception:
                pass
            
            self.log(f"Coluna '{col_name}' reordenada para visual index {dst_idx+1}.")

    def atualizar_aba_auditoria(self):
        if not hasattr(self, "auditoria_txt"):
            return
            
        self.auditoria_txt.configure(state="normal")
        self.auditoria_txt.delete("1.0", "end")
        
        self.auditoria_txt.insert("end", "=== PAINEL DE AUDITORIA E CONFORMIDADE FINANCEIRA ===\n\n")
        
        total_clientes = len(self.registros)
        ativos = [r for r in self.registros if r.get("saneamento_categoria", "ativos") == "ativos"]
        quitados = [r for r in self.registros if r.get("saneamento_categoria") == "quitados"]
        bloqueados = [r for r in self.registros if r.get("saneamento_categoria") == "bloqueados_removidos"]
        atencao = [r for r in self.registros if r.get("saneamento_acao") == "atencao"]
        ignorados = [r for r in self.registros if r.get("saneamento_acao") == "ignorar"]
        fora_roster = [r for r in self.registros if r.get("saneamento_categoria") == "fora_roster"]
        com_divergencia = [r for r in ativos if r.get("divergencias")]
        sem_contrato = [r for r in ativos if r.get("contrato") != "Encontrado"]
        pendentes_wp = [r for r in ativos if r.get("situacao_final") == "Pendente validacao WidePay" or "Pendente" in str(r.get("situacao_final"))]
        erros = [r for r in ativos if r.get("situacao_final") == "ERRO" or r.get("status_atraso_qtd") == -1]
        
        self.auditoria_txt.insert("end", f"Total de Clientes na Base: {total_clientes}\n")
        self.auditoria_txt.insert("end", f"Ativos exibidos na lista principal: {len(ativos)}\n")
        self.auditoria_txt.insert("end", f"Quitados separados: {len(quitados)}\n")
        self.auditoria_txt.insert("end", f"Bloqueados/Removidos separados: {len(bloqueados)}\n")
        self.auditoria_txt.insert("end", f"Ignorados/placeholders: {len(ignorados)}\n")
        self.auditoria_txt.insert("end", f"Fora do roster da planilha: {len(fora_roster)}\n")
        self.auditoria_txt.insert("end", f"Amarelos/atencao: {len(atencao)}\n")
        self.auditoria_txt.insert("end", f"Clientes Conciliados com Sucesso: {total_clientes - len(com_divergencia)}\n")
        self.auditoria_txt.insert("end", f"Clientes com Divergências Ativas: {len(com_divergencia)}\n")
        self.auditoria_txt.insert("end", f"Clientes sem Contrato Físico Confirmado: {len(sem_contrato)}\n")
        self.auditoria_txt.insert("end", f"Pendentes de Validação no WidePay: {len(pendentes_wp)}\n")
        self.auditoria_txt.insert("end", f"Erros ou Falhas Críticas: {len(erros)}\n\n")
        
        self.auditoria_txt.insert("end", "--- DETALHES DAS DIVERGÊNCIAS ATIVAS ---\n")
        if not com_divergencia:
            self.auditoria_txt.insert("end", "Nenhuma divergência financeira/matemática detectada na base atual.\n")
        else:
            for idx, r in enumerate(com_divergencia, 1):
                cliente = r.get("cliente", "Desconhecido")
                lote = r.get("lote", "-")
                quadra = r.get("quadra", "-")
                divs = r.get("divergencias", "")
                self.auditoria_txt.insert("end", f"{idx}. {cliente} (Lote: {lote} / Qd: {quadra}):\n   -> {divs}\n")
                
        self.auditoria_txt.insert("end", "\n--- PENDÊNCIAS DE CONTRATOS FÍSICOS ---\n")
        if not sem_contrato:
            self.auditoria_txt.insert("end", "Todos os clientes ativos possuem contratos confirmados.\n")
        else:
            for idx, r in enumerate(sem_contrato, 1):
                cliente = r.get("cliente", "Desconhecido")
                lote = r.get("lote", "-")
                self.auditoria_txt.insert("end", f"{idx}. {cliente} (Lote: {lote}) - Contrato Físico Faltando ou Não Confirmado\n")
                
        self.auditoria_txt.insert("end", "\n--- CLIENTES COM ERROS OU INCONSISTÊNCIAS WIDEPAY ---\n")
        if not erros:
            self.auditoria_txt.insert("end", "Nenhum erro de processamento cadastral detectada no WidePay.\n")
        else:
            for idx, r in enumerate(erros, 1):
                cliente = r.get("cliente", "Desconhecido")
                sit = r.get("situacao_final", "ERRO")
                self.auditoria_txt.insert("end", f"{idx}. {cliente} - Situação: {sit}\n")

        movimentos = saneamento_clientes.carregar_saneamento().get("auditoria_manual", [])
        self.auditoria_txt.insert("end", "\n--- MOVIMENTACOES MANUAIS RECENTES ---\n")
        if not movimentos:
            self.auditoria_txt.insert("end", "Nenhuma movimentacao manual registrada.\n")
        else:
            for idx, mov in enumerate(movimentos[-15:], 1):
                linha = (
                    f"{idx}. {mov.get('data_hora')} | {mov.get('cliente')} | "
                    f"{mov.get('aba_origem')} -> {mov.get('aba_destino')} | "
                    f"{mov.get('status_anterior')} -> {mov.get('status_novo')}\n"
                )
                self.auditoria_txt.insert("end", linha)
        self.auditoria_txt.configure(state="disabled")

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

    def ordenar_por_coluna(self, col_key):
        if self.sort_column == col_key:
            self.sort_descending = not self.sort_descending
        else:
            self.sort_column = col_key
            self.sort_descending = False
        self.aplicar_filtro()

    def _filtrar_registros_visuais(self, registros):
        filtrados = pesquisa_clientes.filtrar(registros, self.busca_var.get(), self.status_var.get())
        quadra_lote = self.quadra_lote_var.get() if hasattr(self, "quadra_lote_var") else "Todos"
        if quadra_lote and quadra_lote != "Todos":
            alvo = quadra_lote.strip().upper()
            filtrados = [
                item for item in filtrados
                if str(item.get("quadra") or "").strip().upper() == alvo
                or str(item.get("lote") or "").strip().upper() == alvo
                or str(item.get("chave_lote_canonica") or "").strip().upper() == alvo
            ]
        return filtrados

    def _popular_tree_saneamento(self, tree, registros):
        if not tree:
            return
        tree.delete(*tree.get_children())
        self._tree_record_maps[str(tree)] = {}
        for idx, item in enumerate(registros):
            values = [self._valor_grade(item, key) for key, _label, _width in COLUNAS]
            vencidos = item.get("status_atraso_qtd", item.get("boletos_atrasados", 0))
            img_barrinha = self.obter_imagem_barrinha(vencidos)
            iid = f"s{idx}"
            tree.insert("", "end", iid=iid, text="", image=img_barrinha, values=values)
            self._tree_record_maps[str(tree)][iid] = item

    def _popular_tree_pagamentos_recentes(self, registros):
        tree = getattr(self, "tree_recentes", None)
        if not tree:
            return
        meses = self._colunas_pagamentos_recentes()
        colunas_mes = [mes["chave"] for mes in meses]
        tree.delete(*tree.get_children())
        self._tree_record_maps[str(tree)] = {}
        tree["displaycolumns"] = list(getattr(self, "display_cols", [c[0] for c in COLUNAS if c[0] != "observacoes"])) + colunas_mes
        for mes in meses:
            tree.heading(mes["chave"], text=mes["rotulo"])
        colunas_base = [c[0] for c in COLUNAS]
        for idx, item in enumerate(registros):
            valores_base = [self._valor_grade(item, key) for key in colunas_base]
            linha = dict(zip(colunas_base, valores_base))
            mapa = indexador_clientes.normalizar_pagamentos_recentes_5m(item.get("pagamentos_recentes_5m"))
            for mes in meses:
                linha[mes["chave"]] = mapa.get(mes["chave"], "-")
            vencidos = item.get("status_atraso_qtd", item.get("boletos_atrasados", 0))
            iid = f"r{idx}"
            tree.insert(
                "",
                "end",
                iid=iid,
                text="",
                image=self.obter_imagem_barrinha(vencidos),
                values=[linha.get(col, "") for col in tree["columns"]],
            )
            self._tree_record_maps[str(tree)][iid] = item

    def _atualizar_abas_saneamento(self):
        quitados = [r for r in self.registros if r.get("saneamento_categoria") == "quitados"]
        bloqueados = [r for r in self.registros if r.get("saneamento_categoria") == "bloqueados_removidos"]
        self._popular_tree_saneamento(getattr(self, "tree_quitados", None), self._filtrar_registros_visuais(quitados))
        self._popular_tree_saneamento(getattr(self, "tree_bloqueados", None), self._filtrar_registros_visuais(bloqueados))

    def aplicar_filtro(self):
        ativos = [r for r in self.registros if r.get("saneamento_categoria", "ativos") == "ativos"]
        self.filtrados = self._filtrar_registros_visuais(ativos)

        # Aplicar ordenação baseada na coluna ativa
        if self.sort_column:
            def get_sort_key(item):
                col = self.sort_column
                if col == "#0":
                    try:
                        return int(float(item.get("status_atraso_qtd", item.get("boletos_atrasados", 0))))
                    except (ValueError, TypeError):
                        return 0
                elif col == "cliente":
                    val = item.get("cliente") or ""
                    return indexador_clientes.limpar_nome_cliente(str(val)).lower()
                elif col == "lote":
                    lote_can = item.get("chave_lote_canonica") or indexador_clientes.chave_lote_canonica(item) or ""
                    import re
                    match = re.match(r"^([a-zA-Z]+)?(\d+)?", lote_can)
                    if match:
                        alpha = match.group(1) or ""
                        num = int(match.group(2)) if match.group(2) else 0
                        return (alpha.upper(), num)
                    return ("", 0)
                elif col == "contrato_resumo":
                    return indexador_clientes.deduzir_resumo_contrato(item).lower()
                elif col == "parcelas_resumo":
                    res = indexador_clientes.deduzir_resumo_parcelas(item)
                    import re
                    match = re.search(r"(\d+)\s*/\s*(\d+)", res)
                    if match:
                        pago = int(match.group(1))
                        total = int(match.group(2))
                        pct = pago / total if total > 0 else 0
                        return (pct, pago, total)
                    return (0, 0, 0)
                elif col == "situacao_final":
                    val = item.get("situacao_final") or indexador_clientes.deduzir_situacao_final(item) or ""
                    return val.lower()
                elif col == "ultima_atualizacao_widepay":
                    val = item.get("ultima_atualizacao_widepay") or item.get("data_atualizacao") or ""
                    return val
                elif col in ("valor_total_contratado", "valor_total_pago"):
                    val = item.get(col)
                    try:
                        return float(val) if val is not None else 0.0
                    except (ValueError, TypeError):
                        return 0.0
                return ""

            self.filtrados.sort(key=get_sort_key, reverse=self.sort_descending)

        # Atualizar cabeçalhos com indicadores de ordenação ▲ / ▼
        indicator = " ▼" if self.sort_descending else " ▲"
        if self.sort_column == "#0":
            self.tree.heading("#0", text=f"STATUS{indicator}")
        else:
            self.tree.heading("#0", text="STATUS")
            
        for key, label, _width in COLUNAS:
            if self.sort_column == key:
                self.tree.heading(key, text=f"{label}{indicator}")
            else:
                self.tree.heading(key, text=label)

        self.tree.delete(*self.tree.get_children())
        self._tree_record_maps[str(self.tree)] = {}
        for idx, item in enumerate(self.filtrados):
            values = [self._valor_grade(item, key) for key, _label, _width in COLUNAS]
            iid = str(idx)
            
            vencidos = item.get("status_atraso_qtd", item.get("boletos_atrasados", 0))
            img_barrinha = self.obter_imagem_barrinha(vencidos)
            
            # A coluna #0 exibe apenas o ícone da barrinha na coluna STATUS.
            # O texto da coluna #0 fica vazio (""), e o nome do cliente vai no values.
            self.tree.insert("", "end", iid=iid, text="", image=img_barrinha, values=values)
            self._tree_record_maps[str(self.tree)][iid] = item
            if self._chave(item) in self.selecionados:
                self.tree.selection_add(iid)
        self._popular_tree_pagamentos_recentes(self.filtrados)
        self.atualizar_resumo_visual()
        self._atualizar_abas_saneamento()
        self.atualizar_aba_auditoria()
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

    def sincronizar_selecao_tree(self, tree=None):
        tree = tree or self.tree
        self.selecionados = set()
        registros = self._selecionados_registros_tree(tree)
        for item in registros:
            self.selecionados.add(self._chave(item))
        self.log(f"Selecionados: {len(self.selecionados)}")

    def selecionar_todos(self):
        for iid in self.tree.get_children():
            self.tree.selection_add(iid)
        self.sincronizar_selecao_tree(self.tree)

    def limpar_selecao(self):
        self.tree.selection_remove(self.tree.selection())
        self.selecionados.clear()
        self.log("Selecao limpa.")

    def _selecionados_registros_tree(self, tree=None):
        tree = tree or self.tree
        mapa = self._tree_record_maps.get(str(tree), {})
        registros = []
        for iid in tree.selection():
            item = mapa.get(str(iid))
            if item:
                registros.append(item)
        return registros

    def _selecionados_registros(self, tree=None):
        if tree is not None:
            return self._selecionados_registros_tree(tree)
        chaves = set(self.selecionados)
        return [item for item in self.registros if self._chave(item) in chaves]

    def _registro_contexto_ou_primeiro(self, tree=None):
        tree = tree or self._context_tree or self.tree
        mapa = self._tree_record_maps.get(str(tree), {})
        if self._context_iid is not None:
            item = mapa.get(str(self._context_iid))
            if item:
                return item
        registros = self._selecionados_registros_tree(tree)
        return registros[0] if registros else None

    def _rolar_tree(self, event):
        self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def _identificar_aba_tree(self, tree):
        if tree in (self.tree, getattr(self, "tree_recentes", None)):
            return "ativos"
        if tree == getattr(self, "tree_quitados", None):
            return "quitados"
        if tree == getattr(self, "tree_bloqueados", None):
            return "bloqueados_removidos"
        return "ativos"

    def _descricao_destino(self, destino):
        return {
            "ativos": "Ativos",
            "quitados": "Quitados",
            "bloqueados_removidos": "Bloqueados / Removidos",
        }.get(destino, destino)

    def _mover_registros_manual(self, tree, destino):
        origem = self._identificar_aba_tree(tree)
        registros = self._selecionados_registros_tree(tree)
        if not registros:
            messagebox.showinfo("WideAPP_EXTRA", "Nenhum cliente selecionado.")
            return
        destino_label = self._descricao_destino(destino)
        qtd = len(registros)
        if not messagebox.askyesno(
            "WideAPP_EXTRA",
            f"Deseja mover {qtd} cliente(s) para {destino_label}? Essa acao nao apagara dados e podera ser revertida depois.",
        ):
            return
        chaves = [item.get("chave_saneamento") or indexador_clientes.normalizar_registro_cache(item).get("chave_saneamento") for item in registros]
        alterados = saneamento_clientes.registrar_movimentacao_manual(self.registros, chaves, destino, origem)
        if not alterados:
            messagebox.showwarning("WideAPP_EXTRA", "Nenhum cliente selecionado conseguiu ser movido.")
            return
        try:
            indexador_clientes.salvar_cache(self.registros)
            self._recarregar_dados_apos_atualizacao()
        except Exception as exc:
            self.log(f"Erro ao salvar movimentacao manual: {exc}")
            messagebox.showerror("WideAPP_EXTRA", f"Erro ao salvar a movimentacao manual:\n{exc}")
            return
        self.log(f"Movimentacao manual aplicada: {len(alterados)} cliente(s) -> {destino_label}")
        self.atualizar_aba_auditoria()

    def _popular_menu_movimentacao(self, menu, tree):
        aba = self._identificar_aba_tree(tree)
        if aba == "ativos":
            menu.add_command(label="Mover para Quitados", command=lambda current_tree=tree: self._mover_registros_manual(current_tree, "quitados"))
            menu.add_command(label="Mover para Bloqueados / Removidos", command=lambda current_tree=tree: self._mover_registros_manual(current_tree, "bloqueados_removidos"))
        elif aba == "quitados":
            menu.add_command(label="Restaurar para Ativos", command=lambda current_tree=tree: self._mover_registros_manual(current_tree, "ativos"))
            menu.add_command(label="Mover para Bloqueados / Removidos", command=lambda current_tree=tree: self._mover_registros_manual(current_tree, "bloqueados_removidos"))
        elif aba == "bloqueados_removidos":
            menu.add_command(label="Restaurar para Ativos", command=lambda current_tree=tree: self._mover_registros_manual(current_tree, "ativos"))
            menu.add_command(label="Mover para Quitados", command=lambda current_tree=tree: self._mover_registros_manual(current_tree, "quitados"))



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
        self._limpar_links_status()
        for item in resultado["drive"]:
            self._append_links_status(f"{item.get('cliente')} {item.get('lote')}: {item.get('status')} {item.get('link')}\n")
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
            self._append_links_status(f"Destino Drive remoto: {destino}\n")

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
        tree = event.widget if isinstance(event.widget, ttk.Treeview) else self.tree
        row_id = tree.identify_row(event.y)
        if row_id:
            self._context_iid = row_id
            self._context_tree = tree
            if row_id not in tree.selection():
                tree.selection_set(row_id)
            self.sincronizar_selecao_tree(tree)
            
            menu = tk.Menu(self.root, tearoff=0, bg="#242424", fg="#F3F3F3", activebackground="#007A3E", activeforeground="#F3F3F3")
            self._popular_menu_movimentacao(menu, tree)
            if tree in (self.tree, getattr(self, "tree_recentes", None)):
                menu.add_separator()
                menu.add_command(label="Gerar relatorio do(s) selecionado(s)", command=self.gerar_selecionados)
                menu.add_command(label="Abrir pasta do cliente no Explorer", command=self.abrir_pasta_cliente_selecionado)
                menu.add_command(label="Abrir planilha recente do cliente", command=self.abrir_planilha_cliente_selecionado)
                menu.add_separator()
                menu.add_command(label="Atualizar clientes", command=self.atualizar_async)
                menu.add_command(label="Atualizar informacoes da WidePay (selecionados)", command=self.atualizar_widepay_selecionados_async)
            
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

    def visualizar_banco_dados(self):
        from app import paths
        from app.abridor_arquivos import abrir
        path = paths.get_visual_database_path()
        if not path.exists():
            messagebox.showwarning(
                "WideAPP_EXTRA",
                "Banco de dados ainda não foi gerado. Clique em Atualizar clientes primeiro."
            )
            return
        
        self.log(f"SKILL CARREGADA: widepay-abertura-externa")
        self.log(f"EXECUÇÃO EXTERNA: abrindo banco de dados visual: {path.name}")
        try:
            abrir(path)
            self.log(f"VISUALIZADOR PADRÃO: banco de dados visual aberto com sucesso.")
        except Exception as exc:
            self.log(f"Erro ao abrir banco de dados visual: {exc}")
            messagebox.showerror("WideAPP_EXTRA", f"Erro ao abrir o banco de dados visual:\n{exc}")

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
    
    # 1. Base components
    assert hasattr(app, "tree")
    assert root.minsize()[0] >= 1280
    assert root.minsize()[1] >= 760
    assert root.title() == APP_WINDOW_TITLE
    assert app.btn_visualizar_db.cget("text") == "Visualizar banco de dados"
    assert app.btn_visualizar_db.cget("style") == "Info.Toolbar.TButton"
    assert app.app_version_var.get() == APP_VERSION_LABEL
    assert hasattr(app, "version_badge")
    assert APP_VERSION in app.app_version_var.get()
    
    # 2. Absence of legacy sidebar and navigation buttons
    assert not hasattr(app, "sidebar_panel")
    assert not hasattr(app, "nav_buttons")
    
    # 3. Absence of horizontal scrollbar
    assert not hasattr(app, "scroll_x")
    
    # 4. Displaycolumns visually hiding observacoes
    display_cols = list(app.tree["displaycolumns"])
    assert "observacoes" not in display_cols
    
    # 5. Core drag-and-drop / click handlers exist
    assert hasattr(app, "on_tree_press")
    assert hasattr(app, "on_tree_motion")
    assert hasattr(app, "on_tree_release")
    
    # 6. Verify import time is functional
    assert time.time() > 0
    
    # 7. Verification of progress and visual components
    assert hasattr(app, "progress_panel")
    assert app.progress_panel.master is app.header_status_box
    assert hasattr(app, "toolbar_panel")
    assert app.toolbar_panel.master is app.title_box
    assert int(app.progress_mini_log.cget("height")) in (2, 3)
    assert hasattr(app, "workspace_tabs")
    assert len(app.workspace_tabs.tabs()) >= 5
    assert app.workspace_tabs.tab(app.workspace_tabs.tabs()[1], "text") == "Pagamentos Recentes"
    assert hasattr(app, "tree_recentes")
    recentes_cols = [col for col in app.tree_recentes["columns"] if col not in [c[0] for c in COLUNAS]]
    assert len(recentes_cols) == 5
    assert app.status_version_label.cget("textvariable")
    assert hasattr(app, "logo_photo")
    assert hasattr(app, "auditoria_txt")
    assert "PAINEL DE AUDITORIA" in app.auditoria_txt.get("1.0", "end")
    assert hasattr(app, "clientes_paned")
    assert hasattr(app, "inferior_paned")
    
    root.destroy()
    return len(registros)
