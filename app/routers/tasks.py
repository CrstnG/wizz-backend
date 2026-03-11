from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Crea una nueva tarea para el usuario autenticado."""
    return task_service.create_task(db, data, current_user)


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    status: Optional[str] = Query(None, description="Filtrar por estado: pending | in_progress | done"),
    skip: int = Query(0, ge=0, description="Número de registros a saltar (paginación)"),
    limit: int = Query(20, ge=1, le=100, description="Máximo de registros a retornar"),
    order_by: str = Query("created_at", description="Campo por el que ordenar: created_at | updated_at | title"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lista las tareas del usuario autenticado con filtros, paginación y ordenamiento."""
    return task_service.get_tasks(db, current_user, status, skip, limit, order_by)


@router.get("/{task_id}/", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtiene el detalle de una tarea específica."""
    task = task_service.get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task


@router.patch("/{task_id}/", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Actualiza parcialmente una tarea existente."""
    task = task_service.get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task_service.update_task(db, task, data)


@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Elimina una tarea existente."""
    task = task_service.get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    task_service.delete_task(db, task)
