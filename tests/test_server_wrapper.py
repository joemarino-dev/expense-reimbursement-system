"""Wrapper script to start test server with correct DATABASE_URL."""
import os

def run_test_server():
    """Start server with test database URL."""
    # Set DATABASE_URL FIRST
    os.environ['DATABASE_URL'] = "postgresql://expense_user:expense_pass@localhost:5432/test_expense_db"
    
    # Clear any cached imports
    import sys
    for module in list(sys.modules.keys()):
        if module.startswith('app.'):
            del sys.modules[module]
    
    # NOW import and run
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, log_level="error")

if __name__ == "__main__":
    run_test_server()