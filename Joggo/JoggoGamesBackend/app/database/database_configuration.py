from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os, time

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DIALECT = os.getenv('DB_DIALECT')
DB_USER = os.getenv('DB_USER')

URL_CONNECTION = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# engine = create_engine(URL_CONNECTION)
attempts = 10  # Aumenta el número de intentos
while attempts > 0:
    try:
        engine = create_engine(URL_CONNECTION)
        connection = engine.connect()
        print("Conexión a la base de datos exitosa")
        connection.close()
        break
    except OperationalError:
        attempts -= 1
        print(f"Intento de conexión fallido. Reintentando en 5 segundos...")
        time.sleep(30)
else:
    raise Exception("No se pudo conectar a la base de datos después de varios intentos")


localSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()