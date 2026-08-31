"""REST API routes.

Route handlers stay deliberately thin: they read the request, call the
matching core function in app/services/task_service.py, and return the result.
All business rules live in the service layer. Errors raised by the service are
translated into HTTP responses by the handlers registered in app/main.py.
"""

from typing import Optional

from fastapi import APIRouter, Query, Response

from app.models.task import Statistics, Task, TaskCreate, TaskListResponse, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=201)
async def create_task(payload: TaskCreate):
    """Create a task."""
    return task_service.create_task(
        title=payload.title,
        assignee=payload.assignee,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
    )


@router.get("", response_model=TaskListResponse)
async def get_tasks(
    search: Optional[str] = Query(None, description="Search by task title"),
    status: Optional[str] = Query(None, description="TODO, IN_PROGRESS or DONE"),
    priority: Optional[str] = Query(None, description="LOW, MEDIUM or HIGH"),
):
    """List tasks, optionally searched by title and filtered by status/priority."""
    tasks = task_service.search_and_filter(
        search=search, status=status, priority=priority
    )
    return {"count": len(tasks), "data": tasks}


@router.get("/stats", response_model=Statistics)
async def get_statistics():
    """Return task counts calculated from the database."""
    return task_service.calculate_statistics()


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Return a single task by id."""
    return task_service.get_task_by_id(task_id)


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, payload: TaskUpdate):
    """Update the supplied fields of a task."""
    return task_service.update_task(task_id, payload.model_dump(exclude_unset=True))


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """Delete a task."""
    task_service.delete_task(task_id)
    return Response(status_code=204)
