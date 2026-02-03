"""Wrapper script to start test server with correct DATABASE_URL."""
import os
import uvicorn

def run_test_server():
    """Start server with test database URL."""
    os.environ['DATABASE_URL'] = "postgresql://expense_user:expense_pass@localhost:5432/test_expense_db"
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, log_level="error")

if __name__ == "__main__":
    run_test_server()