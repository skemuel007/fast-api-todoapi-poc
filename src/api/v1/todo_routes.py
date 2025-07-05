from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.v1.models import TodoResponse, TodoCreate, TodoUpdate
from src.core.applications.commands.create_todo import CreateTodoCommandHandler, CreateTodoCommand
from src.core.applications.commands.delete_todo import DeleteTodoCommandHandler, DeleteTodoCommand
from src.core.applications.commands.update_todo import UpdateTodoCommandHandler, UpdateTodoCommand
from src.core.applications.queries.get_todo import GetTodoQueryHandler, GetTodoQuery
from src.core.applications.queries.list_todos import ListTodosQueryHandler, ListTodosQuery
from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.todo_repository import SQLAlchemyTodoRepository

router = APIRouter()

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyTodoRepository(db)
    event_bus = None  # Replace with actual Event Bus
    handler = CreateTodoCommandHandler(repo, event_bus)
    command = CreateTodoCommand(title=todo.title, description=todo.description, priority=todo.priority)
    todo_id = await handler.handle(command)
    get_handler = GetTodoQueryHandler(repo)
    query = GetTodoQuery(todo_id)
    created_todo = await get_handler.handle(query)

    if not created_todo:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve created todo")

    return TodoResponse.from_entity(created_todo)

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: UUID, db: Session = Depends(get_db)):
    repo = SQLAlchemyTodoRepository(db)
    handler = GetTodoQueryHandler(repo)
    query = GetTodoQuery(todo_id)
    todo = await handler.handle(query)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return TodoResponse.from_entity(todo)

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: UUID, todo: TodoUpdate, db: Session = Depends(get_db)):
    repo = SQLAlchemyTodoRepository(db)
    get_handler = GetTodoQueryHandler(repo)
    query = GetTodoQuery(todo_id)
    existing_todo = await get_handler.handle(query)
    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    handler = UpdateTodoCommandHandler(repo) # Replace with actual Event Bus
    command = UpdateTodoCommand(todo_id=todo_id, title=todo.title, description=todo.description, priority=todo.priority)
    updated_todo_id = await handler.handle(command)

    query = GetTodoQuery(updated_todo_id)
    updated_todo = await get_handler.handle(query)

    if not updated_todo:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve updated todo")

    return TodoResponse.from_entity(updated_todo)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID, db: Session = Depends(get_db)):
    repo = SQLAlchemyTodoRepository(db)
    handler = DeleteTodoCommandHandler(repo) # Replace with actual Event Bus
    command = DeleteTodoCommand(todo_id=todo_id)
    await handler.handle(command)
    return

@router.get("/", response_model=List[TodoResponse])
async def list_todos(db: Session = Depends(get_db)):
    repo = SQLAlchemyTodoRepository(db)
    handler = ListTodosQueryHandler(repo)
    query = ListTodosQuery()
    todos = await handler.handle(query)
    return [TodoResponse.from_entity(todo) for todo in todos]