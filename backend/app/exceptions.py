"""Application errors.

The core functions in app/services raise these instead of returning error
codes, and app/main.py maps each one to an HTTP status. Keeping them here --
rather than inside the service module -- means both the layer that raises them
and the layer that translates them can import them without depending on
each other.
"""


class TaskValidationError(Exception):
    """The supplied task data is invalid (bad field, value or ID)."""


class TaskNotFoundError(Exception):
    """No task exists with the given ID."""


class DatabaseError(Exception):
    """The database was unreachable or rejected the operation."""
