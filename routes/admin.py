from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, abort,make_response
)
from flask_login import current_user

from extensions import db
from models import Complaint, ComplaintHistory, Attachment
from services.decorators import role_required

from flask import request, redirect, url_for, flash
from datetime import datetime
from models import ReopeningRequest, ComplaintHistory

from services.notification_service import create_notification

admin = Blueprint("admin", __name__, url_prefix="/admin")


VALID_STATUSES = [
    "submitted",
    "under_review",
    "in_progress",
    "resolved"
]

VALID_PRIORITIES = [
    "low",
    "medium",
    "high",
    "critical"
]


# ADMIN DASHBOARD
@admin.route("/dashboard")
@role_required("admin")
def dashboard():

    new_count = Complaint.query.filter_by(status="submitted").count()

    open_count = Complaint.query.filter(
        Complaint.status != "resolved"
    ).count()

    resolved_count = Complaint.query.filter_by(
        status="resolved"
    ).count()

    pending_reopening_count = ReopeningRequest.query.filter_by(
        status="pending"
    ).count()

    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    resolved_complaints = Complaint.query.filter(
        Complaint.status == "resolved",
        Complaint.resolved_at.isnot(None)
    ).all()

    average_resolution_hours = None

    if resolved_complaints:
        total_resolution_hours = sum(
            (
                complaint.resolved_at - complaint.created_at
            ).total_seconds() / 3600
            for complaint in resolved_complaints
        )

        average_resolution_hours = round(
            total_resolution_hours / len(resolved_complaints), 1
        )

    return render_template(
        "admin/dashboard.html",
        complaints=complaints,
        new_count=new_count,
        open_count=open_count,
        resolved_count=resolved_count,
        pending_reopening_count=pending_reopening_count,
        average_resolution_hours=average_resolution_hours
    )

# VIEW AND FILTER COMPLAINTS
@admin.route("/complaints")
@role_required("admin")
def all_complaints():

    status = request.args.get("status", "")
    category = request.args.get("category", "")

    query = Complaint.query

    if status == "open":
        query = query.filter(Complaint.status != "resolved")
    elif status in VALID_STATUSES:
        query = query.filter_by(status=status)

    if category:
        query = query.filter_by(category=category)

    complaints = query.order_by(
        Complaint.created_at.desc()
    ).all()

    response = make_response(render_template(
        "admin/complaints.html",
        complaints=complaints,
        selected_status=status,
        selected_category=category
    ))

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"

    return response


# VIEW INDIVIDUAL COMPLAINT
@admin.route("/complaint/<int:complaint_id>")
@role_required("admin")
def complaint_details(complaint_id):

    complaint = db.session.get(Complaint, complaint_id)

    if not complaint:
        abort(404)

    history = sorted(
        complaint.history,
        key=lambda item: item.created_at
    )

    attachments = complaint.attachments

    return render_template(
        "admin/complaint_details.html",
        complaint=complaint,
        history=history,
        attachments=attachments
    )


# UPDATE PRIORITY AND STATUS
@admin.route("/complaint/<int:complaint_id>/update", methods=["POST"])
@role_required("admin")
def update_complaint(complaint_id):

    complaint = db.session.get(Complaint, complaint_id)

    if not complaint:
        abort(404)

    new_priority = request.form.get("priority", "").strip().lower()
    priority_reason = request.form.get("priority_reason", "").strip()

    new_status = request.form.get("status", "").strip()
    note = request.form.get("note", "").strip()

    

      # Validate priority
    if new_priority:
        if new_priority not in VALID_PRIORITIES:
            flash("Invalid priority selected.", "danger")
            return redirect(url_for(
                "admin.complaint_details",
                complaint_id=complaint.id
            ))

        old_priority = complaint.priority

        # Require a reason only when the priority changes
        if old_priority != new_priority:
            if not priority_reason:
                flash("A reason is required when changing priority.", "danger")
                return redirect(url_for(
                    "admin.complaint_details",
                    complaint_id=complaint.id
                ))

            complaint.priority = new_priority
            complaint.priority_reason = priority_reason

            db.session.add(ComplaintHistory(
                complaint_id=complaint.id,
                actor_id=current_user.id,
                action="Priority assigned or updated",
                note=f"Priority: {old_priority or 'Not assigned'} -> {new_priority}. Reason: {priority_reason}"
            ))

            create_notification(
                user_id=complaint.user_id,
                complaint_id=complaint.id,
                message=f"Your complaint #{complaint.id} priority has been changed to {complaint.priority}."
            )

    # Validate status
    if new_status:

        if new_status not in VALID_STATUSES:
            flash("Invalid status selected.", "danger")
            return redirect(url_for(
                "admin.complaint_details",
                complaint_id=complaint.id
            ))


        old_status = complaint.status

        if old_status != new_status:

            complaint.status = new_status

            if new_status == "resolved":
                from datetime import datetime
                complaint.resolved_at = datetime.utcnow()

            else:
                complaint.resolved_at = None

            db.session.add(ComplaintHistory(
                complaint_id=complaint.id,
                actor_id=current_user.id,
                action="Complaint status updated",
                old_status=old_status,
                new_status=new_status,
                note=note or None
            ))

            create_notification(
            user_id=complaint.user_id,
            complaint_id=complaint.id,
            message=f"Your complaint #{complaint.id} status has been updated to {complaint.status.replace('_', ' ')}."
        )

    db.session.commit()

    flash("Complaint updated successfully.", "success")

    return redirect(url_for("admin.all_complaints"), code=303)


