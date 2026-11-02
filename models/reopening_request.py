from extensions import db


class ReopeningRequest(db.Model):

    __tablename__ = "reopening_requests"

    id = db.Column(db.Integer, primary_key=True)

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=False
    )

    requested_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    reason = db.Column(db.Text, nullable=False)

    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )

    reviewed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    review_note = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    reviewed_at = db.Column(db.DateTime, nullable=True)

    complaint = db.relationship(
        "Complaint",
        back_populates="reopening_requests"
    )

    requester = db.relationship(
        "User",
        foreign_keys=[requested_by]
    )

    reviewer = db.relationship(
        "User",
        foreign_keys=[reviewed_by]
    )