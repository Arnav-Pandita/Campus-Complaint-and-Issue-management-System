from flask import Blueprint, render_template, redirect, url_for, flash
from models import User
from extensions import db
from services.decorators import role_required

superadmin = Blueprint(
    "superadmin",
    __name__,
    url_prefix="/superadmin"
)


@superadmin.route("/dashboard")
@role_required("superadmin")
def dashboard():

    pending_admins = User.query.filter_by(
        role="admin",
        account_status="pending"
    ).order_by(User.created_at.desc()).all()

    approved_admins = User.query.filter_by(
        role="admin",
        account_status="approved",
        is_active=True
    ).all()

    inactive_admins = User.query.filter_by(
        role="admin",
        account_status="approved",
        is_active=False
    ).all()

    return render_template(
        "superadmin/dashboard.html",
        pending_admins=pending_admins,
        approved_admins=approved_admins,
        inactive_admins=inactive_admins
    )


@superadmin.route("/approve/<int:user_id>", methods=["POST"])
@role_required("superadmin")
def approve_admin(user_id):

    admin_user = db.session.get(User, user_id)

    if not admin_user or admin_user.role != "admin":
        flash("Admin account not found.", "danger")
        return redirect(url_for("superadmin.dashboard"))

    if admin_user.account_status != "pending":
        flash("This request is no longer pending.", "warning")
        return redirect(url_for("superadmin.dashboard"))

    admin_user.account_status = "approved"
    admin_user.is_active = True

    db.session.commit()

    flash("Admin account approved successfully.", "success")

    return redirect(url_for("superadmin.dashboard"))


@superadmin.route("/reject/<int:user_id>", methods=["POST"])
@role_required("superadmin")
def reject_admin(user_id):

    admin_user = db.session.get(User, user_id)

    if not admin_user or admin_user.role != "admin":
        flash("Admin account not found.", "danger")
        return redirect(url_for("superadmin.dashboard"))

    if admin_user.account_status != "pending":
        flash("This request is no longer pending.", "warning")
        return redirect(url_for("superadmin.dashboard"))

    admin_user.account_status = "rejected"
    admin_user.is_active = False

    db.session.commit()

    flash("Admin registration request rejected.", "success")

    return redirect(url_for("superadmin.dashboard"))

@superadmin.route("/deactivate/<int:user_id>", methods=["POST"])
@role_required("superadmin")
def deactivate_admin(user_id):

    admin_user = db.session.get(User, user_id)

    if not admin_user or admin_user.role != "admin":
        flash("Admin account not found.", "danger")
        return redirect(url_for("superadmin.dashboard"))

    if admin_user.account_status != "approved":
        flash("Only approved admins can be deactivated.", "warning")
        return redirect(url_for("superadmin.dashboard"))

    admin_user.is_active = False
    db.session.commit()

    flash("Admin account deactivated.", "success")
    return redirect(url_for("superadmin.dashboard"))

@superadmin.route("/reactivate/<int:user_id>", methods=["POST"])
@role_required("superadmin")
def reactivate_admin(user_id):

    admin_user = db.session.get(User, user_id)

    if not admin_user or admin_user.role != "admin":
        flash("Admin account not found.", "danger")
        return redirect(url_for("superadmin.dashboard"))

    if admin_user.account_status != "approved":
        flash("Only previously approved admins can be reactivated.", "warning")
        return redirect(url_for("superadmin.dashboard"))

    admin_user.is_active = True
    db.session.commit()

    flash("Admin account reactivated.", "success")
    return redirect(url_for("superadmin.dashboard"))