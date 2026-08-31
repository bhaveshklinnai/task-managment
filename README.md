# Task Management Dashboard

A task management dashboard for a small software development team. Tasks are
created, searched, filtered and updated from a React frontend, the application
logic lives in reusable Python functions, and MongoDB stores the data.

```
React UI  →  REST API (FastAPI)  →  Core Python functions  →  MongoDB
```

## Features

- **Create, view, update and delete tasks** — full CRUD, including fetching a single task by ID
- **Search by title** — case-insensitive partial match, updating as you type
- **Filter by status and priority** — combinable with each other and with search
- **Task statistics** — Total / TODO / In Progress / Done, counted directly in MongoDB
- **Validation** — required fields, field lengths, and allowed status/priority values, enforced on both the server and the form
- **Error handling** — meaningful messages for invalid input, unknown IDs, missing tasks and database failures
- **Loading and empty states** — including a distinct message for "no tasks yet" vs. "nothing matches your filters"
- **Accurate timestamps** — `created_date` is set once, `updated_date` on every change; both are stored and sent as UTC and displayed in the viewer's local time

## Technology Stack

| Component     | Technology         |
| ------------- | ------------------ |
| Frontend      | React 18           |
| Backend       | Python 3.8+, FastAPI |
| Database      | MongoDB            |
| Communication | REST API (JSON)    |
| HTTP client   | axios              |
| Server        | Uvicorn            |

## Project Structure

Each folder holds one responsibility, so any change has an obvious home.

```
task-management-dashboard/
│
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app: CORS, routers, error handlers
│   │   ├── config.py             # Environment configuration
│   │   ├── exceptions.py         # Application errors, mapped to status codes
│   │   │
│   │   ├── routes/               # ── API layer ──
│   │   │   └── tasks.py          # REST endpoints (thin handlers)
│   │   ├── models/               # ── Request/response shapes ──
│   │   │   └── task.py           # Pydantic models
│   │   ├── services/             # ── Core logic ──
│   │   │   └── task_service.py   # Reusable task functions
│   │   ├── database/             # ── Persistence ──
│   │   │   └── mongodb.py        # Connection + CRUD operations
│   │   └── utils/                # ── Helpers ──
│   │       └── validation.py     # Validation functions
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   │   └── index.html            # Page shell React mounts into
│   ├── src/
│   │   ├── index.js              # Entry point
│   │   ├── index.css             # Global styles
│   │   ├── App.js                # Root component
│   │   ├── constants.js          # Status and priority option lists
│   │   │
│   │   ├── components/           # ── UI, each with its own stylesheet ──
│   │   │   ├── Dashboard.js/.css     # Page state: tasks, stats, filters
│   │   │   ├── Statistics.js/.css    # Statistics cards
│   │   │   ├── SearchFilter.js/.css  # Search box + status/priority selects
│   │   │   ├── TaskList.js/.css      # List, loading and empty states
│   │   │   ├── TaskItem.js/.css      # A single task card
│   │   │   └── TaskForm.js/.css      # Create/edit form with validation
│   │   └── services/             # ── API access ──
│   │       └── taskApi.js        # Every call to the backend
│   │
│   ├── package.json
│   └── .env.example
│
├── screenshots/                  # Images used in this README
├── .gitignore                    # Single ignore list for the whole repo
└── README.md
```

**How to read it.** A request travels down the backend folders in order:
`routes` receives it, `services` decides what it means, `database` stores it.
Nothing skips a layer, and no layer imports the one above it. On the frontend,
`components` render, `services/taskApi.js` is the only file that talks to the
API, and each component's `.css` sits directly beside its `.js`.

## Setup Instructions

### Prerequisites

- Python 3.8 or newer
- Node.js 14 or newer with npm
- MongoDB, either running locally or a MongoDB Atlas cluster

### 1. Backend

```bash
cd backend

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt

cp .env.example .env         # then edit .env with your MongoDB URI

python -m uvicorn app.main:app --reload --port 8000
```

The API runs at `http://localhost:8000`. Interactive documentation is generated
by FastAPI at `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend

npm install

cp .env.example .env         # defaults to http://localhost:8000/api

npm start
```

The dashboard opens at `http://localhost:3000`.

## Environment Variables

Copy `.env.example` to `.env` in each folder. `.env` files are git-ignored and
must never be committed.

### `backend/.env`

| Variable        | Description                          | Example                       |
| --------------- | ------------------------------------ | ----------------------------- |
| `MONGODB_URI`   | MongoDB connection string            | `mongodb://localhost:27017`   |
| `DATABASE_NAME` | Database to use                      | `task_management`             |
| `BACKEND_PORT`  | Port the API listens on              | `8000`                        |

For MongoDB Atlas use the full connection string instead:
`mongodb+srv://username:password@cluster.mongodb.net/`

