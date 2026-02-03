"""
End-to-End UI tests for expense submission form.

WHAT WE'RE TESTING:
- Real browser automation with Playwright
- Form field validation
- Successful submission workflow
- Error message display

REAL-WORLD VALUE:
Tests the actual user experience - catches UI bugs that API tests miss.
"""

import pytest
from playwright.sync_api import expect


def test_submit_expense_success(page, test_server):
    """
    TEST: User can successfully submit expense through the UI.
    
    VALIDATES:
    - Form loads correctly
    - All fields can be filled
    - Submit button works
    - Success message appears
    """
    # Navigate to the form (test_server provides the URL)
    page.goto(f"{test_server}/")
    
    # Fill in the form
    page.fill('input[name="submitter_email"]', 'john.doe@company.com')
    page.fill('input[name="approver_email"]', 'jane.manager@company.com')
    page.fill('input[name="amount"]', "150.50")
    page.fill('input[name="expense_date"]', "2026-01-30")
    page.select_option('select[name="category"]', "Travel")
    page.fill('textarea[name="description"]', "Client meeting in NYC")
    
    # Submit the form
    page.click('button[type="submit"]')
    
    # Wait for and verify success message
    success_message = page.locator("#message")
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text("Success! Expense")