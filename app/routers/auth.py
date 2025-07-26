from datetime import datetime, timedelta
from jose import JWTError, jwt
from app import schemas
from dotenv import load_dotenv
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Crea una instancia de router
router = APIRouter()

# Configuración del OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Cargar variables de entorno
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Función para obtener el usuario actual
@router.get("/usuario")
def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    # Aquí podrías hacer validación de token JWT o simplemente retornar un usuario simulado
    return {"username": "usuario_demo"}

# Crear un token JWT
def crear_token(data: dict):
    to_encode = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expira})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verificar el token JWT
@router.post("/verificar", response_model=schemas.DatosToken)
def verificar_token(token: str):
    credenciales_excepcion = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario: str = payload.get("user_id")
        if id_usuario is None:
            raise credenciales_excepcion
        return schemas.DatosToken(id=id_usuario)
    except JWTError:
        raise credenciales_excepcion
