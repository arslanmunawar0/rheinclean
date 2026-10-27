"""Password hashing and short-lived session cookies."""

import secrets
from datetime import timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from fastapi import Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.core.config import settings

_hasher = PasswordHasher()
_session = URLSafeTimedSerializer(settings.secret_key, salt="rheinclean-session")

SESSION_COOKIE = "rc_session"
CSRF_COOKIE = "rc_csrf"


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def issue_session(admin_id: int) -> str:
    return _session.dumps({"sub": admin_id})


def read_session(token: str) -> int | None:
    try:
        payload = _session.loads(token, max_age=settings.session_seconds)
    except (BadSignature, SignatureExpired):
        return None
    subject = payload.get("sub") if isinstance(payload, dict) else None
    return subject if isinstance(subject, int) else None


def new_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def _cookie_kwargs() -> dict:
    return {
        "secure": settings.cookie_secure,
        "samesite": "lax",
        "path": "/",
        "max_age": settings.session_seconds,
    }


def set_session_cookie(response: Response, admin_id: int) -> None:
    response.set_cookie(SESSION_COOKIE, issue_session(admin_id), httponly=True, **_cookie_kwargs())


def set_csrf_cookie(response: Response, token: str) -> None:
    response.set_cookie(CSRF_COOKIE, token, httponly=False, **_cookie_kwargs())


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE, path="/")
    response.delete_cookie(CSRF_COOKIE, path="/")


def session_lifetime() -> timedelta:
    return timedelta(seconds=settings.session_seconds)
