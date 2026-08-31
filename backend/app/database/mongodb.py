"""MongoDB connection and raw database operations.

This module knows about MongoDB only. It contains no business rules --
those live in app/services/task_service.py.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.config import settings


class MongoDB:
    """Thin wrapper around the `tasks` collection."""

    def __init__(self):
        self.client = None
        self.db = None
        self.tasks = None
        self.connect()

    def connect(self):
        """Open the connection and verify the server is reachable."""
        try:
            # tz_aware=True makes PyMongo return timezone-aware UTC datetimes
            # instead of naive ones, so timestamps stay accurate end to end.
            self.client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                tz_aware=True,
                tzinfo=timezone.utc,
            )
            self.client.admin.command("ping")
            self.db = self.client[settings.DATABASE_NAME]
            self.tasks = self.db["tasks"]
            print(f"Connected to MongoDB (database: {settings.DATABASE_NAME})")
        except (ConnectionFailure, ServerSelectionTimeoutError) as exc:
            print(f"Failed to connect to MongoDB: {exc}")
            raise

    def close(self):
        """Close the connection."""
        if self.client:
            self.client.close()

    # --- CREATE ---
    def insert_task(self, task_data: Dict[str, Any]) -> str:
        """Insert one task and return its new id as a string."""
        now = datetime.now(timezone.utc)
        document = dict(task_data)
        document["created_date"] = now
        document["updated_date"] = now
        result = self.tasks.insert_one(document)
        return str(result.inserted_id)

    # --- READ ---
    def find_tasks(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Find tasks matching a query, newest first."""
        return list(self.tasks.find(query or {}).sort("created_date", -1))

    def find_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Find a single task by its id."""
        return self.tasks.find_one({"_id": ObjectId(task_id)})

    # --- UPDATE ---
    def update_task(self, task_id: str, update_data: Dict[str, Any]) -> bool:
        """Update one task. Returns True if a task with that id existed."""
        fields = dict(update_data)
        fields.pop("created_date", None)  # created_date is never modified
        fields["updated_date"] = datetime.now(timezone.utc)

        result = self.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": fields})
        # matched_count, not modified_count: re-saving identical values is
        # still a successful update.
        return result.matched_count > 0

    # --- DELETE ---
    def delete_task(self, task_id: str) -> bool:
        """Delete one task. Returns True if a task was removed."""
        result = self.tasks.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0

    # --- COUNT (used for statistics) ---
    def count_tasks(self, query: Optional[Dict[str, Any]] = None) -> int:
        """Count tasks matching a query."""
        return self.tasks.count_documents(query or {})


# Single shared database instance
db = MongoDB()
