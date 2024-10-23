from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database_configuration import Base

# Tabla usuario cliente
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # Id del usuario
    username = Column(String(30), index=True, unique=True) # Username del usuario
    password = Column(String(30), index=True) # Contraseña del usuario

    # Relación con las partidas
    games = relationship("GamePlayer", back_populates="user") #

# Tabla juego
class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True) # Id de la partida
    game_name = Column(String)
    num_players = Column(Integer)

    # Relación con jugadores conectados y frases
    players = relationship("GamePlayer", back_populates="game")
    phrases = relationship("GamePhrase", back_populates="game")

# Tabla Juego con las frases
class GamePlayer(Base):
    __tablename__ = 'game_players'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    phrase = Column(String)  # Frase que introduce el jugador

    # Relación con las tablas de juegos y usuarios
    game = relationship("Game", back_populates="players")
    user = relationship("User", back_populates="games")

class GamePhrase(Base):
    __tablename__ = 'game_phrases'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    phrase = Column(String)
    
    # Relación con las respuestas de los jugadores
    responses = relationship("GameResponse", back_populates="phrase")
    game = relationship("Game", back_populates="phrases")

class GameResponse(Base):
    __tablename__ = 'game_responses'

    id = Column(Integer, primary_key=True, index=True)
    game_phrase_id = Column(Integer, ForeignKey('game_phrases.id'))
    player_id = Column(Integer, ForeignKey('users.id'))
    response = Column(String)  # Ejemplo: "He hecho" o "No he hecho"

    # Relación con frase y usuario
    phrase = relationship("GamePhrase", back_populates="responses")
    user = relationship("User")
