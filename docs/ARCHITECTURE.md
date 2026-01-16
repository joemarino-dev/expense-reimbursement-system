# Expense Reimbursement System - Architecture

## Overview

This document describes the architectural design of the Expense Reimbursement System, a full-stack application built to demonstrate modern software development practices, comprehensive test automation, and AI-assisted development workflows.

**Primary Goals:**
- Demonstrate production-quality architecture patterns
- Enable comprehensive test automation across all layers
- Showcase modern Python web development practices
- Provide realistic business domain implementation
- Support multiple testing strategies (unit, integration, API, E2E, database)

## Architectural Pattern

**Layered Architecture with Dependency Injection**

This architecture separates concerns into distinct layers, making each layer independently testable and maintainable. This is the industry-standard pattern for web applications and aligns with what QA automation engineers encounter in production environments.

```
┌─────────────────────────────────────┐
│     Frontend (HTML/JS)              │
└─────────────────────────────────────┘
                 ↓ HTTP
┌─────────────────────────────────────┐
│     API Layer (FastAPI Routes)      │  ← Request/Response handling
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│     Service Layer                   │  ← Business logic
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│     Repository Layer (SQLAlchemy)   │  ← Data access
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│     Database (PostgreSQL)           │  ← Data persistence
└─────────────────────────────────────┘
```

**Why This Architecture?**
- **Clear separation of concerns**: Each layer has a single responsibility
- **Testability**: Each layer can be tested independently with appropriate mocking
- **Industry standard**: This pattern is used across modern web applications
- **Maintainability**: Changes in one layer have minimal impact on others
- **Realistic**: Reflects production application architecture

## Technology Stack

### Backend Framework: FastAPI

**Chosen over Flask because:**
- Built-in OpenAPI/Swagger documentation (industry standard)
- Pydantic models provide automatic request/response validation
- Type hints throughout improve code quality and IDE support
- Modern async support (prepared for future scaling)
- Growing adoption in enterprise environments (Netflix, Uber, Microsoft)

**Testing benefit:** Strong typing and validation reduce bugs, automatic API docs aid API testing

### Database: PostgreSQL (in Docker)

**Chosen over SQLite because:**
- Production-realistic: PostgreSQL is the most common production database
- Full SQL feature support (constraints, transactions, complex queries)
- Better demonstrates database testing skills
- Docker deployment shows DevOps understanding
- More impressive for portfolio/interviews

**Testing benefit:** Real database transactions, constraints testing, more realistic SQL validation

### ORM: SQLAlchemy with Alembic

**Why SQLAlchemy:**
- Industry standard Python ORM
- Enables repository pattern implementation
- Easier to mock for unit testing
- Rich query API demonstrates SQL knowledge
- Supports complex relationships and constraints

**Why Alembic:**
- Database schema versioning (migrations)
- Shows understanding of schema evolution
- Enables test database setup/teardown strategies
- Production-grade database change management

**Testing benefit:** Clean data access abstraction, easy fixture creation, migration testing

### Frontend: Simple HTML/JavaScript

**Deliberately simple because:**
- Focus is on backend and testing, not frontend complexity
- Sufficient to demonstrate E2E testing with Playwright
- Faster development allows more time for comprehensive testing
- Realistic for internal tools and admin interfaces

**Testing benefit:** Stable, straightforward UI for Playwright automation

### Containerization: Docker & Docker Compose

**Why Docker:**
- PostgreSQL runs in container for consistent environment
- Application containerization shows DevOps knowledge
- Enables consistent test environments (CI/CD)
- Standard in modern development workflows

**Testing benefit:** Reproducible test environments, isolated database instances

## Component Breakdown

### Directory Structure