### `frontend/.env`

| Variable             | Description               | Example                       |
| -------------------- | ------------------------- | ----------------------------- |
| `REACT_APP_API_URL`  | Base URL of the REST API  | `http://localhost:8000/api`   |

## API Documentation

Base URL: `http://localhost:8000/api`

| Method   | Endpoint            | Description                       | Success |
| -------- | ------------------- | --------------------------------- | ------- |
| `POST`   | `/tasks`            | Create a task                     | `201`   |
| `GET`    | `/tasks`            | List tasks (search + filters)     | `200`   |
| `GET`    | `/tasks/stats`      | Task statistics                   | `200`   |
| `GET`    | `/tasks/{id}`       | Get one task by ID                | `200`   |
| `PUT`    | `/tasks/{id}`       | Update a task                     | `200`   |
| `DELETE` | `/tasks/{id}`       | Delete a task                     | `204`   |

### Query parameters for `GET /tasks`

| Parameter  | Values                          | Description                     |
| ---------- | ------------------------------- | ------------------------------- |
| `search`   | any text                        | Case-insensitive title match    |
| `status`   | `TODO`, `IN_PROGRESS`, `DONE`   | Filter by status                |
| `priority` | `LOW`, `MEDIUM`, `HIGH`         | Filter by priority              |

All three are optional and can be combined:

```
GET /api/tasks?search=login
GET /api/tasks?status=TODO
GET /api/tasks?priority=HIGH&status=IN_PROGRESS
GET /api/tasks?search=api&status=IN_PROGRESS&priority=HIGH
```

### Task object

```json
{
  "id": "6a95694a2fd525ef99c07897",
  "title": "Fix login redirect loop",
  "description": "Users are bounced back to the login page after sign-in.",
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "assignee": "Priya Sharma",
  "created_date": "2026-08-31T11:45:14.590000+00:00",
  "updated_date": "2026-08-31T11:52:03.120000+00:00"
}
```

`status` is one of `TODO`, `IN_PROGRESS`, `DONE`.
`priority` is one of `LOW`, `MEDIUM`, `HIGH`.

### Example requests

```bash
# Create
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Write tests","description":"Cover the API","status":"TODO","priority":"HIGH","assignee":"Ananya"}'

# Update just the status
curl -X PUT http://localhost:8000/api/tasks/<id> \
  -H "Content-Type: application/json" \
  -d '{"status":"DONE"}'

# Statistics
curl http://localhost:8000/api/tasks/stats
# {"total_tasks":8,"todo_count":3,"in_progress_count":3,"done_count":2}
```

### Status codes and errors

| Code  | Meaning                                                        |
| ----- | -------------------------------------------------------------- |
| `200` | Successful read or update                                       |
| `201` | Task created                                                    |
| `204` | Task deleted                                                    |
| `400` | Invalid input — bad status/priority, empty title, malformed ID  |
| `404` | No task exists with that ID                                     |
| `422` | Request body failed schema validation (missing required field)  |
| `503` | The database was unreachable or rejected the operation          |

Errors always return a `detail` field:

```json
{ "detail": "Invalid priority. Allowed values: LOW, MEDIUM, HIGH" }
```

## Core Python Functions

All application logic lives in `backend/app/services/task_service.py` as plain
functions. They take and return ordinary Python values, raise ordinary Python
exceptions, and know nothing about HTTP or React — so they can equally be called
from a script, a test or a different interface.

| Function                                          | Purpose                                              |
| ------------------------------------------------- | ---------------------------------------------------- |
| `create_task(title, assignee, description, status, priority)` | Validate and insert a task, returning it  |
| `get_all_tasks()`                                 | Retrieve every task                                  |
| `get_task_by_id(task_id)`                         | Retrieve one task                                    |
| `update_task(task_id, update_data)`               | Update the supplied fields, returning the new task   |
| `delete_task(task_id)`                            | Delete a task                                        |
| `search_tasks(search_term)`                       | Search by title                                      |
| `filter_tasks(status, priority)`                  | Filter by status and/or priority                     |
| `search_and_filter(search, status, priority)`     | Search and filter in a single query                  |
| `calculate_statistics()`                          | Count tasks by status                                |
| `serialize_task(document)`                        | Convert a MongoDB document to a JSON-friendly dict    |

They raise the three exceptions defined in `backend/app/exceptions.py`, which
`main.py` maps to HTTP responses:

| Exception              | HTTP  |
| ---------------------- | ----- |
| `TaskValidationError`  | `400` |
| `TaskNotFoundError`    | `404` |
| `DatabaseError`        | `503` |

### Validation functions (`backend/app/utils/validation.py`)

