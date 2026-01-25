"""
Script to clear all test data from the database.
"""
from app.database import SessionLocal
from app.models.database_models import Expense, Notification

def clear_test_data():
    db = SessionLocal()
    
    # Delete all notifications
    notification_count = db.query(Notification).delete()
    print(f"Deleted {notification_count} notifications")
    
    # Delete all expenses
    expense_count = db.query(Expense).delete()
    print(f"Deleted {expense_count} expenses")
    
    db.commit()
    db.close()
    print("\nTest data cleared!")

if __name__ == "__main__":
    clear_test_data()