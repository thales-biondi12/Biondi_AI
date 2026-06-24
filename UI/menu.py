import customtkinter as ctk


class MenuLateral(ctk.CTkFrame):
    """Sidebar com navegação principal."""

    ITENS = [
        ("💬  Conversas",    "conversas"),
        ("🧮  Calculadora",  "calculadora"),
        ("⏳  Cronometro",  "cronometro"),
        ("👤  Perfil",        "perfil"),
        ("⚙️  Configurações", "configuracoes"),
    ]

    def __init__(self, master, ao_selecionar=None, **kwargs):
        super().__init__(master, width=200, corner_radius=0, **kwargs)
        self.ao_selecionar = ao_selecionar
        self._botoes: dict[str, ctk.CTkButton] = {}
        self._selecionado: str | None = None
        self._construir()
        # NÃO chama _selecionar aqui — a janela principal faz isso depois
        # que todas as páginas estão criadas, via destacar()

    # ------------------------------------------------------------------ #
    def _construir(self):
        self.grid_rowconfigure(len(self.ITENS) + 2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Logo / título
        logo = ctk.CTkLabel(
            self,
            text="Biondi AI",
            font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
            anchor="w",
        )
        logo.grid(row=0, column=0, padx=20, pady=(24, 16), sticky="w")

        separador = ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30"))
        separador.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))

        for idx, (rotulo, chave) in enumerate(self.ITENS, start=2):
            btn = ctk.CTkButton(
                self,
                text=rotulo,
                anchor="w",
                height=40,
                corner_radius=8,
                fg_color="transparent",
                hover_color=("gray85", "gray25"),
                font=ctk.CTkFont(size=13),
                command=lambda c=chave: self._ao_clicar(c),
            )
            btn.grid(row=idx, column=0, padx=10, pady=3, sticky="ew")
            self._botoes[chave] = btn

    # ------------------------------------------------------------------ #
    def _ao_clicar(self, chave: str):
        """Chamado pelo botão: destaca visualmente e notifica a janela."""
        self.destacar(chave)
        if self.ao_selecionar:
            self.ao_selecionar(chave)

    # ------------------------------------------------------------------ #
    def destacar(self, chave: str):
        """Atualiza o visual do botão ativo sem disparar o callback."""
        if self._selecionado and self._selecionado in self._botoes:
            self._botoes[self._selecionado].configure(fg_color="transparent")

        self._selecionado = chave
        if chave in self._botoes:
            self._botoes[chave].configure(fg_color=("gray80", "gray20"))
