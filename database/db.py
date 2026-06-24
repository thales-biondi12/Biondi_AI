"""
Camada de acesso ao SQLite — banco único em database/biondi.db
Tabelas:
  conversas  — cada sessão de chat
  mensagens  — mensagens de cada conversa
  perfil     — dados do usuário (1 linha)
"""
import sqlite3
import os
from datetime import datetime

_DB_PATH = os.path.join(os.path.dirname(__file__), "biondi.db")


def _conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # melhor concorrência
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def inicializar():
    """Cria as tabelas se ainda não existirem."""
    with _conectar() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo      TEXT    NOT NULL DEFAULT 'Nova conversa',
                criada_em   TEXT    NOT NULL,
                atualizada_em TEXT  NOT NULL
            );

            CREATE TABLE IF NOT EXISTS mensagens (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                conversa_id  INTEGER NOT NULL REFERENCES conversas(id) ON DELETE CASCADE,
                origem       TEXT    NOT NULL CHECK(origem IN ('usuario','assistente','erro')),
                conteudo     TEXT    NOT NULL,
                enviada_em   TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS perfil (
                id               INTEGER PRIMARY KEY CHECK(id = 1),
                nome_usuario     TEXT NOT NULL DEFAULT 'Você',
                nome_assistente  TEXT NOT NULL DEFAULT 'Biondi'
            );

            -- Garante que sempre existe exatamente 1 linha no perfil
            INSERT OR IGNORE INTO perfil (id, nome_usuario, nome_assistente)
            VALUES (1, 'Você', 'Biondi');
        """)


# ── Conversas ─────────────────────────────────────────────────────────── #

def nova_conversa(titulo: str = "Nova conversa") -> int:
    """Cria uma nova conversa e retorna o id."""
    agora = datetime.now().isoformat(sep=" ", timespec="seconds")
    with _conectar() as conn:
        cur = conn.execute(
            "INSERT INTO conversas (titulo, criada_em, atualizada_em) VALUES (?,?,?)",
            (titulo, agora, agora),
        )
        return cur.lastrowid


def listar_conversas() -> list[dict]:
    """Retorna todas as conversas ordenadas pela mais recente."""
    with _conectar() as conn:
        rows = conn.execute(
            "SELECT * FROM conversas ORDER BY atualizada_em DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def atualizar_titulo(conversa_id: int, titulo: str):
    agora = datetime.now().isoformat(sep=" ", timespec="seconds")
    with _conectar() as conn:
        conn.execute(
            "UPDATE conversas SET titulo=?, atualizada_em=? WHERE id=?",
            (titulo, agora, conversa_id),
        )


def deletar_conversa(conversa_id: int):
    with _conectar() as conn:
        conn.execute("DELETE FROM conversas WHERE id=?", (conversa_id,))


# ── Mensagens ─────────────────────────────────────────────────────────── #

def salvar_mensagem(conversa_id: int, origem: str, conteudo: str) -> int:
    """Salva uma mensagem e atualiza o timestamp da conversa."""
    agora = datetime.now().isoformat(sep=" ", timespec="seconds")
    with _conectar() as conn:
        cur = conn.execute(
            "INSERT INTO mensagens (conversa_id, origem, conteudo, enviada_em) VALUES (?,?,?,?)",
            (conversa_id, origem, conteudo, agora),
        )
        conn.execute(
            "UPDATE conversas SET atualizada_em=? WHERE id=?",
            (agora, conversa_id),
        )
        return cur.lastrowid


def carregar_mensagens(conversa_id: int) -> list[dict]:
    """Retorna todas as mensagens de uma conversa em ordem cronológica."""
    with _conectar() as conn:
        rows = conn.execute(
            "SELECT * FROM mensagens WHERE conversa_id=? ORDER BY id ASC",
            (conversa_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def ultima_conversa_id() -> int | None:
    """Retorna o id da conversa mais recente, ou None se não houver nenhuma."""
    with _conectar() as conn:
        row = conn.execute(
            "SELECT id FROM conversas ORDER BY atualizada_em DESC LIMIT 1"
        ).fetchone()
    return row["id"] if row else None


# ── Perfil ────────────────────────────────────────────────────────────── #

def carregar_perfil() -> dict:
    with _conectar() as conn:
        row = conn.execute("SELECT * FROM perfil WHERE id=1").fetchone()
    return dict(row) if row else {"nome_usuario": "Você", "nome_assistente": "Biondi"}


def salvar_perfil(nome_usuario: str, nome_assistente: str):
    with _conectar() as conn:
        conn.execute(
            "UPDATE perfil SET nome_usuario=?, nome_assistente=? WHERE id=1",
            (nome_usuario, nome_assistente),
        )
