from dataclasses import dataclass
from uuid import UUID

@dataclass
class GetTodoQuery:
    todo_id: UUID

class GetTodoQueryHandler:
    def __init__(self, todo_repository):
        self.todo_repository = todo_repository

    async def handle(self, query: GetTodoQuery):
        todo = await self.todo_repository.get(query.todo_id)
        return todo