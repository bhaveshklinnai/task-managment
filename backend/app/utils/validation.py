"""Reusable validation helpers for task data.

These functions are plain Python: they know nothing about HTTP or MongoDB.
"""

from typing import Any, Dict, Optional, Tuple

from bson.objectid import ObjectId

VALID_STATUSES = ["TODO", "IN_PROGRESS", "DONE"]
VALID_PRIORITIES = ["LOW", "MEDIUM", "HIGH"]

MAX_TITLE_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 2000
MAX_ASSIGNEE_LENGTH = 255


def validate_status(status: str) -> bool:
    """Return True if the status is one of the allowed values."""
    return status in VALID_STATUSES


def validate_priority(priority: str) -> bool:
    """Return True if the priority is one of the allowed values."""
    return priority in VALID_PRIORITIES


def validate_task_id(task_id: str) -> bool:
    """Return True if the string is a well-formed MongoDB ObjectId."""
    return bool(task_id) and ObjectId.is_valid(task_id)


def _validate_text(
    value: Any, field: str, max_length: int, required: bool
) -> Optional[str]:
    """Validate one text field. Returns an error message, or None if valid."""
    if not isinstance(value, str):
        return f"{field} must be text"
    if required and not value.strip():
        return f"{field} is required"
    if len(value) > max_length:
        return f"{field} must be {max_length} characters or less"
    return None


def validate_task_data(
    task_data: Dict[str, Any], partial: bool = False
) -> Tuple[bool, str]:
    """Validate task data for creation or update.

    Args:
        task_data: the fields to validate.
        partial: True for updates, where only the supplied fields are checked.

    Returns:
        (is_valid, error_message). error_message is "" when valid.
    """
    if not isinstance(task_data, dict) or not task_data:
        return False, "No task data provided"

    if not partial:
        for required_field in ("title", "assignee"):
            if required_field not in task_data:
                return False, f"{required_field.capitalize()} is required"

    if "title" in task_data:
        error = _validate_text(
            task_data["title"], "Title", MAX_TITLE_LENGTH, required=True
        )
        if error:
            return False, error

    if "description" in task_data:
        error = _validate_text(
            task_data["description"],
            "Description",
            MAX_DESCRIPTION_LENGTH,
            required=False,
        )
        if error:
            return False, error

    if "assignee" in task_data:
        error = _validate_text(
            task_data["assignee"], "Assignee", MAX_ASSIGNEE_LENGTH, required=True
        )
        if error:
            return False, error

    if "status" in task_data and not validate_status(task_data["status"]):
        return False, f"Invalid status. Allowed values: {', '.join(VALID_STATUSES)}"

    if "priority" in task_data and not validate_priority(task_data["priority"]):
        return (
            False,
            f"Invalid priority. Allowed values: {', '.join(VALID_PRIORITIES)}",
        )

    return True, ""
