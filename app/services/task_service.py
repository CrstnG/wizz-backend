from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, data: TaskCreate, owner: User) -> Task:
    """Crea una nueva tarea asociada al usuario autenticado."""
    task = Task(**data.model_dump(), owner_id=owner.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(
    db: Session,
    owner: User,
    status: str | None = None,
    skip: int = 0,
    limit: int = 20,
    order_by: str = "created_at",
) -> list[Task]:
    """
    Lista las tareas del usuario autenticado con soporte de:
    - Filtro por status (pending | in_progress | done)
    - Paginación (skip + limit)
    - Ordenamiento (created_at | updated_at | title)
    """
    allowed_order_fields = {"created_at", "updated_at", "title"}
    if order_by not in allowed_order_fields:
        order_by = "created_at"

    query = db.query(Task).filter(Task.owner_id == owner.id)

    if status:
        query = query.filter(Task.status == status)

    order_column = getattr(Task, order_by)
    query = query.order_by(order_column)

    return query.offset(skip).limit(limit).all()


def get_task_by_id(db: Session, task_id: int, owner: User) -> Task | None:
    """Retorna una tarea específica del usuario, o None si no existe."""
    return (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == owner.id)
        .first()
    )


def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    """Actualiza solo los campos enviados (PATCH parcial)."""
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    """Elimina una tarea de la base de datos."""
    db.delete(task)
    db.commit()
