"""Core application logic.

Every task operation lives here as a plain, reusable Python function. These
functions do not depend on HTTP, FastAPI or React -- they can be called from a
script, a test or any other interface. The API layer simply calls them.

Errors are reported by raising the exceptions from app/exceptions.py; the API
layer maps them to HTTP status codes.
"""

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo.errors import PyMongoError

from app.database.mongodb import db
from app.exceptions import DatabaseError, TaskNotFoundError, TaskValidationError
from app.utils.validation import (
    validate_priority,
    validate_status,
    validate_task_data,
    validate_task_id,
)

TASK_FIELDS = ("title", "description", "status", "priority", "assignee")


def serialize_task(task: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a MongoDB document into a plain, JSON-friendly dictionary."""
    return {
        "id": str(task["_id"]),
        "title": task.get("title", ""),
        "description": task.get("description", ""),
        "status": task.get("status", ""),
        "priority": task.get("priority", ""),
        "assignee": task.get("assignee", ""),
        "created_date": _to_utc_iso(task.get("created_date")),
        "updated_date": _to_utc_iso(task.get("updated_date")),
    }


def _to_utc_iso(value: Optional[datetime]) -> Optional[str]:
    """Return a UTC ISO-8601 string so clients can convert to local time.

    Documents written before timezone support was added are stored as naive
    UTC, so they are labelled as UTC here rather than guessed at.
    """
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat()


def _build_query(
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a MongoDB query from a search term and filter values."""
    query: Dict[str, Any] = {}

    if search and search.strip():
        # Escape the term so characters like "(" or "*" are matched literally
        # instead of being treated as regular expression syntax.
        query["title"] = {"$regex": re.escape(search.strip()), "$options": "i"}

    if status:
        if not validate_status(status):
            raise TaskValidationError(f"Invalid status: {status}")
        query["status"] = status

    if priority:
        if not validate_priority(priority):
            raise TaskValidationError(f"Invalid priority: {priority}")
        query["priority"] = priority

    return query


def create_task(
    title: str,
    assignee: str,
    description: str = "",
    status: str = "TODO",
    priority: str = "MEDIUM",
) -> Dict[str, Any]:
    """Create a task and return it."""
    task_data = {
        "title": title.strip() if isinstance(title, str) else title,
        "description": description.strip() if isinstance(description, str) else description,
        "status": status,
        "priority": priority,
        "assignee": assignee.strip() if isinstance(assignee, str) else assignee,
    }

    is_valid, error = validate_task_data(task_data)
    if not is_valid:
        raise TaskValidationError(error)

    try:
        task_id = db.insert_task(task_data)
        created = db.find_task_by_id(task_id)
    except PyMongoError as exc:
        raise DatabaseError(f"Could not create task: {exc}") from exc

    return serialize_task(created)


def get_all_tasks() -> List[Dict[str, Any]]:
    """Return every task."""
    try:
        return [serialize_task(task) for task in db.find_tasks()]
    except PyMongoError as exc:
        raise DatabaseError(f"Could not retrieve tasks: {exc}") from exc


def get_task_by_id(task_id: str) -> Dict[str, Any]:
    """Return a single task by id."""
    if not validate_task_id(task_id):
        raise TaskValidationError(f"Invalid task ID: {task_id}")

    try:
        task = db.find_task_by_id(task_id)
    except PyMongoError as exc:
        raise DatabaseError(f"Could not retrieve task: {exc}") from exc

    if not task:
        raise TaskNotFoundError(f"No task found with ID {task_id}")

    return serialize_task(task)


def update_task(task_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update the supplied fields of a task and return the updated task."""
    if not validate_task_id(task_id):
        raise TaskValidationError(f"Invalid task ID: {task_id}")

    # Ignore anything that is not a real task field (id and dates are managed
    # by the application, not the caller).
    fields = {key: value for key, value in update_data.items() if key in TASK_FIELDS}
    for key in ("title", "description", "assignee"):
        if isinstance(fields.get(key), str):
            fields[key] = fields[key].strip()

    if not fields:
        raise TaskValidationError("No valid fields provided to update")

    is_valid, error = validate_task_data(fields, partial=True)
    if not is_valid:
        raise TaskValidationError(error)

    try:
        updated = db.update_task(task_id, fields)
        if not updated:
            raise TaskNotFoundError(f"No task found with ID {task_id}")
        task = db.find_task_by_id(task_id)
    except PyMongoError as exc:
        raise DatabaseError(f"Could not update task: {exc}") from exc

    return serialize_task(task)


def delete_task(task_id: str) -> None:
    """Delete a task."""
    if not validate_task_id(task_id):
        raise TaskValidationError(f"Invalid task ID: {task_id}")

    try:
        deleted = db.delete_task(task_id)
    except PyMongoError as exc:
        raise DatabaseError(f"Could not delete task: {exc}") from exc

    if not deleted:
        raise TaskNotFoundError(f"No task found with ID {task_id}")


def search_tasks(search_term: str) -> List[Dict[str, Any]]:
    """Search tasks by title (case-insensitive, partial match)."""
    return search_and_filter(search=search_term)


def filter_tasks(
    status: Optional[str] = None, priority: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Filter tasks by status and/or priority."""
    return search_and_filter(status=status, priority=priority)


def search_and_filter(
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search by title and filter by status/priority in a single query.

    Any argument may be omitted; omitted arguments are simply not applied.
    """
    query = _build_query(search=search, status=status, priority=priority)

    try:
        return [serialize_task(task) for task in db.find_tasks(query)]
    except PyMongoError as exc:
        raise DatabaseError(f"Could not search tasks: {exc}") from exc


def calculate_statistics() -> Dict[str, int]:
    """Count tasks by status, straight from the database."""
    try:
        return {
            "total_tasks": db.count_tasks(),
            "todo_count": db.count_tasks({"status": "TODO"}),
            "in_progress_count": db.count_tasks({"status": "IN_PROGRESS"}),
            "done_count": db.count_tasks({"status": "DONE"}),
        }
    except PyMongoError as exc:
        raise DatabaseError(f"Could not calculate statistics: {exc}") from exc
