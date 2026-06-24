"""
Módulo de integração com NVIDIA NIM.
- Chave 1: deepseek-v4-flash com reasoning (pensamento profundo)
- Chave 2: deepseek-v4-pro sem reasoning (fallback se a 1 der 429)
Troca automaticamente em caso de rate limit.
"""
import os
import threading
from datetime import datetime
from openai import OpenAI
from openai import RateLimitError


def _carregar_env():
    """Lê o arquivo .env manualmente, sem depender de python-dotenv."""
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    try:
        with open(env_path, encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#") and "=" in linha:
                    chave, _, valor = linha.partition("=")
                    os.environ.setdefault(chave.strip(), valor.strip())
    except FileNotFoundError:
        pass


_carregar_env()

_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Configuração de cada provedor: (chave, modelo, extra_body)
_PROVEDORES = [
    {
        "key":   os.getenv("NVIDIA_API_KEY_1", ""),
        "model": "deepseek-ai/deepseek-v4-flash",
        "extra": {
            "chat_template_kwargs": {
                "thinking": True,
                "reasoning_effort": "high",
            }
        },
        "reasoning": True,
    },
    {
        "key":   os.getenv("NVIDIA_API_KEY_2", ""),
        "model": "deepseek-ai/deepseek-v4-pro",
        "extra": {
            "chat_template_kwargs": {
                "thinking": False,
            }
        },
        "reasoning": False,
    },
]


def _system_prompt() -> str:
    agora       = datetime.now()
    data        = agora.strftime("%d/%m/%Y")
    hora        = agora.strftime("%H:%M")
    dias_semana = ["segunda-feira", "terça-feira", "quarta-feira",
                   "quinta-feira", "sexta-feira", "sábado", "domingo"]
    dia_semana  = dias_semana[agora.weekday()]
    return (
        "Você é o Biondi, um assistente pessoal inteligente, direto e amigável. "
        "Responda sempre em português do Brasil. "
        "Seja conciso: prefira respostas curtas e objetivas, mas completas. "
        "Quando o usuário pedir cálculos ou conversões, resolva diretamente. "
        f"Hoje é {dia_semana}, {data}, e o horário atual é {hora}."
    )


class GeminiChat:
    """
    Cliente de chat com fallback automático entre chaves/modelos.
    Se a chave 1 retornar 429, tenta a chave 2 automaticamente.
    """

    def __init__(self, nome_assistente: str = "Biondi"):
        self._nome      = nome_assistente
        self._historico: list[dict] = []
        # Cria um client OpenAI para cada provedor
        self._clients = [
            OpenAI(api_key=p["key"], base_url=_BASE_URL)
            for p in _PROVEDORES
        ]

    # ------------------------------------------------------------------ #
    def enviar(self, mensagem: str,
               ao_responder=None,
               ao_erro=None,
               ao_reasoning=None,
               ao_provedor=None):
        """
        Envia a mensagem em uma thread separada.
        Tenta os provedores em ordem; usa o próximo se receber 429.

        ao_provedor(info: dict) — chamado antes da resposta com:
            {"chave": 1, "modelo": "deepseek-ai/...", "reasoning": True/False}
        """
        def _tarefa():
            mensagens = [
                {"role": "system", "content": _system_prompt()},
                *self._historico,
                {"role": "user", "content": mensagem},
            ]

            ultimo_erro = None

            for idx, provedor in enumerate(_PROVEDORES):
                try:
                    client = self._clients[idx]

                    completion = client.chat.completions.create(
                        model=provedor["model"],
                        messages=mensagens,
                        temperature=1,
                        top_p=0.95,
                        max_tokens=16384,
                        extra_body=provedor["extra"],
                        stream=False,
                    )

                    msg = completion.choices[0].message

                    # Notifica qual provedor respondeu
                    if ao_provedor:
                        ao_provedor({
                            "chave": idx + 1,
                            "modelo": provedor["model"],
                            "reasoning": provedor["reasoning"],
                        })

                    # Reasoning (só na chave 1)
                    if provedor["reasoning"] and ao_reasoning:
                        reasoning = (
                            getattr(msg, "reasoning", None)
                            or getattr(msg, "reasoning_content", None)
                        )
                        if reasoning:
                            ao_reasoning(reasoning)

                    texto = msg.content.strip()

                    # Salva no histórico
                    self._historico.append({"role": "user",      "content": mensagem})
                    self._historico.append({"role": "assistant", "content": texto})

                    if ao_responder:
                        ao_responder(texto)
                    return  # sucesso — para aqui

                except RateLimitError:
                    ultimo_erro = f"Chave {idx + 1} com rate limit, tentando fallback…"
                    continue

                except Exception as exc:
                    ultimo_erro = f"Erro ao contatar a IA: {exc}"
                    break

            # Todos os provedores falharam
            if ao_erro:
                ao_erro(ultimo_erro or "Todos os provedores falharam.")

        threading.Thread(target=_tarefa, daemon=True).start()

    # ------------------------------------------------------------------ #
    def limpar_historico(self):
        self._historico.clear()
