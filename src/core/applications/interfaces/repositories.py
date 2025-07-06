from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.core.domain.entities.todo import Todo

class TodoRepository(ABC):
    @abstractmethod
    async def create(self, todo: Todo) -> Todo:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> Todo:
        pass

    @abstractmethod
    async def update(self, todo: Todo) -> Todo:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        pass

    @abstractmethod
    async def list(self, offset: int = 0, limit: int = 10) -> List[Todo]:
        pass

    @abstractmethod
    async def list_all(self) -> list[Todo]:
        pass