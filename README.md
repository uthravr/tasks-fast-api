# User Management System API

A RESTful backend service built with FastAPI, MySQL, SQLAlchemy ORM, Pydantic v2, and JWT-based authentication. This project provides secure user registration, token-based authentication, and CRUD operations for managing user profiles.

---

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [API Documentation (Swagger UI)](#api-documentation-swagger-ui)
- [Testing](#testing)

---

## Overview

The User Management System API provides a modular backend for account lifecycle management. It includes:
- User registration with input validation, duplicate email detection, and bcrypt password hashing.
- Token-based authentication using JSON Web Tokens (JWT) adhering to RFC 7519.
- Role-less resource isolation ensuring authenticated users can only create, view, update, and delete their own profile records.
- SQLAlchemy ORM session management integrated with FastAPI dependency injection.
- Automated API documentation generated via OpenAPI 3.1.0 specifications.

---

## Technology Stack

- **Runtime**: Python 3.10+
- **Web Framework**: FastAPI 0.110+
- **ASGI Server**: Uvicorn
- **Database**: MySQL Server 8.0+
- **ORM**: SQLAlchemy 2.0+
- **DB Driver**: PyMySQL + Cryptography
- **Data Validation & Serialization**: Pydantic v2
- **Password Hashing**: Bcrypt
- **Authentication**: PyJWT (HMAC-SHA256)
- **API Testing**: HTTPX / Starlette TestClient

---

## Project Architecture

The application adopts a separation-of-concerns pattern:

```
fast-api/
|
|-- app/
|   |-- __init__.py
|   |-- main.py              # Application entrypoint, CORS, and OpenAPI routing
|   |-- config.py            # Environment variable loading and configuration
|   |-- database.py          # Engine configuration, sessionmaker, and get_db dependency
|   |-- models/              # SQLAlchemy database models
|   |   |-- __init__.py
|   |   |-- user.py          # User ORM model
|   |   `-- profile.py       # Profile ORM model (Foreign Key: users.id)
|   |-- schemas/             # Pydantic validation and serialization schemas
|   |   |-- __init__.py
|   |   |-- user.py          # User registration, login, and response schemas
|   |   `-- profile.py       # Profile CRUD request and response schemas
|   |-- routers/             # Endpoint definitions
|   |   |-- __init__.py
|   |   |-- auth.py          # Authentication routes (/auth/register, /auth/login)
|   |   `-- users.py         # Profile management routes (/users/profile, /users/me, /users)
|   `-- utils/               # Reusable business and security utilities
|       |-- __init__.py
|       |-- security.py      # Bcrypt hashing and password verification
|       `-- auth.py          # JWT creation and get_current_user dependency
|
|-- .env                     # Local environment variables (excluded from VCS)
|-- .env.example             # Template environment variables
|-- .gitignore               # Version control exclusion rules
|-- requirements.txt         # Production and development dependencies
|-- test_api.py              # End-to-end integration test suite
`-- README.md                # Technical project documentation
```

---

## Database Schema

The database consists of two relational tables with referential integrity and cascading delete rules.

### 1. `users` Table

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | Primary Key, Auto Increment | Unique user identifier |
| `name` | VARCHAR(100) | NOT NULL | User's full name |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE, Indexed | Unique login email address |
| `hashed_password` | VARCHAR(255) | NOT NULL | Bcrypt hashed password string |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| `updated_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account update timestamp |

### 2. `profiles` Table

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | Primary Key, Auto Increment | Unique profile record identifier |
| `user_id` | INT | NOT NULL, UNIQUE, FK (`users.id` ON DELETE CASCADE) | Reference to owning user |
| `phone_number` | VARCHAR(20) | NULL | Optional contact phone number |
| `address` | TEXT | NULL | Optional postal address |
| `date_of_birth` | DATE | NULL | Optional date of birth (YYYY-MM-DD) |
| `bio` | TEXT | NULL | Optional biography or notes |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Profile creation timestamp |
| `updated_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Profile update timestamp |

---

## API Endpoints

### Authentication Endpoints

| HTTP Method | Route | Access | Request Body | Description |
|---|---|---|---|---|
| POST | `/auth/register` | Public | `UserRegister` | Registers a new user account |
| POST | `/auth/login` | Public | `UserLogin` | Verifies credentials and returns JWT |

### User Profile Endpoints

| HTTP Method | Route | Access | Request Body | Description |
|---|---|---|---|---|
| POST | `/users/profile` | Bearer Token | `ProfileCreate` | Creates personal profile for the authenticated user |
| GET | `/users/me` | Bearer Token | None | Retrieves authenticated user details and profile |
| GET | `/users` | Bearer Token | None | Retrieves paginated list of registered users |
| PUT | `/users/profile` | Bearer Token | `ProfileUpdate` | Updates profile fields for authenticated user |
| DELETE | `/users/profile` | Bearer Token | None | Deletes profile record of authenticated user |

### System Endpoints

| HTTP Method | Route | Access | Request Body | Description |
|---|---|---|---|---|
| GET | `/` | Public | None | Health check and documentation links |

---

## Prerequisites

Ensure the following tools are installed on your host system:
- Python 3.10 or higher
- MySQL Server 8.0 or higher
- Git

---

## Environment Configuration

Create a `.env` file in the project root directory based on `.env.example`:

```env
# Database Connection URL (Format: mysql+pymysql://<user>:<password>@<host>:<port>/<database>)
DATABASE_URL=mysql+pymysql://root:your_mysql_password@localhost:3306/user_management_db

# Security Configuration
SECRET_KEY=replace_with_a_secure_random_256_bit_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/uthravr/tasks-fast-api.git
   cd tasks-fast-api
   ```

2. **Create and activate a virtual environment:**
   - On Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - On Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the MySQL database exists:**
   ```sql
   CREATE DATABASE IF NOT EXISTS user_management_db;
   ```
   *(Tables are automatically created by SQLAlchemy during application startup).*

---

## Running the Application

Start the Uvicorn ASGI development server:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The service will be accessible at:
- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## API Documentation (Swagger UI)

FastAPI automatically serves an interactive Swagger documentation portal at `/docs`.

### Authentication Workflow in Swagger UI:
1. Navigate to `http://127.0.0.1:8000/docs`.
2. Execute `POST /auth/register` to create a user account.
3. Execute `POST /auth/login` with the registered email and password.
4. Copy the `access_token` string from the JSON response.
5. Click the **Authorize** button at the top right of the page.
6. Enter the token into the **Value** field and confirm.
7. All protected `/users/*` endpoints can now be executed directly within the browser interface.

---

## Testing

An end-to-end integration test suite is included in `test_api.py`. It verifies all 10 core specification modules:
- User registration and duplicate constraint validation
- Schema format validation
- Authentication credential verification
- JWT generation and bearer token authorization
- CRUD operations for user profiles
- Direct database persistence checks against MySQL

Run the test suite:

```bash
python test_api.py
```
