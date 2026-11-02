from extensions import db


class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=True
    )

    message = db.Column(db.Text, nullable=False)

    is_read = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User")

    complaint = db.relationship("Complaint")