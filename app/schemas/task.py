from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
