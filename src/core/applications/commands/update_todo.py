from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateTodoCommand:
    todo_id: UUID
    title: str
    description: str
    priority: str


class UpdateTodoCommandHandler:
    def __init__(self, todo_repository, event_bus):
        self.todo_repository = todo_repository
        self.event_bus = event_bus

    async def handle(self, command: UpdateTodoCommand):

        from src.core.domain.entities.todo import Todo
        from src.core.domain.value_objects.priority import Priority

        existing_todo = await self.todo_repository.get(command.todo_id)

        if not existing_todo:
            return None

        existing_todo.update(
            title=command.title,
            description=command.description,
            priority=Priority(command.priority),
        )

        await self.todo_repository.update(existing_todo)
        return existing_todo.id