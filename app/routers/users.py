from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, schemas, crud, auth

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/registro", response_model=schemas.UsuarioMostrar)
def registrar_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(database.SessionLocal)):
    db_user = crud.obtener_usuario_por_username(db, usuario.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return crud.crear_usuario(db, usuario)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.SessionLocal)):
    usuario = crud.obtener_usuario_por_username(db, form_data.username)
    if not usuario or not auth.verificar_password(form_data.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = auth.crear_token({"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}