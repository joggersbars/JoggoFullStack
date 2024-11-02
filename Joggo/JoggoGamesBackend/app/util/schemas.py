# app/schemas.py

from pydantic import BaseModel

class UserData(BaseModel):
    username: str
    password: str  # 'bar' o 'jugador'

class UserId(UserData):
    id: int

class Jugador(BaseModel):
    id_partida: str
    apodo_jugador: str 

class FraseEntrada(Jugador):
    frase_jugador: str

class MensajeInicioPartida(BaseModel):
    mensaje_inicio: str
    id_partida: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PartidaCreate(BaseModel):
    juego: str