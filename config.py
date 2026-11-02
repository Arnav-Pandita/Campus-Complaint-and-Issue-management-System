import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SUPERADMIN_SETUP_KEY = os.getenv("SUPERADMIN_SETUP_KEY")

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}