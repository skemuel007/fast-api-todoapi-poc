import uuid

from sqlalchemy import Column, String, Boolean, DateTime, Uuid, ARRAY, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

Base = declarative_base()

class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="todos")
    tags = relationship("Tag", secondary="todo_tags", back_populates="todos")

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(String), default=[])  # Store roles as a list of strings
    permissions = Column(ARRAY(String), default=[])  # Store permissions as a list of strings
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    todos = relationship("TodoModel", back_populates="user")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    todos = relationship("TodoModel", secondary="todo_tags", back_populates="tags")

todo_tags = Table(
    "todo_tags",
    Base.metadata,
    Column("todo_id", Uuid(as_uuid=True), ForeignKey("todos.id"), primary_key=True),
    Column("tag_id", Uuid(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
)