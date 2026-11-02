from extensions import db
from models import Notification


def create_notification(user_id, message, complaint_id=None):
    notification = Notification(
        user_id=user_id,
        complaint_id=complaint_id,
        message=message
    )

    db.session.add(notification)