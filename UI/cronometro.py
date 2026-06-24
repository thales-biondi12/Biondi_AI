import customtkinter as ctk
from Modules.cronometro import Cronometro, Timer

# ── Paleta ───────────────────────────────────────────────────────────────
_COR_CARD        = ("gray88", "gray14")
_COR_DISPLAY_BG  = ("gray92", "gray10")
_COR_BTN         = ("gray80", "gray22")
_COR_BTN_HOVER   = ("gray70", "gray32")
_COR_BTN_VERDE   = ("#2e7d32", "#43a047")
_COR_BTN_VERDE_H = ("#1b5e20", "#388e3c")
_COR_BTN_VERMELHO   = ("#c62828", "#e53935")
_COR_BTN_VERMELHO_H = ("#b71c1c", "#c62828")
_COR_BTN_AZUL    = ("#1f6aa5", "#3a7ebf")
_COR_BTN_AZUL_H  = ("#185d94", "#2d6ea8")
_COR_VOLTA       = ("gray85", "gray18")


class CronometroView(ctk.CTkFrame):
    """Tela com abas: Cronômetro e Timer."""

    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._construir()

    def _construir(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Abas
        self.abas = ctk.CTkTabview(self, corner_radius=12)
        self.abas.grid(row=0, column=0, sticky="nsew", padx=40, pady=30)

        self.abas.add("⏱  Cronômetro")
        self.abas.add("⏲  Timer")

        self._construir_cronometro(self.abas.tab("⏱  Cronômetro"))
        self._construir_timer(self.abas.tab("⏲  Timer"))

    # ══════════════════════════════════════════════════════════════════════
    # ABA CRONÔMETRO
    # ══════════════════════════════════════════════════════════════════════
    def _construir_cronometro(self, tab):
        self._crono = Cronometro()
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)

        # Display principal
        frame_display = ctk.CTkFrame(tab, corner_radius=12,
                                     fg_color=_COR_DISPLAY_BG)
        frame_display.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))

        self._lbl_crono = ctk.CTkLabel(
            frame_display, text="00:00.00",
            font=ctk.CTkFont(family="Arial", size=56, weight="bold"),
        )
        self._lbl_crono.pack(pady=20)

        # Botões
        frame_btns = ctk.CTkFrame(tab, fg_color="transparent")
        frame_btns.grid(row=1, column=0, pady=8)

        self._btn_crono_start = ctk.CTkButton(
            frame_btns, text="▶  Iniciar", width=130, height=44,
            corner_radius=22,
            fg_color=_COR_BTN_VERDE, hover_color=_COR_BTN_VERDE_H,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._crono_toggle,
        )
        self._btn_crono_start.grid(row=0, column=0, padx=6)

        ctk.CTkButton(
            frame_btns, text="⟳  Volta", width=110, height=44,
            corner_radius=22,
            fg_color=_COR_BTN_AZUL, hover_color=_COR_BTN_AZUL_H,
            font=ctk.CTkFont(size=14),
            command=self._crono_volta,
        ).grid(row=0, column=1, padx=6)

        ctk.CTkButton(
            frame_btns, text="↺  Resetar", width=110, height=44,
            corner_radius=22,
            fg_color=_COR_BTN, hover_color=_COR_BTN_HOVER,
            font=ctk.CTkFont(size=14),
            command=self._crono_resetar,
        ).grid(row=0, column=2, padx=6)

        # Lista de voltas
        self._scroll_voltas = ctk.CTkScrollableFrame(
            tab, corner_radius=8, fg_color=_COR_DISPLAY_BG,
            label_text="Voltas", label_font=ctk.CTkFont(size=12)
        )
        self._scroll_voltas.grid(row=2, column=0, sticky="nsew",
                                 padx=20, pady=(8, 20))
        self._scroll_voltas.grid_columnconfigure(0, weight=1)

        self._atualizar_crono()

    def _crono_toggle(self):
        if self._crono.rodando:
            self._crono.pausar()
            self._btn_crono_start.configure(
                text="▶  Continuar",
                fg_color=_COR_BTN_VERDE, hover_color=_COR_BTN_VERDE_H,
            )
        else:
            self._crono.iniciar()
            self._btn_crono_start.configure(
                text="⏸  Pausar",
                fg_color=_COR_BTN_VERMELHO, hover_color=_COR_BTN_VERMELHO_H,
            )

    def _crono_volta(self):
        if self._crono.rodando or self._crono.tempo_total > 0:
            self._crono.volta()
            voltas = self._crono.voltas
            idx    = len(voltas)
            t      = voltas[-1]
            # Tempo da volta (diferença da anterior)
            anterior = voltas[-2] if len(voltas) > 1 else 0.0
            delta    = t - anterior
            linha = ctk.CTkFrame(self._scroll_voltas, fg_color=_COR_VOLTA,
                                 corner_radius=6)
            linha.grid(row=idx - 1, column=0, sticky="ew", padx=4, pady=2)
            linha.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(linha, text=f"Volta {idx}",
                         font=ctk.CTkFont(size=12),
                         text_color=("gray50", "gray55")).grid(
                row=0, column=0, padx=10, pady=6)
            ctk.CTkLabel(linha, text=Cronometro.formatar(delta),
                         font=ctk.CTkFont(size=12, weight="bold"),
                         anchor="e").grid(row=0, column=1, padx=10)
            ctk.CTkLabel(linha, text=Cronometro.formatar(t),
                         font=ctk.CTkFont(size=12),
                         text_color=("gray50", "gray55")).grid(
                row=0, column=2, padx=10)

    def _crono_resetar(self):
        self._crono.resetar()
        self._btn_crono_start.configure(
            text="▶  Iniciar",
            fg_color=_COR_BTN_VERDE, hover_color=_COR_BTN_VERDE_H,
        )
        # Limpa voltas
        for w in self._scroll_voltas.winfo_children():
            w.destroy()

    def _atualizar_crono(self):
        self._lbl_crono.configure(
            text=Cronometro.formatar(self._crono.tempo_total)
        )
        self.after(33, self._atualizar_crono)  # ~30 fps

    # ══════════════════════════════════════════════════════════════════════
    # ABA TIMER
    # ══════════════════════════════════════════════════════════════════════
    def _construir_timer(self, tab):
        self._timer = Timer(ao_zerar=self._timer_zerou)
        tab.grid_columnconfigure(0, weight=1)

        # Display
        frame_display = ctk.CTkFrame(tab, corner_radius=12,
                                     fg_color=_COR_DISPLAY_BG)
        frame_display.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))

        self._lbl_timer = ctk.CTkLabel(
            frame_display, text="00:00:00",
            font=ctk.CTkFont(family="Arial", size=56, weight="bold"),
        )
        self._lbl_timer.pack(pady=20)

        # Inputs HH MM SS
        frame_inputs = ctk.CTkFrame(tab, fg_color="transparent")
        frame_inputs.grid(row=1, column=0, pady=8)

        for i, (label, attr) in enumerate(
            [("Horas", "_entry_h"), ("Minutos", "_entry_m"), ("Segundos", "_entry_s")]
        ):
            ctk.CTkLabel(frame_inputs, text=label,
                         font=ctk.CTkFont(size=12)).grid(
                row=0, column=i * 2, padx=(16, 2))
            entry = ctk.CTkEntry(
                frame_inputs, width=64, height=40,
                corner_radius=10,
                font=ctk.CTkFont(size=18, weight="bold"),
                justify="center",
                placeholder_text="00",
            )
            entry.grid(row=0, column=i * 2 + 1, padx=(0, 4))
            setattr(self, attr, entry)

        # Botões
        frame_btns = ctk.CTkFrame(tab, fg_color="transparent")
        frame_btns.grid(row=2, column=0, pady=8)

        ctk.CTkButton(
            frame_btns, text="▶  Iniciar", width=130, height=44,
            corner_radius=22,
            fg_color=_COR_BTN_VERDE, hover_color=_COR_BTN_VERDE_H,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._timer_iniciar,
        ).grid(row=0, column=0, padx=6)

        ctk.CTkButton(
            frame_btns, text="⏸  Pausar", width=110, height=44,
            corner_radius=22,
            fg_color=_COR_BTN_VERMELHO, hover_color=_COR_BTN_VERMELHO_H,
            font=ctk.CTkFont(size=14),
            command=self._timer_pausar,
        ).grid(row=0, column=1, padx=6)

        ctk.CTkButton(
            frame_btns, text="↺  Resetar", width=110, height=44,
            corner_radius=22,
            fg_color=_COR_BTN, hover_color=_COR_BTN_HOVER,
            font=ctk.CTkFont(size=14),
            command=self._timer_resetar,
        ).grid(row=0, column=2, padx=6)

        self._lbl_timer_status = ctk.CTkLabel(
            tab, text="",
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray55"),
        )
        self._lbl_timer_status.grid(row=3, column=0, pady=4)

        self._atualizar_timer()

    def _timer_iniciar(self):
        def _ler(entry) -> int:
            try:
                return max(0, int(entry.get()))
            except ValueError:
                return 0

        h = _ler(self._entry_h)
        m = _ler(self._entry_m)
        s = _ler(self._entry_s)

        if not self._timer.rodando:
            if self._timer.restante == 0:
                # Configura só se não tem tempo restante (início novo)
                self._timer.configurar(h, m, s)
            self._timer.iniciar()
            self._lbl_timer_status.configure(text="")

    def _timer_pausar(self):
        self._timer.pausar()

    def _timer_resetar(self):
        self._timer.resetar()
        self._lbl_timer_status.configure(text="")

    def _timer_zerou(self):
        """Chamado pela thread do timer quando zera."""
        self.after(0, self._lbl_timer_status.configure,
                   {"text": "⏰  Tempo esgotado!", "text_color": ("#e53935", "#ef5350")})

    def _atualizar_timer(self):
        self._lbl_timer.configure(
            text=Timer.formatar(self._timer.restante)
        )
        self.after(250, self._atualizar_timer)
