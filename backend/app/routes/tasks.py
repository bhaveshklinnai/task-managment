"""FastAPI routes for task management."""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.task import TaskCreate, TaskUpdate, Task, Statistics
from app.services import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task."""
    task_id, error = task_service.create_task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        assignee=task.assignee
    )
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return {
        "id": task_id,
        "message": "Task created successfully"
    }


@router.get("", status_code=200)
async def get_tasks(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None)
):
    """Get all tasks with optional search and filtering."""
    try:
        if search or status or priority:
            tasks, error = task_service.search_and_filter(
                search_term=search,
                status=status,
                priority=priority
            )
            if error:
                raise HTTPException(status_code=400, detail=error)
        else:
            tasks = task_service.get_all_tasks()
        
        # Convert ObjectId to string for JSON serialization
        for task in tasks:
            task['_id'] = str(task['_id'])
        
        return {"data": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", status_code=200)
async def get_statistics():
    """Get task statistics."""
    try:
        stats = task_service.calculate_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}", status_code=200)
async def get_task(task_id: str):
    """Get a single task by ID."""
    try:
        task = task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task['_id'] = str(task['_id'])
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{task_id}", status_code=200)
async def update_task(task_id: str, update_data: TaskUpdate):
    """Update a task."""
    try:
        # Filter out None values
        update_dict = update_data.model_dump(exclude_unset=True)
        
        success, error = task_service.update_task(task_id, update_dict)
        if not success:
            if error == "Task not found":
                raise HTTPException(status_code=404, detail=error)
            else:
                raise HTTPException(status_code=400, detail=error)
        
        return {"message": "Task updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """Delete a task."""
    try:
        success, error = task_service.delete_task(task_id)
        if not success:
            if error == "Task not found":
                raise HTTPException(status_code=404, detail=error)
            else:
                raise HTTPException(status_code=400, detail=error)
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
