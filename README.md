# 🤖 Biondi AI

<p align="center">
  <img src="assets/logo.png" width="200">
</p>

<p align="center">
  <strong>Seu assistente pessoal desenvolvido em Python.</strong>
</p>

---

# 📖 Sobre o Projeto

O **Biondi AI** é um projeto pessoal criado por **Thales Biondi** com o objetivo de desenvolver uma inteligência artificial completa capaz de auxiliar em tarefas do dia a dia, programação, estudos, automação e controle de dispositivos.

O projeto está sendo construído de forma gradual, começando por funcionalidades básicas e evoluindo até uma plataforma completa com:

- Assistente virtual
- Comandos de voz
- Banco de dados
- Automações
- Integração com ESP32
- Dashboard
- Visão computacional
- Aplicativo mobile
- Sincronização em nuvem

---

# 🚀 Status Atual

Versão atual:

```txt
Biondi AI v1.0 (Em Desenvolvimento)
```

Funcionalidades concluídas:

- [x] Interface principal
- [x] Menu lateral
- [x] Chat funcional
- [x] Banco de dados SQLite

Funcionalidades em desenvolvimento:

- [ ] Histórico de mensagens
- [ ] Perfil do usuário
- [ ] Tema claro/escuro
- [ ] Calculadora
- [ ] Relógio
- [ ] Cronômetro
- [ ] Conversor de unidades

---

# 🛠 Tecnologias Utilizadas

## Linguagem

- Python 

## Banco de Dados

- SQLite


---

# 📂 Estrutura do Projeto

```txt
BIONDI_IA/
│
├── assets/
│
├── config/
│
├── database/
│   └── biondi.db
│
├── Modules/
│
├── UI/
│
├── .gitignore
│
└── main.py
```

---

# ⚙️ Instalação

Clone o projeto:

```bash
git clone https://github.com/thales-biondi12/Biondi_AI
```

Entre na pasta:

```bash
cd Biondi_IA
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / MacOS

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o projeto:

```bash
python main.py
```

---

# 💾 Banco de Dados

Atualmente o sistema utiliza SQLite.

Tabela principal:

```sql
CREATE TABLE mensagens(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texto TEXT NOT NULL
);
```

---

# 🎯 Roadmap

## 🚀 Versão 1.0 - Fundação

- Chat
- Histórico
- Perfil
- Calculadora
- Relógio
- Cronômetro
- Conversor
- SQLite

## 🚀 Versão 2.0 - Assistente Pessoal

- Agenda
- Calendário
- Tarefas
- Lembretes
- Notificações

## 🚀 Versão 3.0 - Voz Inteligente

- Reconhecimento de fala
- Respostas por voz
- Palavra de ativação

## 🚀 Versão 4.0 - Internet e APIs

- Clima
- Notícias
- CEP
- Tradutor
- Wikipedia

## 🚀 Versão 5.0 - Programador

- Gerador de código
- Gerador SQL
- README automático
- Integração GitHub

## 🚀 Versão 6.0 - Dashboard

- Monitoramento de CPU
- RAM
- Disco
- Rede

## 🚀 Versão 7.0 - Casa Inteligente

- ESP32
- LEDs
- Sensores
- Robótica

## 🚀 Versão 8.0 - Memória Inteligente

- Memória permanente
- Preferências do usuário
- Aprendizado de hábitos

## 🚀 Versão 9.0 - Central de Estudos

- Resumos
- Flashcards
- Quiz
- Leitura de PDF

## 🚀 Versão 10.0+

- Visão Computacional
- Aplicativo Mobile
- Nuvem
- API própria
- Sistema de Plugins

---


# 👨‍💻 Autor

### Thales Andrade Biondi

Desenvolvedor do projeto Biondi AI.


# ⭐ Objetivo Final

Criar uma plataforma completa de inteligência artificial pessoal capaz de:

- Conversar naturalmente
- Aprender preferências
- Controlar dispositivos
- Auxiliar nos estudos
- Programar
- Automatizar tarefas
- Integrar hardware e software

---

<p align="center">
  <strong>🚀 Biondi AI — Do sonho à realidade.</strong>
</p>