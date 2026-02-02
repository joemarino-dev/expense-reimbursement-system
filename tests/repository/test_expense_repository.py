"""
Repository tests for ExpenseRepository.

These tests use a real SQLite test database to validate:
- Data persistence and retrieval
- Database constraints
- Query correctness
- Transaction handling
"""

import pytest
from datetime import date
from app.repositories.expense_repository import ExpenseRepository
from app.schemas import ExpenseCreate


def test_create_expense_persists_to_database(
    expense_repository,
    sample_user,
    sample_approver
):
    """Test that creating an expense actually saves it to the database."""
    # Arrange - Create expense data with required emails
    expense_data = ExpenseCreate(
        submitter_email=sample_user.email,
        approver_email=sample_approver.email,
        amount=150.00,
        expense_date=date(2026, 1, 15),
        category="Travel",
        description="Client meeting"
    )
    
    # Act - Create expense
    expense = expense_repository.create(expense_data)
    
    # Assert - Verify it was saved
    assert expense.id is not None
    assert expense.amount == 150.00
    assert expense.status == "Submitted"
    assert expense.user_email == sample_user.email
    assert expense.approver_email == sample_approver.email
    assert expense.submitted_at is not None


def test_get_by_id_retrieves_correct_expense(
    expense_repository,
    sample_user,
    sample_approver
):
    """Test that we can retrieve an expense by its ID."""
    # Arrange - Create an expense first
    expense_data = ExpenseCreate(
        submitter_email=sample_user.email,
        approver_email=sample_approver.email,
        amount=250.00,
        expense_date=date(2026, 1, 20),
        category="Meals",
        description="Team lunch"
    )
    
    created_expense = expense_repository.create(expense_data)
    
    # Act - Retrieve by ID
    retrieved = expense_repository.get_by_id(created_expense.id)
    
    # Assert
    assert retrieved is not None
    assert retrieved.id == created_expense.id
    assert retrieved.amount == 250.00
    assert retrieved.category == "Meals"
    assert retrieved.description == "Team lunch"


def test_get_by_id_returns_none_for_nonexistent_expense(expense_repository):
    """Test that querying a non-existent ID returns None."""
    # Act
    result = expense_repository.get_by_id(99999)
    
    # Assert
    assert result is None


def test_multiple_expenses_can_be_created_for_same_user(
    expense_repository,
    sample_user,
    sample_approver
):
    """Test that a user can submit multiple expenses."""
    # Arrange - Create first expense data
    expense_data1 = ExpenseCreate(
        submitter_email=sample_user.email,
        approver_email=sample_approver.email,
        amount=100.00,
        expense_date=date(2026, 1, 15),
        category="Travel",
        description="Flight"
    )
    
    # Act - Create first expense
    expense1 = expense_repository.create(expense_data1)
    
    # Arrange - Create second expense data
    expense_data2 = ExpenseCreate(
        submitter_email=sample_user.email,
        approver_email=sample_approver.email,
        amount=50.00,
        expense_date=date(2026, 1, 16),
        category="Meals",
        description="Dinner"
    )
    
    # Act - Create second expense
    expense2 = expense_repository.create(expense_data2)
    
    # Assert
    assert expense1.id != expense2.id
    assert expense1.user_email == expense2.user_email == sample_user.email