```
expense-reimbursement-system/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Environment-based configuration
│   ├── database.py              # Database connection and session management
│   │
│   ├── api/                     # API Layer - HTTP request/response handling
│   │   ├── __init__.py
│   │   ├── dependencies.py      # Dependency injection
│   │   ├── expenses.py          # Expense endpoints
│   │   └── health.py            # Health check endpoints
│   │
│   ├── services/                # Service Layer - Business logic
│   │   ├── __init__.py
│   │   ├── expense_service.py   # Expense business rules
│   │   └── notification_service.py  # Notification logic
│   │
│   ├── repositories/            # Repository Layer - Data access
│   │   ├── __init__.py
│   │   ├── expense_repository.py
│   │   └── user_repository.py
│   │
│   └── models/
│       ├── __init__.py
│       ├── database_models.py   # SQLAlchemy ORM models
│       └── schemas.py           # Pydantic request/response models
│
├── tests/
│   ├── conftest.py              # Shared pytest fixtures
│   ├── unit/                    # Service layer unit tests (mocked repos)
│   ├── integration/             # Repository layer tests (real DB)
│   ├── api/                     # API endpoint tests
│   ├── database/                # Property-based database tests
│   ├── e2e/                     # Playwright end-to-end tests
│   └── bdd/                     # pytest-bdd feature files
│
├── alembic/                     # Database migrations
│   ├── versions/
│   └── env.py
│
├── frontend/                    # Simple HTML/JS frontend
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── docker-compose.yml           # Multi-container setup
├── Dockerfile                   # Application container
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
└── docs/
    ├── ARCHITECTURE.md          # This file
    ├── API.md                   # API documentation
    └── TESTING_STRATEGY.md      # Test approach and coverage
```

### Layer Responsibilities

#### API Layer (`app/api/`)
- HTTP request/response handling
- Input validation (Pydantic schemas)
- Route definitions
- Dependency injection setup
- Error handling and status codes

**No business logic** - delegates to service layer

#### Service Layer (`app/services/`)
- Business rule implementation
- Workflow orchestration
- Transaction boundaries
- Cross-cutting concerns (logging, etc.)
- Business validation

**No data access logic** - calls repository layer

#### Repository Layer (`app/repositories/`)
- Database queries (SQLAlchemy)
- CRUD operations
- Data filtering and aggregation
- No business logic - pure data access

**Benefits:** Easy to mock for service layer testing, isolates SQL logic

## Data Model

### Database Schema

```sql
-- Users (simplified - no authentication for MVP)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expenses
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    expense_date DATE NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('Travel', 'Meals', 'Supplies', 'Equipment', 'Other')),
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Submitted' CHECK (status IN ('Submitted', 'Approved', 'Rejected')),
    approver_email VARCHAR(255),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_email) REFERENCES users(email)
);

-- Approvals (audit trail)
CREATE TABLE approvals (
    id SERIAL PRIMARY KEY,
    expense_id INTEGER NOT NULL,
    approver_email VARCHAR(255) NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('Approved', 'Rejected')),
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expense_id) REFERENCES expenses(id),
    FOREIGN KEY (approver_email) REFERENCES users(email)
);

-- Notifications (no actual emails - just audit log)
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    expense_id INTEGER NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expense_id) REFERENCES expenses(id)
);
```

**Key Design Decisions:**
- Email as user identifier (simplified auth for MVP)
- CHECK constraints demonstrate database-level validation
- Foreign keys ensure referential integrity
- Separate approvals table for audit trail
- Timestamps for all key events

**Testing implications:**
- Constraints allow testing database-level validation
- Audit trail enables testing approval workflows
- Clear relationships support integration testing

## API Design

### RESTful Endpoints

```
POST   /api/expenses              # Submit new expense
GET    /api/expenses              # List all expenses (with filters)
GET    /api/expenses/{id}         # Get specific expense
PUT    /api/expenses/{id}/approve # Approve expense
PUT    /api/expenses/{id}/reject  # Reject expense

GET    /api/dashboard/summary     # Get expense summaries/totals

GET    /health                    # Health check
```

### Request/Response Schemas (Pydantic)

```python
class ExpenseCreate(BaseModel):
    user_email: EmailStr
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    expense_date: date
    category: ExpenseCategory  # Enum
    description: str = Field(min_length=10, max_length=500)
    approver_email: EmailStr

class ExpenseResponse(BaseModel):
    id: int
    user_email: EmailStr
    amount: Decimal
    expense_date: date
    category: ExpenseCategory
    description: str
    status: ExpenseStatus  # Enum
    approver_email: EmailStr
    submitted_at: datetime
    updated_at: datetime
```

**Testing benefit:** Pydantic provides automatic validation, making API contract testing straightforward

## Testing Strategy Alignment

