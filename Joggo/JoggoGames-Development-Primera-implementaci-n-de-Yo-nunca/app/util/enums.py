# enums.py

from enum import Enum

class EstadoMaquina(Enum):
    INITIAL = "inicial"
    REGISTERED = "registrados"
    CREATED = "creada"
    JOINED = "unidos"
    STARTED = "iniciada"
    PLAYING = "jugando"
    FINALIZED = "finalizada"
    ERROR = "error"
