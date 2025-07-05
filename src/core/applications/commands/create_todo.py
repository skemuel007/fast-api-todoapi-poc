from dataclasses import dataclass

from src.core.applications.interfaces.event_bus import EventBus
from src.core.applications.interfaces.repositories import TodoRepository


@dataclass
class CreateTodoCommand:
    title: str
    description: str
    priority: str


class CreateTodoCommandHandler:
    def __init__(self, todo_repository: TodoRepository, event_bus: EventBus):
        self.todo_repository = todo_repository
        self.event_bus = event_bus

    async def handle(self, command: CreateTodoCommand):
        from src.core.domain.entities.todo import Todo
        from src.core.domain.value_objects.priority import Priority

        todo = Todo(title=command.title, description=command.description, priority=Priority(command.priority))
        await self.todo_repository.save(todo)

        from src.core.domain.events.todo_created_event import TodoCreatedEvent
        self.event_bus.publish(TodoCreatedEvent(todo_id=todo.id, title=todo.title)) # publish event

        return todo.id