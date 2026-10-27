from app.db.session import SessionLocal
from app.models.quote import QuoteRequest
from tests.conftest import quote_payload


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "secret" not in response.text.lower()


def test_services(client):
    response = client.get("/api/v1/services")
    ids = [item["id"] for item in response.json()["items"]]
    assert response.status_code == 200
    assert ids == ["buero", "treppenhaus", "praxis", "fenster", "grund", "individuell"]


def test_valid_quote_is_stored_with_a_public_reference(client):
    response = client.post("/api/v1/quote-requests", json=quote_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["reference"].startswith("RC-")
    assert len(body["reference"]) == 11
    assert "anna@example.com" not in response.text
    assert "verbindlicher Auftrag" in body["message"]

    db = SessionLocal()
    try:
        row = db.query(QuoteRequest).one()
    finally:
        db.close()
    assert row.reference == body["reference"]
    assert row.email == "anna@example.com"
    assert row.status == "neu"
    assert row.privacy_version == "2026-10-01"


def test_invalid_email(client):
    response = client.post("/api/v1/quote-requests", json=quote_payload(email="keine-adresse"))
    assert response.status_code == 422


def test_missing_required_fields(client):
    payload = quote_payload()
    del payload["name"]
    del payload["message"]
    response = client.post("/api/v1/quote-requests", json=payload)
    assert response.status_code == 422


def test_excessively_long_message(client):
    response = client.post("/api/v1/quote-requests", json=quote_payload(message="a" * 2001))
    assert response.status_code == 422


def test_unknown_service_is_rejected(client):
    response = client.post("/api/v1/quote-requests", json=quote_payload(service="garten"))
    assert response.status_code == 422


def test_references_are_unique(client):
    first = client.post("/api/v1/quote-requests", json=quote_payload()).json()["reference"]
    second = client.post("/api/v1/quote-requests", json=quote_payload(name="Bert Beispiel")).json()["reference"]
    assert first != second
