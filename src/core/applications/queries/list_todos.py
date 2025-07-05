from dataclasses import dataclass

from src.core.applications.interfaces.repositories import TodoRepository


@dataclass
class ListTodosQuery:
    pass

class ListTodosQueryHandler:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    async def handle(self, query: ListTodosQuery):
        return await self.todo_repository.list()