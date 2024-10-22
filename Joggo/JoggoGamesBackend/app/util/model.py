from sqlalchemy import Column, String, Integer

from app.database.database_configuration import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), index=True, unique=True)
    password = Column(String(30), index=True)