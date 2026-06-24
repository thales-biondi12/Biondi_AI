import customtkinter as ctk
import database.db as db


class PerfilView(ctk.CTkFrame):
    """Painel de perfil do usuário — dados persistidos no SQLite."""

    def __init__(self, master, nome_usuario="Você",
                 nome_assistente="Biondi", **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        db.inicializar()
        perfil = db.carregar_perfil()
        self.nome_usuario    = perfil.get("nome_usuario",    nome_usuario)
        self.nome_assistente = perfil.get("nome_assistente", nome_assistente)
        self._construir()

    # ------------------------------------------------------------------ #
    def _construir(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Cartão central
        cartao = ctk.CTkFrame(self, width=360, corner_radius=16)
        cartao.place(relx=0.5, rely=0.5, anchor="center")
        cartao.grid_columnconfigure(0, weight=1)

        # Avatar placeholder
        avatar = ctk.CTkLabel(
            cartao,
            text="👤",
            font=ctk.CTkFont(size=64),
        )
        avatar.grid(row=0, column=0, pady=(32, 8))

        # Nome
        self.lbl_nome = ctk.CTkLabel(
            cartao,
            text=self.nome_usuario,
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
        )
        self.lbl_nome.grid(row=1, column=0, padx=24, pady=(0, 4))

        # Assistente vinculado
        lbl_sub = ctk.CTkLabel(
            cartao,
            text=f"Assistente: {self.nome_assistente}",
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray55"),
        )
        lbl_sub.grid(row=2, column=0, padx=24, pady=(0, 24))

        separador = ctk.CTkFrame(cartao, height=1,
                                 fg_color=("gray75", "gray30"))
        separador.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 20))

        # Campo para alterar o nome
        ctk.CTkLabel(
            cartao,
            text="Alterar nome de exibição",
            font=ctk.CTkFont(size=12),
            anchor="w",
        ).grid(row=4, column=0, sticky="w", padx=24)

        self.campo_nome = ctk.CTkEntry(
            cartao,
            placeholder_text="Novo nome…",
            height=38,
            corner_radius=10,
        )
        self.campo_nome.grid(row=5, column=0, padx=24, pady=(4, 12), sticky="ew")
        self.campo_nome.bind("<Return>", self._salvar_nome)

        btn = ctk.CTkButton(
            cartao,
            text="Salvar",
            height=38,
            corner_radius=10,
            command=self._salvar_nome,
        )
        btn.grid(row=6, column=0, padx=24, pady=(0, 32), sticky="ew")

    # ------------------------------------------------------------------ #
    def _salvar_nome(self, _event=None):
        novo = self.campo_nome.get().strip()
        if novo:
            self.nome_usuario = novo
            self.lbl_nome.configure(text=novo)
            self.campo_nome.delete(0, "end")
            db.salvar_perfil(self.nome_usuario, self.nome_assistente)
