"""
Repository for notification data access operations.
Handles all database interactions for Notification entities.
"""
from sqlalchemy.orm import Session
from app.models.database_models import Notification


class NotificationRepository:
    """Handles database operations for notifications."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, expense_id: int, event_type: str, message: str) -> Notification:
        """Create a notification event log."""
        notification = Notification(
            expense_id=expense_id,
            event_type=event_type,
            message=message
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def get_by_expense_id(self, expense_id: int) -> list[Notification]:
        """Get all notifications for a specific expense."""
        return self.db.query(Notification).filter(
            Notification.expense_id == expense_id
        ).all()
