"""
Business logic for expense operations.
Uses repository layer for data access.
"""
from datetime import date
from decimal import Decimal
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
        """Create a new expense with validation."""
        # Validate users exist
        submitter = self.user_repo.get_by_email(expense_data.submitter_email)
        if not submitter:
            raise HTTPException(
                status_code=404,
                detail=f"User not found: {expense_data.submitter_email}"
            )
        
        approver = self.user_repo.get_by_email(expense_data.approver_email)
        if not approver:
            raise HTTPException(
                status_code=404,
                detail=f"Approver not found: {expense_data.approver_email}"
            )
        
        # Create expense
        expense = self.expense_repo.create(expense_data)
        
        # Log notification
        self.notification_repo.create(
            expense_id=expense.id,
            event_type="expense_submitted",
            message=f"Expense submitted by {expense_data.submitter_email}"
        )
        
        return expense