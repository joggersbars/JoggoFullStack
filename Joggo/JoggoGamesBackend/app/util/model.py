# app/models.py
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid
import secrets

class Usuario(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    nombre = fields.CharField(max_length=50, unique=True, null=False)
    tipo = fields.CharField(max_length=20, default='jugador')  # 'bar' o 'jugador'
    token = fields.CharField(max_length=64, unique=True, null=False, default=lambda: secrets.token_hex(32))
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    partidas_creadas = fields.ReverseRelation["Partida"]
    partidas_jugadas = fields.ManyToManyRelation["Partida"]

class Partida(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    codigo_qr = fields.CharField(max_length=255, null=True)
    juego = fields.CharField(max_length=50)
    estado = fields.CharField(max_length=20, default='esperando')  # 'esperando', 'iniciada', 'finalizada'
    fecha_creacion = fields.DatetimeField(auto_now_add=True)
    bar = fields.ForeignKeyField('models.Usuario', related_name='partidas_creadas')
    jugadores = fields.ManyToManyField('models.Usuario', related_name='partidas_jugadas', through='partida_usuario')
    current_frase_index = fields.IntField(default=0)

class Frase(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    texto = fields.TextField()
    autor = fields.ForeignKeyField("models.Usuario", related_name="frases")
    partida = fields.ForeignKeyField("models.Partida", related_name="frases")
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

class Respuesta(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    frase = fields.ForeignKeyField("models.Frase", related_name="respuestas")
    usuario = fields.ForeignKeyField("models.Usuario", related_name="respuestas")
    hecho = fields.BooleanField()  # True si el jugador ha hecho lo indicado en la frase, False si no
    fecha_respuesta = fields.DatetimeField(auto_now_add=True)

# Generar modelos Pydantic
Usuario_Pydantic = pydantic_model_creator(Usuario, name="Usuario")
UsuarioIn_Pydantic = pydantic_model_creator(Usuario, name="UsuarioIn", exclude_readonly=True)
Partida_Pydantic = pydantic_model_creator(Partida, name="Partida")
PartidaIn_Pydantic = pydantic_model_creator(Partida, name="PartidaIn", exclude_readonly=True)
Frase_Pydantic = pydantic_model_creator(Frase, name="Frase")
FraseIn_Pydantic = pydantic_model_creator(Frase, name="FraseIn", exclude_readonly=True)
Respuesta_Pydantic = pydantic_model_creator(Respuesta, name="Respuesta")
RespuestaIn_Pydantic = pydantic_model_creator(Respuesta, name="RespuestaIn", exclude_readonly=True)
