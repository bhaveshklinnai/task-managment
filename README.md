# Task Management Dashboard

A full-stack Task Management Dashboard application built with React, Python FastAPI, and MongoDB.

## Features

- ✅ **Create Tasks** - Add new tasks with title, description, status, priority, and assignee
- ✅ **View All Tasks** - Display all tasks in a clean, organized list
- ✅ **View Single Task** - Get detailed information about a specific task
- ✅ **Update Tasks** - Edit task information while preserving creation date
- ✅ **Delete Tasks** - Remove tasks with confirmation
- ✅ **Search Tasks** - Search tasks by title
- ✅ **Filter by Status** - Filter tasks by TODO, IN_PROGRESS, or DONE
- ✅ **Filter by Priority** - Filter tasks by LOW, MEDIUM, or HIGH
- ✅ **Task Statistics** - View dashboard statistics (Total, TODO, In Progress, Done)
- ✅ **Validation & Error Handling** - Comprehensive input validation and user-friendly error messages
- ✅ **Loading States** - Show loading indicators during API calls
- ✅ **Empty States** - Display helpful messages when no tasks exist

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React 18 |
| Backend | Python with FastAPI |
| Database | MongoDB |
| Communication | REST API |

## Project Structure

```
task-management-dashboard/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Configuration & environment
│   │   ├── models/
│   │   │   └── task.py                # Pydantic models
│   │   ├── services/
│   │   │   └── task_service.py        # Core business logic
│   │   ├── routes/
│   │   │   └── tasks.py               # API routes
│   │   ├── database/
│   │   │   └── mongodb.py             # MongoDB operations
│   │   └── utils/
│   │       └── validation.py          # Validation functions
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js
│   │   │   ├── TaskList.js
│   │   │   ├── TaskForm.js
│   │   │   ├── TaskItem.js
│   │   │   ├── Statistics.js
│   │   │   └── SearchFilter.js
│   │   ├── pages/
│   │   │   └── Home.js
│   │   ├── services/
│   │   │   └── taskApi.js
│   │   ├── styles/
│   │   │   ├── Dashboard.css
│   │   │   ├── TaskList.css
│   │   │   ├── TaskForm.css
│   │   │   ├── TaskItem.js
│   │   │   ├── Statistics.css
│   │   │   └── SearchFilter.css
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── .env.example
│   └── .gitignore
│
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- MongoDB (local or Atlas cloud database)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

5. **Configure environment variables in `.env`:**
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=task_management
   BACKEND_PORT=8000
   ```

6. **Run the backend server:**
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```

The backend will be available at `http://localhost:8000`

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

4. **Configure environment variables in `.env`:**
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

5. **Start the development server:**
   ```bash
   npm start
   ```

The frontend will open automatically at `http://localhost:3000`

## API Endpoints

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks` | Get all tasks (with optional filters) |
| GET | `/api/tasks/{task_id}` | Get a single task |
| PUT | `/api/tasks/{task_id}` | Update a task |
| DELETE | `/api/tasks/{task_id}` | Delete a task |
| GET | `/api/tasks/stats` | Get task statistics |

### Query Parameters

**GET /api/tasks** supports the following query parameters:
- `search` - Search by task title
- `status` - Filter by status (TODO, IN_PROGRESS, DONE)
- `priority` - Filter by priority (LOW, MEDIUM, HIGH)

Examples:
```
GET /api/tasks?search=login
GET /api/tasks?status=TODO
GET /api/tasks?priority=HIGH
GET /api/tasks?search=api&status=IN_PROGRESS&priority=HIGH
```

## Core Python Functions

The application implements reusable Python functions in `app/services/task_service.py`:

- `create_task()` - Create a new task
- `get_all_tasks()` - Retrieve all tasks
- `get_task_by_id()` - Retrieve a task by ID
- `update_task()` - Update a task
- `delete_task()` - Delete a task
- `search_tasks()` - Search tasks by title
- `filter_tasks()` - Filter tasks by status and/or priority
- `search_and_filter()` - Combined search and filter
- `calculate_statistics()` - Calculate task statistics

**MongoDB Operations** in `app/database/mongodb.py`:

- `insert_task()` - Insert a document
- `find_all_tasks()` - Find all documents
- `find_task_by_id()` - Find by ObjectId
- `find_tasks_by_search()` - Search by title
- `find_tasks_by_status()` - Filter by status
- `find_tasks_by_priority()` - Filter by priority
- `find_tasks_with_filters()` - Combined search/filter
- `update_task()` - Update a document
- `delete_task()` - Delete a document
- `get_task_count_by_status()` - Count by status
- `get_total_task_count()` - Count all tasks

## Task Data Model

Each task contains:

```json
{
  "_id": "ObjectId",
  "title": "Task title",
  "description": "Task description",
  "status": "TODO|IN_PROGRESS|DONE",
  "priority": "LOW|MEDIUM|HIGH",
  "assignee": "Assignee name",
  "created_date": "2026-08-31T12:00:00",
  "updated_date": "2026-08-31T12:00:00"
}
```

### Status Values
- `TODO` - Task not started
- `IN_PROGRESS` - Task in progress
- `DONE` - Task completed

### Priority Values
- `LOW` - Low priority
- `MEDIUM` - Medium priority
- `HIGH` - High priority

## MongoDB Setup

### Using MongoDB Atlas (Cloud)

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Create a database user
4. Get your connection string
5. Update the `MONGODB_URI` in your `.env` file

### Using Local MongoDB

1. Install MongoDB Community Edition
2. Start MongoDB service:
   ```bash
   # On Windows:
   mongod
   # On macOS:
   brew services start mongodb-community
   ```
3. Set `MONGODB_URI` to `mongodb://localhost:27017`

