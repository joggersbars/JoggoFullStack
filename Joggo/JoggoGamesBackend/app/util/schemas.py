# app/schemas.py

from pydantic import BaseModel

class UserData(BaseModel):
    username: str
    password: str  # 'bar' o 'jugador'

class UserId(UserData):
    id: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PartidaCreate(BaseModel):
    juego: str