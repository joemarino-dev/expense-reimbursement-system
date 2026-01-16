# Expense Reimbursement System - Architecture

## Overview
Three-tier web application: Frontend (HTML/JS) → Backend API (Flask) → Database (SQLite)

## Technology Stack

**Backend:**
- Flask (REST API)
- SQLite (database)
- SQLAlchemy (ORM - optional, can use raw SQL)

**Frontend:**
- HTML/CSS/JavaScript (vanilla or minimal framework)
- Fetch API for backend calls

**Testing:**
- pytest (unit, integration, API tests)
- Playwright (E2E UI tests)
- pytest-bdd (BDD scenarios)
- Allure (reporting)

**DevOps:**
- GitHub Actions (CI/CD)
- Docker (containerization)

## API Design

### Endpoints

**Expenses**
- POST /api/expenses - Submit new expense
- GET /api/expenses - List expenses (with filters)
- GET /api/expenses/:id - Get expense details
- PUT /api/expenses/:id/approve - Approve expense
- PUT /api/expenses/:id/reject - Reject expense

**Analytics**
- GET /api/expenses/summary - Totals by status, category

### Sample Request/Response

POST /api/expenses
```json
{
  "user_email": "joe@example.com",
  "amount": 125.50,
  "date": "2026-01-15",
  "category": "Meals",
  "description": "Client dinner",
  "approver_email": "manager@example.com"
}
```

Response:
```json
{
  "id": 1,
  "status": "Submitted",
  "submitted_at": "2026-01-15T10:30:00Z"
}
```

## Database Schema
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    user_email TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    date DATE NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    approver_email TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_email) REFERENCES users(email),
    FOREIGN KEY (approver_email) REFERENCES users(email)
);

CREATE TABLE approvals (
    id INTEGER PRIMARY KEY,
    expense_id INTEGER NOT NULL,
    approver_email TEXT NOT NULL,
    action TEXT NOT NULL,
    rejection_reason TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expense_id) REFERENCES expenses(id)
);

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    expense_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expense_id) REFERENCES expenses(id)
);
```

## State Machine
```
[Submitted] --> [Approved]
            --> [Rejected]
```

Business Rules:
- Once approved/rejected, status is final (no state reversal)
- Only expenses in "Submitted" status can be approved/rejected
- Rejection requires reason; approval does not

## Testing Strategy

**Unit Tests:** Business logic, validation rules
**API Tests:** All endpoints, error handling, status codes
**Database Tests:** Data integrity, constraints, aggregations
**Integration Tests:** Full workflows (submit → approve → notification)
**E2E Tests:** UI interactions with Playwright
**Property-Based Tests:** Mathematical invariants (totals, balances)

## Deployment

**Local Development:**
```bash
python app.py  # Runs on localhost:5000
```

**Docker:**
```bash
docker build -t expense-app .
docker run -p 5000:5000 expense-app
```

**CI/CD:**
GitHub Actions runs on every commit:
- Linting (flake8)
- Unit tests
- API tests
- Integration tests
- E2E tests
- Test coverage report
