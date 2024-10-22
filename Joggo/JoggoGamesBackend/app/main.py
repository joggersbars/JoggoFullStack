# app/main.py
from fastapi import FastAPI
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users
import uvicorn

_logger = logging.getLogger(__name__)



def get_app():
    app = FastAPI()
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplaza con la URL de tu frontend http://localhost:8001/
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    app.include_router(users.router)
    return app
app = get_app()