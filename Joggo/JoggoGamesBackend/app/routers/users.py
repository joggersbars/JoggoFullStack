# app/routers.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pprint import pprint
from app.util.schemas import UserData, UserId, Jugador, FraseEntrada, MensajeInicioPartida, RespuestaJugador
import app.util.crud as crud
from app.util.utils import generate_code, generate_unique_code
from app.database.database_configuration import Base
from app.util.util_classes import Iterator
from sqlalchemy.orm import Session
from app.database.database_configuration import engine, localSession

from typing import List

import logging
import requests

Base.metadata.create_all(bind=engine)

_logger = logging.getLogger(__name__)

router = APIRouter()

iterator = Iterator()

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
        return JSONResponse(content={"message":"El usuario no está registrado"}, status_code=status.HTTP_404_NOT_FOUND)
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
    id_partida = generate_unique_code(check_codes)
    nueva_partida = crud.create_partida(db=db,id_partida=id_partida,nombre_juego=nombre_juego,num_jugadores=num_jugadores)
    url_partida = f"http://localhost:8001/{nombre_juego.lower().replace(' ','_')}_{id_partida}"
    response = {'id_partida':id_partida, 'url_partida':url_partida}
    print("La partida tiene estos datos:")
    pprint(response)
    print("\n")
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)

# Endpoint para crear jugador
@router.post('/crear_jugador', tags= ["Añadiendo Jugador"], description="Añadiendo jugador")
async def crear_jugador(jugador: Jugador, db: Session=Depends(get_db)):
    print("Llego un jugador\n")
    check_jugador = crud.get_jugador_by_nombre_and_codigo(db=db,apodo_jugador=jugador.apodo_jugador, id_partida=jugador.id_partida)
    if check_jugador != None:
        #raise HTTPException(status_code=400, detail="El usuario no está registrado")
        return JSONResponse(content={"message":"El nombre del jugador ya existe"}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        if not jugador.id_partida or not jugador.apodo_jugador:
            raise HTTPException(status_code=400, detail="Faltan datos obligatorios")
        crud.crear_jugador(db=db,apodo_jugador=jugador.apodo_jugador,id_partida=jugador.id_partida)
        response_jugador = {"message":"Jugador conectado correctamente"}
        json_response = JSONResponse(content=response_jugador, status_code=status.HTTP_201_CREATED)
        return json_response

# Endpoint para añadir frase al jugador correspondiente Joao me tiene que enviar Frase entrada(schemas.py)
@router.post('/añadir_frase', tags=['Add-ons'], description="Añadiendo frase de jugador")
async def anadiendo_frase(frase_entrada: FraseEntrada, db: Session=Depends(get_db)):
    print(f"Jugador: {frase_entrada.apodo_jugador}, Id Partida: {frase_entrada.id_partida}, frase: {frase_entrada.frase_jugador}")
    check_jugador = crud.get_jugador_by_nombre_and_codigo(db=db, apodo_jugador=frase_entrada.apodo_jugador, id_partida=frase_entrada.id_partida)
    if crear_jugador == None:
        return JSONResponse(content={"message":"Esa frase ya está cogida"}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        if not frase_entrada.frase_jugador:
            raise HTTPException(status_code=400, detail="Faltan la frase")
        crud.añadir_frase_a_jugador(db=db,apodo_jugador=frase_entrada.apodo_jugador, frase_jugador=frase_entrada.frase_jugador, id_partida=frase_entrada.id_partida)
        response_frase = {"message":"Frase añadida correctamente"}
        json_response = JSONResponse(content=response_frase, status_code=status.HTTP_201_CREATED)
        return json_response 

# Endpoint empezar_partida para sacar la cantidad de frases
@router.post('/empezar_partida', tags=["Empezar Partida"], description="Empezando la partida")
async def empezar_partida(message: MensajeInicioPartida, db: Session=Depends(get_db)):
    if message.mensaje_inicio == "vamos a empezar partida yo nunca":
        iterator.establecer_cantidad_frases(cantidad_frases=int(crud.obtener_cantidad_frases_codigo(db=db, id_partida=message.id_partida)))
        iterator.mostrar_cantidad_frases()
    else:
        raise HTTPException(status_code=400, detail="El mensaje es incorrecto")

# Endpoint para coger la frase que se mostrará por pantalla
@router.get('/coger_frase', tags=["Frases Juego"], description="Frases que se van a ir poniendo en la pantalla del bar")
async def coger_frase(id_partida: str, db: Session=Depends(get_db)):
    frase_pantalla = crud.get_frase_by_id_and_codigo(db=db,id=iterator.retornar_id(),id_partida=id_partida)
    iterator.incrementar_contador()
    response_frase_pantalla = {"frase":frase_pantalla}
    json_response = JSONResponse(content=response_frase_pantalla, status_code=status.HTTP_201_CREATED)
    return json_response

# Endpoint respuesta jugador
# @router.post('/recibir_respuesta',tags=["Respuestas Jugadores"], description="Las respuestas a las frases de yo nunca de los jugadores")
# async def recibir_respuesta(respuesta_jugador: RespuestaJugador, db: Session=Depends(get_db)):
#     check_jugador = crud.get_jugador_by_nombre_and_codigo(db=db, apodo_jugador=respuesta_jugador.apodo_jugador, id_partida=respuesta_jugador.id_partida)
#     if check_jugador:



