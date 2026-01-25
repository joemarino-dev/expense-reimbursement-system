"""
Script to create test users for development/testing.
"""
from app.database import SessionLocal
from app.models.database_models import User

def create_test_users():
    db = SessionLocal()
    
    # Test users
    users = [
        User(email="john.doe@company.com", name="John Doe"),
        User(email="jane.manager@company.com", name="Jane Manager"),
        User(email="bob.employee@company.com", name="Bob Employee"),
    ]
    
    for user in users:
        # Check if user already exists
        existing = db.query(User).filter(User.email == user.email).first()
        if not existing:
            db.add(user)
            print(f"Created user: {user.email}")
        else:
            print(f"User already exists: {user.email}")
    
    db.commit()
    db.close()
    print("\nTest users ready!")

if __name__ == "__main__":
    create_test_users()