from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import models, schemas
from .auth import obtener_usuario_actual
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# ✅ Crear pedido
@router.post("/", response_model=schemas.PedidoOut)
def crear_pedido(
    pedido: schemas.PedidoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    nuevo = models.Pedido(
        **pedido.dict(),
        usuario_id=usuario.id,
        creado_por=usuario.nombre,
        creado_en=datetime.now()
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ✅ Listar pedidos con paginación y búsqueda opcional
@router.get("/", response_model=schemas.PaginatedPedidos)
def listar_pedidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    buscar: str = Query(None),
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    query = db.query(models.Pedido).filter(models.Pedido.usuario_id == usuario.id)

    if buscar:
        buscar = f"%{buscar.lower()}%"
        query = query.filter(models.Pedido.cliente.ilike(buscar))

    total = query.count()
    pedidos = query.offset(skip).limit(limit).all()

    return {
        "pedidos": pedidos,
        "totalPaginas": (total + limit - 1) // limit,
        "paginaActual": (skip // limit) + 1
    }

# ✅ Obtener un pedido específico
@router.get("/{id}", response_model=schemas.PedidoOut)
def obtener_pedido(
    id: int,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == id,
        models.Pedido.usuario_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    return pedido

# ✅ Actualizar un pedido
@router.put("/{id}", response_model=schemas.PedidoOut)
def actualizar_pedido(
    id: int,
    pedido_actualizado: schemas.PedidoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == id,
        models.Pedido.usuario_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    for campo, valor in pedido_actualizado.dict().items():
        setattr(pedido, campo, valor)

    # 🔍 Auditoría
    pedido.modificado_por = usuario.nombre
    pedido.fecha_modificacion = datetime.now()

    try:
        db.commit()
        db.refresh(pedido)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")

    return pedido

# ✅ Eliminar un pedido
@router.delete("/{id}", response_model=dict)
def eliminar_pedido(
    id: int,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == id,
        models.Pedido.usuario_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    db.delete(pedido)
    db.commit()

    return {"mensaje": "Pedido eliminado correctamente"}