## Validation & Error Handling

The application includes comprehensive validation:

**Backend Validation:**
- Required fields validation
- Field length validation
- Enum validation for status and priority
- Invalid ObjectId handling
- Task not found handling
- Database error handling

**Frontend Validation:**
- Required field validation
- Form input validation before submission
- API error handling and display
- Loading state management
- Empty state handling

## HTTP Status Codes

- `201 Created` - Task created successfully
- `200 OK` - Successful retrieval/update
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid input or validation error
- `404 Not Found` - Task not found
- `500 Internal Server Error` - Server error

## Usage Guide

### Creating a Task

1. Click "+ Create New Task" button
2. Fill in the form:
   - **Title** (required) - Task title
   - **Description** - Detailed description
   - **Status** - TODO, In Progress, or Done
   - **Priority** - Low, Medium, or High
   - **Assignee** (required) - Person assigned to task
3. Click "Create Task"

### Searching Tasks

1. Enter search term in the search box
2. Click "Filter" button or just type to search

### Filtering Tasks

1. Select status from the dropdown
2. Select priority from the dropdown
3. Click "Filter" button

### Updating a Task

1. Click "Edit" on the task
2. Modify the form fields
3. Click "Update Task"

### Deleting a Task

1. Click "Delete" on the task
2. Confirm deletion in the popup

## Important Design Decisions

1. **Separation of Concerns**
   - Routes handle HTTP requests/responses
   - Services contain core business logic
   - Database module manages all MongoDB operations
   - Validation is centralized

2. **Date Handling**
   - `created_date` is set at task creation and never modified
   - `updated_date` is automatically updated on any modification
   - Dates are stored as ISO format strings in MongoDB

3. **Error Handling**
   - Backend returns meaningful error messages
   - Frontend displays user-friendly error messages
   - No sensitive information leaked in error responses

4. **CORS Configuration**
   - Configured for local development (localhost:3000)
   - Easy to update for production

5. **Validation**
   - Backend validation is the source of truth
   - Frontend validation provides better UX
   - Both work together for a robust solution

## Environment Variables

### Backend (.env)
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=task_management
BACKEND_PORT=8000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Git Commit History

```
Initial project setup
Implement MongoDB connection
Implement task CRUD core logic
Add FastAPI task routes
Implement search and filtering
Implement task statistics
Build React dashboard
Integrate frontend with API
Add validation and error handling
Add README and finalize project
```

## Troubleshooting

### MongoDB Connection Error

**Error:** `Failed to connect to MongoDB`

**Solution:**
- Verify MongoDB is running
- Check MONGODB_URI in .env file
- Ensure database credentials are correct
- Check network connectivity for Atlas

### CORS Error

**Error:** `Access to XMLHttpRequest blocked by CORS`

**Solution:**
- Ensure backend is running on port 8000
- Check REACT_APP_API_URL in frontend .env
- Verify CORS_ORIGINS in backend config includes frontend URL

### Port Already in Use

**Backend (Port 8000):**
```bash
# Find and kill process using port 8000
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Frontend (Port 3000):**
```bash
# Kill process or run on different port
PORT=3001 npm start
```

### Module Not Found Errors

**Backend:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Frontend:**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Screenshots

[Add screenshots of the dashboard here when UI is complete]

## Future Enhancements

- User authentication and authorization
- Task categories/tags
- Task comments and activity log
- Recurring tasks
- Task due dates
- Email notifications
- Sorting and pagination
- Advanced statistics
- Dark mode
- Mobile app

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository.
