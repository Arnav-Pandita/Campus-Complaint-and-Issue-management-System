
from app import app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash
from getpass import getpass


with app.app_context():

    print("\n========== CREATE ADMIN ACCOUNT ==========\n")

    name = input("Admin Name: ").strip()
    email = input("Admin Email: ").strip().lower()
    college_id = input("Admin ID: ").strip()

    if not all([name, email, college_id]):
        print("All details are required.")
        raise SystemExit

    existing = User.query.filter(
        db.or_(
            User.email == email,
            User.college_id == college_id
        )
    ).first()

    if existing:
        print("An account with this email or ID already exists.")
        raise SystemExit

    print("\nPassword Requirements:")
    print("- Minimum 8 characters")
    print("- Password and confirmation must match")

    while True:

        password = getpass("\nEnter Password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters. Try again.")
            continue

        confirm = getpass("Confirm Password: ")

        if password != confirm:
            print("Passwords do not match. Please try again.")
            continue

        break

    admin_user = User(
        name=name,
        email=email,
        college_id=college_id,
        password_hash=generate_password_hash(password),
        role="admin"
    )

    db.session.add(admin_user)
    db.session.commit()

    print("\nAdmin account created successfully!")
