"""
Repository for user data access operations.
Handles all database interactions for User entities.
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.database_models import User


class UserRepository:
    """Handles database operations for users."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, email: str, name: str) -> User:
        """Create a new user record."""
        user = User(email=email, name=name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_all(self) -> list[User]:
        """Get all users."""
        return self.db.query(User).all()
