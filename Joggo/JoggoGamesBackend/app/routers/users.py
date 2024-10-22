# app/routers.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.util.model import (
    Usuario, Partida, Frase, Respuesta,
    Usuario_Pydantic,
    UsuarioIn_Pydantic,
    Partida_Pydantic,
    PartidaIn_Pydantic,
    Frase_Pydantic,
    FraseIn_Pydantic,
    Respuesta_Pydantic,
    RespuestaIn_Pydantic
)
from app.util.schemas import UsuarioCreate, TokenResponse, PartidaCreate
import logging
import json
import sqlalchemy
from tortoise.exceptions import DoesNotExist
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from uuid import UUID

_logger = logging.getLogger(__name__)

router = APIRouter()

# Configuración de HTTPBearer para manejar tokens personalizados
security = HTTPBearer()

# --- Endpoints de Autenticación ---

@router.post("/login_user", tags=["Autenticación"], description="Login User")
async def login_user(usuario: UsuarioCreate): # usuario: UsuarioCreate
    """
    Logear nuevo usuario bar y obtener un token de acceso.
    """
    print(f"Usuario: {usuario.username} y contraseña: {usuario.password}")
    _logger.info("Entrando en el servidor")
    if not usuario.username or not usuario.password:
        raise HTTPException(status_code=400, detail="Faltan datos obligatorios")
    _logger.info(f"Logging Usuario {usuario.username}: tipo: {usuario.password}")

    response_dict = {"message":"Bienvenido"}
    json_response = JSONResponse(content=response_dict, status_code=status.HTTP_201_CREATED)
    return json_response



