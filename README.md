# Expense Reimbursement System

Full-stack expense reimbursement application with comprehensive test automation suite. Demonstrates AI-assisted development, pytest, Playwright, API testing, and CI/CD.

## Quick Start

### Prerequisites
- Python 3.12+
- Docker Desktop

### Setup

1. Clone the repository
2. Create virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Start PostgreSQL:
```bash
   docker-compose up -d
```

5. Run database migrations:
```bash
   alembic upgrade head
```

6. Create test users:
```bash
   python create_test_users.py
```

7. Start the application:
```bash
   uvicorn app.main:app --reload
```

8. Access the application:
   - **API Documentation**: http://127.0.0.1:8000/docs
   - **Submit Expense Form**: http://127.0.0.1:8000/static/submit_expense.html
   - **Health Check**: http://127.0.0.1:8000/health

## Documentation

- **[Architecture Overview](docs/ARCHITECTURE.md)** - Technical architecture and design decisions

## Project Status

### Completed Features
- ✅ User management (basic)
- ✅ Expense submission with validation
- ✅ Notification event logging
- ✅ API documentation (auto-generated)

### In Progress
- 🚧 Approval workflow
- 🚧 Expense dashboard
- 🚧 Comprehensive test suite

## License

MIT