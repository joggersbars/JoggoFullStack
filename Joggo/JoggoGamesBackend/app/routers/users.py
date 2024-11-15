# app/routers.py

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pprint import pprint
from app.util.schemas import UserData, UserId, Jugador, FraseEntrada, MensajeInicioPartida, RespuestaJugador, IdPartida
import app.util.crud as crud
from app.util.utils import generate_code, generate_unique_code
from app.database.database_configuration import Base
from app.util.util_classes import Iterator
from sqlalchemy.orm import Session
from app.database.database_configuration import engine, localSession

from typing import List
from dotenv import load_dotenv
import logging, os
import requests

Base.metadata.create_all(bind=engine)

_logger = logging.getLogger(__name__)

load_dotenv()

# Simula la autenticación
def is_authenticated(request: Request):
    return request.cookies.get("session_token") == "valid_token"

FRONTEND_URL = os.getenv('FRONTEND_URL')

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
async def login_user(usuario: UserData, response: Response, db: Session = Depends(get_db)):
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
        valid_user = crud.login_user(db=db,username=usuario.username,password=usuario.password)
        if valid_user.get("message") == "Bienvenido":
            _logger.info(f"Logging Usuario {usuario.username}: tipo: {usuario.password}")

            #token = "valid_token"  # Generar un token real en producción
            #response.set_cookie(key="auth_token", value=token, httponly=True, secure=True, path="/")
            
            # Logs servidor
            print(f"Loggeando usuario {usuario.username}, con contraseña: {usuario.password}\n")
            
            json_response = JSONResponse(content=valid_user, status_code=status.HTTP_201_CREATED)
        else:
            json_response = JSONResponse(content=valid_user, status_code=status.HTTP_201_CREATED)
        return json_response

@router.get('/crear_partida/{nombre_juego}', tags=['Creando partida'], description="Creando la partida")
async def crear_partida(nombre_juego: str, num_jugadores: int = 150, db: Session=Depends(get_db)):
    print("Entro")
    check_codes = crud.get_partida_codigos(db)
    id_partida = generate_unique_code(check_codes)
    nueva_partida = crud.create_partida(db=db,id_partida=id_partida,nombre_juego=nombre_juego,num_jugadores=num_jugadores)
    url_partida = f"{FRONTEND_URL}/{nombre_juego.lower().replace(' ','_')}_{id_partida}"
    response = {'id_partida':id_partida, 'url_partida':url_partida}
    print("La partida tiene estos datos:")
    pprint(response)
    print("\n")
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)

# Endpoint para crear jugador
@router.post('/crear_jugador', tags=["Añadiendo Jugador"], description="Añadiendo jugador")
async def crear_jugador(jugador: Jugador, db: Session = Depends(get_db)):
    print("Llego un jugador\n")
    check_jugador = crud.get_jugador_by_nombre_and_codigo(db=db, apodo_jugador=jugador.apodo_jugador, id_partida=jugador.id_partida)
    
    # Si el jugador ya existe, retorna la misma respuesta que cuando se crea exitosamente
    if check_jugador is not None:
        response_jugador = {"message": "Jugador conectado correctamente"}
        return JSONResponse(content=response_jugador, status_code=status.HTTP_201_CREATED)
    
    # Si falta algún dato obligatorio, lanza una excepción
    if not jugador.id_partida or not jugador.apodo_jugador:
        raise HTTPException(status_code=400, detail="Faltan datos obligatorios")
    
    # Si el jugador no existe, crea el jugador
    crud.crear_jugador(db=db, apodo_jugador=jugador.apodo_jugador, id_partida=jugador.id_partida)
    response_jugador = {"message": "Jugador conectado correctamente"}
    return JSONResponse(content=response_jugador, status_code=status.HTTP_201_CREATED)

    
# Endpoint para checkear si todos los jugadores se han conectado 
@router.get("/all_jugadores_conectados/{id_partida}", tags=["Checkeo Jugadores Conectados"], description="Checkeo de si todos los jugadores se han conectado")
async def all_jugadores_conectados(id_partida: str, db: Session=Depends(get_db)):
    respuesta_booleana = crud.verificar_jugadores_conectados(db=db, id_partida=id_partida)
    print(respuesta_booleana)
    response_dict = {"check_connection":respuesta_booleana[0]}
    return JSONResponse(content = response_dict, status_code = status.HTTP_201_CREATED)

