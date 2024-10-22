from sqlalchemy.orm import Session

from app.util.model import User
from passlib.context import CryptContext
from app.util.schemas import UserData

# Configuración de passlib
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

def get_user_by_name(db: Session, name: str):
    return  db.query(User).filter(User.username == name).first()

def create_user(db: Session, user: UserData):
    hashed_password = user.password #pwd_context.hash(user.password)
    new_user = User(name=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.flush(new_user)
    return new_user

def verify_user_password(db: Session, username: str, password: str):
    user = get_user_by_name(db, username)
    if password == user.password:
        return True
    return False

def login_user(db: Session, username: str, password: str):
    if verify_user_password(db, username, password):
        return {"message": "Bienvenido"}
    else:
        return {"error": "Nombre de usuario o contraseña incorrectos"}
