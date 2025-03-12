# FastAPI JWT RBAC API

A RESTful API that implements user authentication with JWT (JSON Web Token) and Role-Based Access Control (RBAC) using FastAPI and PostgreSQL with SQLModel.

## Features

- User registration and authentication
- JWT-based authorization
- Role-based access control (admin and user roles)
- CRUD operations for projects
- PostgreSQL database with SQLModel ORM
- Comprehensive test suite

## Project Structure

```bash
app/
├── main.py                  # FastAPI application entry point
├── config/config.py         # Configuration settings
├── models/                  # SQLModel models
│   ├── __init__.py
│   ├── user.py              # User model with role field
│   └── project.py           # Project model
├── schemas/                 # Pydantic schemas for request/response
│   ├── __init__.py
│   ├── user.py              # User schemas (registration, login)
│   └── project.py           # Project schemas
├── services/                # Business logic
│   ├── __init__.py
│   ├── auth.py              # Auth-related operations (JWT, password)
│   ├── user.py              # User service
│   └── project.py           # Project service
├── api/                     # API routes
│   ├── __init__.py
│   ├── auth.py              # Auth endpoints (register, login)
│   ├── users.py             # User endpoints
│   └── projects.py          # Project endpoints
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── security.py          # JWT and password hashing
│   ├── permissions.py       # Role-based permissions
│   ├── database.py          # Database connection and session management
│   ├── dependencies.py      # Dependency injection (auth, permissions)
│   └── exceptions.py        # Custom exceptions
└── tests/                   # Tests for the application
    ├── __init__.py
    ├── conftest.py          # Test fixtures
    ├── test_auth.py         # Auth tests
    └── test_projects.py     # Project tests
```

## Prerequisites

- Python 3.9 or higher
- PostgreSQL

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nabobery/coding-sphere-take-home-assignment.git
   cd ding-sphere-take-home-assignment
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:

   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_jwt_rbac
   SECRET_KEY=your_secret_key_here
   ```

5. Create a PostgreSQL database:

   ```sql
   CREATE DATABASE fastapi_jwt_rbac;
   ```

6. Run the application:

   ```bash
   python main.py
   ```

7. The API will be available at: [http://localhost:8000](http://localhost:8000)
8. Access the API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Required Dependencies

Create a `requirements.txt` file with the following dependencies:

```
bcrypt==4.3.0
cryptography==44.0.2
fastapi==0.115.11
httpx==0.28.1
passlib==1.7.4
psycopg2==2.9.10
pydantic-settings==2.8.1
pytest==8.3.5
python-jose==3.4.0
sqlmodel==0.0.24
uvicorn==0.34.0
```

## API Endpoints

### Authentication

- **POST /api/v1/auth/register**: Register a new user

  ```json
  {
    "username": "example",
    "password": "password123",
    "email": "example@example.com",
    "full_name": "Example User",
    "role": "user"
  }
  ```

- **POST /api/v1/auth/login**: Login and get JWT token

  ```json
  {
    "username": "example",
    "password": "password123"
  }
  ```

### Projects

All project endpoints require authentication via JWT token.

- **GET /api/v1/project/projects**: Get all projects (accessible by all authenticated users)
- **GET /api/v1/project/projects{project_id}**: Get project by ID (accessible by all authenticated users)
- **POST /api/v1/project/projects**: Create a new project (accessible by admin users only)

  ```json
  {
    "name": "Project Name",
    "description": "Project Description"
  }
  ```

- **PUT /api/v1/project/projects{project_id}**: Update a project (accessible by admin users or project owners)

  ```json
  {
    "name": "Updated Name",
    "description": "Updated Description"
  }
  ```

- **DELETE /api/v1/project/projects{project_id}**: Delete a project (accessible by admin users only)

## Running Tests

Run tests using pytest:

```bash
pytest
```

## Role-Based Access Control

The API implements two roles:

- **admin**: Has full access to all endpoints
- **user**: Can only access read-only endpoints

## License

MIT