# Endpoint para añadir frase al jugador correspondiente Joao me tiene que enviar Frase entrada(schemas.py)
@router.post('/añadir_frase', tags=['Add-ons'], description="Añadiendo frase de jugador")
async def anadiendo_frase(frase_entrada: FraseEntrada, db: Session=Depends(get_db)):
    print(f"Jugador: {frase_entrada.apodo_jugador}, Id Partida: {frase_entrada.id_partida}, frase: {frase_entrada.frase_jugador}")
    check_jugador = crud.get_jugador_by_nombre_and_codigo(db=db, apodo_jugador=frase_entrada.apodo_jugador, id_partida=frase_entrada.id_partida)
    if check_jugador == None:
        return JSONResponse(content={"message":"Esa frase ya está cogida"}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        if not frase_entrada.frase_jugador:
            raise HTTPException(status_code=400, detail="Faltan la frase")
        print(frase_entrada)
        crud.añadir_frase_a_jugador(db=db,apodo_jugador=frase_entrada.apodo_jugador, frase_jugador=frase_entrada.frase_jugador, id_partida=frase_entrada.id_partida)
        crud.aumentar_jugador_conectado(db=db, id_partida=frase_entrada.id_partida)
        response_frase = {"message":"Frase añadida correctamente"}
        json_response = JSONResponse(content=response_frase, status_code=status.HTTP_201_CREATED)
        return json_response 
    
# Endpoint para establecer indices numéricos a la frases de esa partida concreta
@router.post('/establecer_indices_frases', tags=["Indices Frases"], description= "Establecemos el orden iterativo de las frases de la partida")
async def establecer_indices_frases(id_partida: IdPartida, db: Session=Depends(get_db)):
    print(f"Estableciendo los indices en las frases de la partida: {id_partida.id_partida}\n")
    crud.actualizar_id_frases_para_partida(db=db,id_partida=id_partida.id_partida)
    crud.actualizar_num_jugadores(db=db, id_partida=id_partida.id_partida)
    crud.cambiar_estado_partida(db=db,id_partida=id_partida.id_partida, estado_juego="frases") 
    response_frase = {"message":"Indices añadidos correctamente"}
    json_response = JSONResponse(content=response_frase, status_code=status.HTTP_201_CREATED)
    return json_response

# Endpoint empezar_partida para sacar la cantidad de frases
@router.post('/empezar_partida', tags=["Empezar Partida"], description="Empezando la partida")
async def empezar_partida(message: MensajeInicioPartida, db: Session=Depends(get_db)):
    if message.mensaje_inicio == "vamos a empezar partida yo nunca":
        iterator.establecer_cantidad_frases(cantidad_frases=int(crud.obtener_cantidad_frases_codigo(db=db, id_partida=message.id_partida)))
        iterator.mostrar_cantidad_frases()
        crud.cambiar_estado_partida(db=db,id_partida=message.id_partida,estado_juego="comenzado")
        _, num_jugadores = crud.actualizar_num_jugadores(db=db, id_partida=message.id_partida)
        print(f"El número de jugadores es:{num_jugadores}")
    else:
        raise HTTPException(status_code=400, detail="El mensaje es incorrecto")

# Endpoint para checkear el estado de la partida
@router.get("/game/status/{id_partida}", tags = ["Checkear el estado de la partida"], description="Los jugadores checkean el estado de la partida")
async def check_status_partida(id_partida: str, db: Session=Depends(get_db)):
    estado = crud.consultar_estado_partida(db=db,id_partida=id_partida)
    print(estado)
    response_dict = {"id_partida": id_partida, "estado": estado[0]}
    return JSONResponse(content=response_dict, status_code=status.HTTP_201_CREATED)

# Endpoint para coger la frase que se mostrará por pantalla
@router.post('/coger_frase', tags=["Frases Juego"], description="Frases que se van a ir poniendo en la pantalla del bar")
async def coger_frase(id_partida: IdPartida, db: Session=Depends(get_db)):
    frase_pantalla = crud.get_frase_by_id_and_codigo(db=db,id_frase=iterator.retornar_id(),id_partida=id_partida.id_partida)
    print(f"La frase que se va enviar:{frase_pantalla}")
    if iterator.contador != 0 or frase_pantalla != None:
        response_frase_pantalla = {"frase": str(frase_pantalla[0])}
        iterator.frase_actual = response_frase_pantalla["frase"]
    else:
        response_frase_pantalla = {"frase": "Fin_frases"}
    json_response = JSONResponse(content=response_frase_pantalla, status_code=status.HTTP_201_CREATED)
    iterator.incrementar_contador()
    return json_response

# Endpoint para que en la pantalla de los jugadores se muestra la frase de pantalla
@router.get("/coger_frase_jugador/{id_partida}", tags=["Frase jugador Pantalla"], description="Frases que se van a presentar en la pantalla de los jugadores")
async def coger_frase_jugador(id_partida: str):
    print(f"La frase actual es: {iterator.frase_actual}")
    response_frase = {"frase":iterator.frase_actual}
    return JSONResponse(content=response_frase, status_code=status.HTTP_201_CREATED)

# Endpoint respuesta jugador
@router.post('/recibir_respuesta/{id_partida}/{apodo_jugador}/{respuesta}', tags=["Respuestas Jugadores"], description="Las respuestas a las frases de yo nunca de los jugadores")
async def recibir_respuesta(id_partida: str, apodo_jugador: str, respuesta: str , db: Session = Depends(get_db)):
    try:
        check_jugador = crud.get_jugador_by_nombre_and_codigo(db=db, apodo_jugador=apodo_jugador, id_partida=id_partida)
        if check_jugador and check_jugador:
            print("Almacenando respuesta jugador")
            nueva_respuesta = crud.crear_respuesta_jugador(
                db=db,
                id_partida=id_partida,
                apodo_jugador=apodo_jugador,
                respuesta_jugador=respuesta
            )
            return {"message": "Respuesta almacenada correctamente"}
        else:
            raise HTTPException(status_code=400, detail="La respuesta falló al almacenarse")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para aumentar el like de una frase
@router.post("/enviar_like/{id_partida}/{frase}", tags=["Aumentar Like Frase"])
async def aumentar_like(id_partida: str, frase: str, db: Session=Depends(get_db)):
    crud.aumenta_likes_frase_de_jugador(db=db, frase_jugador=frase,id_partida=id_partida)
    response = {"like":"ok"}
    return JSONResponse(content=response,status_code=status.HTTP_201_CREATED)


# Mandar resultados
@router.get("/mandar_stats/{id_partida}", tags=["Mandando estadísticas"], description="Mandando estadísticas de la partida")
async def mandar_stats(id_partida: str, db: Session = Depends(get_db)):
    # Obtiene las estadísticas de la partida específica
    statistics = crud.get_stats(db=db, id_partida=id_partida)
    crud.cambiar_estado_partida(db=db,id_partida=id_partida,estado_juego="finalizado")
    # Convierte los resultados a un diccionario
    jugadores_dict = {resultado.apodo_jugador: resultado.respuesta_jugador for resultado in statistics}
    
    # Crea una respuesta JSON
    return JSONResponse(content={"estadisticas": jugadores_dict},status_code=status.HTTP_201_CREATED)

# Endpoint para mandar a cada jugador su cantidad de sies
@router.get("/resultado_jugador/{id_partida}/{apodo_jugador}")
async def mandar_resultado_jugador(id_partida: str, apodo_jugador: str, db: Session=Depends(get_db)):
    resultado_jugador = crud.get_resultados_jugador(db=db, id_partida=id_partida, apodo_jugador=apodo_jugador)
    num_frases = crud.obtener_num_jugadores(db=db, id_partida=id_partida)
    print(resultado_jugador, num_frases)
    resultado_dict = {"result":resultado_jugador,"frases_totales":num_frases}
    return JSONResponse(content=resultado_dict, status_code=status.HTTP_201_CREATED)