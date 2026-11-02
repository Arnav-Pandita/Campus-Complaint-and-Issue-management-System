from extensions import db


class Complaint(db.Model):

    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(100), nullable=False)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="submitted"
    )

    priority = db.Column(db.String(20), nullable=True)

    priority_reason = db.Column(db.Text, nullable=True)

    assigned_admin_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    is_public = db.Column(db.Boolean, default=True, nullable=False)

    access_code_hash = db.Column(db.String(255), unique=True, nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    resolved_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="complaints"
    )

    assigned_admin = db.relationship(
        "User",
        foreign_keys=[assigned_admin_id]
    )

    history = db.relationship(
        "ComplaintHistory",
        back_populates="complaint",
        cascade="all, delete-orphan"
    )

    attachments = db.relationship(
        "Attachment",
        back_populates="complaint",
        cascade="all, delete-orphan"
    )

    reopening_requests = db.relationship(
        "ReopeningRequest",
        back_populates="complaint",
        cascade="all, delete-orphan"
    )