# APPROVE OR REJECT ATTACHMENTS FOR PUBLIC VISIBILITY
@admin.route("/attachment/<int:attachment_id>/visibility", methods=["POST"])
@role_required("admin")
def update_attachment_visibility(attachment_id):

    attachment = db.session.get(Attachment, attachment_id)

    if not attachment:
        abort(404)

    action = request.form.get("action")

    if action not in ["approve", "reject"]:
        abort(400)

    attachment.is_public_approved = (action == "approve")

    db.session.add(ComplaintHistory(
        complaint_id=attachment.complaint_id,
        actor_id=current_user.id,
        action=(
            "Attachment approved for public visibility"
            if action == "approve"
            else "Attachment not approved for public visibility"
        )
    ))

    db.session.commit()

    flash("Attachment visibility updated.", "success")

    return redirect(url_for(
        "admin.complaint_details",
        complaint_id=attachment.complaint_id
    ))

@admin.route("/reopening-requests")
@role_required("admin")
def reopening_requests():

    requests_list = ReopeningRequest.query.filter_by(
        status="pending"
    ).order_by(ReopeningRequest.created_at.asc()).all()

    return render_template(
        "admin/reopening_requests.html",
        requests_list=requests_list
    )


@admin.route("/reopening-request/<int:request_id>/review",
             methods=["POST"])
@role_required("admin")
def review_reopening_request(request_id):

    reopening_request = db.session.get(
        ReopeningRequest, request_id
    )

    if not reopening_request:
        abort(404)

    if reopening_request.status != "pending":
        flash("This request has already been reviewed.", "warning")
        return redirect(url_for("admin.reopening_requests"))

    action = request.form.get("action")
    review_note = request.form.get("review_note", "").strip()

    if action not in ["approve", "reject"]:
        abort(400)

    if action == "reject" and not review_note:
        flash("Please provide a reason for rejecting the request.", "danger")
        return redirect(url_for("admin.reopening_requests"))

    complaint = reopening_request.complaint

    old_status = complaint.status

    if action == "approve":

        reopening_request.status = "approved"

        complaint.status = "under_review"
        complaint.resolved_at = None

        history_note = (
            f"Reopening approved. Student's reason: "
            f"{reopening_request.reason}"
        )

        if review_note:
            history_note += f" Admin note: {review_note}"

        flash("Reopening request approved.", "success")

        action_name = "Reopening request approved"

        create_notification(
        user_id=complaint.user_id,
        complaint_id=complaint.id,
        message=f"Your reopening request for complaint #{complaint.id} has been approved. The complaint is now under review."
    )

    else:

        reopening_request.status = "rejected"

        history_note = (
            f"Reopening rejected. Student's reason: "
            f"{reopening_request.reason}. "
            f"Admin response: {review_note}"
        )

        flash("Reopening request rejected.", "success")

        action_name = "Reopening request rejected"

        create_notification(
        user_id=complaint.user_id,
        complaint_id=complaint.id,
        message=f"Your reopening request for complaint #{complaint.id} has been rejected. Admin response: {review_note}"
    )

    reopening_request.reviewed_by = current_user.id
    reopening_request.reviewed_at = datetime.utcnow()
    reopening_request.review_note = review_note

    history = ComplaintHistory(
        complaint_id=complaint.id,
        actor_id=current_user.id,
        action=action_name,
        old_status=old_status,
        new_status=complaint.status,
        note=history_note
    )

    db.session.add(history)
    db.session.commit()

    return redirect(url_for("admin.reopening_requests"),code=303)