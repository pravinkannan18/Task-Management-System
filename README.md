Task Management System API

A lightweight Task Management API built with FastAPI, PostgreSQL, PyJWT, smtplib, Celery, and Redis.

## Setup Instructions

### Local Setup
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd task-management-api
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` (see sample).
5. Start PostgreSQL and Redis:
   ```bash
   sudo service postgresql start
   sudo service redis start
   ```
6. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
7. Start Celery worker and beat:
   ```bash
   celery -A app.celery_config worker --loglevel=info
   celery -A app.celery_config beat --loglevel=info
   ```

### Deployed Setup
- Deployed on Render: `<your-deployed-url>`
- Sample credentials:
  - Username: `testuser@example.com`
  - Password: `testpassword123`
- Get token: `POST /token` with credentials.

## Database Schema
- **users**: id (PK), email (unique), hashed_password
- **projects**: id (PK), name, description, user_id (FK)
- **tasks**: id (PK), title, description, status (enum), priority, due_date, project_id (FK), assigned_user_id (FK)

### Schema Diagram
```
[Users] --1:N--> [Projects] --1:N--> [Tasks]
          |
          N
          |
        [Tasks]
```

## Sample cURL Requests
1. Get token:
   ```bash
   curl -X POST "<your-url>/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=testuser@example.com&password=testpassword123"
   ```
2. Create project:
   ```bash
   curl -X POST "<your-url>/projects/" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"name":"My Project","description":"Test project"}'
   ```
3. List tasks with filters:
   ```bash
   curl -X GET "<your-url>/tasks/?status=pending&priority=1&sort_by=due_date&order=asc&page=1&per_page=10" -H "Authorization: Bearer <token>"
   ```

## Celery Setup
- **Worker**: Handles async email notifications for task assignments and status changes.
- **Beat**: Schedules daily overdue task summaries at 8 AM UTC.
- **Broker**: Redis for task queue management.

## Deployment
- Build and run with Docker:
  ```bash
  docker build -t task-management-api .
  docker run -d -p 8000:8000 --env-file .env task-management-api
  ```

## Contact
If stuck, email krithik@macv.ai.


task-management-api/
├── app/                           # Core application code
│   ├── __init__.py               # Marks app as a Python package
│   ├── main.py                   # FastAPI app setup and entry point
│   ├── dependencies.py           # Authentication and dependency injection logic
│   ├── models.py                 # SQLAlchemy database models
│   ├── schemas.py                # Pydantic schemas for request/response validation
│   ├── crud.py                   # Database CRUD operations
│   ├── database.py               # Database connection and session management
│   ├── email.py                  # Email sending logic using smtplib
│   ├── celery_config.py          # Celery configuration for background tasks
│   ├── routes/                   # API route definitions
│   │   ├── __init__.py           # Marks routes as a Python package
│   │   ├── auth.py               # Authentication endpoints (e.g., /token, /users/)
│   │   ├── projects.py           # Project-related endpoints (e.g., /projects/)
│   │   ├── tasks.py              # Task-related endpoints (e.g., /tasks/)
├── migrations/                   # Alembic migrations for database schema (optional)
│   ├── env.py                    # Alembic environment configuration
│   ├── script.py.mako            # Alembic migration template
│   ├── versions/                 # Directory for migration scripts
├── tests/                        # Unit tests (optional)
│   ├── __init__.py               # Marks tests as a Python package
│   ├── test_auth.py              # Tests for authentication endpoints
│   ├── test_projects.py          # Tests for project endpoints
│   ├── test_tasks.py             # Tests for task endpoints
├── Dockerfile                    # Docker configuration for containerization
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (not committed)
├── README.md                     # Project documentation
├── postman_collection.json       # Postman collection for API testing (optional)