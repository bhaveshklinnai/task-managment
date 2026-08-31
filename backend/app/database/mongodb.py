from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson.objectid import ObjectId
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.config import settings


class MongoDB:
    """MongoDB database connection and CRUD operations."""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.tasks_collection = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            # Verify connection
            self.client.admin.command('ping')
            self.db = self.client[settings.DATABASE_NAME]
            self.tasks_collection = self.db['tasks']
            print("✓ Connected to MongoDB successfully")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            raise
    
    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
    
    # CREATE
    def insert_task(self, task_data: Dict[str, Any]) -> str:
        """Insert a new task into the database."""
        task_data['created_date'] = datetime.utcnow()
        task_data['updated_date'] = datetime.utcnow()
        result = self.tasks_collection.insert_one(task_data)
        return str(result.inserted_id)
    
    # READ
    def find_all_tasks(self) -> List[Dict[str, Any]]:
        """Retrieve all tasks."""
        tasks = list(self.tasks_collection.find())
        return tasks
    
    def find_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a task by ID."""
        try:
            task = self.tasks_collection.find_one({"_id": ObjectId(task_id)})
            return task
        except Exception:
            return None
    
    def find_tasks_by_search(self, search_term: str) -> List[Dict[str, Any]]:
        """Search tasks by title (case-insensitive)."""
        tasks = list(self.tasks_collection.find(
            {"title": {"$regex": search_term, "$options": "i"}}
        ))
        return tasks
    
    def find_tasks_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Filter tasks by status."""
        tasks = list(self.tasks_collection.find({"status": status}))
        return tasks
    
    def find_tasks_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Filter tasks by priority."""
        tasks = list(self.tasks_collection.find({"priority": priority}))
        return tasks
    
    def find_tasks_with_filters(
        self,
        search_term: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Find tasks with combined search and filters."""
        query = {}
        
        if search_term:
            query["title"] = {"$regex": search_term, "$options": "i"}
        
        if status:
            query["status"] = status
        
        if priority:
            query["priority"] = priority
        
        tasks = list(self.tasks_collection.find(query))
        return tasks
    
    # UPDATE
    def update_task(self, task_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a task by ID."""
        try:
            update_data['updated_date'] = datetime.utcnow()
            # Don't allow updating created_date
            update_data.pop('created_date', None)
            
            result = self.tasks_collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    # DELETE
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID."""
        try:
            result = self.tasks_collection.delete_one({"_id": ObjectId(task_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    # STATISTICS
    def get_task_count_by_status(self, status: str) -> int:
        """Count tasks by status."""
        return self.tasks_collection.count_documents({"status": status})
    
    def get_total_task_count(self) -> int:
        """Get total count of all tasks."""
        return self.tasks_collection.count_documents({})


# Global database instance
db = MongoDB()
