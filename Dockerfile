
FROM python:3.11-slim-buster

WORKDIR /app

# Copy Poetry configuration
COPY pyproject.toml poetry.lock ./

# Copy the requirements.txt file
COPY requirements.txt ./

# Install Poetry - should have started with poetry but started with pip
# RUN pip install poetry

# Install dependencies
# RUN poetry install --no-root --no-interaction --no-ansi

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src
COPY .env ./
COPY alembic.ini ./
COPY migrations ./migrations

# Expose port
EXPOSE 8000

# Command to run the application
#CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]