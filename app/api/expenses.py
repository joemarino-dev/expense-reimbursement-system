"""
API endpoints for expense operations.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import ExpenseCreate, ExpenseResponse
from app.database import get_db
from app.services import expense_service

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseResponse, status_code=201)
def create_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db)
):
    """Create a new expense submission."""
    return expense_service.create_expense(expense_data, db)