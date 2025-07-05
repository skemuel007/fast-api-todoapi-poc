from dataclasses import dataclass
from uuid import UUID

from src.core.applications.interfaces.event_bus import EventBus
from src.core.applications.interfaces.repositories import TodoRepository


@dataclass
class DeleteTodoCommand:
    todo_id: UUID


class DeleteTodoCommandHandler:
    def __init__(self, todo_repository: TodoRepository, event_bus: EventBus = None):
        self.todo_repository = todo_repository
        self.event_bus = event_bus

    async def handle(self, command: DeleteTodoCommand):
        await self.todo_repository.delete(command.todo_id)