# app/schemas.py

from pydantic import BaseModel

class UserData(BaseModel):
    username: str
    password: str  # 'bar' o 'jugador'

class UserId(UserData):
    id: int

class IdPartida(BaseModel):
    id_partida: str
    
class Jugador(BaseModel):
    id_partida: str
    apodo_jugador: str 

class FraseEntrada(Jugador):
    frase_jugador: str

class MensajeInicioPartida(BaseModel):
    mensaje_inicio: str
    id_partida: str

class RespuestaJugador(BaseModel):
    apodo_jugador: str
    id_partida: str
    respuesta_jugador: str