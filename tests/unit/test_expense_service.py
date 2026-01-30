"""
Unit tests for ExpenseService.create_expense()

PURPOSE OF THESE TESTS:
We are testing the SERVICE LAYER'S BUSINESS LOGIC in isolation.

WHAT WE'RE TESTING:
1. Does the service validate users exist before creating expense?
2. Does the service raise correct exceptions when validation fails?
3. Does the service call repositories in the correct order?
4. Does the service pass correct data to repositories?

WHAT WE'RE NOT TESTING:
- Does the repository actually save to database? (that's repository tests)
- Does the API endpoint work? (that's API tests)
- Does the full system work end-to-end? (that's integration tests)

WHY MOCK REPOSITORIES:
- Unit tests should be FAST (no database I/O)
- Unit tests should be ISOLATED (one failure = one problem)
- We're testing the service's LOGIC, not the repository's implementation
"""

import pytest
from datetime import date
from fastapi import HTTPException
from app.services.expense_service import ExpenseService
from app.models.database_models import User, Expense
from app.schemas import ExpenseCreate


def test_create_expense_success(
    mock_user_repository,
    mock_expense_repository,
    mock_notification_repository,
    mocker
):
    """
    TEST: Happy path - all validations pass, expense created successfully.
    
    BUSINESS LOGIC BEING TESTED:
    1. Service validates submitter exists
    2. Service validates approver exists  
    3. Service creates expense via repository
    4. Service logs notification event
    5. Service returns created expense
    
    WHY THIS TEST MATTERS:
    Proves the service orchestrates all steps in correct order without errors.
    """
    
    # ========================================================================
    # ARRANGE - Set up mocks to simulate successful flow
    # ========================================================================
    
    # Create service with mocked database session
    mock_db = mocker.Mock()
    service = ExpenseService(mock_db)
    
    # Monkey-patch: Replace repositories service created with our mocks
    service.user_repo = mock_user_repository
    service.expense_repo = mock_expense_repository
    service.notification_repo = mock_notification_repository
    
    # Create fake users that repository would return
    submitter = User(id=1, email="john@company.com", name="John Doe")
    approver = User(id=2, email="jane@company.com", name="Jane Manager")
    
    # Configure mock: first call returns submitter, second call returns approver
    mock_user_repository.get_by_email.side_effect = [submitter, approver]
    
    # Create fake expense that repository would return after saving
    created_expense = Expense(
        id=1,
        user_email="john@company.com",      # CORRECT
        approver_email="jane@company.com",  # CORRECT
        amount=150.00,
        expense_date=date(2026, 1, 15),
        category="Travel",
        description="Client meeting",
        status="Submitted"
)
    
    # Configure mock: when create() is called, return this fake expense
    mock_expense_repository.create.return_value = created_expense
    
    # Prepare input data
    expense_data = ExpenseCreate(
        submitter_email="john@company.com",
        approver_email="jane@company.com",
        amount=150.00,
        expense_date=date(2026, 1, 15),
        category="Travel",
        description="Client meeting"
    )
    
    # ========================================================================
    # ACT - Call the service method we're testing
    # ========================================================================
    
    result = service.create_expense(expense_data)
    
    # ========================================================================
    # ASSERT - Verify the service orchestrated everything correctly
    # ========================================================================
    
    # Verify user validation happened (get_by_email called twice)
    assert mock_user_repository.get_by_email.call_count == 2
    
    # Verify expense creation happened
    mock_expense_repository.create.assert_called_once()
    
    # Verify notification was logged
    mock_notification_repository.create.assert_called_once()
    
    # Verify service returned the expense from repository
    assert result == created_expense
    assert result.id == 1
    assert result.amount == 150.00


def test_create_expense_submitter_not_found(
    mock_user_repository,
    mock_expense_repository,
    mock_notification_repository,
    mocker
):
    """
    TEST: Service raises HTTPException when submitter doesn't exist.
    
    BUSINESS LOGIC BEING TESTED:
    - Service validates submitter exists BEFORE creating expense
    - Service raises 404 HTTPException with correct error message
    - Service does NOT create expense if validation fails
    
    WHY THIS TEST MATTERS:
    Ensures bad data is caught early and doesn't pollute the database.
    """
    
    # ARRANGE
    mock_db = mocker.Mock()
    service = ExpenseService(mock_db)
    
    # Monkey-patch repositories
    service.user_repo = mock_user_repository
    service.expense_repo = mock_expense_repository
    service.notification_repo = mock_notification_repository
    
    # Configure mock: submitter not found (returns None)
    mock_user_repository.get_by_email.return_value = None
    
    expense_data = ExpenseCreate(
        submitter_email="nonexistent@company.com",
        approver_email="jane@company.com",
        amount=150.00,
        expense_date=date(2026, 1, 15),
        category="Travel",
        description="Test"
    )
    
    # ACT & ASSERT - Verify exception is raised
    with pytest.raises(HTTPException) as exc_info:
        service.create_expense(expense_data)
    
    # Verify exception details
    assert exc_info.value.status_code == 404
    assert "Submitter email" in exc_info.value.detail
    assert "nonexistent@company.com" in exc_info.value.detail
    
    # Verify expense was NEVER created (validation failed first)
    mock_expense_repository.create.assert_not_called()
    
    # Verify notification was NEVER logged (validation failed first)
    mock_notification_repository.create.assert_not_called()


def test_create_expense_approver_not_found(
    mock_user_repository,
    mock_expense_repository,
    mock_notification_repository,
    mocker
):
    """
    TEST: Service raises HTTPException when approver doesn't exist.
    
    BUSINESS LOGIC BEING TESTED:
    - Service validates approver exists AFTER submitter validation
    - Service raises 404 HTTPException with correct error message
    - Service does NOT create expense if validation fails
    
    WHY THIS TEST MATTERS:
    Ensures both users are validated before any database writes occur.
    """
    
    # ARRANGE
    mock_db = mocker.Mock()
    service = ExpenseService(mock_db)
    
    # Monkey-patch repositories
    service.user_repo = mock_user_repository
    service.expense_repo = mock_expense_repository
    service.notification_repo = mock_notification_repository
    
    # Configure mock: submitter exists, but approver doesn't
    submitter = User(id=1, email="john@company.com", name="John Doe")
    mock_user_repository.get_by_email.side_effect = [submitter, None]
    
    expense_data = ExpenseCreate(
        submitter_email="john@company.com",
        approver_email="nonexistent@company.com",
        amount=150.00,
        expense_date=date(2026, 1, 15),
        category="Travel",
        description="Test"
    )
    
    # ACT & ASSERT
    with pytest.raises(HTTPException) as exc_info:
        service.create_expense(expense_data)
    
    assert exc_info.value.status_code == 404
    assert "Approver email" in exc_info.value.detail
    assert "nonexistent@company.com" in exc_info.value.detail
    
    # Verify expense never created
    mock_expense_repository.create.assert_not_called()
    mock_notification_repository.create.assert_not_called()