| Function                                | Purpose                                             |
| --------------------------------------- | --------------------------------------------------- |
| `validate_task_data(data, partial)`     | Validate a whole task, or just the supplied fields  |
| `validate_status(status)`               | Check the status is TODO / IN_PROGRESS / DONE       |
| `validate_priority(priority)`           | Check the priority is LOW / MEDIUM / HIGH           |
| `validate_task_id(task_id)`             | Check the ID is a well-formed MongoDB ObjectId      |

### MongoDB operations (`backend/app/database/mongodb.py`)

| Method                          | MongoDB operation                          |
| ------------------------------- | ------------------------------------------ |
| `insert_task(task_data)`        | `insert_one` — sets both timestamps        |
| `find_tasks(query)`             | `find` — used for listing, search and filter |
| `find_task_by_id(task_id)`      | `find_one`                                 |
| `update_task(task_id, fields)`  | `update_one` with `$set`                   |
| `delete_task(task_id)`          | `delete_one`                               |
| `count_tasks(query)`            | `count_documents` — used for statistics    |

Search and filtering are done by the database. `find_tasks` receives a query
built by `search_and_filter`, which uses a `$regex` match on `title` for search
and equality matches on `status` and `priority` for filtering. No task data is
hardcoded anywhere in the application.

## Screenshots

**Dashboard** — statistics, search and filter bar, and the task list.

![Dashboard](screenshots/01-dashboard.png)

**Search by title** — results narrow as you type.

![Search](screenshots/02-search.png)

**Filter by status and priority** — combinable with search.

![Filter](screenshots/03-filter.png)

**No results** — distinct from the "no tasks yet" empty state.

![Empty state](screenshots/04-empty-state.png)

**Create task form**

![Create task](screenshots/05-create-task.png)

**Form validation** — required fields are flagged before the request is sent.

![Form validation](screenshots/06-form-validation.png)

**Edit task** — the same form, pre-filled.

![Edit task](screenshots/07-edit-task.png)

## Important Design Decisions

**1. Logic lives in functions, not in route handlers.**
Every route handler does three things: read the request, call one function in
`task_service.py`, return the result. Nothing else. The service functions do not
import FastAPI, and the database module does not know about business rules, so
each layer can be read, reused and tested on its own.

**2. Errors are exceptions, not return values.**
The service layer raises `TaskValidationError`, `TaskNotFoundError` or
`DatabaseError`. `main.py` registers one handler per exception type, so the
correct status code is produced in a single place and route handlers stay free
of `try`/`except` blocks.

**3. Timestamps are stored and transmitted in UTC.**
The MongoDB client is opened with `tz_aware=True`, so timestamps come back as
timezone-aware UTC values rather than naive ones. The API serialises them as ISO
strings that carry the offset (`...+00:00`), and the browser converts them to
the viewer's local time. Without the offset the browser would read a UTC time as
if it were local, which is what previously made the displayed times wrong.
`created_date` is set on insert and explicitly removed from every update, so it
can never be overwritten.

**4. Updates use `matched_count`, not `modified_count`.**
Saving a task without altering any value is a successful update, not a failure.
MongoDB reports `modified_count: 0` in that case, so the presence of the
document is what determines success.

**5. Search and filtering happen in a single database query.**
`search_and_filter` builds one query object and issues one `find`, rather than
fetching all tasks and filtering them in Python. Search terms are passed through
`re.escape`, so characters like `(` or `*` are matched literally instead of
being interpreted as regular expression syntax.

**6. Statistics are counted by the database.**
`calculate_statistics` issues `count_documents` calls, so the numbers always
reflect what is actually stored. They are reloaded alongside the task list after
every create, update and delete.

**7. Search and filters apply as you use them.**
The dashboard holds the filter values and reloads whenever they change; typing
is debounced by 300 ms so a request is not sent per keystroke. Because responses
can arrive out of order, a reload that has been superseded is marked cancelled
when the filters change again, so a slower earlier response cannot overwrite
newer results.

**8. Validation runs on both sides, but the server decides.**
The form checks required fields and lengths for fast feedback; the same rules
are enforced again in `validate_task_data` before anything reaches MongoDB, so
the API is safe regardless of which client calls it.

## Troubleshooting

**`Failed to connect to MongoDB`** — check that MongoDB is running and that
`MONGODB_URI` in `backend/.env` is correct. For Atlas, confirm your IP address is
allowed in the cluster's network access list.

**CORS errors in the browser** — the API allows `http://localhost:3000` by
default. If the frontend runs on another port, add it to `CORS_ORIGINS` in
`backend/app/config.py`.

**Port already in use** — run the API on another port with
`--port 8001`, and update `REACT_APP_API_URL` in `frontend/.env` to match.
Restart `npm start` afterwards, since Create React App reads `.env` at startup.

## Possible Enhancements

Sorting, pagination, unit tests, due dates and Docker packaging are natural next
steps; none are required for the current feature set.
