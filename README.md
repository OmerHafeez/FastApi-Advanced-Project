# FastAPI User Management System

A production-quality User Management System built with FastAPI, featuring JWT authentication, async SQLAlchemy ORM, and complete CRUD operations.

## Features

- JWT Authentication with configurable token expiration
- User Management with complete CRUD operations
- Input Validation using Pydantic schemas
- Async Database with SQLAlchemy ORM (SQLite, easily switchable to PostgreSQL/MySQL)
- Clean Code Structure with separation of concerns
- Proper HTTP Status Codes (201, 400, 401, 403, 404, 409, 500)
- Dependency Injection for auth and database sessions
- Environment Configuration via .env file
- Auto-generated API Documentation

## Project Structure

```
FastApi Advanced/
├── config.py              # Application configuration
├── database.py            # Database connection and session management
├── dependencies.py        # FastAPI dependency functions (auth)
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── models/
│   └── user.py           # SQLAlchemy User model
├── schemas/
│   └── user.py           # Pydantic schemas for validation
├── services/
│   ├── auth.py           # Authentication service (JWT, password hashing)
│   └── user.py           # User CRUD service
└── routers/
    ├── auth.py           # Authentication endpoints (register, login)
    └── users.py          # User management endpoints (CRUD)
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Navigate to the project directory:
```bash
cd "/Users/mac/Documents/FastApi Advanced"
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Install dependencies:
```bash
./venv/bin/pip install -r requirements.txt
```

4. Configure environment variables:
Edit the `.env` file to change settings if needed. Default configuration is ready to use.

### Running the Application

```bash
./venv/bin/python main.py
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## API Endpoints

### Public Endpoints (No Authentication)

**POST /auth/register** - Register a new user
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

**POST /auth/login** - Login and get JWT token
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### User Endpoints (Authentication Required)

**GET /users/me** - Get current user profile

**PUT /users/me** - Update current user profile
```json
{
  "username": "new_username",
  "email": "new_email@example.com"
}
```

**DELETE /users/me** - Delete current user account

## Authentication

### Token-Based Authentication

1. Register a new user using `/auth/register`
2. Login using `/auth/login` to receive an access token
3. Use the token in subsequent requests with the Authorization header:
   ```
   Authorization: Bearer <your_access_token>
   ```
4. Tokens expire after 30 minutes (configurable in .env)

### Using the Interactive Documentation

1. Open http://localhost:8000/docs
2. Register and login to get your token
3. Click the "Authorize" button at the top right
4. Enter: `Bearer <your_token>`
5. Test protected endpoints

## Security Features

- **Password Hashing**: Passwords are hashed using bcrypt (12 rounds)
- **JWT Tokens**: Signed tokens with HS256 algorithm
- **Token Expiration**: Tokens automatically expire after configured time (default: 30 minutes)
- **Account Status**: Inactive accounts cannot access the API
- **Input Validation**: All inputs are validated using Pydantic schemas

## HTTP Status Codes

- **200 OK**: Successful GET, PUT, DELETE requests
- **201 Created**: Successful resource creation
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Invalid or missing authentication token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Duplicate resource (email/username already exists)
- **500 Internal Server Error**: Unexpected server error

## Database Configuration

The application uses SQLite by default. To switch to another database:

### PostgreSQL

1. Install the driver:
```bash
./venv/bin/pip install asyncpg
```

2. Update `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

### MySQL

1. Install the driver:
```bash
./venv/bin/pip install aiomysql
```

2. Update `.env`:
```
DATABASE_URL=mysql+aiomysql://user:password@localhost/dbname
```

## Environment Variables

Configuration is managed through the `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| APP_NAME | User Management System | Application name |
| DEBUG | True | Debug mode |
| DATABASE_URL | sqlite+aiosqlite:///./users.db | Database connection string |
| SECRET_KEY | (provided) | JWT secret key (change in production) |
| ALGORITHM | HS256 | JWT signing algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | 30 | Token expiration time |
| BCRYPT_ROUNDS | 12 | Password hashing rounds |

## Development

### Code Structure

- **Routers**: Handle HTTP requests and responses
- **Services**: Business logic and database operations
- **Models**: Database table definitions (SQLAlchemy)
- **Schemas**: Request/response validation (Pydantic)
- **Dependencies**: Reusable dependency functions (authentication)

### Key Concepts

- **Async/Await**: All database operations are asynchronous for better performance
- **Dependency Injection**: FastAPI automatically provides database sessions and current user
- **Pydantic Models**: Automatic validation and serialization
- **SQLAlchemy ORM**: Database operations using Python objects

## Important Notes

1. Change the SECRET_KEY in production (current key is for development only)
2. Tokens expire after 30 minutes by default (configurable)
3. CORS is configured to allow all origins (specify exact origins in production)
4. SQLite is suitable for development; use PostgreSQL for production

## License

This project is open source and available for learning purposes.
