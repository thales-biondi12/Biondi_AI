import customtkinter as ctk
from datetime import datetime
from Modules.ia import GeminiChat
import database.db as db


class ChatView(ctk.CTkFrame):
    """Painel de chat com sidebar de histórico de conversas."""

    COR_USUARIO    = ("gray80", "gray20")
    COR_ASSISTENTE = ("gray90", "gray15")
    COR_ERRO       = ("#ffd6d6", "#5c1a1a")
    COR_SIDEBAR    = ("gray85", "gray13")
    COR_BTN_ATIVO  = ("gray75", "gray25")

    def __init__(self, master, nome_usuario="Você",
                 nome_assistente="Biondi", **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.nome_usuario    = nome_usuario
        self.nome_assistente = nome_assistente
        self.FONTE_MSG  = ctk.CTkFont(family="Arial", size=13)
        self.FONTE_HORA = ctk.CTkFont(family="Arial", size=10)

        self._ia = GeminiChat(nome_assistente=nome_assistente)
        db.inicializar()

        self._conversa_id: int = self._obter_conversa_ativa()
        self._btns_conversa: dict[int, ctk.CTkButton] = {}

        self._construir()
        self._carregar_historico()

    # ------------------------------------------------------------------ #
    def _obter_conversa_ativa(self) -> int:
        cid = db.ultima_conversa_id()
        if cid is None:
            cid = db.nova_conversa("Nova conversa")
        return cid

    # ══════════════════════════════════════════════════════════════════════
    # LAYOUT PRINCIPAL
    # ══════════════════════════════════════════════════════════════════════
    def _construir(self):
        self.grid_columnconfigure(0, weight=0)   # sidebar fixa
        self.grid_columnconfigure(1, weight=1)   # chat expansível
        self.grid_rowconfigure(0, weight=1)

        self._construir_sidebar()
        self._construir_area_chat()

    # ── SIDEBAR ──────────────────────────────────────────────────────────
    def _construir_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=200, corner_radius=0,
            fg_color=self.COR_SIDEBAR,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(1, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        # Botão Nova Conversa
        ctk.CTkButton(
            self.sidebar,
            text="＋  Nova conversa",
            height=36, corner_radius=8,
            fg_color=("gray78", "gray22"),
            hover_color=("gray68", "gray30"),
            font=ctk.CTkFont(size=13),
            command=self._nova_conversa,
        ).grid(row=0, column=0, padx=10, pady=(12, 6), sticky="ew")

        # Lista scrollável de conversas
        self._lista_scroll = ctk.CTkScrollableFrame(
            self.sidebar, corner_radius=0,
            fg_color="transparent", label_text=""
        )
        self._lista_scroll.grid(row=1, column=0, sticky="nsew", padx=4)
        self._lista_scroll.grid_columnconfigure(0, weight=1)

        # Separador
        ctk.CTkFrame(
            self.sidebar, height=1,
            fg_color=("gray75", "gray28")
        ).grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 0))

        self._popular_lista()

    def _popular_lista(self):
        """Limpa e repopula a lista de conversas."""
        for w in self._lista_scroll.winfo_children():
            w.destroy()
        self._btns_conversa.clear()

        conversas = db.listar_conversas()
        for i, conv in enumerate(conversas):
            cid    = conv["id"]
            titulo = conv["titulo"] or "Nova conversa"
            # Trunca título longo
            if len(titulo) > 22:
                titulo = titulo[:22] + "…"

            frame = ctk.CTkFrame(
                self._lista_scroll, corner_radius=8,
                fg_color="transparent"
            )
            frame.grid(row=i, column=0, sticky="ew", pady=2)
            frame.grid_columnconfigure(0, weight=1)

            cor = self.COR_BTN_ATIVO if cid == self._conversa_id else "transparent"
            btn = ctk.CTkButton(
                frame,
                text=titulo,
                anchor="w",
                height=36, corner_radius=8,
                fg_color=cor,
                hover_color=("gray78", "gray28"),
                font=ctk.CTkFont(size=12),
                command=lambda c=cid: self._abrir_conversa(c),
            )
            btn.grid(row=0, column=0, sticky="ew")
            self._btns_conversa[cid] = btn

            # Botão deletar (×)
            ctk.CTkButton(
                frame,
                text="×",
                width=24, height=24,
                corner_radius=6,
                fg_color="transparent",
                hover_color=("gray70", "#5c1a1a"),
                text_color=("gray50", "gray55"),
                font=ctk.CTkFont(size=14),
                command=lambda c=cid: self._deletar_conversa(c),
            ).grid(row=0, column=1, padx=(2, 4))

    # ── ÁREA DE CHAT ─────────────────────────────────────────────────────
    def _construir_area_chat(self):
        area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        area.grid(row=0, column=1, sticky="nsew")
        area.grid_rowconfigure(1, weight=1)
        area.grid_columnconfigure(0, weight=1)

        # Cabeçalho
        cab = ctk.CTkFrame(area, height=46, corner_radius=0,
                           fg_color=("gray88", "gray12"))
        cab.grid(row=0, column=0, sticky="ew")
        cab.grid_columnconfigure(0, weight=1)
        cab.grid_columnconfigure(1, weight=0)
        cab.grid_propagate(False)

        self._lbl_titulo = ctk.CTkLabel(
            cab, text="Nova conversa",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self._lbl_titulo.grid(row=0, column=0, padx=16, sticky="w")

        # Badge do modelo ativo
        self._lbl_modelo = ctk.CTkLabel(
            cab, text="",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray55"),
            anchor="e",
        )
        self._lbl_modelo.grid(row=0, column=1, padx=16, sticky="e")

        # Histórico scrollável
        self.scroll = ctk.CTkScrollableFrame(
            area, corner_radius=0, fg_color="transparent", label_text=""
        )
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

        # Barra de entrada
        barra = ctk.CTkFrame(area, height=60, corner_radius=0,
                             fg_color=("gray90", "gray13"))
        barra.grid(row=2, column=0, sticky="ew")
        barra.grid_columnconfigure(0, weight=1)

        self.campo = ctk.CTkEntry(
            barra,
            placeholder_text="Digite sua mensagem…",
            height=40, corner_radius=20,
            font=ctk.CTkFont(size=13),
        )
        self.campo.grid(row=0, column=0, padx=(12, 8), pady=10, sticky="ew")
        self.campo.bind("<Return>", self._ao_enviar)

        self.btn_enviar = ctk.CTkButton(
            barra,
            text="Enviar",
            width=90, height=40, corner_radius=20,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._ao_enviar,
        )
        self.btn_enviar.grid(row=0, column=1, padx=(0, 12), pady=10)

    # ══════════════════════════════════════════════════════════════════════
    # AÇÕES DA SIDEBAR
    # ══════════════════════════════════════════════════════════════════════
    def _nova_conversa(self):
        self._conversa_id = db.nova_conversa("Nova conversa")
        self._ia.limpar_historico()
        self._limpar_tela()
        self._lbl_titulo.configure(text="Nova conversa")
        self._popular_lista()

    def _abrir_conversa(self, cid: int):
        if cid == self._conversa_id:
            return
        self._conversa_id = cid
        self._ia.limpar_historico()
        self._limpar_tela()
        self._carregar_historico()
        # Atualiza destaque na lista
        for c, btn in self._btns_conversa.items():
            btn.configure(
                fg_color=self.COR_BTN_ATIVO if c == cid else "transparent"
            )

    def _deletar_conversa(self, cid: int):
        db.deletar_conversa(cid)
        if cid == self._conversa_id:
            # Abre ou cria outra conversa
            self._conversa_id = self._obter_conversa_ativa()
            if self._conversa_id == cid:
                self._conversa_id = db.nova_conversa("Nova conversa")
            self._ia.limpar_historico()
            self._limpar_tela()
            self._carregar_historico()
        self._popular_lista()

    def _limpar_tela(self):
        for w in self.scroll.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════════════
    # HISTÓRICO
    # ══════════════════════════════════════════════════════════════════════
    def _carregar_historico(self):
        mensagens = db.carregar_mensagens(self._conversa_id)

        # Atualiza título no cabeçalho
        convs = {c["id"]: c for c in db.listar_conversas()}
        if self._conversa_id in convs:
            self._lbl_titulo.configure(
                text=convs[self._conversa_id]["titulo"] or "Nova conversa"
            )

        for msg in mensagens:
            if msg["origem"] in ("usuario", "assistente"):
                self._renderizar_mensagem(
                    msg["conteudo"],
                    msg["origem"],
                    msg["enviada_em"][11:16],
                )
                role = "user" if msg["origem"] == "usuario" else "assistant"
                self._ia._historico.append({
                    "role": role, "content": msg["conteudo"]
                })
        self.after(100, self._scroll_fim)

    # ══════════════════════════════════════════════════════════════════════
    # ENVIO E CALLBACKS DA IA
    # ══════════════════════════════════════════════════════════════════════
    def _ao_enviar(self, _event=None):
        texto = self.campo.get().strip()
        if not texto:
            return

        self.campo.delete(0, "end")
        self._set_input_estado(False)

        db.salvar_mensagem(self._conversa_id, "usuario", texto)
        self.adicionar_mensagem(texto, origem="usuario")

        # Atualiza título com as primeiras palavras
        titulo = " ".join(texto.split()[:6])
        db.atualizar_titulo(self._conversa_id, titulo)
        self._lbl_titulo.configure(text=titulo)
        if self._conversa_id in self._btns_conversa:
            t = titulo if len(titulo) <= 22 else titulo[:22] + "…"
            self._btns_conversa[self._conversa_id].configure(text=t)

        self._mostrar_digitando()
        self._ia.enviar(
            mensagem=texto,
            ao_responder=self._receber_resposta,
            ao_erro=self._receber_erro,
            ao_reasoning=self._receber_reasoning,
            ao_provedor=self._receber_provedor,
        )

    def _receber_resposta(self, texto: str):
        self.after(0, self._exibir_resposta, texto)

    def _receber_erro(self, msg: str):
        self.after(0, self._exibir_erro, msg)

    def _receber_reasoning(self, texto: str):
        self.after(0, self._exibir_reasoning, texto)

    def _receber_provedor(self, info: dict):
        self.after(0, self._exibir_provedor, info)

    def _exibir_provedor(self, info: dict):
        modelo = info["modelo"].split("/")[-1]          # ex: deepseek-v4-flash
        chave  = info["chave"]
        icone  = "🧠" if info["reasoning"] else "⚡"
        self._lbl_modelo.configure(
            text=f"{icone} {modelo}  •  chave {chave}",
            text_color=("gray45", "gray55"),
        )

    def _exibir_resposta(self, texto: str):
        self._remover_digitando()
        db.salvar_mensagem(self._conversa_id, "assistente", texto)
        self.adicionar_mensagem(texto, origem="assistente")
        self._set_input_estado(True)

    def _exibir_erro(self, msg: str):
        self._remover_digitando()
        self.adicionar_mensagem(msg, origem="erro")
        self._set_input_estado(True)

    def _exibir_reasoning(self, texto: str):
        linha = len(self.scroll.winfo_children())
        container = ctk.CTkFrame(self.scroll, fg_color="transparent")
        container.grid(row=linha, column=0, sticky="ew", padx=8, pady=(4, 0))
        container.grid_columnconfigure(0, weight=1)

        self._reasoning_visivel = False
        conteudo_frame = ctk.CTkFrame(
            container, corner_radius=8,
            fg_color=("gray85", "gray17"),
            border_width=1, border_color=("gray70", "gray30"),
        )

        def _toggle():
            self._reasoning_visivel = not self._reasoning_visivel
            if self._reasoning_visivel:
                conteudo_frame.grid(row=1, column=0, sticky="ew",
                                    padx=(0, 60), pady=(2, 0))
                btn.configure(text="🧠 Raciocínio  ▲")
            else:
                conteudo_frame.grid_forget()
                btn.configure(text="🧠 Raciocínio  ▼")
            self.after(50, self._scroll_fim)

        btn = ctk.CTkButton(
            container, text="🧠 Raciocínio  ▼",
            anchor="w", height=28, corner_radius=6,
            fg_color=("gray85", "gray17"),
            hover_color=("gray75", "gray25"),
            text_color=("gray45", "gray55"),
            font=ctk.CTkFont(size=11, slant="italic"),
            command=_toggle,
        )
        btn.grid(row=0, column=0, sticky="w", padx=(0, 60))

        ctk.CTkLabel(
            conteudo_frame, text=texto,
            font=ctk.CTkFont(size=11),
            text_color=("gray45", "gray55"),
            wraplength=420, justify="left", anchor="w",
        ).pack(padx=10, pady=8, fill="x")

    # ── Digitando ─────────────────────────────────────────────────────── #
    def _mostrar_digitando(self):
        linha = len(self.scroll.winfo_children())
        self._frame_digitando = ctk.CTkFrame(
            self.scroll, fg_color="transparent"
        )
        self._frame_digitando.grid(
            row=linha, column=0, sticky="w", padx=8, pady=4
        )
        ctk.CTkLabel(
            self._frame_digitando,
            text=f"{self.nome_assistente} está digitando…",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=("gray50", "gray55"),
        ).pack(padx=12, pady=6)
        self.after(50, self._scroll_fim)

    def _remover_digitando(self):
        if hasattr(self, "_frame_digitando"):
            self._frame_digitando.destroy()
            del self._frame_digitando

    # ── Balões ────────────────────────────────────────────────────────── #
    def adicionar_mensagem(self, texto: str, origem: str = "usuario",
                           hora_str: str | None = None):
        self._renderizar_mensagem(
            texto, origem,
            hora_str or datetime.now().strftime("%H:%M")
        )
        self.after(50, self._scroll_fim)

    def _renderizar_mensagem(self, texto: str, origem: str, hora_str: str):
        eh_usuario = origem == "usuario"
        eh_erro    = origem == "erro"

        nome = self.nome_usuario if eh_usuario else self.nome_assistente
        if eh_erro:
            cor, lado = self.COR_ERRO, "w"
        else:
            cor  = self.COR_USUARIO if eh_usuario else self.COR_ASSISTENTE
            lado = "e" if eh_usuario else "w"

        linha = len(self.scroll.winfo_children())
        container = ctk.CTkFrame(self.scroll, fg_color="transparent")
        container.grid(row=linha, column=0, sticky="ew", padx=8, pady=4)
        container.grid_columnconfigure(0, weight=1)

        balao = ctk.CTkFrame(container, corner_radius=14, fg_color=cor)
        balao.grid(
            row=0, column=0,
            sticky="e" if eh_usuario else "w",
            padx=(60, 0) if eh_usuario else (0, 60),
        )

        ctk.CTkLabel(
            balao,
            text=f"{nome}  {hora_str}",
            font=self.FONTE_HORA,
            text_color=("gray50", "gray55"),
            anchor=lado,
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 0))

        ctk.CTkLabel(
            balao,
            text=texto,
            font=self.FONTE_MSG,
            wraplength=400,
            justify="right" if eh_usuario else "left",
            anchor=lado,
        ).grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 10))

    # ── Utilitários ───────────────────────────────────────────────────── #
    def _scroll_fim(self):
        self.scroll.update_idletasks()
        self.scroll._parent_canvas.yview_moveto(1.0)

    def _set_input_estado(self, ativo: bool):
        estado = "normal" if ativo else "disabled"
        self.campo.configure(state=estado)
        self.btn_enviar.configure(state=estado)
        if ativo:
            self.campo.focus()
