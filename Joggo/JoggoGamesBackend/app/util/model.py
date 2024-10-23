from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database_configuration import Base

STRING_LENGTH = 30

# Tabla usuario cliente
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # Id del usuario
    username = Column(String(STRING_LENGTH), index=True, unique=True) # Username del usuario
    password = Column(String(STRING_LENGTH), index=True) # Contraseña del usuario
    # Pendiente: activo e inactivo

# Tabla jugadores partida
class Gamers(Base):
    __tablename__ = 'gamers'

    id = Column(Integer, primary_key=True, index=True) # Id del gamer
    gamer_name = Column(String(STRING_LENGTH)) # Nombre del gamer

     # Relación con las partidas
    games = relationship("GamePlayer", back_populates="gamers") 

# Tabla juego
class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, index=True) # Id de la partida
    game_code = Column(String(STRING_LENGTH)) # Código de la partida
    game_name = Column(String(STRING_LENGTH)) # Nombre del juego
    num_players = Column(Integer) # Número total de jugadores

    # Relación con jugadores conectados y frases
    players = relationship("GamePlayer", back_populates="game")
    phrases = relationship("GamePhrase", back_populates="game")

# Tabla Juego con las frases
# class GamePlayer(Base):
#     __tablename__ = 'game_players'

#     id = Column(Integer, primary_key=True, index=True) # Id identificativo del juego el jugador y la frase
#     game_id = Column(Integer, ForeignKey('game.game_code')) # Código de la partida
#     gamer_id = Column(Integer, ForeignKey('gamers.name')) # Nombre del jugador
#     phrase = Column(String(STRING_LENGTH))  # Frase que introduce el jugador

#     # Relación con las tablas de juegos y usuarios
#     game = relationship("Game", back_populates="players")
#     gamers = relationship("Gamers", back_populates="games")

# # Tabla de respuestas del juego
# class GamerResponse(Base):
#     __tablename__ = 'gamer_responses'

#     id = Column(Integer, primary_key=True, index=True) # Identificativo
#     game_phrase_text = Column(Integer) # Frase que ha salido en pantalla
#     player_id = Column(Integer, ForeignKey('gamers.id')) # Id del usuario
#     response = Column(String(STRING_LENGTH)) # Respuesta dle jugador. Ejemplo: "He hecho" o "No he hecho"

#     # Relación con frase y usuario
#     phrase = relationship("GamePhrase", back_populates="responses")
#     user = relationship("User")
