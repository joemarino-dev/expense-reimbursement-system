"""
Business logic for expense operations.
Uses repository layer for data access.
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas import ExpenseCreate
from app.models.database_models import Expense
from app.repositories import ExpenseRepository, UserRepository, NotificationRepository


class ExpenseService:
    """Business logic for expense operations."""
    
    def __init__(self, db: Session):
        self.expense_repo = ExpenseRepository(db)
        self.user_repo = UserRepository(db)
        self.notification_repo = NotificationRepository(db)
    
    def create_expense(self, expense_data: ExpenseCreate) -> Expense:
        """
        Create a new expense submission.
        
        Business rules:
        - Submitter must exist in system
        - Approver must exist in system
        - Creates notification event log
        """
        # Validate submitter exists
        submitter = self.user_repo.get_by_email(expense_data.submitter_email)
        if not submitter:
            raise HTTPException(
                status_code=404,
                detail=f"Submitter email '{expense_data.submitter_email}' not found in system"
            )
        
        # Validate approver exists
        approver = self.user_repo.get_by_email(expense_data.approver_email)
        if not approver:
            raise HTTPException(
                status_code=404,
                detail=f"Approver email '{expense_data.approver_email}' not found in system"
            )
        
        # Create expense
        expense = self.expense_repo.create(
            expense_data=expense_data,
            user_email=expense_data.submitter_email,
            approver_email=expense_data.approver_email
        )
        
        # Log notification event
        self.notification_repo.create(
            expense_id=expense.id,
            event_type="expense_submitted",
            message=f"Expense ${expense.amount} submitted by {expense.user_email}"
        )
        
        return expense
