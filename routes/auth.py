from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

from extensions import db
from models import User
from email_validator import validate_email, EmailNotValidError

auth = Blueprint("auth", __name__, url_prefix="/auth")


# STUDENT REGISTRATION

@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        college_id = request.form.get("college_id", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Check empty fields
        if not all([name, email, college_id, password, confirm_password]):
            flash("Please fill in all fields.", "danger")
            return render_template("auth/register.html")

        # Validate email format
        try:
            valid_email = validate_email(
                email,
                check_deliverability=False
            )
            email = valid_email.normalized

        except EmailNotValidError:
            flash("Please enter a valid email address.", "danger")
            return render_template("auth/register.html")

        # Validate password
        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        # Check duplicate email and college ID
        existing_user = User.query.filter(
            or_(
                User.email == email,
                User.college_id == college_id
            )
        ).first()

        if existing_user:
            flash("Email or college ID is already registered.", "danger")
            return render_template("auth/register.html")

        # Create student account
        new_user = User(
            name=name,
            email=email,
            college_id=college_id,
            password_hash=generate_password_hash(password),
            role="student",
            account_status="active",
            is_active=True
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth.route("/admin-register", methods=["GET", "POST"])
def admin_register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    def render_admin_register():
        return render_template(
            "auth/admin_register.html",
            name=request.form.get("name", ""),
            email=request.form.get("email", ""),
            college_id=request.form.get("college_id", "")
        )

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        college_id = request.form.get("college_id", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not all([name, email, college_id, password, confirm_password]):
            flash("Please fill in all fields.", "danger")
            return render_admin_register()

        # Email validation
        try:
            valid_email = validate_email(
                email,
                check_deliverability=False
            )
            email = valid_email.normalized

        except EmailNotValidError:
            flash("Please enter a valid email address.", "danger")
            return render_admin_register()

        # Password validation
        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return render_admin_register()

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_admin_register()

        # Check duplicate accounts
        existing_user = User.query.filter(
            or_(
                User.email == email,
                User.college_id == college_id
            )
        ).first()

        if existing_user:
            flash("Email or college ID is already registered.", "danger")
            return render_admin_register()

        # Create pending admin account
        new_admin = User(
            name=name,
            email=email,
            college_id=college_id,
            password_hash=generate_password_hash(password),
            role="admin",
            account_status="pending",
            is_active=False
        )

        db.session.add(new_admin)
        db.session.commit()

        flash(
            "Registration request submitted. Awaiting superadmin approval.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("auth/admin_register.html")

# LOGIN (STUDENT AND ADMIN)
@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "superadmin":
            return redirect(url_for("superadmin.dashboard"))

        elif current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("student.dashboard"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter(
            or_(
                User.email == email,
                User.college_id == email
            )
        ).first()

        if not user or not check_password_hash(
            user.password_hash, password
        ):
            flash("Invalid email or password.", "danger")

        elif user.account_status == "pending":
            flash("Your admin registration is awaiting approval.", "warning")

        elif user.account_status == "rejected":
            flash("Your admin registration was rejected.", "danger")

        elif not user.is_active:
            flash("Your account is inactive. Contact the administrator.", "danger")

        else:

            login_user(user)

            if user.role == "superadmin":
                return redirect(url_for("superadmin.dashboard"))

            elif user.role == "admin":
                return redirect(url_for("admin.dashboard"))

            return redirect(url_for("student.dashboard"))

    return render_template("auth/login.html")


# LOGOUT
@auth.route("/logout", methods=["POST"])
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))