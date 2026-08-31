"""Core business logic for task operations."""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from bson.objectid import ObjectId
from app.database.mongodb import db
from app.utils.validation import validate_task_data, validate_status, validate_priority


def create_task(
    title: str,
    description: str,
    status: str,
    priority: str,
    assignee: str
) -> Tuple[Optional[str], Optional[str]]:
    """
    Create a new task.
    Returns (task_id, error_message)
    """
    task_data = {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "assignee": assignee
    }
    
    is_valid, error_msg = validate_task_data(task_data)
    if not is_valid:
        return None, error_msg
    
    try:
        task_id = db.insert_task(task_data)
        return task_id, None
    except Exception as e:
        return None, f"Failed to create task: {str(e)}"


def get_all_tasks() -> List[Dict[str, Any]]:
    """Retrieve all tasks."""
    try:
        tasks = db.find_all_tasks()
        return tasks
    except Exception as e:
        raise Exception(f"Failed to retrieve tasks: {str(e)}")


def get_task_by_id(task_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single task by ID."""
    try:
        if not ObjectId.is_valid(task_id):
            return None
        task = db.find_task_by_id(task_id)
        return task
    except Exception:
        return None


def update_task(task_id: str, update_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Update a task.
    Returns (success, error_message)
    """
    # Validate the update data
    is_valid, error_msg = validate_task_data(update_data)
    if not is_valid:
        return False, error_msg
    
    try:
        if not ObjectId.is_valid(task_id):
            return False, "Invalid task ID"
        
        # Check if task exists
        existing_task = db.find_task_by_id(task_id)
        if not existing_task:
            return False, "Task not found"
        
        # Update the task
        success = db.update_task(task_id, update_data)
        if success:
            return True, None
        else:
            return False, "Failed to update task"
    except Exception as e:
        return False, f"Error updating task: {str(e)}"


def delete_task(task_id: str) -> Tuple[bool, Optional[str]]:
    """
    Delete a task.
    Returns (success, error_message)
    """
    try:
        if not ObjectId.is_valid(task_id):
            return False, "Invalid task ID"
        
        # Check if task exists
        existing_task = db.find_task_by_id(task_id)
        if not existing_task:
            return False, "Task not found"
        
        # Delete the task
        success = db.delete_task(task_id)
        if success:
            return True, None
        else:
            return False, "Failed to delete task"
    except Exception as e:
        return False, f"Error deleting task: {str(e)}"


def search_tasks(search_term: str) -> List[Dict[str, Any]]:
    """Search tasks by title."""
    try:
        if not search_term:
            return get_all_tasks()
        tasks = db.find_tasks_by_search(search_term)
        return tasks
    except Exception as e:
        raise Exception(f"Failed to search tasks: {str(e)}")


def filter_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Filter tasks by status and/or priority.
    Returns (tasks, error_message)
    """
    try:
        if status and not validate_status(status):
            return [], f"Invalid status: {status}"
        
        if priority and not validate_priority(priority):
            return [], f"Invalid priority: {priority}"
        
        tasks = db.find_tasks_with_filters(status=status, priority=priority)
        return tasks, None
    except Exception as e:
        return [], f"Failed to filter tasks: {str(e)}"


def search_and_filter(
    search_term: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Search and filter tasks combined.
    Returns (tasks, error_message)
    """
    try:
        if status and not validate_status(status):
            return [], f"Invalid status: {status}"
        
        if priority and not validate_priority(priority):
            return [], f"Invalid priority: {priority}"
        
        tasks = db.find_tasks_with_filters(
            search_term=search_term,
            status=status,
            priority=priority
        )
        return tasks, None
    except Exception as e:
        return [], f"Failed to search and filter tasks: {str(e)}"


def calculate_statistics() -> Dict[str, int]:
    """Calculate task statistics."""
    try:
        total = db.get_total_task_count()
        todo = db.get_task_count_by_status("TODO")
        in_progress = db.get_task_count_by_status("IN_PROGRESS")
        done = db.get_task_count_by_status("DONE")
        
        return {
            "total_tasks": total,
            "todo_count": todo,
            "in_progress_count": in_progress,
            "done_count": done
        }
    except Exception as e:
        raise Exception(f"Failed to calculate statistics: {str(e)}")
