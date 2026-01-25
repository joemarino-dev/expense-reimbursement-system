"""
Business logic for expense operations.
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas import ExpenseCreate
from app.models.database_models import Expense, User, Notification


def create_expense(expense_data: ExpenseCreate, db: Session) -> Expense:
    """
    Create a new expense submission.
    
    Business rules:
    - Submitter must exist as a user
    - Approver must exist as a user
    - Status defaults to 'Submitted'
    
    Raises:
        HTTPException: If submitter or approver not found
    
    Returns:
        Created Expense object
    """
    # Verify submitter exists
    submitter = db.query(User).filter(User.email == expense_data.submitter_email).first()
    if not submitter:
        raise HTTPException(
            status_code=404,
            detail=f"Submitter with email {expense_data.submitter_email} not found. User must be registered first."
        )
    
    # Verify approver exists
    approver = db.query(User).filter(User.email == expense_data.approver_email).first()
    if not approver:
        raise HTTPException(
            status_code=404,
            detail=f"Approver with email {expense_data.approver_email} not found. User must be registered first."
        )
    
    # Create the expense
    new_expense = Expense(
        user_email=expense_data.submitter_email,
        amount=expense_data.amount,
        expense_date=expense_data.expense_date,
        category=expense_data.category,
        description=expense_data.description,
        status="Submitted",
        approver_email=expense_data.approver_email
    )
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    # Create notification event
    notification = Notification(
        expense_id=new_expense.id,
        event_type="expense_submitted",
        message=f"Expense #{new_expense.id} submitted by {expense_data.submitter_email} for ${expense_data.amount}"
    )
    
    db.add(notification)
    db.commit()
    
    return new_expense