"""
Lógica da calculadora — separada da UI para facilitar testes.
"""


class Calculadora:
    """Máquina de estados da calculadora."""

    def __init__(self):
        self._resetar()

    # ------------------------------------------------------------------ #
    def _resetar(self):
        self._valor_atual   = "0"
        self._valor_anterior = None
        self._operador       = None
        self._novo_numero    = True   # próximo dígito começa entrada nova
        self._resultado      = False  # acabou de pressionar =

    # ------------------------------------------------------------------ #
    # Propriedade pública
    @property
    def display(self) -> str:
        return self._valor_atual

    # ------------------------------------------------------------------ #
    def digito(self, d: str) -> str:
        if self._resultado:
            self._valor_atual = d
            self._resultado   = False
            self._novo_numero = False
        elif self._novo_numero:
            self._valor_atual = d
            self._novo_numero = False
        else:
            if d == "." and "." in self._valor_atual:
                return self._valor_atual
            if self._valor_atual == "0" and d != ".":
                self._valor_atual = d
            else:
                self._valor_atual += d
        return self._valor_atual

    # ------------------------------------------------------------------ #
    def operador(self, op: str) -> str:
        """Registra operador. Se já havia um pendente, calcula antes."""
        if self._operador and not self._novo_numero:
            self._calcular()
        self._valor_anterior = float(self._valor_atual)
        self._operador       = op
        self._novo_numero    = True
        self._resultado      = False
        return self._valor_atual

    # ------------------------------------------------------------------ #
    def igual(self) -> str:
        if self._operador and self._valor_anterior is not None:
            self._calcular()
            self._operador       = None
            self._valor_anterior = None
            self._resultado      = True
        return self._valor_atual

    # ------------------------------------------------------------------ #
    def _calcular(self):
        try:
            a = self._valor_anterior
            b = float(self._valor_atual)
            if self._operador == "+":
                r = a + b
            elif self._operador == "−":
                r = a - b
            elif self._operador == "×":
                r = a * b
            elif self._operador == "÷":
                if b == 0:
                    self._valor_atual = "Erro"
                    return
                r = a / b
            else:
                return
            # Remove .0 desnecessário
            self._valor_atual = (
                str(int(r)) if r == int(r) and abs(r) < 1e15 else str(r)
            )
        except Exception:
            self._valor_atual = "Erro"

    # ------------------------------------------------------------------ #
    def backspace(self) -> str:
        if self._valor_atual not in ("0", "Erro") and len(self._valor_atual) > 1:
            self._valor_atual = self._valor_atual[:-1]
        else:
            self._valor_atual = "0"
        return self._valor_atual

    def limpar(self) -> str:
        self._resetar()
        return self._valor_atual

    def limpar_entrada(self) -> str:
        self._valor_atual = "0"
        self._novo_numero = True
        return self._valor_atual

    def porcentagem(self) -> str:
        try:
            v = float(self._valor_atual)
            if self._valor_anterior is not None:
                v = self._valor_anterior * v / 100
            else:
                v = v / 100
            self._valor_atual = (
                str(int(v)) if v == int(v) and abs(v) < 1e15 else str(v)
            )
        except Exception:
            self._valor_atual = "Erro"
        self._novo_numero = True
        return self._valor_atual

    def inverter_sinal(self) -> str:
        try:
            v = float(self._valor_atual)
            v = -v
            self._valor_atual = (
                str(int(v)) if v == int(v) and abs(v) < 1e15 else str(v)
            )
        except Exception:
            pass
        return self._valor_atual
