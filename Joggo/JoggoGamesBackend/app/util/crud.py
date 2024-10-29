from sqlalchemy.orm import Session

from app.util.model import User, Jugadores, Juego
from passlib.context import CryptContext
from app.util.schemas import UserData

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
def get_partida_by_codigo(db: Session, codigo_juego: int):
    return db.query(Juego).filter(Juego.codigo_juego == codigo_juego).first()

# Obtener codigos de partidas existentes
def get_partida_codigos(db: Session):
    return db.query(Juego.codigo_juego)

# Crear una nueva partida
def create_partida(db: Session, codigo_juego: str, nombre_juego: str, num_jugadores: int):
    new_game = Juego(codigo_juego=codigo_juego, nombre_juego=nombre_juego, num_jugadores=num_jugadores)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

### Funciones de Jugadores en Partida ###
# Obtener jugador por nombre
def get_jugador_by_nombre(db: Session, nombre_jugador: str):
    return db.query(Jugadores).filter(Jugadores.nombre_jugador == nombre_jugador).first()

# Crear jugador y añadirlo a la base de datos
def crear_jugador(db: Session, nombre_jugador: str, codigo_juego: str):
    new_jugador = Jugadores(nombre_jugador=nombre_jugador, codigo_juego=codigo_juego, frase_jugador="")
    db.add(new_jugador)
    db.commit()
    db.refresh(new_jugador)
    return new_jugador

# Añadir frase a jugador en la base de datos
def añadir_frase_a_jugador(db: Session, nombre_jugador: str, frase_jugador: str):
    jugador = get_jugador_by_nombre(db=db,nombre_jugador=nombre_jugador)
    # Añadir la nueva frase al jugador
    jugador.frase_jugador = frase_jugador
    
    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(jugador)
    
    return jugador

# # Añadir un jugador a una partida
# def add_player_to_game(db: Session, game_id: int, user_id: int, phrase: str = None):
#     new_player = GamePlayer(game_id=game_id, user_id=user_id, phrase=phrase)
#     db.add(new_player)
#     db.commit()
#     db.refresh(new_player)
#     return new_player

# # Obtener jugadores de una partida
# def get_players_in_game(db: Session, game_id: int):
#     return db.query(GamePlayer).filter(GamePlayer.game_id == game_id).all()

# ### Funciones de Frases ###

# # Añadir una nueva frase a una partida
# def add_phrase_to_game(db: Session, game_id: int, phrase: str):
#     new_phrase = GamerPhrase(game_id=game_id, phrase=phrase)
#     db.add(new_phrase)
#     db.commit()
#     db.refresh(new_phrase)
#     return new_phrase

# # Obtener todas las frases de una partida
# def get_phrases_in_game(db: Session, game_id: int):
#     return db.query(GamePhrase).filter(GamePhrase.game_id == game_id).all()

# ### Funciones de Respuestas ###

# # Añadir una respuesta de un jugador a una frase
# def add_player_response(db: Session, game_phrase_id: int, player_id: int, response: str):
#     new_response = GameResponse(game_phrase_id=game_phrase_id, player_id=player_id, response=response)
#     db.add(new_response)
#     db.commit()
#     db.refresh(new_response)
#     return new_response

# # Obtener todas las respuestas de una frase
# def get_responses_for_phrase(db: Session, game_phrase_id: int):
#     return db.query(GameResponse).filter(GameResponse.game_phrase_id == game_phrase_id).all()