from typing import List
from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.core.applications.interfaces.repositories import TodoRepository
from src.core.domain.entities.todo import Todo
from src.infrastructure.database.models import TodoModel


class SQLAlchemyTodoRepository(TodoRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, todo: Todo):
        db_todo = TodoModel(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            priority=todo.priority.value,
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    async def get(self, id: UUID) -> Todo:
        try:
            db_todo = self.db.query(TodoModel).filter(TodoModel.id == id).one()
            return Todo(
                id=db_todo.id,
                title=db_todo.title,
                description=db_todo.description,
                priority=db_todo.priority,
                completed=db_todo.completed,
                created_at=db_todo.created_at,
                updated_at=db_todo.updated_at,
            )
        except NoResultFound:
            return None

    async def update(self, todo: Todo):
        db_todo =  self.db.query(TodoModel).filter(TodoModel.id == id).first()
        if db_todo:
            db_todo.title = todo.title
            db_todo.description = todo.description
            db_todo.priority = todo.priority.value
            db_todo.completed = todo.completed
            db_todo.updated_at = todo.updated_at
            self.db.commit()
            self.db.refresh(db_todo)
            return db_todo
        return None


    async def delete(self, id: UUID):
        db_todo =  self.db.query(TodoModel).filter(TodoModel.id == id).first()
        if db_todo:
            self.db.delete(db_todo)
            self.db.commit()

    async def list(self) -> List[Todo]:
        db_todos = self.db.query(TodoModel).all()
        todos = [
            Todo(
                id=db_todo.id,
                title=db_todo.title,
                description=db_todo.description,
                priority=db_todo.priority,
                completed=db_todo.completed,
                created_at=db_todo.created_at,
                updated_at=db_todo.updated_at,
            )
            for db_todo in db_todos
        ]
        return todos
