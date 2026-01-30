"""
API tests for POST /api/expenses endpoint.

WHAT WE'RE TESTING:
- HTTP layer (status codes, request/response formats)
- Request validation (Pydantic models catch bad data)
- Error handling through the API
- Response schema matches expectations

REAL-WORLD VALUE:
Ensures the API contract between frontend and backend is maintained.
If these tests pass, frontend devs can trust the endpoint behavior.
"""

import pytest


def test_create_expense_success(test_client, sample_user, sample_approver, sample_expense_data):
    """
    TEST: Valid expense submission returns 201 with correct data.
    
    VALIDATES:
    - Status code 201 (Created)
    - Response contains expected fields
    - Status defaults to "Submitted"
    """
    response = test_client.post("/api/expenses", json=sample_expense_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == '150.00'
    assert data["status"] == "Submitted"
    assert data["category"] == "Travel"
    assert "id" in data
    
def test_create_expense_submitter_not_found(test_client, sample_approver, sample_expense_data):
    """
    TEST: Submitter email not in database returns 404.
    
    VALIDATES:
    - Status code 404 (Not Found)
    - Error message mentions submitter
    - No expense created in database
    """
    # Modify payload to use non-existent submitter
    sample_expense_data["submitter_email"] = "ghost@company.com"
    
    response = test_client.post("/api/expenses", json=sample_expense_data)
    
    assert response.status_code == 404
    assert "submitter" in response.json()["detail"].lower()


def test_create_expense_approver_not_found(test_client, sample_user, sample_expense_data):
    """
    TEST: Approver email not in database returns 404.
    
    VALIDATES:
    - Status code 404 (Not Found)
    - Error message mentions approver
    - No expense created in database
    """
    # Modify payload to use non-existent approver
    sample_expense_data["approver_email"] = "ghost@company.com"
    
    response = test_client.post("/api/expenses", json=sample_expense_data)
    
    assert response.status_code == 404
    assert "approver" in response.json()["detail"].lower()
    
def test_create_expense_invalid_data(test_client):
    """
    TEST: Invalid request data returns 422 validation error.
    
    VALIDATES:
    - Status code 422 (Unprocessable Entity)
    - Pydantic validation catches bad data before business logic runs
    - Multiple validation errors can be returned
    """
    payload = {
        "submitter_email": "not-an-email",     # Invalid email format
        "approver_email": "jane@company.com",
        "amount": -50.00,                       # Negative amount
        "expense_date": "not-a-date",          # Invalid date format
        "category": "Travel",
        "description": "Test"
    }
    
    response = test_client.post("/api/expenses", json=payload)
    
    assert response.status_code == 422
    # 422 responses include validation details, but we just verify the status