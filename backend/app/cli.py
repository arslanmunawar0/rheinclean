"""Create the first administrator or delete old enquiries. There is no public registration."""

import os
import sys

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal, create_tables
from app.models.admin import AdminUser
from app.services.quotes import purge_older_than

_BLOCKED = {"password", "admin", "changeme", "rheinclean"}


def create_admin() -> None:
    email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
    password = os.environ.get("ADMIN_PASSWORD", "")
    if "@" not in email:
        sys.exit("Setze ADMIN_EMAIL auf eine gültige Adresse.")
    if len(password) < 12 or password.lower() in _BLOCKED:
        sys.exit("ADMIN_PASSWORD muss mindestens 12 Zeichen haben und kein Standardpasswort sein.")
    create_tables()
    db = SessionLocal()
    try:
        existing = db.scalar(select(AdminUser).where(AdminUser.email == email))
        if existing:
            sys.exit("Für diese Adresse gibt es bereits ein Konto.")
        db.add(AdminUser(email=email, password_hash=hash_password(password)))
        db.commit()
    finally:
        db.close()
    print("Administratorkonto angelegt.")


def purge() -> None:
    raw = os.environ.get("RETAIN_DAYS", "365")
    if not raw.isdigit() or int(raw) < 1:
        sys.exit("RETAIN_DAYS muss eine positive Zahl sein.")
    create_tables()
    db = SessionLocal()
    try:
        removed = purge_older_than(db, int(raw))
    finally:
        db.close()
    print(f"{removed} Anfragen gelöscht, die älter als {raw} Tage sind.")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "create-admin":
        create_admin()
    elif command == "purge-enquiries":
        purge()
    else:
        sys.exit("Verwendung: python -m app.cli create-admin | purge-enquiries")
