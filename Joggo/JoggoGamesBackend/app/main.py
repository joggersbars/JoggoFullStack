# app/main.py
from fastapi import FastAPI
import logging
from app.database.database_configuration import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users
import uvicorn

_logger = logging.getLogger(__name__)



def get_app():
    app = FastAPI()
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # Reemplaza con la URL de tu frontend http://localhost:8001/
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    init_db(app)
    app.include_router(users.router)
    return app
app = get_app()