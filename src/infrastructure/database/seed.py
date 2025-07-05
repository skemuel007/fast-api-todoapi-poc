from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from src.core.domain.value_objects.Permission import Permission
from src.core.domain.value_objects.roles import Role
from src.infrastructure.database.models import User, TodoModel # Import your models
from src.infrastructure.authentication.auth_utils import hash_password


def seed_data(db: Session):
    """Seeds the database with initial data."""

    # Check if users already exist
    if db.query(User).count() == 0:
        # Create an admin user
        admin_hashed_password = hash_password("adminpassword") # Replace with a strong password
        admin_user = User(
            id=uuid4(),
            username="adminuser", # Replace with a username
            hashed_password=admin_hashed_password,
            roles=[Role.ADMIN],
            permissions=[Permission.CREATE_TODO, Permission.READ_TODO, Permission.UPDATE_TODO, Permission.DELETE_TODO],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created.")

        # Create a regular user
        user_hashed_password = hash_password("userpassword") # Replace with a strong password
        regular_user = User(
            id=uuid4(),
            username="regularuser", # Replace with a username
            hashed_password=user_hashed_password,
            roles=[Role.USER],
            permissions=[Permission.READ_TODO],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(regular_user)
        db.commit()
        print("Regular user created.")


    #Check if Todos already exist
    if db.query(TodoModel).count() == 0:
        # Create initial todos
        todo1 = TodoModel(
            id=uuid4(),
            title="Learn FastAPI",
            description="Complete the FastAPI tutorial",
            priority="high",
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        todo2 = TodoModel(
            id=uuid4(),
            title="Build Todo App",
            description="Implement the features of the Todo app",
            priority="medium",
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add_all([todo1, todo2])
        db.commit()
        print("Initial todos created.")

    print("Database seeding complete.")