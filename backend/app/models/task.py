from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """Model for creating a new task."""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=2000)
    status: str = Field(default="TODO")
    priority: str = Field(default="MEDIUM")
    assignee: str = Field(..., min_length=1, max_length=255)


class TaskUpdate(BaseModel):
    """Model for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = Field(None, min_length=1, max_length=255)


class Task(BaseModel):
    """Model for a task response."""
    id: str = Field(alias="_id")
    title: str
    description: str
    status: str
    priority: str
    assignee: str
    created_date: datetime
    updated_date: datetime

    class Config:
        populate_by_name = True


class Statistics(BaseModel):
    """Model for task statistics."""
    total_tasks: int
    todo_count: int
    in_progress_count: int
    done_count: int
