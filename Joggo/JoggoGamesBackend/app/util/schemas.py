# app/schemas.py

from pydantic import BaseModel

class UserData(BaseModel):
    username: str
    password: str  # 'bar' o 'jugador'

class UserId(UserData):
    id: int

class Jugador(BaseModel):
    codigo_juego: str
    nombre_jugador: str

class FraseEntrada(Jugador):
    frase_jugador: str

class MensajeInicioPartida(BaseModel):
    mensaje_inicio: str
    codigo_juego: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PartidaCreate(BaseModel):
    juego: str