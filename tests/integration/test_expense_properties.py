"""
Property-based tests for expense system invariants.

Uses Hypothesis to generate random test data and verify mathematical
properties that must ALWAYS hold true regardless of input.
"""

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from datetime import date, timedelta
from decimal import Decimal
from app.services.expense_service import ExpenseService
from app.models.database_models import User, Expense, Notification
from app.schemas import ExpenseCreate


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    amounts=st.lists(
        st.decimals(min_value=Decimal('0.01'), max_value=Decimal('9999.99'), places=2),
        min_size=1,
        max_size=20
    )
)
def test_total_expenses_equals_sum_of_amounts(postgres_test_db, amounts):
    """
    Property: Sum of all expense amounts in DB = sum of individual expenses.
    
    This tests data integrity - money can't appear or disappear.
    """
    # Clear database from previous Hypothesis runs
    postgres_test_db.query(Notification).delete()
    postgres_test_db.query(Expense).delete()
    postgres_test_db.query(User).delete()
    postgres_test_db.commit()
    
    # Arrange - Create service and users
    service = ExpenseService(postgres_test_db)
    
    submitter = User(email="john@test.com", name="John")
    approver = User(email="jane@test.com", name="Jane")
    postgres_test_db.add_all([submitter, approver])
    postgres_test_db.commit()
    
    # Act - Create expenses for each amount
    created_expenses = []
    for i, amount in enumerate(amounts):
        expense_data = ExpenseCreate(
            submitter_email="john@test.com",
            approver_email="jane@test.com",
            amount=amount,
            expense_date=date.today() - timedelta(days=i),
            category="Travel",
            description=f"Expense {i}"
        )
        expense = service.create_expense(expense_data)
        created_expenses.append(expense)
    
    # Assert - Verify property holds
    total_from_db = sum(
        e.amount for e in postgres_test_db.query(Expense).all()
    )
    expected_total = sum(amounts)
    
    assert total_from_db == expected_total


def test_every_expense_has_notification(postgres_test_db):
    """
    Property: Number of expenses = number of notifications.
    
    This tests the business rule that every expense creates exactly one notification.
    """
    # Arrange
    service = ExpenseService(postgres_test_db)
    
    submitter = User(email="john@test.com", name="John")
    approver = User(email="jane@test.com", name="Jane")
    postgres_test_db.add_all([submitter, approver])
    postgres_test_db.commit()
    
    # Act - Create 5 expenses
    for i in range(5):
        expense_data = ExpenseCreate(
            submitter_email="john@test.com",
            approver_email="jane@test.com",
            amount=Decimal('100.00'),
            expense_date=date.today(),
            category="Travel",
            description=f"Expense {i}"
        )
        service.create_expense(expense_data)
    
    # Assert - Verify property
    expense_count = postgres_test_db.query(Expense).count()
    notification_count = postgres_test_db.query(Notification).count()
    
    assert expense_count == notification_count
    assert expense_count == 5