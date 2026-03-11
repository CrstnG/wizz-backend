from fastapi import FastAPI

from app.db import Base, engine
from app.models import user, task  # noqa: F401 — importados para que SQLAlchemy registre los modelos
from app.routers import auth, tasks

# Crea todas las tablas en la base de datos al iniciar (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wizz Life — Task Manager API",
    description="API REST para gestión de tareas de equipo",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Wizz Life API running"}
