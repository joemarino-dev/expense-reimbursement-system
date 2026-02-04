# Expense Reimbursement System

Full-stack expense reimbursement application demonstrating professional QA automation engineering practices with comprehensive multi-layer test coverage, CI/CD pipeline, and AI-assisted development workflow.

[![Tests](https://github.com/joemarino-dev/expense-reimbursement-system/actions/workflows/tests.yml/badge.svg)](https://github.com/joemarino-dev/expense-reimbursement-system/actions/workflows/tests.yml)

## Portfolio Highlights

This project demonstrates:

- **Multi-Layer Test Strategy** - Comprehensive test coverage across unit, repository, API, integration, property-based, and E2E tests
- **CI/CD Pipeline** - GitHub Actions running full test suite on every commit
- **Agile Development** - GitHub Projects board tracking user stories with Definition of Done
- **Production Architecture** - FastAPI with layered architecture (Controller → Service → Repository → Database)
- **GenAI-Assisted Development** - Leveraged AI tools for rapid feature development and test generation
- **Professional Practices** - Docker containerization, database migrations (Alembic), environment-based configuration

## Tech Stack

**Backend:** FastAPI, Python 3.12, SQLAlchemy, Pydantic
**Database:** PostgreSQL (production), SQLite (testing)
**Testing:** pytest, Playwright, Hypothesis (property-based testing), pytest-cov
**Infrastructure:** Docker Compose, Alembic migrations, GitHub Actions CI/CD
**Frontend:** HTML5, JavaScript (Vanilla)

## Project Management

- **GitHub Projects Board:** [View Stories & Progress](https://github.com/users/joemarino-dev/projects/2/views/3)
- **Architecture Documentation:** [Technical Design Decisions](docs/ARCHITECTURE.md)

## Quick Start

### Prerequisites
- Python 3.12+
- Docker Desktop

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/joemarino-dev/expense-reimbursement-system.git
   cd expense-reimbursement-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start PostgreSQL**
   ```bash
   docker-compose up -d
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Create test users**
   ```bash
   python create_test_users.py
   ```

7. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Access the application**
   - **API Documentation:** http://127.0.0.1:8000/docs
   - **Submit Expense Form:** http://127.0.0.1:8000/
   - **Health Check:** http://127.0.0.1:8000/health

## Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage Report
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View detailed coverage report
```

### Run Specific Test Types
```bash
# Unit tests only (fast, mocked dependencies)
pytest tests/unit/ -v

# Repository tests (database layer)
pytest tests/repository/ -v

# API tests (HTTP endpoint validation)
pytest tests/api/ -v

# Integration tests (multi-layer)
pytest tests/integration/ -v

# E2E tests (full stack with browser)
pytest tests/e2e/ -v
```

### Test Coverage by Layer

| Test Type | Purpose | Speed |
|-----------|---------|-------|
| Unit | Service layer business logic with mocked dependencies | ⚡ Fast |
| Repository | Database operations and SQL validation | 🔥 Fast |
| API | HTTP endpoint contracts and response validation | 🔥 Fast |
| Integration | Multi-layer integration (service + repository + DB) | 🐢 Medium |
| Property-based | Business rule invariants using Hypothesis | 🐢 Medium |
| E2E | Full user workflow through browser (Playwright) | 🐌 Slow |

## Features

### Core Functionality

**Expense Submission:**
- Submit expense reimbursement requests with required fields (submitter email, approver email, amount, date, category, description)
- Auto-assign status: "Submitted"
- Validate submitter and approver exist in system
- Log notification events to database
- Client-side JavaScript form validation
- Server-side Pydantic schema validation

**API Endpoints:**
- `POST /api/expenses` - Create new expense
- `GET /health` - Health check endpoint

**Testing:**
- Comprehensive multi-layer test strategy (unit, repository, API, integration, property-based, E2E)
- GitHub Actions CI/CD pipeline running full test suite on every push
- High test coverage across all application layers

**Planned Enhancements:**
- View and filter submitted expenses
- Approval workflow with status updates
- Rejection workflow with required reasoning
- Expense dashboard with aggregate metrics and visualizations

## Architecture Highlights

**Layered Architecture:**
```
┌─────────────────────┐
│   Controller Layer  │  FastAPI routes, request/response handling
├─────────────────────┤
│   Service Layer     │  Business logic, orchestration, validation
├─────────────────────┤
│  Repository Layer   │  Database operations, SQL/ORM abstraction
├─────────────────────┤
│   Database Layer    │  PostgreSQL (prod), SQLite (test)
└─────────────────────┘
```

**Key Design Patterns:**
- **Repository Pattern** - Abstracts database operations for testability
- **Dependency Injection** - Services receive repository instances (enables mocking)
- **Schema Validation** - Pydantic models enforce data contracts
- **Test Isolation** - Separate test databases prevent side effects

## Development Approach

This project follows a **story-by-story development methodology** where each user story achieves "Definition of Done" before moving to the next:

1. **Build** - Implement API endpoint, service layer, repository, UI
2. **Test** - Write comprehensive test coverage across all layers
3. **Commit** - Mark story complete, merge to main
4. **Iterate** - Move to next story

This approach demonstrates professional Agile practices and ensures each feature is production-ready with comprehensive test coverage before advancing.

## AI-Assisted Development

This project leverages Generative AI tools to accelerate development:

- **Code Generation** - AI-assisted implementation of boilerplate and repetitive patterns
- **Test Strategy** - AI-guided test planning and comprehensive test case generation
- **Architecture Decisions** - Collaborative exploration of design patterns and best practices
- **Documentation** - AI-enhanced documentation creation and technical writing

## CI/CD Pipeline

GitHub Actions automatically runs on every push:

1. Set up Python 3.12 environment
2. Install dependencies
3. Start PostgreSQL test database (Docker)
4. Run database migrations
5. Execute comprehensive test suite (unit, repository, API, integration, property-based, E2E)
6. Generate coverage report
7. Report results

View pipeline: [GitHub Actions](https://github.com/joemarino-dev/expense-reimbursement-system/actions)

## Database Schema

**Users Table:**
- id (Primary Key)
- email (Unique, Not Null)
- name (Not Null)

**Expenses Table:**
- id (Primary Key)
- user_email (Foreign Key → Users.email)
- approver_email (Foreign Key → Users.email)
- amount (Decimal)
- expense_date (Date)
- category (Enum: Travel, Meals, Supplies, Equipment, Other)
- description (Text)
- status (Enum: Submitted, Approved, Rejected)
- submitted_at (Timestamp)
- updated_at (Timestamp)

**Notifications Table:**
- id (Primary Key)
- expense_id (Foreign Key → Expenses.id)
- event_type (String)
- message (Text)
- created_at (Timestamp)

## License

MIT

## Author

**Joe Marino**
- Email: joe@mistermarino.com
- LinkedIn: [linkedin.com/in/joemarino](https://linkedin.com/in/joemarino)
- GitHub: [github.com/joemarino-dev](https://github.com/joemarino-dev)
