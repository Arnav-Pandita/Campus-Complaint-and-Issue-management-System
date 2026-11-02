from flask import Flask,redirect,url_for
from sqlalchemy import text

from config import Config
from extensions import db, migrate, login_manager, csrf

import models
from models import User

from routes.auth import auth
from routes.student import student
from routes.admin import admin

from routes.setup import setup
from routes.superadmin import superadmin
from routes.complaints import complaints

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(admin)
    app.register_blueprint(setup)
    app.register_blueprint(superadmin)
    app.register_blueprint(complaints)

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    @app.route("/test-db")
    def test_db():

        try:
            db.session.execute(text("SELECT 1"))
            return "PostgreSQL connected successfully!"

        except Exception as e:
            db.session.rollback()
            return f"Database connection failed: {str(e)}", 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)