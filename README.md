# Todo API with FastAPI, PostgreSQL, Clean Architecture, DDD, and CQRS

This project is a Todo API built using FastAPI, PostgreSQL, and implementing Clean Architecture, Domain-Driven Design (DDD), and Command Query Responsibility Segregation (CQRS) principles. It also includes logging, authentication, request validation, domain events, and comprehensive unit tests.

## Features

*   **Clean Architecture:** Separates concerns into distinct layers (Core, Application, Infrastructure, API) for maintainability and testability.
*   **Domain-Driven Design (DDD):** Focuses on the core domain logic, defining Entities, Value Objects, and Domain Events.
*   **Command Query Responsibility Segregation (CQRS):** Separates read and write operations into distinct models, improving performance and scalability.
*   **FastAPI:** A modern, high-performance, web framework for building APIs with Python.
*   **PostgreSQL:** A robust, open-source relational database.
*   **Authentication:** JWT-based authentication for secure access to the API.
*   **Request Validation:** Pydantic models for request validation and data serialization.
*   **Domain Events:**  Uses domain events to trigger actions in response to changes in the domain.
*   **Logging:** Configured logging for debugging and monitoring.
*   **Swagger/OpenAPI:**  Automatically generated API documentation using Swagger UI.
*   **Unit Tests:**  Comprehensive unit tests for core domain logic, infrastructure components, and API endpoints.
*   **Dockerized:**  Easy to deploy using Docker and Docker Compose.
*   **Alembic:** Database migrations for managing schema changes.

## Architecture

The project is structured as follows:

*   **`src/core/`:** Contains the core domain logic.
    *   **`domain/`:** Entities, Value Objects, Domain Events.
    *   **`application/`:** Use Cases/Interactors, Commands, Queries, Interfaces.
*   **`src/infrastructure/`:** Implementation details for databases, external services, authentication, logging, and event bus.
*   **`src/api/`:** FastAPI endpoints and request/response models.
*   **`src/config.py`:** Configuration settings.
*   **`src/main.py`:** FastAPI app initialization.
*   **`tests/`:** Unit tests.
*   **`Dockerfile`:** Dockerfile for containerizing the application.
*   **`docker-compose.yml`:** Docker Compose file for defining the services.
*   **`.env`:** Environment variables.
*   **`alembic.ini`:** Alembic configuration file.
*   **`pyproject.toml` (or `requirements.txt`):** Project dependencies.

## Requirements

*   Python 3.11+
*   Docker
*   Docker Compose (optional, but recommended)
*   Poetry (recommended for dependency management - alternative is pip)
*   PostgreSQL database
*   Redis (for event bus implementation)

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Configure Environment Variables:**

    Create a `.env` file based on the `.env` example:

    ```
    DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/yourdatabase
    POSTGRES_USER=youruser
    POSTGRES_PASSWORD=yourpassword
    POSTGRES_DB=yourdatabase
    SECRET_KEY=your_secret_key_here
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REDIS_HOST=localhost
    REDIS_PORT=6379
    ```

    Replace the placeholder values with your actual database and Redis credentials.  Generate a strong secret key for JWT.

3.  **Install Dependencies:**

    *   **Using Poetry (Recommended):**

        ```bash
        poetry install
        ```

    *   **Using pip:**

        ```bash
        pip install -r requirements.txt
        ```

4.  **Database Migrations:**

    a.  Ensure your database is running.

    b.  Configure `alembic.ini` with the correct `sqlalchemy.url`.

    c.  Run the database migrations:

        ```bash
        alembic upgrade head
        ```

5.  **Run the Application:**

    *   **Using Poetry:**

        ```bash
        poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
        ```

    *   **Using Python directly:**

        ```bash
        uvicorn src.main:app --host 0.0.0.0 --port 8000
        ```

6.  **Access the API:**

    Open your browser and navigate to:

    *   `http://localhost:8000/api/docs` for Swagger UI.
    *   `http://localhost:8000/api/redoc` for ReDoc documentation.

## Running with Docker Compose

1.  **Ensure Docker and Docker Compose are installed.**

2.  **Configure the `.env` file (as described above).**

3.  **Run Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    This will build and start the PostgreSQL, Redis, and FastAPI application containers.

4.  **Access the API:**

    The API will be accessible at `http://localhost:8000/api/docs` (or `/api/redoc`).

## Testing

To run the unit tests:

1.  **Ensure you have installed the development dependencies (if using poetry, it would be `poetry install --with dev`)**
2.  **Run Pytest:**

    ```bash
    pytest
    ```

    (You might need to specify the tests directory if pytest doesn't automatically find them.)

## API Endpoints

The API provides the following endpoints:

*   `POST /api/v1/todos/`: Create a new todo.
*   `GET /api/v1/todos/{todo_id}`: Get a specific todo by ID.
*   `PUT /api/v1/todos/{todo_id}`: Update a todo.
*   `DELETE /api/v1/todos/{todo_id}`: Delete a todo.
*   `GET /api/v1/todos/`: List all todos.
*   `POST /api/v1/auth/register`: Register a new user.
*   `POST /api/v1/auth/token`: Obtain a JWT token (login).
*   `GET /api/v1/auth/users/me`: Get the current user's information (requires authentication).

## Domain Events

The application uses domain events to trigger actions in response to changes in the domain.  For example, when a new todo is created, a `TodoCreated` event is published to a Redis-based event bus.

To handle domain events:

1.  Create an event handler function that takes the event data as input.
2.  Subscribe the handler to the event type using the `EventBus.subscribe` method.

## Switching to Poetry
```bash
pip install poetry
poetry init
poetry --version

cat requirements.txt | sed 's/==.*//g' | xargs -n 1 poetry add
```

## Running docker compose and exporting variables - Linux/MacOS and Windows
```bash
# Linux/MacOS
export POSTGRES_USER=your_postgres_user
export POSTGRES_PASSWORD=your_postgres_password
export POSTGRES_DB=your_postgres_db
export SECRET_KEY=your_secret_key
export REDIS_HOST=localhost
export REDIS_PORT=6379
export DATABASE_URL=postgresql://your_postgres_user:your_postgres_password@localhost:5432/your_postgres_db  #If DATABASE_URL is not defined, add it too
docker-compose up --build

# Windows
$env:POSTGRES_USER="your_postgres_user"
$env:POSTGRES_PASSWORD="your_postgres_password"
$env:POSTGRES_DB="your_postgres_db"
$env:SECRET_KEY="your_secret_key"
$env:REDIS_HOST="localhost"
$env:REDIS_PORT=6379
$env:DATABASE_URL="postgresql://your_postgres_user:your_postgres_password@localhost:5432/your_postgres_db" #If DATABASE_URL is not defined, add it too
docker-compose up --build
```

## Pass arguments to docker compose
```bash
docker-compose up -e POSTGRES_USER=your_postgres_user -e POSTGRES_PASSWORD=your_postgres_password -e POSTGRES_DB=your_postgres_db --buil
```

## Setting up alembic
```bash
alembic init alembic # initialize alembic
alembic init src/infrastructure/database # initialize alembic
```

## Running migrations
```bash
alembic revision --autogenerate -m "Initial migration

alembic -c alembic.ini revision --autogenerate -m "create_todos_table" 

alembic upgrade head

alembic -c alembic.ini downgrade -1
```

## Contributing

Contributions are welcome!  Please submit a pull request with your changes.  Make sure to include unit tests and follow the project's coding style.

## License

[MIT License](LICENSE)

