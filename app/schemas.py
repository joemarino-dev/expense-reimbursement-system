"""
Pydantic schemas for API request/response validation.
"""
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense submission."""
    submitter_email: EmailStr
    amount: Decimal = Field(..., gt=0, description="Amount must be greater than 0")
    expense_date: date
    category: str = Field(..., description="Must be one of: Travel, Meals, Supplies, Equipment, Other")
    description: str = Field(..., min_length=1, max_length=500)
    approver_email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "submitter_email": "john.doe@company.com",
                "amount": 125.50,
                "expense_date": "2026-01-20",
                "category": "Travel",
                "description": "Uber to client meeting",
                "approver_email": "jane.manager@company.com"
            }
        }
    }


class ExpenseResponse(BaseModel):
    """Schema for expense data returned by the API."""
    id: int
    user_email: str
    amount: Decimal
    expense_date: date
    category: str
    description: str
    status: str
    approver_email: str
    submitted_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}