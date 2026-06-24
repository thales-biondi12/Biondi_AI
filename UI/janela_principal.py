import json
import os
import customtkinter as ctk

from UI.menu import MenuLateral
from UI.chat import ChatView
from UI.perfil import PerfilView
from UI.configuracoes import ConfiguracoesView
from UI.calculadora_view import CalculadoraView
from UI.cronometro import CronometroView


_DIR_CONFIG = os.path.join(os.path.dirname(__file__), "..", "config", "settings.json")


def _carregar_config() -> dict:
    try:
        with open(_DIR_CONFIG, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


class JanelaPrincipal(ctk.CTk):
    """Janela raiz: sidebar + área de conteúdo."""

    def __init__(self):
        super().__init__()
        self._cfg = _carregar_config()

        ctk.set_appearance_mode(self._cfg.get("appearance_mode", "dark"))
        ctk.set_default_color_theme(self._cfg.get("color_theme", "blue"))

        nome    = self._cfg.get("app_name", "Biondi AI")
        largura = self._cfg.get("window_width", 1000)
        altura  = self._cfg.get("window_height", 620)

        self.title(nome)
        self.geometry(f"{largura}x{altura}")
        self.minsize(700, 460)

        self.update_idletasks()
        x = (self.winfo_screenwidth()  - largura) // 2
        y = (self.winfo_screenheight() - altura)  // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        # Declara estado ANTES de qualquer widget que possa chamar _trocar_pagina
        self._paginas: dict = {}
        self._pagina_atual = None

        self._construir()

    # ------------------------------------------------------------------ #
    def _construir(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── Sidebar ──────────────────────────────────────────────────────
        # ao_selecionar=None aqui; vínculo feito depois que as páginas existem
        self.menu = MenuLateral(
            self,
            ao_selecionar=None,
            fg_color=("gray88", "gray12"),
        )
        self.menu.grid(row=0, column=0, sticky="nsew")

        # Separador vertical
        sep = ctk.CTkFrame(self, width=1, corner_radius=0,
                           fg_color=("gray75", "gray25"))
        sep.grid(row=0, column=0, sticky="nse")

        # ── Área de conteúdo ─────────────────────────────────────────────
        self.conteudo = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.conteudo.grid(row=0, column=1, sticky="nsew")
        self.conteudo.grid_rowconfigure(0, weight=1)
        self.conteudo.grid_columnconfigure(0, weight=1)

        # ── Páginas ──────────────────────────────────────────────────────
        self._paginas["conversas"] = ChatView(
            self.conteudo,
            nome_usuario=self._cfg.get("user_name", "Você"),
            nome_assistente=self._cfg.get("assistant_name", "Biondi"),
        )
        self._paginas["calculadora"] = CalculadoraView(self.conteudo)
        self._paginas["cronometro"]  = CronometroView(self.conteudo)
        self._paginas["perfil"] = PerfilView(
            self.conteudo,
            nome_usuario=self._cfg.get("user_name", "Você"),
            nome_assistente=self._cfg.get("assistant_name", "Biondi"),
        )
        self._paginas["configuracoes"] = ConfiguracoesView(
            self.conteudo,
            ao_salvar=self._aplicar_config,
        )

        # Agora vincula o callback e seleciona a primeira página
        self.menu.ao_selecionar = self._trocar_pagina
        self._trocar_pagina("conversas")
        self.menu.destacar("conversas")

    # ------------------------------------------------------------------ #
    def _trocar_pagina(self, chave: str):
        if self._pagina_atual is not None:
            self._pagina_atual.grid_forget()

        pagina = self._paginas.get(chave)
        if pagina:
            pagina.grid(row=0, column=0, sticky="nsew")
            self._pagina_atual = pagina

    # ------------------------------------------------------------------ #
    def _aplicar_config(self, cfg: dict):
        """Recebe o dict atualizado de configurações e aplica o que for possível em tempo real."""
        novo_nome = cfg.get("app_name", "Biondi AI")
        self.title(novo_nome)
        ctk.set_appearance_mode(cfg.get("appearance_mode", "dark"))

    # ------------------------------------------------------------------ #
    @staticmethod
    def _pagina_placeholder(titulo: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(master=None, corner_radius=0,
                             fg_color="transparent")
        lbl = ctk.CTkLabel(
            frame,
            text=titulo,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray50", "gray60"),
        )
        lbl.place(relx=0.5, rely=0.5, anchor="center")
        return frame
