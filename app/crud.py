from sqlalchemy.orm import Session
from . import models, schemas, auth

def crear_usuario(db: Session, usuario: schemas.UsuarioCrear):
    hashed_password = auth.encriptar_password(usuario.password)
    nuevo_usuario = models.User(
        username=usuario.username,
        email=usuario.email,
        hashed_password=hashed_password
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def obtener_usuario_por_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
