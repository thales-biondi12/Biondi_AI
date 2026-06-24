import customtkinter as ctk
from Modules.calculadora import Calculadora


# ── Paleta de cores (compatível com o tema dark/light do app) ────────────
_COR_DISPLAY_BG  = ("gray92", "gray10")
_COR_NUM         = ("gray82", "gray22")   # botões numéricos
_COR_NUM_HOVER   = ("gray72", "gray32")
_COR_OP          = ("gray75", "gray18")   # operadores secundários (CE, C, ⌫, %)
_COR_OP_HOVER    = ("gray65", "gray28")
_COR_OP_PRINCIPAL = ("#3a7ebf", "#1f6aa5") # azul do tema — operadores + / − × ÷
_COR_OP_PRINCIPAL_HOVER = ("#2d6ea8", "#185d94")
_COR_IGUAL       = ("#1f6aa5", "#3a7ebf")  # azul mais vibrante para =
_COR_IGUAL_HOVER = ("#185d94", "#2d6ea8")

_FONTE_DISPLAY   = ("Arial", 36, "bold")
_FONTE_EXPR      = ("Arial", 12)
_FONTE_BTN       = ("Arial", 16)
_FONTE_BTN_SM    = ("Arial", 13)


class CalculadoraView(ctk.CTkFrame):
    """Calculadora estilo Windows com o tema do app."""

    # Layout: (texto, chave_interna, estilo, colspan)
    # estilo: "num" | "op" | "op_sec" | "igual"
    _BOTOES = [
        # linha 1
        [("%",  "pct",  "op_sec", 1), ("CE", "ce",  "op_sec", 1),
         ("C",  "c",    "op_sec", 1), ("⌫",  "bs",  "op_sec", 1)],
        # linha 2
        [("⅟x", "inv",  "op_sec", 1), ("x²", "sqr", "op_sec", 1),
         ("√x", "sqrt", "op_sec", 1), ("÷",  "÷",   "op_pri", 1)],
        # linha 3
        [("7",  "7",   "num", 1), ("8", "8", "num", 1),
         ("9",  "9",   "num", 1), ("×", "×", "op_pri", 1)],
        # linha 4
        [("4",  "4",   "num", 1), ("5", "5", "num", 1),
         ("6",  "6",   "num", 1), ("−", "−", "op_pri", 1)],
        # linha 5
        [("1",  "1",   "num", 1), ("2", "2", "num", 1),
         ("3",  "3",   "num", 1), ("+", "+", "op_pri", 1)],
        # linha 6
        [("+/−", "neg", "num", 1), ("0", "0", "num", 1),
         (",",  ".",   "num", 1), ("=", "=", "igual", 1)],
    ]

    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._calc = Calculadora()
        self._construir()

    # ------------------------------------------------------------------ #
    def _construir(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Cartão central — limita largura como a calculadora do Windows
        cartao = ctk.CTkFrame(self, corner_radius=12,
                              fg_color=("gray88", "gray14"))
        cartao.place(relx=0.5, rely=0.5, anchor="center")

        for c in range(4):
            cartao.grid_columnconfigure(c, weight=1, minsize=72)

        # ── Display ──────────────────────────────────────────────────────
        display_frame = ctk.CTkFrame(cartao, corner_radius=8,
                                     fg_color=_COR_DISPLAY_BG)
        display_frame.grid(row=0, column=0, columnspan=4,
                           padx=12, pady=(16, 8), sticky="ew")

        # Expressão (linha superior pequena)
        self._lbl_expr = ctk.CTkLabel(
            display_frame, text="",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color=("gray50", "gray55"),
            anchor="e",
        )
        self._lbl_expr.pack(fill="x", padx=12, pady=(6, 0))

        # Valor principal
        self._lbl_valor = ctk.CTkLabel(
            display_frame, text="0",
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            anchor="e",
        )
        self._lbl_valor.pack(fill="x", padx=12, pady=(0, 10))

        # ── Botões ────────────────────────────────────────────────────────
        for r_idx, linha in enumerate(self._BOTOES, start=1):
            for c_idx, (texto, chave, estilo, span) in enumerate(linha):
                self._criar_botao(cartao, texto, chave, estilo,
                                  r_idx, c_idx, span)

        # Padding externo
        for widget in cartao.winfo_children():
            pass  # grid já tem padx/pady

    # ------------------------------------------------------------------ #
    def _criar_botao(self, parent, texto, chave, estilo, row, col, span):
        cores = {
            "num":    (_COR_NUM,          _COR_NUM_HOVER),
            "op_sec": (_COR_OP,           _COR_OP_HOVER),
            "op_pri": (_COR_OP_PRINCIPAL, _COR_OP_PRINCIPAL_HOVER),
            "igual":  (_COR_IGUAL,        _COR_IGUAL_HOVER),
        }
        fg, hover = cores.get(estilo, (_COR_NUM, _COR_NUM_HOVER))
        fonte_tamanho = 13 if len(texto) > 2 else 16

        btn = ctk.CTkButton(
            parent,
            text=texto,
            width=68,
            height=56,
            corner_radius=6,
            fg_color=fg,
            hover_color=hover,
            text_color=("gray10", "gray95"),
            font=ctk.CTkFont(family="Arial", size=fonte_tamanho),
            command=lambda c=chave: self._pressionar(c),
        )
        btn.grid(row=row, column=col, columnspan=span,
                 padx=4, pady=4, sticky="nsew")

    # ------------------------------------------------------------------ #
    def _pressionar(self, chave: str):
        calc = self._calc

        if chave in "0123456789":
            calc.digito(chave)
        elif chave == ".":
            calc.digito(".")
        elif chave in ("+", "−", "×", "÷"):
            calc.operador(chave)
            self._lbl_expr.configure(
                text=f"{calc._valor_anterior} {chave}"
            )
        elif chave == "=":
            expr = ""
            if calc._valor_anterior is not None and calc._operador:
                expr = f"{calc._valor_anterior} {calc._operador} {calc._valor_atual} ="
            calc.igual()
            self._lbl_expr.configure(text=expr)
        elif chave == "pct":
            calc.porcentagem()
        elif chave == "neg":
            calc.inverter_sinal()
        elif chave == "bs":
            calc.backspace()
        elif chave == "ce":
            calc.limpar_entrada()
        elif chave == "c":
            calc.limpar()
            self._lbl_expr.configure(text="")
        elif chave == "inv":
            try:
                v = float(calc.display)
                if v == 0:
                    calc._valor_atual = "Erro"
                else:
                    r = 1 / v
                    calc._valor_atual = (
                        str(int(r)) if r == int(r) and abs(r) < 1e15 else str(r)
                    )
            except Exception:
                calc._valor_atual = "Erro"
        elif chave == "sqr":
            try:
                v = float(calc.display)
                r = v ** 2
                calc._valor_atual = (
                    str(int(r)) if r == int(r) and abs(r) < 1e15 else str(r)
                )
            except Exception:
                calc._valor_atual = "Erro"
        elif chave == "sqrt":
            try:
                v = float(calc.display)
                if v < 0:
                    calc._valor_atual = "Erro"
                else:
                    import math
                    r = math.sqrt(v)
                    calc._valor_atual = (
                        str(int(r)) if r == int(r) and abs(r) < 1e15 else str(r)
                    )
            except Exception:
                calc._valor_atual = "Erro"

        self._atualizar_display()

    # ------------------------------------------------------------------ #
    def _atualizar_display(self):
        valor = self._calc.display
        # Limita tamanho para não estourar o display
        if len(valor) > 15:
            try:
                valor = f"{float(valor):.6e}"
            except Exception:
                pass
        self._lbl_valor.configure(text=valor)
