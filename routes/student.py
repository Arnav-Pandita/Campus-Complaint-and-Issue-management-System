from flask import Blueprint, render_template, abort,current_app,make_response
from flask_login import current_user

from models import Complaint
from services.decorators import role_required
from models.complaint_vote import ComplaintVote

from flask import request, redirect, url_for, flash
from datetime import datetime
from extensions import db
from models import ReopeningRequest, ComplaintHistory,Notification
import os

student = Blueprint("student", __name__, url_prefix="/student")


# STUDENT DASHBOARD
@student.route("/dashboard")
@role_required("student")
def dashboard():

    complaints = Complaint.query.filter_by(
        user_id=current_user.id
    ).order_by(Complaint.created_at.desc()).all()

    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).limit(20).all()

    notification_groups = {}

    for notification in notifications:
        group_id = notification.complaint_id or f"notification-{notification.id}"

        if group_id not in notification_groups:
            notification_groups[group_id] = {
                "complaint": notification.complaint,
                "notifications": [],
                "unread_count": 0
            }

        notification_groups[group_id]["notifications"].append(notification)

        if not notification.is_read:
            notification_groups[group_id]["unread_count"] += 1

    return render_template(
        "student/dashboard.html",
        complaints=complaints,
        notifications=notifications,
        notification_groups=notification_groups,
    )


# INDIVIDUAL COMPLAINT DETAILS
@student.route("/complaint/<int:complaint_id>")
@role_required("student")
def complaint_details(complaint_id):

    complaint = Complaint.query.filter_by(
        id=complaint_id,
        user_id=current_user.id
    ).first()

    if not complaint:
        abort(404)

    history = sorted(
        complaint.history,
        key=lambda item: item.created_at
    )

    return render_template(
        "student/complaint_details.html",
        complaint=complaint,
        history=history
    )

# DELETE COMPLAINT — only before processing starts
@student.route("/complaint/<int:complaint_id>/delete", methods=["POST"])
@role_required("student")
def delete_complaint(complaint_id):
    complaint = Complaint.query.filter_by(
        id=complaint_id,
        user_id=current_user.id
    ).first_or_404()

    if complaint.status != "submitted":
        flash(
            "You can only delete a complaint before processing starts.",
            "warning"
        )
        return redirect(url_for(
            "student.complaint_details",
            complaint_id=complaint.id
        ))

    # Remove uploaded files from storage
    for attachment in complaint.attachments:
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            attachment.file_path
        )

        if os.path.isfile(file_path):
            os.remove(file_path)

    # Remove related records, then the complaint
    ComplaintHistory.query.filter_by(
        complaint_id=complaint.id
    ).delete()

    Attachment.query.filter_by(
        complaint_id=complaint.id
    ).delete()

    ReopeningRequest.query.filter_by(
        complaint_id=complaint.id
    ).delete()

    db.session.delete(complaint)
    db.session.commit()

    flash("Complaint deleted successfully.", "success")
    return redirect(url_for("student.dashboard"))

#--

@student.route("/complaint/<int:complaint_id>/reopen", methods=["POST"])
@role_required("student")
def request_reopening(complaint_id):

    complaint = Complaint.query.filter_by(
        id=complaint_id,
        user_id=current_user.id
    ).first_or_404()

    if complaint.status != "resolved":
        flash("Only resolved complaints can be reopened.", "warning")
        return redirect(url_for(
            "student.complaint_details",
            complaint_id=complaint.id
        ))

    existing_request = ReopeningRequest.query.filter_by(
        complaint_id=complaint.id,
        status="pending"
    ).first()

    if existing_request:
        flash("A reopening request is already pending.", "warning")
        return redirect(url_for(
            "student.complaint_details",
            complaint_id=complaint.id
        ))

    reason = request.form.get("reason", "").strip()

    if not reason:
        flash("Please provide a reason for reopening.", "danger")
        return redirect(url_for(
            "student.complaint_details",
            complaint_id=complaint.id
        ))

    reopening_request = ReopeningRequest(
        complaint_id=complaint.id,
        requested_by=current_user.id,
        reason=reason,
        status="pending"
    )

    db.session.add(reopening_request)
    db.session.commit()

    flash("Your reopening request has been submitted.", "success")

    return redirect(url_for(
        "student.complaint_details",
        complaint_id=complaint.id
    ))

@student.route("/notification/<int:notification_id>/read",
               methods=["POST"])
@role_required("student")
def mark_notification_read(notification_id):

    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=current_user.id
    ).first_or_404()

    notification.is_read = True
    db.session.commit()

    return redirect(url_for("student.dashboard"))


@student.route("/public-complaints")
@role_required("student")
def public_complaints():
    return redirect(url_for("complaints.public_complaints"))