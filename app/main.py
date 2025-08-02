from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ Importar el middleware de CORS

from .database import Base, engine
from .routers import auth, pedidos, usuarios  # ✅ Incluir el módulo usuarios

app = FastAPI()

# ✅ Habilitar CORS
origins = [
    "http://localhost:5173",
    "https://front-textil.vercel.app",  # 👈 Agrega aquí tu dominio de producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Dominios permitidos
    allow_credentials=True,         # Permitir envío de cookies/autenticación
    allow_methods=["*"],            # Métodos permitidos
    allow_headers=["*"],            # Headers permitidos
)

# ✅ Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

# ✅ Incluir los routers
app.include_router(auth.router)
app.include_router(pedidos.router)
app.include_router(usuarios.router)
