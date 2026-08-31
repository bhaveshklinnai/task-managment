"""Pydantic models describing the shape of API requests and responses."""

from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Request body for creating a task."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=2000)
    status: str = Field(default="TODO")
    priority: str = Field(default="MEDIUM")
    assignee: str = Field(..., min_length=1, max_length=255)


class TaskUpdate(BaseModel):
    """Request body for updating a task. Every field is optional."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = Field(None, min_length=1, max_length=255)


class Task(BaseModel):
    """A task as returned by the API."""

    id: str
    title: str
    description: str
    status: str
    priority: str
    assignee: str
    created_date: Optional[str] = None
    updated_date: Optional[str] = None


class TaskListResponse(BaseModel):
    """A list of tasks plus the number returned."""

    count: int
    data: list[Task]


class Statistics(BaseModel):
    """Task counts calculated from the database."""

    total_tasks: int
    todo_count: int
    in_progress_count: int
    done_count: int
