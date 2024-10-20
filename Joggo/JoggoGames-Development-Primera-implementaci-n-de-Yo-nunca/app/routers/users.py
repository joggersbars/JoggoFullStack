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

@router.post("/register", response_model=TokenResponse, tags=["Autenticación"])
async def register(usuario: UsuarioCreate):
    """
    Registrar un nuevo usuario (bar o jugador) y obtener un token de acceso.
    """
    
    existing_usuario = await Usuario.filter(nombre=usuario.nombre).first()
    if existing_usuario:
        raise HTTPException(status_code=400, detail="El nombre ya existe, elige otro.")
    
    # Crear el usuario; el token se genera automáticamente mediante el default en el modelo
    usuario_obj = await Usuario.create(nombre=usuario.nombre, tipo=usuario.tipo)
    _logger.info(f"Logging Usuario {usuario.nombre}: tipo: {usuario.tipo}")
     # Crear la respuesta y establecer la cookie
    response = JSONResponse(content={"access_token": usuario_obj.token, "token_type": "bearer"})
    response.set_cookie(
        key="access_token",
        value=usuario_obj.token,
        httponly=True,
        secure=True,  # Establece en True en producción
        samesite="lax",  # Ajusta según tus necesidades
    )
    return response

# --- Dependencia para Obtener el Usuario Actual ---

