from dataclasses import dataclass
from typing import List

from src.core.applications.interfaces.repositories import TodoRepository
from src.core.domain.entities.todo import Todo


@dataclass
class ListTodosQuery:
    pass

class ListTodosQueryHandler:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    async def handle(self, query: ListTodosQuery) -> List[Todo]:
        return await self.todo_repository.list()


@dataclass
class PaginatedListTodosQuery:
    page: int = 1
    page_size: int = 10

class PaginatedListTodosQueryHandler:
    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    async def handle(self, query: PaginatedListTodosQuery) -> List[Todo]:
        offset = (query.page - 1) * query.page_size
        todos = await self.todo_repository.list(offset=offset, limit=query.page_size)
        return todos