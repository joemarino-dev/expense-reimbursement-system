"""
API routes for expense operations.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import ExpenseCreate, ExpenseResponse
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    """
    Submit a new expense for approval.
    
    - **submitter_email**: Email of employee submitting expense
    - **approver_email**: Email of manager who will approve
    - **amount**: Expense amount (must be positive)
    - **date**: Date of expense
    - **category**: Expense category
    - **description**: Detailed description
    """
    service = ExpenseService(db)
    return service.create_expense(expense)

