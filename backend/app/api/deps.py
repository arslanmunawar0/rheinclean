"""Authentication and CSRF checks for admin routes."""

import secrets

from fastapi import Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.security import CSRF_COOKIE, SESSION_COOKIE, read_session, set_csrf_cookie
from app.db.session import get_db
from app.models.admin import AdminUser


def ensure_csrf(request: Request, response: Response) -> str:
    token = request.cookies.get(CSRF_COOKIE)
    if not token:
        token = secrets.token_urlsafe(32)
        set_csrf_cookie(response, token)
    return token


def require_csrf(request: Request) -> None:
    cookie = request.cookies.get(CSRF_COOKIE, "")
    header = request.headers.get("x-csrf-token", "")
    if not cookie or not header or not secrets.compare_digest(cookie, header):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ungültiges Sicherheitstoken")


def current_admin(request: Request, db: Session = Depends(get_db)) -> AdminUser:
    admin_id = read_session(request.cookies.get(SESSION_COOKIE, ""))
    if admin_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Anmeldung erforderlich")
    admin = db.get(AdminUser, admin_id)
    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Anmeldung erforderlich")
    return admin
