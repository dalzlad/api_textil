from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(contraseña: str):
    return pwd_context.hash(contraseña)
