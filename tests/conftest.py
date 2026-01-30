"""
Shared test fixtures and configuration.

Organized by test type:
- Database & Infrastructure (all tests)
- Repository Tests (real DB)
- Unit Tests (mocks)
- API/Integration Tests (test client + data)
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


# ============================================================================
# SHARED INFRASTRUCTURE (Used by all test types)
# ============================================================================

@pytest.fixture(scope="function")
def test_db():
    """Creates a fresh in-memory SQLite database for each test."""
    from app.models.database_models import User, Expense, Notification  # Import models
    from app.database import Base
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


# ============================================================================
# REPOSITORY TESTS - Real database, testing repository layer
# ============================================================================

@pytest.fixture
def user_repository(test_db):
    """Provides UserRepository instance with test database."""
    from app.repositories.user_repository import UserRepository
    return UserRepository(test_db)


@pytest.fixture
def expense_repository(test_db):
    """Provides ExpenseRepository instance with test database."""
    from app.repositories.expense_repository import ExpenseRepository
    return ExpenseRepository(test_db)


@pytest.fixture
def notification_repository(test_db):
    """Provides NotificationRepository instance with test database."""
    from app.repositories.notification_repository import NotificationRepository
    return NotificationRepository(test_db)


@pytest.fixture
def sample_user(test_db):
    """Creates a sample user in the test database."""
    from app.models.database_models import User
    
    user = User(email="john.doe@company.com", name="John Doe")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def sample_approver(test_db):
    """Creates a sample approver user in the test database."""
    from app.models.database_models import User
    
    approver = User(email="jane.manager@company.com", name="Jane Manager")
    test_db.add(approver)
    test_db.commit()
    test_db.refresh(approver)
    return approver


# ============================================================================
# UNIT TESTS - Mocked dependencies, no database
# ============================================================================

@pytest.fixture
def mock_user_repository(mocker):
    """Provides mocked UserRepository for unit tests."""
    from app.repositories.user_repository import UserRepository
    return mocker.Mock(spec=UserRepository)


@pytest.fixture
def mock_expense_repository(mocker):
    """Provides mocked ExpenseRepository for unit tests."""
    from app.repositories.expense_repository import ExpenseRepository
    return mocker.Mock(spec=ExpenseRepository)


@pytest.fixture
def mock_notification_repository(mocker):
    """Provides mocked NotificationRepository for unit tests."""
    from app.repositories.notification_repository import NotificationRepository
    return mocker.Mock(spec=NotificationRepository)


# ============================================================================
# API/INTEGRATION TESTS - HTTP endpoints with test database
# ============================================================================

@pytest.fixture(scope="function")
def test_client(test_db):
    """Provides FastAPI TestClient with test database."""
    from fastapi.testclient import TestClient
    from app.main import app
    from app.dependencies import get_db
    
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_expense_data():
    """Provides sample expense request data for API tests."""
    return {
        "submitter_email": "john.doe@company.com",
        "approver_email": "jane.manager@company.com",
        "amount": 150.00,
        "expense_date": "2026-01-15",
        "category": "Travel",
        "description": "Client meeting transportation"
    }
    
# ============================================================================
# E2E/UI TESTS - Server startup for browser testing
# ============================================================================

@pytest.fixture(scope="module")
def test_server():
    """
    Starts FastAPI server with test database for E2E tests.
    Uses .env.test configuration file.
    """
    import os
    import time
    from multiprocessing import Process
    from dotenv import load_dotenv
    
    # Load test environment variables
    load_dotenv('.env.test', override=True)
    
    # Create test database and populate with users
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.database import Base
    from app.models.database_models import User
    
    test_db_path = "test_e2e.db"
    engine = create_engine(f"sqlite:///./{test_db_path}")
    Base.metadata.create_all(bind=engine)
    
    # Add test users
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    user = User(email="john.doe@company.com", name="John Doe")
    approver = User(email="jane.manager@company.com", name="Jane Manager")
    db.add(user)
    db.add(approver)
    db.commit()
    db.close()
    
    # Start server
    import uvicorn
    config = uvicorn.Config(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="error"
    )
    server = uvicorn.Server(config)
    process = Process(target=server.run, daemon=True)
    process.start()
    
    # Wait for server to start
    time.sleep(2)
    
    yield "http://localhost:8000"
    
    # Cleanup
    process.terminate()
    process.join()
    
    # Remove test database file
    if os.path.exists(test_db_path):
        os.remove(test_db_path)