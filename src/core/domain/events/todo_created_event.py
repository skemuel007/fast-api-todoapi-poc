from dataclasses import dataclass
from uuid import UUID


@dataclass
class TodoCreatedEvent:
    todo_id: UUID
    title: str