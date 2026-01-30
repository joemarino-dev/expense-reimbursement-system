"""
Repository for expense data access operations.
Handles all database interactions for Expense entities.
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.database_models import Expense
from app.schemas import ExpenseCreate


class ExpenseRepository:
    """Handles database operations for expenses."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, expense_data: ExpenseCreate, user_email: str, approver_email: str) -> Expense:
        """Create a new expense record."""
        expense = Expense(
            user_email=user_email,
            amount=expense_data.amount,
            expense_date=expense_data.expense_date,
            category=expense_data.category,
            description=expense_data.description,
            status="Submitted",
            approver_email=approver_email
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense
    
    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        """Get expense by ID."""
        return self.db.query(Expense).filter(Expense.id == expense_id).first()
    
    def get_all(self) -> list[Expense]:
        """Get all expenses."""
        return self.db.query(Expense).all()
