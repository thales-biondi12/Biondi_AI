import json
import os
import customtkinter as ctk

_DIR_CONFIG = os.path.join(os.path.dirname(__file__), "..", "config", "settings.json")


def _carregar() -> dict:
    try:
        with open(_DIR_CONFIG, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _salvar(dados: dict) -> None:
    with open(_DIR_CONFIG, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


class ConfiguracoesView(ctk.CTkFrame):
    """Painel de configurações — lê e salva settings.json em tempo real."""

    TEMAS_APARENCIA = ["dark", "light", "system"]
    TEMAS_COR       = ["blue", "green", "dark-blue"]

    def __init__(self, master, ao_salvar=None, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.ao_salvar = ao_salvar   # callback opcional para notificar a janela principal
        self._cfg = _carregar()
        self._construir()

    # ------------------------------------------------------------------ #
    def _construir(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Cartão central scrollável ────────────────────────────────────
        scroll = ctk.CTkScrollableFrame(
            self, corner_radius=0, fg_color="transparent", label_text=""
        )
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        linha = 0

        # ── Título ───────────────────────────────────────────────────────
        ctk.CTkLabel(
            scroll,
            text="⚙️  Configurações",
            font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
            anchor="w",
        ).grid(row=linha, column=0, sticky="w", padx=32, pady=(28, 20))
        linha += 1

        # ── Seção: Aparência ─────────────────────────────────────────────
        linha = self._secao(scroll, linha, "Aparência")

        linha = self._linha_label(scroll, linha, "Tema")
        self.opt_aparencia = ctk.CTkOptionMenu(
            scroll,
            values=self.TEMAS_APARENCIA,
            command=self._preview_aparencia,
        )
        self.opt_aparencia.set(self._cfg.get("appearance_mode", "dark"))
        self.opt_aparencia.grid(row=linha, column=0, sticky="w",
                                padx=32, pady=(0, 12))
        linha += 1

        linha = self._linha_label(scroll, linha, "Cor de destaque")
        self.opt_cor = ctk.CTkOptionMenu(
            scroll,
            values=self.TEMAS_COR,
        )
        self.opt_cor.set(self._cfg.get("color_theme", "blue"))
        self.opt_cor.grid(row=linha, column=0, sticky="w",
                          padx=32, pady=(0, 12))
        linha += 1

        # ── Seção: Janela ────────────────────────────────────────────────
        linha = self._secao(scroll, linha, "Janela")

        linha = self._linha_label(scroll, linha, "Nome da aplicação")
        self.entry_app_name = ctk.CTkEntry(scroll, placeholder_text="Biondi AI",
                                           height=36, corner_radius=10, width=260)
        self.entry_app_name.insert(0, self._cfg.get("app_name", "Biondi AI"))
        self.entry_app_name.grid(row=linha, column=0, sticky="w",
                                 padx=32, pady=(0, 12))
        linha += 1

        frame_wh = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_wh.grid(row=linha, column=0, sticky="w", padx=32, pady=(0, 12))
        linha += 1

        ctk.CTkLabel(frame_wh, text="Largura").grid(row=0, column=0, padx=(0, 6))
        self.entry_largura = ctk.CTkEntry(frame_wh, width=80, height=36,
                                          corner_radius=10)
        self.entry_largura.insert(0, str(self._cfg.get("window_width", 1000)))
        self.entry_largura.grid(row=0, column=1, padx=(0, 20))

        ctk.CTkLabel(frame_wh, text="Altura").grid(row=0, column=2, padx=(0, 6))
        self.entry_altura = ctk.CTkEntry(frame_wh, width=80, height=36,
                                         corner_radius=10)
        self.entry_altura.insert(0, str(self._cfg.get("window_height", 620)))
        self.entry_altura.grid(row=0, column=3)

        # ── Seção: Assistente ────────────────────────────────────────────
        linha = self._secao(scroll, linha, "Assistente")

        linha = self._linha_label(scroll, linha, "Nome do assistente")
        self.entry_assistente = ctk.CTkEntry(scroll, placeholder_text="Biondi",
                                             height=36, corner_radius=10, width=260)
        self.entry_assistente.insert(0, self._cfg.get("assistant_name", "Biondi"))
        self.entry_assistente.grid(row=linha, column=0, sticky="w",
                                   padx=32, pady=(0, 12))
        linha += 1

        linha = self._linha_label(scroll, linha, "Nome do usuário")
        self.entry_usuario = ctk.CTkEntry(scroll, placeholder_text="Você",
                                          height=36, corner_radius=10, width=260)
        self.entry_usuario.insert(0, self._cfg.get("user_name", "Você"))
        self.entry_usuario.grid(row=linha, column=0, sticky="w",
                                padx=32, pady=(0, 24))
        linha += 1

        # ── Botões ───────────────────────────────────────────────────────
        frame_btns = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_btns.grid(row=linha, column=0, sticky="w", padx=32, pady=(0, 32))

        ctk.CTkButton(
            frame_btns,
            text="Salvar",
            width=120,
            height=38,
            corner_radius=10,
            command=self._salvar,
        ).grid(row=0, column=0, padx=(0, 12))

        ctk.CTkButton(
            frame_btns,
            text="Restaurar padrões",
            width=160,
            height=38,
            corner_radius=10,
            fg_color=("gray75", "gray25"),
            hover_color=("gray65", "gray35"),
            text_color=("gray10", "gray90"),
            command=self._restaurar_padroes,
        ).grid(row=0, column=1)

        # Label de feedback
        self.lbl_status = ctk.CTkLabel(
            scroll, text="", font=ctk.CTkFont(size=12),
            text_color=("green", "#4caf50")
        )
        self.lbl_status.grid(row=linha + 1, column=0, sticky="w",
                             padx=32, pady=(0, 16))

    # ── Helpers de layout ─────────────────────────────────────────────── #
    @staticmethod
    def _secao(parent, linha: int, titulo: str) -> int:
        """Insere um separador + título de seção. Retorna a próxima linha."""
        sep = ctk.CTkFrame(parent, height=1, fg_color=("gray75", "gray30"))
        sep.grid(row=linha, column=0, sticky="ew", padx=24, pady=(8, 0))

        ctk.CTkLabel(
            parent, text=titulo,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray45", "gray55"),
            anchor="w",
        ).grid(row=linha + 1, column=0, sticky="w", padx=32, pady=(6, 4))

        return linha + 2

    @staticmethod
    def _linha_label(parent, linha: int, texto: str) -> int:
        ctk.CTkLabel(
            parent, text=texto,
            font=ctk.CTkFont(size=13),
            anchor="w",
        ).grid(row=linha, column=0, sticky="w", padx=32, pady=(0, 2))
        return linha + 1

    # ── Ações ─────────────────────────────────────────────────────────── #
    def _preview_aparencia(self, valor: str):
        """Aplica o tema de aparência imediatamente como preview."""
        ctk.set_appearance_mode(valor)

    def _salvar(self):
        # Valida largura/altura
        try:
            largura = int(self.entry_largura.get())
            altura  = int(self.entry_altura.get())
        except ValueError:
            self._status("⚠️  Largura e altura precisam ser números inteiros.", erro=True)
            return

        self._cfg.update({
            "app_name":        self.entry_app_name.get().strip()  or "Biondi AI",
            "appearance_mode": self.opt_aparencia.get(),
            "color_theme":     self.opt_cor.get(),
            "window_width":    largura,
            "window_height":   altura,
            "assistant_name":  self.entry_assistente.get().strip() or "Biondi",
            "user_name":       self.entry_usuario.get().strip()    or "Você",
        })

        _salvar(self._cfg)
        ctk.set_appearance_mode(self._cfg["appearance_mode"])
        self._status("✔  Configurações salvas. Reinicie para aplicar todas as mudanças.")

        if self.ao_salvar:
            self.ao_salvar(self._cfg)

    def _restaurar_padroes(self):
        padroes = {
            "app_name":        "Biondi AI",
            "appearance_mode": "dark",
            "color_theme":     "blue",
            "window_width":    1000,
            "window_height":   620,
            "assistant_name":  "Biondi",
            "user_name":       "Você",
        }
        # Atualiza campos visuais
        self.entry_app_name.delete(0, "end")
        self.entry_app_name.insert(0, padroes["app_name"])
        self.opt_aparencia.set(padroes["appearance_mode"])
        self.opt_cor.set(padroes["color_theme"])
        self.entry_largura.delete(0, "end")
        self.entry_largura.insert(0, str(padroes["window_width"]))
        self.entry_altura.delete(0, "end")
        self.entry_altura.insert(0, str(padroes["window_height"]))
        self.entry_assistente.delete(0, "end")
        self.entry_assistente.insert(0, padroes["assistant_name"])
        self.entry_usuario.delete(0, "end")
        self.entry_usuario.insert(0, padroes["user_name"])

        self._cfg = padroes
        _salvar(padroes)
        ctk.set_appearance_mode(padroes["appearance_mode"])
        self._status("✔  Padrões restaurados.")

    def _status(self, msg: str, erro: bool = False):
        cor = ("red", "#ef5350") if erro else ("green", "#4caf50")
        self.lbl_status.configure(text=msg, text_color=cor)
        # Limpa a mensagem após 4 segundos
        self.after(4000, lambda: self.lbl_status.configure(text=""))