This architecture enables **5 distinct test levels**:

### 1. Unit Tests (`tests/unit/`)
- **Target:** Service layer functions
- **Approach:** Mock repository layer
- **Example:** Test expense approval business rules with mocked data access
- **Speed:** Very fast (no I/O)

### 2. Integration Tests (`tests/integration/`)
- **Target:** Repository layer + database
- **Approach:** Real PostgreSQL test database
- **Example:** Test that expense queries return correct filtered results
- **Speed:** Fast (local database)

### 3. API Tests (`tests/api/`)
- **Target:** FastAPI endpoints
- **Approach:** FastAPI TestClient with test database
- **Example:** POST expense, verify 201 response and correct JSON
- **Coverage:** Request validation, status codes, response schemas

### 4. Database Tests (`tests/database/`)
- **Target:** Data integrity and constraints
- **Approach:** Property-based testing with direct SQL
- **Example:** Verify amount calculations, constraint violations
- **Coverage:** Business rules at database level

### 5. End-to-End Tests (`tests/e2e/`)
- **Target:** Full application workflow
- **Approach:** Playwright browser automation
- **Example:** Submit expense via UI, approve via UI, verify in database
- **Coverage:** Complete user journeys

**Plus:** BDD layer (`tests/bdd/`) with Gherkin scenarios can span multiple levels

## Configuration Management

### Environment-Based Configuration

```python
# app/config.py
class Settings(BaseSettings):
    database_url: str
    environment: str = "development"
    api_prefix: str = "/api"
    
    class Config:
        env_file = ".env"

# .env (not committed)
DATABASE_URL=postgresql://user:pass@localhost:5432/expense_db
ENVIRONMENT=development

# .env.test
DATABASE_URL=postgresql://user:pass@localhost:5432/expense_test_db
ENVIRONMENT=test
```

**Testing benefit:** Separate test database configuration, environment isolation

## Deployment Architecture

### Docker Compose Setup

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: expense_db
      POSTGRES_USER: expense_user
      POSTGRES_PASSWORD: expense_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build: .
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://expense_user:expense_pass@db:5432/expense_db
    ports:
      - "8000:8000"
    volumes:
      - ./frontend:/app/frontend

volumes:
  postgres_data:
```

**Testing benefit:** Consistent local development and CI/CD environments

## Why This Architecture is Business-Relevant

### Modern Industry Practices
✅ **FastAPI** - Rapidly growing, used by major tech companies  
✅ **PostgreSQL** - Most popular production database for web apps  
✅ **SQLAlchemy** - Python ORM standard  
✅ **Docker** - Universal containerization  
✅ **Layered architecture** - Foundational pattern across all industries  
✅ **RESTful APIs** - Microservices standard  
✅ **Type hints** - Modern Python best practice  

### QA Automation Relevance
✅ **Multiple test layers** - Demonstrates comprehensive QA strategy  
✅ **Testable architecture** - Shows understanding of design for testability  
✅ **Real database** - Production-realistic validation scenarios  
✅ **API-first** - Reflects microservices testing approaches  
✅ **CI/CD ready** - Docker enables automated testing pipelines  

## Evolution and Future Enhancements

**Current MVP Scope:**
- Basic CRUD operations
- Simple approval workflow
- No authentication
- Single-page frontend

**Production Considerations (documented, not implemented):**
- JWT-based authentication
- Role-based authorization (Employee/Manager/Admin)
- Receipt file attachments (S3/blob storage)
- Actual email notifications (SendGrid/AWS SES)
- Audit logging
- API rate limiting
- Database connection pooling
- Redis caching
- Monitoring/observability (logging, metrics)

**Testing Evolution:**
- Performance testing (Locust/K6)
- Security testing (OWASP, API security)
- Load testing
- Contract testing (Pact)

## Summary

This architecture balances **production realism** with **portfolio project scope**:

- **Realistic enough:** Uses industry-standard technologies and patterns
- **Manageable scope:** Simplified authentication and single deployment
- **Test-focused:** Every architectural decision supports comprehensive testing

The result is a portfolio project that demonstrates both **development capabilities** (AI-assisted) and **QA automation expertise** (comprehensive test coverage) using architecture patterns you'd encounter in real jobs.
