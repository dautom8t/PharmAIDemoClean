"""
Database configuration and session management.

This module sets up a simple SQLAlchemy engine pointing at an SQLite database by default.
You can switch the database URL via the `DATABASE_URL` environment variable.

The sessionmaker pattern is used to provide dependency‑injected sessions in FastAPI endpoints.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Default to a local SQLite database.  For production use, replace with Postgres or MySQL.
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pharmAI.db")

# The `check_same_thread` argument is needed for SQLite in multithreaded FastAPI applications.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions.
Base = declarative_base()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations.

    This function is used as a dependency in FastAPI endpoints.  It yields a SQLAlchemy
    session and ensures that the session is closed after the request is finished.

    Example:
        with get_db() as db:
            # use db session here
    """
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()