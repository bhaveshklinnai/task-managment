"""Validation utilities for task data."""

VALID_STATUSES = ["TODO", "IN_PROGRESS", "DONE"]
VALID_PRIORITIES = ["LOW", "MEDIUM", "HIGH"]


def validate_status(status: str) -> bool:
    """Validate if status is one of the allowed values."""
    return status in VALID_STATUSES


def validate_priority(priority: str) -> bool:
    """Validate if priority is one of the allowed values."""
    return priority in VALID_PRIORITIES


def validate_task_data(task_data: dict) -> tuple[bool, str]:
    """
    Validate task data for creation/update.
    Returns (is_valid, error_message)
    """
    if "title" in task_data and not task_data["title"]:
        return False, "Title cannot be empty"
    
    if "title" in task_data and len(task_data["title"]) > 255:
        return False, "Title must be 255 characters or less"
    
    if "description" in task_data and len(task_data["description"]) > 2000:
        return False, "Description must be 2000 characters or less"
    
    if "status" in task_data and not validate_status(task_data["status"]):
        return False, f"Invalid status. Allowed values: {', '.join(VALID_STATUSES)}"
    
    if "priority" in task_data and not validate_priority(task_data["priority"]):
        return False, f"Invalid priority. Allowed values: {', '.join(VALID_PRIORITIES)}"
    
    if "assignee" in task_data and not task_data["assignee"]:
        return False, "Assignee cannot be empty"
    
    if "assignee" in task_data and len(task_data["assignee"]) > 255:
        return False, "Assignee must be 255 characters or less"
    
    return True, ""
