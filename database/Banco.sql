-- Schema de referência — o banco real é criado automaticamente em biondi.db
-- Este arquivo serve apenas como documentação da estrutura.

CREATE TABLE IF NOT EXISTS conversas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo        TEXT    NOT NULL DEFAULT 'Nova conversa',
    criada_em     TEXT    NOT NULL,   -- ISO 8601
    atualizada_em TEXT    NOT NULL    -- ISO 8601
);

CREATE TABLE IF NOT EXISTS mensagens (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    conversa_id  INTEGER NOT NULL REFERENCES conversas(id) ON DELETE CASCADE,
    origem       TEXT    NOT NULL CHECK(origem IN ('usuario','assistente','erro')),
    conteudo     TEXT    NOT NULL,
    enviada_em   TEXT    NOT NULL    -- ISO 8601
);

CREATE TABLE IF NOT EXISTS perfil (
    id               INTEGER PRIMARY KEY CHECK(id = 1),
    nome_usuario     TEXT NOT NULL DEFAULT 'Você',
    nome_assistente  TEXT NOT NULL DEFAULT 'Biondi'
);
