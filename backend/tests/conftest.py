import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["ENVIRONMENT"] = "test"

import pytest
from fastapi.testclient import TestClient

from app.core.limiter import limiter
from app.core.security import hash_password
from app.db.session import SessionLocal, create_tables
from app.main import app
from app.models.admin import AdminUser
from app.models.quote import QuoteRequest


@pytest.fixture
def client():
    limiter.reset()
    create_tables()
    db = SessionLocal()
    db.query(QuoteRequest).delete()
    db.query(AdminUser).delete()
    db.add(AdminUser(email="admin@rheinclean.example", password_hash=hash_password("ein-langes-passwort")))
    db.commit()
    db.close()
    with TestClient(app) as test_client:
        yield test_client


def csrf_headers(client: TestClient) -> dict[str, str]:
    token = client.get("/api/v1/admin/session").json()["csrf_token"]
    return {"X-CSRF-Token": token}


def login(client: TestClient) -> dict[str, str]:
    headers = csrf_headers(client)
    response = client.post(
        "/api/v1/admin/login",
        json={"email": "admin@rheinclean.example", "password": "ein-langes-passwort"},
        headers=headers,
    )
    assert response.status_code == 200
    return {"X-CSRF-Token": response.json()["csrf_token"]}


def quote_payload(**overrides):
    payload = {
        "name": "Anna Beispiel",
        "email": "anna@example.com",
        "telephone": None,
        "company": None,
        "service": "buero",
        "property_type": "buero",
        "area_sqm": 120,
        "preferred_date": None,
        "message": "Bitte um ein Angebot für die wöchentliche Büroreinigung.",
        "privacy_accepted": True,
    }
    payload.update(overrides)
    return payload
