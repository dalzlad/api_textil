from sqlalchemy.orm import Session
from . import models, schemas, routers

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed = routers.auth.encriptar_password(usuario.contrasena)
    nuevo = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        contrasena=hashed
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_usuario_por_username(db: Session, nombre: str):
    return db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()