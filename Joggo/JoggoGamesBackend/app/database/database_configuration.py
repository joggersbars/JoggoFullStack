from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed
import os, time

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DIALECT = os.getenv('DB_DIALECT')
DB_USER = os.getenv('DB_USER')

URL_CONNECTION = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

@retry(stop=stop_after_attempt(10), wait=wait_fixed(5))
def get_engine():
    return create_engine(URL_CONNECTION)

engine = get_engine()

localSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()