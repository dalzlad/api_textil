from pydantic import BaseModel
from typing import Optional
from datetime import date

class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioOut(UsuarioBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DatosToken(BaseModel):
    id: Optional[int] = None

class PedidoBase(BaseModel):
    cliente: str
    prenda: str
    cantidad: int
    fecha_entrega: date
    estado: Optional[str] = "pendiente"

class PedidoCreate(PedidoBase):
    pass

class PedidoOut(PedidoBase):
    id: int
    usuario_id: int
    class Config:
        orm_mode = True