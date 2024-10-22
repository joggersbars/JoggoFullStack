# app/schemas.py

from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    username: str
    password: str  # 'bar' o 'jugador'

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PartidaCreate(BaseModel):
    juego: str