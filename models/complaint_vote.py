from extensions import db


class ComplaintVote(db.Model):
    __tablename__ = "complaint_votes"

    id = db.Column(db.Integer, primary_key=True)

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "complaint_id",
            "user_id",
            name="unique_complaint_vote"
        ),
    )