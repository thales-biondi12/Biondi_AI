"""
Lógica do cronômetro e do timer — separada da UI.
"""
import time
import threading


class Cronometro:
    """Cronômetro progressivo com suporte a voltas (laps)."""

    def __init__(self):
        self._inicio:    float | None = None
        self._acumulado: float        = 0.0
        self._rodando:   bool         = False
        self._voltas:    list[float]  = []

    # ── Estado ────────────────────────────────────────────────────────── #
    @property
    def rodando(self) -> bool:
        return self._rodando

    @property
    def tempo_total(self) -> float:
        """Segundos decorridos (incluindo o trecho atual se estiver rodando)."""
        if self._rodando and self._inicio is not None:
            return self._acumulado + (time.monotonic() - self._inicio)
        return self._acumulado

    @property
    def voltas(self) -> list[float]:
        return list(self._voltas)

    # ── Controles ─────────────────────────────────────────────────────── #
    def iniciar(self):
        if not self._rodando:
            self._inicio  = time.monotonic()
            self._rodando = True

    def pausar(self):
        if self._rodando and self._inicio is not None:
            self._acumulado += time.monotonic() - self._inicio
            self._inicio     = None
            self._rodando    = False

    def resetar(self):
        self._inicio     = None
        self._acumulado  = 0.0
        self._rodando    = False
        self._voltas.clear()

    def volta(self):
        """Registra o tempo atual como uma volta."""
        self._voltas.append(self.tempo_total)

    # ── Formatação ────────────────────────────────────────────────────── #
    @staticmethod
    def formatar(segundos: float) -> str:
        s  = int(segundos)
        ms = int((segundos - s) * 100)
        h, rem = divmod(s, 3600)
        m, s   = divmod(rem, 60)
        if h:
            return f"{h:02d}:{m:02d}:{s:02d}.{ms:02d}"
        return f"{m:02d}:{s:02d}.{ms:02d}"


class Timer:
    """Temporizador regressivo com callback ao zerar."""

    def __init__(self, ao_zerar=None):
        self._duracao:   float        = 0.0
        self._inicio:    float | None = None
        self._acumulado: float        = 0.0   # quanto já foi contado
        self._rodando:   bool         = False
        self._ao_zerar                = ao_zerar
        self._thread:    threading.Thread | None = None

    # ── Estado ────────────────────────────────────────────────────────── #
    @property
    def rodando(self) -> bool:
        return self._rodando

    @property
    def restante(self) -> float:
        """Segundos restantes."""
        decorrido = self._acumulado
        if self._rodando and self._inicio is not None:
            decorrido += time.monotonic() - self._inicio
        r = self._duracao - decorrido
        return max(r, 0.0)

    # ── Controles ─────────────────────────────────────────────────────── #
    def configurar(self, horas: int, minutos: int, segundos: int):
        self._duracao    = horas * 3600 + minutos * 60 + segundos
        self._acumulado  = 0.0
        self._inicio     = None
        self._rodando    = False

    def iniciar(self):
        if not self._rodando and self.restante > 0:
            self._inicio  = time.monotonic()
            self._rodando = True
            self._thread  = threading.Thread(
                target=self._monitorar, daemon=True
            )
            self._thread.start()

    def pausar(self):
        if self._rodando and self._inicio is not None:
            self._acumulado += time.monotonic() - self._inicio
            self._inicio     = None
            self._rodando    = False

    def resetar(self):
        self._acumulado = 0.0
        self._inicio    = None
        self._rodando   = False

    # ── Interno ───────────────────────────────────────────────────────── #
    def _monitorar(self):
        """Thread que aguarda o timer zerar e dispara o callback."""
        while self._rodando and self.restante > 0:
            time.sleep(0.05)
        if self._rodando and self.restante <= 0:
            self._rodando = False
            if self._ao_zerar:
                self._ao_zerar()

    # ── Formatação ────────────────────────────────────────────────────── #
    @staticmethod
    def formatar(segundos: float) -> str:
        s  = int(segundos)
        h, rem = divmod(s, 3600)
        m, s   = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
