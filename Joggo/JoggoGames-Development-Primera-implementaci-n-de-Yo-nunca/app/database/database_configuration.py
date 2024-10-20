# app/database_configuration.py

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

DATABASE_URL = "sqlite://db.sqlite3"  # Cambia la URL según tu base de datos

def init_db(app):
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["app.util.model"]},
        generate_schemas=True,  # Generar esquemas automáticamente
        add_exception_handlers=True,
    )