async def get_current_usuario(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Usuario:
    """
    Extraer y verificar el usuario actual a partir del token proporcionado en las cabeceras de autorización.
    """
    token = credentials.credentials
    try:
        usuario = await Usuario.get(token=token)
        return usuario
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- Endpoints para Partidas ---

@router.post("/partida/", response_model=Partida_Pydantic, tags=["Partidas"])
async def crear_partida(partida: PartidaCreate, current_usuario: Usuario = Depends(get_current_usuario)):
    """
    Crear una nueva partida. Solo usuarios de tipo 'bar' pueden crear partidas.
    """
    if current_usuario.tipo != 'bar':
        raise HTTPException(status_code=403, detail="Solo los bares pueden crear partidas.")
    
    partida_obj = await Partida.create(juego=partida.juego, bar=current_usuario)
    # Generar la URL para unirse a la partida
    partida_obj.codigo_qr = f"http://localhost:8000/unirse/{partida_obj.id}"
    await partida_obj.save()
    
    return await Partida_Pydantic.from_tortoise_orm(partida_obj)

@router.post("/unirse/{partida_id}", response_model=dict, tags=["Partidas"])
async def unirse_partida(partida_id: UUID, current_usuario: Usuario = Depends(get_current_usuario)):
    """
    Unirse a una partida existente.
    """
    try:
        partida = await Partida.get(id=partida_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")
    
    if partida.estado != 'esperando':
        raise HTTPException(status_code=400, detail="No es posible unirse a esta partida.")
    
    if current_usuario not in await partida.jugadores.all():
        await partida.jugadores.add(current_usuario)
    
    return {"message": "Usuario unido a la partida"}

@router.post("/partida/{partida_id}/iniciar", response_model=dict, tags=["Partidas"])
async def iniciar_partida(partida_id: UUID, current_usuario: Usuario = Depends(get_current_usuario)):
    """
    Iniciar una partida. Solo el bar que creó la partida puede iniciarla.
    """
    try:
        partida = await Partida.get(id=partida_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")
    
    if partida.bar_id != current_usuario.id:
        raise HTTPException(status_code=403, detail="Solo el bar que creó la partida puede iniciarla.")
    
    if partida.estado != 'esperando':
        raise HTTPException(status_code=400, detail="La partida ya ha sido iniciada.")
    
    partida.estado = 'iniciada'
    await partida.save()
    
    return {"message": "Partida iniciada"}

# --- Endpoints para Frases ---

@router.post("/partida/{partida_id}/frase", response_model=Frase_Pydantic, tags=["Frases"])
async def enviar_frase(partida_id: UUID, frase_in: FraseIn_Pydantic, current_usuario: Usuario = Depends(get_current_usuario)):
    """
    Enviar una frase de "Yo Nunca". Solo los jugadores de la partida pueden enviar frases.
    """
    try:
        partida = await Partida.get(id=partida_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")
    
    if partida.estado != 'iniciada':
        raise HTTPException(status_code=400, detail="No se pueden enviar frases en este momento.")
    
    if current_usuario not in await partida.jugadores.all():
        raise HTTPException(status_code=403, detail="No perteneces a esta partida.")
    
    frase = await Frase.create(**frase_in.dict(), autor=current_usuario, partida=partida)
    
    # Comprobar si todos han enviado su frase
    total_jugadores = await partida.jugadores.all().count()
    total_frases = await Frase.filter(partida=partida).count()
    if total_frases == total_jugadores:
        partida.estado = 'jugando'
        await partida.save()
    
    return await Frase_Pydantic.from_tortoise_orm(frase)

@router.get("/partida/{partida_id}/frase_actual", response_model=Frase_Pydantic, tags=["Frases"])
async def obtener_frase_actual(partida_id: UUID, current_usuario: Usuario = Depends(get_current_usuario)):
    """
    Obtener la frase actual de la partida. Solo el bar puede acceder a este endpoint.
    """
    try:
        partida = await Partida.get(id=partida_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")
    
    if partida.estado not in ['jugando', 'finalizada']:
        raise HTTPException(status_code=400, detail="La partida no ha comenzado o ya ha finalizado.")
    
    # Solo el bar puede obtener la frase actual
    if partida.bar_id != current_usuario.id:
        raise HTTPException(status_code=403, detail="Solo el bar puede ver la frase actual.")
    
    frases = await Frase.filter(partida=partida).order_by('fecha_creacion')
    
    if partida.current_frase_index < len(frases):
        frase_actual = frases[partida.current_frase_index]
        return await Frase_Pydantic.from_tortoise_orm(frase_actual)
    else:
        partida.estado = 'finalizada'
        await partida.save()
        raise HTTPException(status_code=404, detail="No hay más frases. La partida ha finalizado.")

# --- Endpoints para Respuestas ---

@router.post("/partida/{partida_id}/frase/{frase_id}/respuesta", response_model=Respuesta_Pydantic, tags=["Respuestas"])
async def enviar_respuesta(partida_id: UUID, frase_id: UUID, respuesta_in: RespuestaIn_Pydantic, current_usuario: Usuario = Depends(get_current_usuario)):
    """
    Enviar una respuesta a una frase. Solo los jugadores de la partida pueden enviar respuestas.
    """
    try:
        partida = await Partida.get(id=partida_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")
    
    if partida.estado != 'jugando':
        raise HTTPException(status_code=400, detail="No se pueden enviar respuestas en este momento.")
    
    try:
        frase = await Frase.get(id=frase_id, partida=partida)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Frase no encontrada en esta partida.")
    
    if current_usuario not in await partida.jugadores.all():
        raise HTTPException(status_code=403, detail="No perteneces a esta partida.")
    
    # Verificar si ya respondió
    existe_respuesta = await Respuesta.filter(frase=frase, usuario=current_usuario).exists()
    if existe_respuesta:
        raise HTTPException(status_code=400, detail="Ya has respondido a esta frase.")
    
    respuesta = await Respuesta.create(**respuesta_in.dict(), frase=frase, usuario=current_usuario)
    
    # Comprobar si todos han respondido
    total_jugadores = await partida.jugadores.all().count()
    total_respuestas = await Respuesta.filter(frase=frase).count()
    if total_respuestas == total_jugadores:
        # Avanzar a la siguiente frase
        partida.current_frase_index += 1
        await partida.save()
    
    return await Respuesta_Pydantic.from_tortoise_orm(respuesta)

# --- Endpoints para Resultados ---

@router.get("/partida/{partida_id}/resultados", response_model=List[dict], tags=["Resultados"])
async def obtener_resultados(partida_id: UUID, current_usuario: Usuario = Depends(get_current_usuario)):
    """
    Obtener los resultados finales de la partida. Solo el bar puede acceder a este endpoint.
    """
    try:
        partida = await Partida.get(id=partida_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Partida no encontrada.")
    
    if partida.estado != 'finalizada':
        raise HTTPException(status_code=400, detail="La partida aún no ha finalizado.")
    
    # Solo el bar puede obtener los resultados
    if partida.bar_id != current_usuario.id:
        raise HTTPException(status_code=403, detail="Solo el bar puede ver los resultados.")
    
    jugadores = await partida.jugadores.all()
    resultados = []
    for jugador in jugadores:
        hecho_count = await Respuesta.filter(usuario=jugador, hecho=True, frase__partida=partida).count()
        resultados.append({
            'usuario': jugador.nombre,
            'hecho': hecho_count
        })
    return resultados

# --- Endpoints Adicionales para Usuarios ---

@router.get("/usuario/partidas_jugadas", response_model=List[Partida_Pydantic], tags=["Usuarios"])
async def obtener_partidas_jugadas(current_usuario: Usuario = Depends(get_current_usuario)):
    """
    Obtener las partidas en las que el usuario ha jugado.
    """
    return await Partida_Pydantic.from_queryset(current_usuario.partidas_jugadas.all())

@router.get("/usuario/partidas_creadas", response_model=List[Partida_Pydantic], tags=["Usuarios"])
async def obtener_partidas_creadas(current_usuario: Usuario = Depends(get_current_usuario)):
    """
    Obtener las partidas creadas por el usuario.
    """
    if current_usuario.tipo != 'bar':
        raise HTTPException(status_code=403, detail="Solo los bares pueden tener partidas creadas.")
    return await Partida_Pydantic.from_queryset(current_usuario.partidas_creadas.all())