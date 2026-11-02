import secrets
import hashlib


def generate_tracking_code():

    return secrets.token_urlsafe(16)


def hash_tracking_code(code):

    return hashlib.sha256(
        code.encode("utf-8")
    ).hexdigest()