# app/routers.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pprint import pprint
from app.util.schemas import UserData, UserId
import app.util.crud as crud
from app.util.utils import generate_code, generate_unique_code
from app.database.database_configuration import Base

from sqlalchemy.orm import Session
from app.database.database_configuration import engine, localSession

from typing import List

import logging

Base.metadata.create_all(bind=engine)

_logger = logging.getLogger(__name__)

router = APIRouter()

# Configuración de HTTPBearer para manejar tokens personalizados
security = HTTPBearer()

def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints de Autenticación ---

@router.get('/')
async def root():
    return 'Hi, my name is FastAPI'

@router.get('/users', response_model=List[UserId])
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

@router.get('/users/{id: int}')
async def get_user(id, db: Session = Depends(get_db)):
    user_by_id = crud.get_user_by_id(db=db, id=id)
    if user_by_id:
        return user_by_id
    raise HTTPException(status_code=404, detail="Usuario no Encontrado")

@router.post("/register_user", tags=["Autenticación"], description="Register User")
async def register_user(usuario: UserData, db: Session = Depends(get_db)): # usuario: UsuarioCreate
    """
    Logear nuevo usuario bar y obtener un token de acceso.
    """
    check_name = crud.get_user_by_name(db=db, name=usuario.username)
    if check_name:
        raise HTTPException(status_code=400, detail="User already exists...")
    return crud.create_user(db=db, user=usuario)

@router.post("/login_user", tags=["Autenticación"], description="Usuario logging")
async def login_user(usuario: UserData, db: Session = Depends(get_db)):
    print("\nLoggeando usuario:")
    check_name = crud.get_user_by_name(db=db, name=usuario.username)
    if check_name == None:
        #raise HTTPException(status_code=400, detail="El usuario no está registrado")
        return JSONResponse(content={"message":"El usuario no está registrado"}, status_code=status.HTTP_200_OK)
    else:
        print("Entrando al servidor")
        _logger.info("Entrando en el servidor")
        if not usuario.username or not usuario.password:
            raise HTTPException(status_code=400, detail="Faltan datos obligatorios")
        response_dict = crud.login_user(db=db,username=usuario.username,password=usuario.password)
        print(f"Loggeando usuario {usuario.username}, con contraseña: {usuario.password}\n")
        _logger.info(f"Logging Usuario {usuario.username}: tipo: {usuario.password}")
        json_response = JSONResponse(content=response_dict, status_code=status.HTTP_201_CREATED)
        return json_response

@router.get('/crear_partida/{nombre_juego}', tags=['Creando partida'], description="Creando la partida")
async def crear_partida(nombre_juego: str, num_jugadores: int = 150, db: Session=Depends(get_db)):
    print("Entro")
    check_codes = crud.get_partida_codigos(db)
    codigo_juego = generate_unique_code(check_codes)
    nueva_partida = crud.create_partida(db=db,codigo_juego=codigo_juego,nombre_juego=nombre_juego,num_jugadores=num_jugadores)
    url_partida = f"http://localhost:8001/{nombre_juego.lower().replace(' ','_')}_{codigo_juego}"
    response = {'id_partida':codigo_juego, 'url_partida':url_partida}
    print("La partida tiene estos datos:")
    pprint(response)
    print("\n")
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)



