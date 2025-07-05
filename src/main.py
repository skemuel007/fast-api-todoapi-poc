# Create tables if they don't exist (on app startup)
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import todo_routes, auth_routes
from src.infrastructure.database.database import engine
from src.infrastructure.database.models import Base
from src.infrastructure.event_bus.redis_event_bus import RedisEventBus
from src.infrastructure.logging.logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo App",
    description="A simple Todo API built with FastAPI, PostgreSQL, and Clean Architecture",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS configuration (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routers
app.include_router(todo_routes.router, prefix="/api/v1/todos", tags=["todos"])
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    # Initialize Redis event bus and start listening
    app.state.event_bus = RedisEventBus()
    asyncio.create_task(app.state.event_bus.listen())
    logger.info("Application started successfully")

@app.get("/health")
async def health_check():
    return {"status": "OK"}