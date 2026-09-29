from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import auth_router, users_router
import app.models  # Ensures all models are registered with Base.metadata

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables automatically upon startup if they do not exist
    Base.metadata.create_all(bind=engine)
    yield

tags_metadata = [
    {
        "name": "Authentication",
        "description": "User registration and login operations with JWT token generation.",
    },
    {
        "name": "User Profiles",
        "description": "Authenticated CRUD operations for managing user profiles and viewing registered users.",
    },
]

app = FastAPI(
    title="User Management System API",
    description="""
## User Management System API with FastAPI & MySQL

This backend API provides secure user registration, authentication via JWT Bearer tokens, and full CRUD operations for managing user profiles.

### Features
* **Module 1**: Project Setup & MySQL connection using SQLAlchemy ORM.
* **Module 2**: User Registration with input validation, duplicate check, and bcrypt password hashing.
* **Module 3**: User Login with password verification and JWT token issuance.
* **Module 4**: Authentication & Authorization protecting profile endpoints.
* **Module 5**: Create User Profile (phone number, address, date of birth, bio).
* **Module 6**: Read User Profile (`/users/me`) and list registered users (`/users`).
* **Module 7**: Update User Profile (`PUT /users/profile`).
* **Module 8**: Delete User Profile (`DELETE /users/profile`).
* **Module 9**: Robust error handling with clear HTTP status codes.
* **Module 10**: Interactive testing via Swagger UI (`/docs`).

### How to Authenticate in Swagger UI:
1. Register a new user at `POST /auth/register` or log in at `POST /auth/login`.
2. Copy the `access_token` from the response.
3. Click the **Authorize** button (padlock icon) at the top right of this page.
4. Paste your token into the **Value** input field and click **Authorize**.
5. You can now execute all protected endpoints (`/users/profile`, `/users/me`, `/users`).
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(auth_router)
app.include_router(users_router)

@app.get("/", tags=["Root"])
def root():
    return {
        "project": "User Management System API",
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
