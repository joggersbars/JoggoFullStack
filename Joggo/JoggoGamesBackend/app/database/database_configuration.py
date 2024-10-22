from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_CONNECTION = 'mysql+pysql://root:12345@localhost/test'

engine = create_engine(URL_CONNECTION)