"""
Shared test fixtures and configuration.

Organized by test type:
- SQLite Database (Unit & Repository tests - FAST)
- PostgreSQL Database (Integration, API, E2E tests - ACCURATE)
- Mocked Dependencies (Unit tests)
- Test Clients & Sample Data
"""

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

def _create_postgres_test_database(db_name="test_expense_db"):
    """
    Helper: Creates PostgreSQL test database.
    Returns engine connected to the new database.
    """
    admin_engine = create_engine("postgresql://expense_user:expense_pass@localhost:5432/postgres")
    
    with admin_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        conn.execute(text(f"CREATE DATABASE {db_name}"))
    
    admin_engine.dispose()
    return create_engine(f"postgresql://expense_user:expense_pass@localhost:5432/{db_name}")

def _drop_postgres_test_database(db_name="test_expense_db"):
    """Helper: Drops PostgreSQL test database."""
    admin_engine = create_engine("postgresql://expense_user:expense_pass@localhost:5432/postgres")
    
    with admin_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
    
    admin_engine.dispose()

# ============================================================================
# SQLITE DATABASE (Unit & Repository Tests - Fast, isolated)
# ============================================================================

@pytest.fixture(scope="function")
def test_db():
    """
    Creates a fresh in-memory SQLite database for each test.
    
    Used by: Unit tests, Repository tests
    Why SQLite: Fast (1-10ms), no external dependencies, perfect for isolated testing
    """
    from app.models.database_models import User, Expense, Notification
    from app.database import Base
    
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
# POSTGRESQL DATABASE (Integration, API, E2E Tests - Production-accurate)
# ============================================================================

@pytest.fixture(scope="function")
def postgres_test_db():
    """
    Creates a fresh PostgreSQL test database for each test.
    
    Used by: Integration tests, API tests, E2E tests
    Why PostgreSQL: Matches production environment, catches DB-specific issues
    
    Creates test_expense_db in your Docker PostgreSQL, uses it for the test,
    then drops it. Your main expense_db database remains untouched.
    """
    from app.database import Base
    
    # Create and connect to the test database
    test_engine = _create_postgres_test_database()
    Base.metadata.create_all(bind=test_engine)
    
    TestingSessionLocal = sessionmaker(bind=test_engine)
    db = TestingSessionLocal()
    
    yield db
    
    # Cleanup
    db.close()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
    _drop_postgres_test_database()

# ============================================================================
# REPOSITORY TESTS - SQLite database fixtures
# ============================================================================

@pytest.fixture
def user_repository(test_db):
    """Provides UserRepository instance with SQLite test database."""
    from app.repositories.user_repository import UserRepository
    return UserRepository(test_db)


@pytest.fixture
def expense_repository(test_db):
    """Provides ExpenseRepository instance with SQLite test database."""
    from app.repositories.expense_repository import ExpenseRepository
    return ExpenseRepository(test_db)


@pytest.fixture
def notification_repository(test_db):
    """Provides NotificationRepository instance with SQLite test database."""
    from app.repositories.notification_repository import NotificationRepository
    return NotificationRepository(test_db)


@pytest.fixture
def sample_user(test_db):
    """Creates a sample user in the SQLite test database."""
    from app.models.database_models import User
    
    user = User(email="john.doe@company.com", name="John Doe")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def sample_approver(test_db):
    """Creates a sample approver user in the SQLite test database."""
    from app.models.database_models import User
    
    approver = User(email="jane.manager@company.com", name="Jane Manager")
    test_db.add(approver)
    test_db.commit()
    test_db.refresh(approver)
    return approver


# ============================================================================
# INTEGRATION TESTS - PostgreSQL database fixtures
# ============================================================================

@pytest.fixture
def postgres_user_repository(postgres_test_db):
    """Provides UserRepository instance with PostgreSQL test database."""
    from app.repositories.user_repository import UserRepository
    return UserRepository(postgres_test_db)


@pytest.fixture
def postgres_expense_repository(postgres_test_db):
    """Provides ExpenseRepository instance with PostgreSQL test database."""
    from app.repositories.expense_repository import ExpenseRepository
    return ExpenseRepository(postgres_test_db)


@pytest.fixture
def postgres_notification_repository(postgres_test_db):
    """Provides NotificationRepository instance with PostgreSQL test database."""
    from app.repositories.notification_repository import NotificationRepository
    return NotificationRepository(postgres_test_db)


@pytest.fixture
def postgres_sample_user(postgres_test_db):
    """Creates a sample user in the PostgreSQL test database."""
    from app.models.database_models import User
    
    user = User(email="john.doe@company.com", name="John Doe")
    postgres_test_db.add(user)
    postgres_test_db.commit()
    postgres_test_db.refresh(user)
    return user


@pytest.fixture
def postgres_sample_approver(postgres_test_db):
    """Creates a sample approver user in the PostgreSQL test database."""
    from app.models.database_models import User
    
    approver = User(email="jane.manager@company.com", name="Jane Manager")
    postgres_test_db.add(approver)
    postgres_test_db.commit()
    postgres_test_db.refresh(approver)
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
# API TESTS - HTTP endpoints with PostgreSQL test database
# ============================================================================

@pytest.fixture(scope="function")
def test_client(postgres_test_db):
    """
    Provides FastAPI TestClient with PostgreSQL test database.
    
    Used by: API tests
    Why PostgreSQL: Tests full HTTP stack with production-accurate database
    """
    from fastapi.testclient import TestClient
    from app.main import app
    from app.dependencies import get_db
    from app.models.database_models import User
    
    # Create sample users in the database for API tests
    user = User(email="john.doe@company.com", name="John Doe")
    approver = User(email="jane.manager@company.com", name="Jane Manager")
    postgres_test_db.add(user)
    postgres_test_db.add(approver)
    postgres_test_db.commit()
    
    def override_get_db():
        try:
            yield postgres_test_db
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
# E2E/UI TESTS - Server startup with PostgreSQL for browser testing
# ============================================================================

@pytest.fixture(scope="module")
def test_server():
    """
    Starts FastAPI server with PostgreSQL test database for E2E tests.
    """
    import time
    import os
    from multiprocessing import Process
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from app.database import Base
    from app.models.database_models import User
    
    # Create and connect to test database and populate with users
    test_engine = _create_postgres_test_database()
    Base.metadata.create_all(bind=test_engine)
    
    # Add test users
    SessionLocal = sessionmaker(bind=test_engine)
    db = SessionLocal()
    user = User(email="john.doe@company.com", name="John Doe")
    approver = User(email="jane.manager@company.com", name="Jane Manager")
    db.add(user)
    db.add(approver)
    db.commit()
    db.close()
    test_engine.dispose()  # CLOSE the engine so database isn't "in use"
    
    # Start server using wrapper
    from tests.test_server_wrapper import run_test_server
    process = Process(target=run_test_server, daemon=False)
    process.start()
    
    # Wait for server to start
    time.sleep(3)
    
    yield "http://localhost:8000"
    
    # Cleanup
    process.terminate()
    process.join()
    
    # Drop test database
    _drop_postgres_test_database()