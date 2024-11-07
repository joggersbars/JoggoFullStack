# app/main.py
from fastapi import FastAPI
import logging
import signal
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users
from app.database.database_configuration import engine
import uvicorn

_logger = logging.getLogger(__name__)

def get_app():
    origins = [
        "http://localhost:8001"  # Agrega cualquier otro origen que necesites permitir
    ]
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Reemplaza con la URL de tu frontend http://localhost:8001/
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(users.router)

    return app

# Creando aplicación
app = get_app()

# # Configuración de señales 
# def setup_signal_handlers():
#     loop = asyncio.get_running_loop()
#     for sig in (signal.SIGINT, signal.SIGTERM):
#         loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown_app()))

# async def shutdown_app():
#     await app.router.shutdown()
#     await engine.dispose()
#     _logger.info("Señal de cierre recibida. Conexiones cerradas")

# setup_signal_handlers()