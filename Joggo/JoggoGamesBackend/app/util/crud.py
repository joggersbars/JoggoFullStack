from sqlalchemy.orm import Session

from app.util.model import User, Jugadores, Juego, Respuestas
from passlib.context import CryptContext
from app.util.schemas import UserData
from sqlalchemy import and_, func

# Configuración de passlib para hashear contraseñas de forma segura
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

### Funciones de usuarios ###

# Obtener todos los usuarios
def get_users(db: Session):
    return db.query(User).all()

# Obtener un usuario por su ID
def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

# Obtener un usuario por su nombre
def get_user_by_name(db: Session, name: str):
    return  db.query(User).filter(User.username == name).first()

# Crear un nuevo usuario    
def create_user(db: Session, user: UserData):
    hashed_password = user.password #pwd_context.hash(user.password)
    new_user = User(name=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Verificar la contraseña del usuario
def verify_user_password(db: Session, username: str, password: str):
    user = get_user_by_name(db, username)
    if password == user.password:
        return True
    return False

# Función de inicio de sesión de usuario
def login_user(db: Session, username: str, password: str):
    if verify_user_password(db, username, password):
        return {"message": "Bienvenido"}
    else:
        return {"message": "Nombre de usuario o contraseña incorrectos"}

### Funciones de Partidas (Games) ###
# Obtener una partida por su codigo
def get_partida_by_codigo(db: Session, id_partida: int):
    return db.query(Juego).filter(Juego.id_partida == id_partida).first()

# Obtener codigos de partidas existentes
def get_partida_codigos(db: Session):
    return db.query(Juego.id_partida)

# Crear una nueva partida
def create_partida(db: Session, id_partida: str, nombre_juego: str, num_jugadores: int):
    new_game = Juego(id_partida=id_partida, nombre_juego=nombre_juego, num_jugadores=num_jugadores, estado_juego="IDLE", num_jugadores_conectados=0)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

# Cambiar estado partida
def cambiar_estado_partida(db: Session, id_partida: str, estado_juego: str):
    juego = db.query(Juego).filter(Juego.id_partida==id_partida).first()
    juego.estado_juego = estado_juego
    db.commit()
    db.refresh(juego)
    return juego

# Consultar el estado de la partida
def consultar_estado_partida(db: Session, id_partida: str):
    return db.query(Juego.estado_juego).filter(Juego.id_partida == id_partida).first()

### Funciones de Jugadores en Partida ###
# Obtener jugador por nombre
def get_jugador_by_nombre_and_codigo(db: Session, apodo_jugador: str, id_partida: str):
    return db.query(Jugadores).filter(
        and_(
            Jugadores.apodo_jugador == apodo_jugador,
            Jugadores.id_partida == id_partida
        )
    ).first()

# Obtener Jugador por frase e id
def get_jugador_by_frase_and_codigo(db: Session, frase_jugador: str, id_partida: str):
    return db.query(Jugadores).filter(
        and_(
            Jugadores.apodo_jugador == frase_jugador,
            Jugadores.id_partida == id_partida
        )
    ).first()

# Aumentar contador de likes
def aumenta_likes_frase_de_jugador(db: Session, apodo_jugador: str, id_partida: str):
    jugador = get_jugador_by_nombre_and_codigo(db=db,apodo_jugador=apodo_jugador,id_partida=id_partida)
    print("Aver si entro aqui si quiera")
    if jugador:
        print("Aumento like")
        jugador.contador_like_frases += 1
        db.commit()
        db.refresh(jugador)
    return jugador

# Crear jugador y añadirlo a la base de datos
def crear_jugador(db: Session, apodo_jugador: str, id_partida: str):
    new_jugador = Jugadores(apodo_jugador=apodo_jugador, id_partida=id_partida, frase_jugador="", id_frase=0, contador_like_frases=0)
    db.add(new_jugador)
    db.commit()
    db.refresh(new_jugador)
    return new_jugador

# Aumentar la cantidad de jugadores conectados en la partida
def aumentar_jugador_conectado(db: Session, id_partida: str):
        
    partida = db.query(Juego).filter(Juego.id_partida==id_partida).first()

    # Aumentar en 1 el campo num_jugadores_conectados si la partida existe
    if partida:
        partida.num_jugadores_conectados += 1
        db.commit()
        db.refresh(partida)
    
    return partida

# Aumentar la cantidad de jugadores conectados en la partida
def aumentar_jugador_partida(db: Session, id_partida: str, apodo_jugador: str):
    jugador_existente = db.query(Jugadores).filter(
        and_(
            Jugadores.id_partida == id_partida,
            Jugadores.apodo_jugador == apodo_jugador
        )
    ).first()

    if jugador_existente:
        # El jugador ya está conectado, no incrementa el contador
        print(f"Jugador {apodo_jugador} ya está conectado en la partida {id_partida}.")
        return None
    
    partida = db.query(Juego).filter(Juego.id_partida==id_partida).first()

    # Aumentar en 1 el campo num_jugadores_conectados si la partida existe
    if partida:
        partida.num_jugadores += 1
        db.commit()
        db.refresh(partida)
    
    return partida

# Verificamos si todos los jugadores se han conectado
def verificar_jugadores_conectados(db: Session, id_partida: str) -> bool:
    # Obtener la partida específica
    partida = db.query(Juego).filter(Juego.id_partida == id_partida).first()
    
    # Comparar num_jugadores y num_jugadores_conectados
    if partida and partida.num_jugadores == partida.num_jugadores_conectados:
        return True
    return False

# Checkear cantidad de jugadores
def obtener_num_jugadores(db: Session, id_partida: str) -> int:
    # Obtener la partida específica
    partida = db.query(Juego).filter(Juego.id_partida == id_partida).first()
    
    # Devolver el número de jugadores, si la partida existe
    return partida.num_jugadores_conectados if partida else None

# Actualizar el número de jugadores en una partida
def actualizar_num_jugadores(db: Session, id_partida: str):
    # Contar la cantidad de jugadores asociados al id_partida en la tabla Jugadores
    num_jugadores = obtener_num_jugadores(db=db, id_partida=id_partida)
    print(num_jugadores)
    # Obtener la partida correspondiente en la tabla Juego
    partida = db.query(Juego).filter(Juego.id_partida == id_partida).first()
    
    # Actualizar el campo num_jugadores en la partida
    if partida:
        partida.num_jugadores = num_jugadores
        db.commit()
        db.refresh(partida)
    
    return partida, num_jugadores

# Añadir frase a jugador en la base de datos
def añadir_frase_a_jugador(db: Session, apodo_jugador: str, frase_jugador: str, id_partida: str):
    jugador = get_jugador_by_nombre_and_codigo(db=db,apodo_jugador=apodo_jugador,id_partida=id_partida)
    # Añadir la nueva frase al jugador
    jugador.frase_jugador = frase_jugador
    
    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(jugador)
    
    return jugador

def obtener_cantidad_frases_codigo(db: Session, id_partida: int):
    return db.query(func.count(Jugadores.frase_jugador)).filter(Jugadores.id_partida == id_partida).scalar()

def actualizar_id_frases_para_partida(db: Session, id_partida: str):
    # Obtiene todos los jugadores de la partida específica, ordenados por su ID
    jugadores = db.query(Jugadores).filter(Jugadores.id_partida == id_partida).order_by(Jugadores.id).all()
    
    # Itera y asigna un id_frase secuencial
    for index, jugador in enumerate(jugadores, start=1):
        jugador.id_frase = index  # Supón que has añadido una columna `id_frase` en la tabla
    
    # Guarda los cambios
    db.commit()

# Obtener frasen para ir mostrando por pantalla
def get_frase_by_id_and_codigo(db: Session, id_frase: int, id_partida: str):
    return db.query(Jugadores.frase_jugador).filter(
        and_(
            Jugadores.id_frase == id_frase,
            Jugadores.id_partida == id_partida
        )
    ).first()

# Crear respuesta jugador:
def crear_respuesta_jugador(db: Session, id_partida: str, apodo_jugador: str, respuesta_jugador: str):
    # Buscar si ya existe una entrada para el jugador y el código de partida
    respuesta_existente = db.query(Respuestas).filter(
        Respuestas.id_partida == id_partida,
        Respuestas.apodo_jugador == apodo_jugador,
    ).first()
    
    # Si existe y la respuesta es "si", incrementar respuesta_jugador
    if respuesta_existente:
        print(respuesta_jugador)
        if respuesta_jugador.lower() == "si":
            print(respuesta_existente.respuesta_jugador)
            respuesta_existente.respuesta_jugador = respuesta_existente.respuesta_jugador + 1
            db.commit()
            db.refresh(respuesta_existente)
            return respuesta_existente
        else:
            # Si la respuesta no es "si", se ignora o podrías manejarlo de otra forma
            return {"message": "Respuesta no almacenada porque no es 'si'."}
    else:
        # Si no existe, crear una nueva entrada
        new_respuesta = Respuestas(
            id_partida=id_partida,
            apodo_jugador=apodo_jugador,
            respuesta_jugador=1 if respuesta_jugador.lower() == "si" else 0
        )
        db.add(new_respuesta)
        db.commit()
        db.refresh(new_respuesta)
        return new_respuesta
    
def get_stats(db: Session, id_partida: str):
    return db.query(Respuestas.apodo_jugador, Respuestas.respuesta_jugador).filter(
        Respuestas.id_partida == id_partida
    ).order_by(Respuestas.respuesta_jugador.desc()).all()

def get_resultados_jugador(db: Session, id_partida: str, apodo_jugador: str):
    return db.query(Respuestas.respuesta_jugador).join(
        Jugadores, Respuestas.apodo_jugador == Jugadores.apodo_jugador
    ).filter(
        and_(
            Jugadores.id_partida == id_partida,
            Jugadores.apodo_jugador == apodo_jugador
        )
    ).first()

