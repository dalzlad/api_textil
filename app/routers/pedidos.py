from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from .auth import obtener_usuario_actual
from app.database import get_db

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=schemas.PedidoOut)
def crear_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db), usuario=Depends(obtener_usuario_actual)):
    nuevo = models.Pedido(**pedido.dict(), usuario_id=usuario.id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[schemas.PedidoOut])
def listar_pedidos(db: Session = Depends(get_db), usuario=Depends(obtener_usuario_actual)):
    return db.query(models.Pedido).filter(models.Pedido.usuario_id == usuario.id).all()
