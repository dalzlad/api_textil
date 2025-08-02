from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

# ---------------------------
# Usuario
# ---------------------------

class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioOut(UsuarioBase):
    id: int
    model_config = {"from_attributes": True}

# ---------------------------
# Token
# ---------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class DatosToken(BaseModel):
    id: Optional[int] = None

# ---------------------------
# Pedido
# ---------------------------

class PedidoBase(BaseModel):
    cliente: Optional[str] = Field(None, description="Nombre del cliente")
    prenda: Optional[str] = Field(None, description="Nombre de la prenda")
    cantidad: Optional[int] = Field(None, description="Cantidad de prendas")
    fecha_entrega: Optional[date] = Field(None, description="Fecha de entrega")
    whatsapp: Optional[str] = Field(None, description="Número de WhatsApp del cliente")
    valor: Optional[float] = Field(None, description="Valor del pedido")
    estado: Optional[str] = Field("pendiente", description="Estado del pedido")

class PedidoCreate(PedidoBase):
    pass

class PedidoOut(PedidoBase):
    id: int
    usuario_id: int
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]
    eliminado: Optional[bool] = False

    model_config = {"from_attributes": True}

class PaginatedPedidos(BaseModel):
    pedidos: List[PedidoOut]
    totalPaginas: int
    paginaActual: int