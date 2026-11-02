
from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    college_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="student"
    )

    account_status = db.Column(
        db.String(20),
        nullable=False,
        default="active",
        server_default="active"
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    complaints = db.relationship(
        "Complaint",
        foreign_keys="Complaint.user_id",
        back_populates="student"
    )
