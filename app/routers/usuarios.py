from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, schemas, crud
from .auth import verificar_password, crear_token

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/registro", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    if crud.obtener_usuario_por_username(db, usuario.nombre):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe")
    return crud.crear_usuario(db, usuario)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    usuario = crud.obtener_usuario_por_username(db, form_data.username)
    if not usuario or not verificar_password(form_data.password, usuario.contrasena):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = crear_token({"sub": usuario.nombre, "user_id": usuario.id})
    return {"access_token": token, "token_type": "bearer"}
