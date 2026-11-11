# PMS – Project Management System

A REST API built using FastAPI and PostgreSQL to manage users, authentication, roles, and task assignments.

The system provides JWT-based authentication, secure user sessions, and role-based access control for teachers and students.

## Technologies Used

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Psycopg
- PyJWT
- pwdlib
- Argon2
- python-dotenv
- Postman

## Project Structure

```text
fastapi_101/
├── application/
│ └── pms/
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── users.py
│ ├── tasks.py
│ ├── auth.py
│ ├── security.py
│ ├── dependencies.py
│ ├── migrate_auth.py
│ └── seed_teacher.py
├── tests/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Database Design

The project uses three database tables.

### 1. Users

- id – Primary Key
- name
- email – Unique
- phone
- password_hash – Stores hashed passwords
- role – Teacher or Student
- status
- created_at

### 2. Tasks

- id – Primary Key
- title
- description
- status – pending, in progress, or done
- user_id – Assigned student's ID
- teacher_id – Teacher who created the task
- work_notes
- created_at

### 3. Auth Sessions

- id – Primary Key
- user_id – Foreign Key referencing users.id
- refresh_token_hash
- expires_at
- revoked_at
- created_at

### Relationships and Constraints

- One user can have multiple assigned tasks.
- Each task belongs to a student.
- Teachers can create and assign tasks.
- Each task can record the teacher who assigned it.
- Passwords are stored as hashes, never as plaintext.
- Refresh tokens are stored as hashes in the database.
- Sessions support expiry and revocation.
- Email addresses must be unique.
- Task statuses are validated through Pydantic schemas.

## Authentication and Authorization

The application uses JWT (JSON Web Tokens) for authentication.

Authentication features include:

- Student registration
- User login
- Access token generation
- Refresh token rotation
- Session expiry
- Logout and session revocation
- Authenticated user profile

### Authentication Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a student |
| POST | `/auth/login` | Login and obtain tokens |
| POST | `/auth/refresh` | Refresh tokens |
| POST | `/auth/logout` | Revoke a session |
| GET | `/auth/me` | Get logged-in user's profile |

New public registrations receive the student role by default. Teacher accounts are created through the local teacher setup script.

## Role-Based Access Control

### Teacher

- View all registered users.
- View individual user profiles and their tasks.
- Create and assign tasks to students.
- View all tasks.
- View individual tasks.
- Update and reassign tasks.
- Delete tasks.
- Filter tasks by status.
- View task progress summaries.

### Student

- View their own profile.
- View their assigned tasks.
- Update their own task status.
- Add or update work notes.

Students cannot create, assign, delete, or view all tasks. They cannot access teacher-only user information.

## API Endpoints

### Users

| Method | Endpoint | Description |
|---|---|---|
| GET | `/pms/users/` | View all users (Teacher only) |
| GET | `/pms/users/{user_id}` | View user details and tasks (Teacher only) |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/pms/tasks/` | Create and assign a task (Teacher only) |
| GET | `/pms/tasks/` | View all tasks (Teacher only) |
| GET | `/pms/tasks/my` | View own tasks (Student only) |
| GET | `/pms/tasks/{task_id}` | View an individual task (Teacher only) |
| PUT | `/pms/tasks/{task_id}` | Update a task (Teacher only) |
| PATCH | `/pms/tasks/{task_id}/work` | Update own task status and notes (Student only) |
| DELETE | `/pms/tasks/{task_id}` | Delete a task (Teacher only) |
| GET | `/pms/tasks/filter/?status=pending` | Filter tasks (Teacher only) |
| GET | `/pms/tasks/progress/` | View task progress summary (Teacher only) |

## Installation and Setup

1. Clone the repository.
2. Open the project folder.
3. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate.bat
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a PostgreSQL database named `pms_db`.

6. Create a `.env` file in the project root with your own local configuration:

```env
DATABASE_URL=postgresql+psycopg://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost:5432/pms_db
SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Generate a private secret key for your own environment. Never commit real credentials or `.env` files to GitHub.

7. Run the authentication database migration:

```bash
python -m application.pms.migrate_auth
```

8. Create a teacher account securely:

```bash
python -m application.pms.seed_teacher
```

The script prompts for teacher details and password locally.

Students can register through the `/auth/register` endpoint.

## Run the Application

Start the FastAPI application:

```bash
uvicorn application.quotes:app --reload
```

Open Swagger documentation:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Protected endpoints require a valid Bearer access token.

## Testing

API endpoints were tested using Postman.

Authentication and authorization tests included:

- Teacher and student login
- Successful student registration
- Teacher task creation and assignment
- Student task retrieval
- Student task status and work-note updates
- Teacher task updates and deletion
- Role-based access restrictions
- Invalid login credentials
- Missing authentication token
- Expired access token
- Revoked sessions
- Refresh token rotation
- Invalid task status
- Missing task records
- Task filtering and progress summary

Run automated tests using:

```bash
python -m pytest -v
```

## Error Handling and Validation

The API uses appropriate HTTP status codes:

- 200 – Successful request
- 201 – Resource created
- 400 – Invalid request or duplicate email
- 401 – Invalid, expired, or revoked authentication
- 403 – Insufficient permissions
- 404 – User or task not found
- 422 – Request validation error

## Security Features

- Password hashing using pwdlib and Argon2.
- JWT access and refresh tokens.
- Hashed refresh tokens in the database.
- Session expiry and revocation.
- Role-based authorization.
- Protected task and user endpoints.
- Environment variables for sensitive configuration.
- Student-specific task access restrictions.

## Database Migrations with Alembic

Alembic is used to manage database schema changes and migrations in the PMS project.

### Migration Commands

```bash
# Generate a migration after changing SQLAlchemy models
alembic revision --autogenerate -m "migration description"

# Apply all pending migrations
alembic upgrade head

# Roll back the latest migration
alembic downgrade -1

# Check the current migration version
alembic current

# View migration history
alembic history
```

### Migration Workflow

1. Update the SQLAlchemy models.
2. Generate a migration using `alembic revision --autogenerate`.
3. Review the generated migration file.
4. Apply changes using `alembic upgrade head`.
5. Verify the database schema.

Alembic migrations help maintain database schema changes in a version-controlled and organized way.

## Task Pagination, Search and Filtering

The teacher task listing endpoint supports pagination, title search, and filtering.

### Query Parameters

| Parameter | Description | Example |
|---|---|---|
| skip | Number of records to skip | skip=0 |
| limit | Maximum records to return | limit=5 |
| search | Search tasks by title | search=Python |
| status | Filter by task status | status=pending |
| user_id | Filter by assigned student | user_id=2 |

### Example Request

GET /pms/tasks/?skip=0&limit=5&status=pending&user_id=2

All parameters are optional.

## Automated Testing with Pytest

Install project dependencies:

```bash
pip install -r requirements.txt
```

Run automated tests:

```bash
python -m pytest -q
```

The tests cover authentication, authorization, task creation, assignment, updating, and deletion.

## Continuous Integration with GitHub Actions

GitHub Actions automatically runs the project's pytest test suite whenever code is pushed or a pull request is created.

The workflow is located at:

`.github/workflows/tests.yml`

The workflow performs these steps:

1. Checks out the repository.
2. Sets up Python 3.13.
3. Installs project dependencies.
4. Runs automated tests using pytest.

Test results can be viewed in the **Actions** tab of the GitHub repository.
