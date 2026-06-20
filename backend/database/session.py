"""
Database Session
================
SQLAlchemy engine and session factory.

Configuration is read from the DATABASE_URL environment variable (see .env).
Default: SQLite for zero-config local development.
Production: Set DATABASE_URL to a PostgreSQL connection string.

Usage (in route handlers):
    from backend.database.session import get_db
    from fastapi import Depends

    @router.get("/example")
    def example(db: Session = Depends(get_db)):
        ...
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./corpus_dev.db")

# SQLite needs this extra flag; it is ignored for other databases.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency that yields a database session per request."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
