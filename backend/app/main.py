"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import DatabaseError, TaskNotFoundError, TaskValidationError
from app.routes import tasks

app = FastAPI(
    title="Task Management Dashboard API",
    description="REST API for managing a development team's tasks",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)


# --- Error handling ---
# The service layer raises plain Python exceptions; they are turned into
# meaningful HTTP responses here so the route handlers stay free of try/except.


@app.exception_handler(TaskValidationError)
async def handle_validation_error(request: Request, exc: TaskValidationError):
    """Invalid input (missing field, bad status/priority, malformed id)."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(TaskNotFoundError)
async def handle_not_found(request: Request, exc: TaskNotFoundError):
    """No task exists with the requested id."""
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(DatabaseError)
async def handle_database_error(request: Request, exc: DatabaseError):
    """The database was unreachable or rejected the operation."""
    return JSONResponse(status_code=503, content={"detail": str(exc)})


@app.get("/")
async def root():
    """API information."""
    return {"message": "Task Management Dashboard API", "docs": "/docs"}


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.BACKEND_PORT)
