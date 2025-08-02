from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    contrasena = Column(String, nullable=False)

    pedidos = relationship("Pedido", back_populates="usuario")

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False, index=True)
    prenda = Column(String, nullable=True, index=True)
    cantidad = Column(Integer, nullable=False)
    fecha_entrega = Column(DateTime, nullable=False)
    whatsapp = Column(String, nullable=True)
    valor = Column(Float, nullable=True)
    estado = Column(String, default="pendiente", nullable=False, index=True)

    # Auditoría
    creado_en = Column(DateTime, default=func.now())
    actualizado_en = Column(DateTime, default=func.now(), onupdate=func.now())
    creado_por = Column(String, nullable=True)

    eliminado = Column(Boolean, default=False)

    # Usuario relacionado
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="pedidos")
