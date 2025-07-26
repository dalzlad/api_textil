from datetime import datetime, timedelta
from jose import JWTError, jwt
from app import schemas
from dotenv import load_dotenv
import os
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    # Aquí podrías hacer validación de token JWT o simplemente retornar un usuario simulado
    return {"username": "usuario_demo"}


def crear_token(data: dict):
    to_encode = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expira})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(token: str, credenciales_excepcion):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario: str = payload.get("user_id")
        if id_usuario is None:
            raise credenciales_excepcion
        return schemas.DatosToken(id=id_usuario)
    except JWTError:
        raise credenciales_excepcion
