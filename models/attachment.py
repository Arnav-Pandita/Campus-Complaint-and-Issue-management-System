from extensions import db


class Attachment(db.Model):

    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=False
    )

    uploaded_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    file_path = db.Column(db.String(255), nullable=False)

    original_filename = db.Column(db.String(255))

    is_public_approved = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    complaint = db.relationship(
        "Complaint",
        back_populates="attachments"
    )

    uploader = db.relationship("User")