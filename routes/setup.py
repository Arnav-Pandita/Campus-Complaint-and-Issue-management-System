from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import or_
import secrets

from extensions import db
from models import User

setup = Blueprint("setup", __name__, url_prefix="/setup")


@setup.route("/superadmin", methods=["GET", "POST"])
def create_superadmin():

    # Check if a superadmin already exists
    existing_superadmin = User.query.filter_by(
        role="superadmin"
    ).first()

    if existing_superadmin:
        return "Superadmin setup is already completed.", 403

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        college_id = request.form.get("college_id", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        setup_key = request.form.get("setup_key", "")

        if not all([name, email, college_id, password, confirm_password, setup_key]):
            flash("Please fill in all fields.", "danger")
            return render_template("auth/superadmin_setup.html")

        # Verify setup key
        stored_key = current_app.config.get("SUPERADMIN_SETUP_KEY")

        if not stored_key or not secrets.compare_digest(setup_key, stored_key):
            flash("Invalid setup key.", "danger")
            return render_template("auth/superadmin_setup.html")

        # Validate email
        try:
            valid_email = validate_email(
                email,
                check_deliverability=False
            )
            email = valid_email.normalized

        except EmailNotValidError:
            flash("Please enter a valid email address.", "danger")
            return render_template("auth/superadmin_setup.html")

        # Validate password
        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return render_template("auth/superadmin_setup.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/superadmin_setup.html")

        # Check duplicate accounts
        existing_user = User.query.filter(
            or_(
                User.email == email,
                User.college_id == college_id
            )
        ).first()

        if existing_user:
            flash("Email or college ID is already registered.", "danger")
            return render_template("auth/superadmin_setup.html")

        # Create superadmin
        superadmin = User(
            name=name,
            email=email,
            college_id=college_id,
            password_hash=generate_password_hash(password),
            role="superadmin",
            account_status="active",
            is_active=True
        )

        db.session.add(superadmin)
        db.session.commit()

        flash("Superadmin account created successfully. Please log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/superadmin_setup.html")