# auth.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app import schemas, models
from app.database import get_db

# Cargar variables de entorno
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

router = APIRouter()


# === FUNCIONES DE AUTENTICACIÓN ===

def encriptar_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def crear_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# === UTILIDAD PARA OBTENER USUARIO ACTUAL ===

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> schemas.UsuarioOut:
    cred_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise cred_ex
    except JWTError:
        raise cred_ex

    usuario = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if usuario is None:
        raise cred_ex

    return schemas.UsuarioOut.model_validate(usuario)


# === ENDPOINT: Obtener usuario actual desde el token ===

@router.get("/usuario", response_model=schemas.UsuarioOut)
def obtener_usuario_actual(usuario: schemas.UsuarioOut = Depends(get_current_user)):
    return usuario


# === ENDPOINT: Verificar un token manualmente ===

@router.post("/verificar", response_model=schemas.DatosToken)
def verificar_token_route(token: str):
    cred_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise cred_ex
        return schemas.DatosToken(id=user_id)
    except JWTError:
        raise cred_ex
