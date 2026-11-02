import os
import secrets

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, current_app,abort,send_from_directory,make_response,jsonify
)
from flask_login import current_user,login_required
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import RequestEntityTooLarge

from extensions import db
from models import Complaint, ComplaintHistory, Attachment
from services.decorators import role_required
from services.complaint_service import (
    generate_tracking_code,
    hash_tracking_code
)
from models.complaint_vote import ComplaintVote


complaints = Blueprint(
    "complaints",
    __name__,
    url_prefix="/complaints"
)


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@complaints.route("/submit", methods=["GET", "POST"])
@role_required("student")
def submit():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        visibility = request.form.get("visibility", "").strip()

        valid_categories = [
            "Infrastructure",
            "Electricity",
            "Water Supply",
            "Cleanliness",
            "Internet",
            "Academic",
            "Other"
        ]

        if (
            not title
            or not description
            or category not in valid_categories
            or visibility not in ["public", "private"]
        ):
            flash("Please provide all required complaint details and choose a visibility.", "danger")
            return render_template("student/submit_complaint.html")

        if len(title) > 200 or len(description) > 10000:
            flash("Title or description exceeds the allowed length.", "danger")
            return render_template("student/submit_complaint.html")

        uploaded_files = request.files.getlist("images")

        total_size = 0

        for file in uploaded_files:
            if file and file.filename:
                file.stream.seek(0, os.SEEK_END)
                total_size += file.stream.tell()
                file.stream.seek(0)

        if total_size > 5 * 1024 * 1024:
            flash("Total image upload size must not exceed 5 MB.", "danger")
            return render_template("student/submit_complaint.html")

        # Validate all uploaded files before saving anything
        for file in uploaded_files:

            if not file or not file.filename:
                continue

            if not allowed_file(file.filename):
                flash("Only PNG, JPG, JPEG and WEBP images are allowed.", "danger")
                return render_template("student/submit_complaint.html")

        tracking_code = generate_tracking_code()

        complaint = Complaint(
            user_id=current_user.id,
            title=title,
            description=description,
            category=category,
            status="submitted",
            is_public=(visibility == "public"),
            access_code_hash=hash_tracking_code(tracking_code)
        )

        db.session.add(complaint)

        try:
            db.session.flush()

            history = ComplaintHistory(
                complaint_id=complaint.id,
                actor_id=current_user.id,
                action="Complaint submitted",
                new_status="submitted"
            )

            db.session.add(history)

            os.makedirs(
                current_app.config["UPLOAD_FOLDER"],
                exist_ok=True
            )

            for file in uploaded_files:

                if not file or not file.filename:
                    continue

                original_name = secure_filename(file.filename)

                extension = original_name.rsplit(".", 1)[1].lower()

                unique_name = secrets.token_hex(16) + "." + extension

                file_path = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    unique_name
                )

                file.save(file_path)

                attachment = Attachment(
                    complaint_id=complaint.id,
                    uploaded_by=current_user.id,
                    file_path=unique_name,
                    original_filename=original_name,
                    is_public_approved=(visibility == "public")
                )

                db.session.add(attachment)

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return render_template(
            "student/complaint_success.html",
            complaint=complaint,
            tracking_code=tracking_code
        )

    similar_complaints = Complaint.query.filter_by(
        category=request.args.get("category", ""),
        is_public=True
    ).order_by(Complaint.created_at.desc()).limit(5).all()

    return render_template(
        "student/submit_complaint.html",
        similar_complaints=similar_complaints
    )

@complaints.route("/track", methods=["GET", "POST"])
def track_complaint():

    complaint = None
    error = None

    if request.method == "POST":
        tracking_code = request.form.get("tracking_code", "").strip()

        if not tracking_code:
            error = "Please enter your tracking code."
        else:
            code_hash = hash_tracking_code(tracking_code)

            complaint = Complaint.query.filter_by(
                access_code_hash=code_hash
            ).first()

            if not complaint:
                error = "Invalid tracking code. Please check and try again."

    return render_template(
        "student/track_complaint.html",
        complaint=complaint,
        error=error
    )

@complaints.route("/public/<int:complaint_id>")
def public_complaint_details(complaint_id):
    complaint = Complaint.query.filter_by(
        id=complaint_id,
        is_public=True
    ).first_or_404()

    attachments = [
        attachment
        for attachment in complaint.attachments
        if attachment.is_public_approved
    ]

    vote_count = ComplaintVote.query.filter_by(
        complaint_id=complaint.id
    ).count()

    user_voted = False
    if current_user.is_authenticated:
        user_voted = ComplaintVote.query.filter_by(
            complaint_id=complaint.id,
            user_id=current_user.id
        ).first() is not None

    return render_template(
        "student/public_complaint_details.html",
        complaint=complaint,
        attachments=attachments,
        vote_count=vote_count,
        user_voted=user_voted
    )

@complaints.route("/public")
def public_complaints():
    complaints_list = Complaint.query.filter_by(
        is_public=True
    ).order_by(Complaint.created_at.desc()).all()

    for complaint in complaints_list:
        complaint.vote_count = ComplaintVote.query.filter_by(
            complaint_id=complaint.id
        ).count()

        complaint.user_voted = False
        if current_user.is_authenticated:
            complaint.user_voted = ComplaintVote.query.filter_by(
                complaint_id=complaint.id,
                user_id=current_user.id
            ).first() is not None

    response = make_response(
        render_template(
            "student/public_complaints.html",
            complaints=complaints_list
        )
    )

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"

    return response

@complaints.route("/public/<int:complaint_id>/vote", methods=["POST"])
@login_required
def toggle_public_complaint_vote(complaint_id):
    complaint = Complaint.query.filter_by(
        id=complaint_id,
        is_public=True
    ).first_or_404()

    if current_user.role != "student":
        abort(403)

    action = request.form.get("action")

    existing_vote = ComplaintVote.query.filter_by(
        complaint_id=complaint.id,
        user_id=current_user.id
    ).first()

    if action == "upvote":
        if existing_vote is None:
            db.session.add(ComplaintVote(
                complaint_id=complaint.id,
                user_id=current_user.id
            ))
    elif action == "remove":
        if existing_vote is not None:
            db.session.delete(existing_vote)
    else:
        abort(400)

    db.session.commit()

    return jsonify({
        "vote_count": ComplaintVote.query.filter_by(
            complaint_id=complaint.id
        ).count(),
        "user_voted": action == "upvote"
    })

@complaints.route("/attachment/<int:attachment_id>")
def view_attachment(attachment_id):

    attachment = db.session.get(Attachment, attachment_id)

    if not attachment:
        abort(404)

    complaint = attachment.complaint

    # Admins can view attachments for complaint management.
    if current_user.is_authenticated and current_user.role == "admin":
        allowed = True

    # The student who submitted the complaint can view their attachments.
    elif (
        current_user.is_authenticated
        and current_user.role == "student"
        and complaint.user_id == current_user.id
    ):
        allowed = True

    # Other students can only view attachments approved for public display.
    elif (
        current_user.is_authenticated
        and current_user.role == "student"
        and complaint.is_public
        and attachment.is_public_approved
    ):
        allowed = True

    else:
        allowed = False

    if not allowed:
        abort(403)

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        attachment.file_path,
        as_attachment=False
    )