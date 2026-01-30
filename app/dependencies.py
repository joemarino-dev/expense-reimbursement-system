"""Dependency injection functions for FastAPI."""

from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import SessionLocal
from app.services.expense_service import ExpenseService


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to provide database session.
    Yields session and ensures it's closed after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_expense_service(db: Session = Depends(get_db)) -> ExpenseService:
    """Dependency to provide ExpenseService instance."""
    return ExpenseService(db)