# PMS – Project Management System

A REST API built using FastAPI and PostgreSQL to manage users and their tasks.

## Technologies Used
- Python 3.13.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Psycopg
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
│ └── tasks.py
├── tests/
├── requirements.txt
└── README.md
```

## Database Design

The project contains two tables:

### Users
- id – Primary Key
- name
- email – Unique
- phone
- status
- created_at

### Tasks
- id – Primary Key
- title
- description
- status
- user_id – Foreign Key referencing users.id
- created_at

### Relationships and Constraints
- One user can have multiple tasks.
- Each task belongs to one user.
- Primary keys uniquely identify records.
- The foreign key connects tasks to users.
- Email must be unique.
- Required fields use NOT NULL constraints.
- Indexes are used on selected columns to support faster lookups.
- Deleting a user also deletes their associated tasks through the configured relationship cascade.
- Task status values are validated through Pydantic schemas.

## API Endpoints

### Users
- GET `/pms/users/` – Get all users
- GET `/pms/users/{user_id}` – Get user details with tasks
- POST `/pms/users/` – Create a user
- PUT `/pms/users/{user_id}` – Update a user
- DELETE `/pms/users/{user_id}` – Delete a user

### Tasks
- GET `/pms/tasks/` – Get all tasks
- GET `/pms/tasks/{task_id}` – Get a task by ID
- POST `/pms/tasks/` – Create and assign a task
- PUT `/pms/tasks/{task_id}` – Update a task
- DELETE `/pms/tasks/{task_id}` – Delete a task
- GET `/pms/tasks/filter/?status=pending` – Filter tasks by status

## Installation and Setup

1. Clone the repository.
2. Open the project folder.
3. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a PostgreSQL database named `pms_db`.
6. Configure the database connection in `application/pms/database.py` using your local PostgreSQL credentials.
7. Ensure the database tables have been created.

## Run the Application

```bash
uvicorn application.quotes:app --reload
```

Open Swagger documentation:

`http://127.0.0.1:8000/docs`

## Testing

API endpoints were tested using Postman.

Run automated tests using:

```bash
python -m pytest -v
```

## Error Handling and Validation

- 400 – Duplicate user email
- 404 – User or task not found
- 422 – Invalid request data or validation errors

```