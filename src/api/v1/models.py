from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from src.core.domain.entities.todo import Todo as TodoEntity
from src.core.domain.value_objects.priority import Priority


class TodoBase(BaseModel):
    title: str
    description: str
    priority: str  # Priority Enum as string

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: UUID
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, todo: TodoEntity):
        return cls(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            priority=todo.priority.value,
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )

class UserCreate(BaseModel):
    username: str
    password: str

class TokenRequest(BaseModel):
    username: str
    password: str