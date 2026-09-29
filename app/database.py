from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator
from app.config import DATABASE_URL

# Create the SQLAlchemy engine for MySQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# Create session maker for managing database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

def get_db() -> Generator:
    """
    Dependency that provides a database session to FastAPI route handlers.
    Ensures that the session is properly closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
