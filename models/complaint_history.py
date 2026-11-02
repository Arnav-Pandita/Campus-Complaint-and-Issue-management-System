from extensions import db


class ComplaintHistory(db.Model):

    __tablename__ = "complaint_history"

    id = db.Column(db.Integer, primary_key=True)

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=False
    )

    actor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    action = db.Column(db.String(100), nullable=False)

    old_status = db.Column(db.String(30), nullable=True)

    new_status = db.Column(db.String(30), nullable=True)

    note = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    complaint = db.relationship(
        "Complaint",
        back_populates="history"
    )

    actor = db.relationship("User")