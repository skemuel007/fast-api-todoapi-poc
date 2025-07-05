import uuid

from sqlalchemy import Column, String, Boolean, DateTime, Uuid, ARRAY
from sqlalchemy.ext.declarative import declarative_base
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

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(String), default=[])  # Store roles as a list of strings
    permissions = Column(ARRAY(String), default=[])  # Store permissions as a list of strings
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())