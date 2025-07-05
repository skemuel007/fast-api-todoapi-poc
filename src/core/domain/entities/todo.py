from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from src.core.domain.value_objects.priority import Priority


class Todo:

    id: UUID = field(default_factory=uuid4)
    title: str
    description: str
    priority: Priority = Priority.LOW
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def mark_completed(self):
        self.completed = True
        self.updated_at = datetime.utcnow()