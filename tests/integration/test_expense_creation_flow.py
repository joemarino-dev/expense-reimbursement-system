"""
Integration test: Expense creation flow through all layers.

Tests Service → Repository → Database without mocks.
"""
import pytest
from datetime import date
from app.services.expense_service import ExpenseService


def test_expense_creation_full_flow(postgres_test_db):
    """Test complete expense creation through all layers."""
    # Arrange - Create the service with real repositories
    service = ExpenseService(postgres_test_db)
    
    # Create test users
    from app.models.database_models import User
    submitter = User(email="john@test.com", name="John")
    approver = User(email="jane@test.com", name="Jane")
    postgres_test_db.add_all([submitter, approver])
    postgres_test_db.commit()
    
    # Create expense data
    from app.schemas import ExpenseCreate
    expense_data = ExpenseCreate(
        submitter_email="john@test.com",
        approver_email="jane@test.com",
        amount=100.00,
        expense_date=date(2026, 2, 3),
        category="Travel",
        description="Test expense"
    )
    
    # Act - Create expense through service
    result = service.create_expense(expense_data)
    
    # Assert - Verify in database
    assert result.id is not None
    assert result.status == "Submitted"
    
    # Verify notification was created in database
    from app.models.database_models import Notification
    notifications = postgres_test_db.query(Notification).filter_by(expense_id=result.id).all()
    assert len(notifications) > 0
    assert notifications[0].event_type == "expense_submitted"