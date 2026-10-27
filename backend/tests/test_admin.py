from tests.conftest import login, quote_payload


def test_admin_routes_reject_anonymous_clients(client):
    assert client.get("/api/v1/admin/quote-requests").status_code == 401
    assert client.get("/api/v1/admin/quote-requests/RC-ABCDEFGH").status_code == 401
    assert client.get("/api/v1/admin/stats").status_code == 401


def test_login_rejects_a_wrong_password(client):
    token = client.get("/api/v1/admin/session").json()["csrf_token"]
    response = client.post(
        "/api/v1/admin/login",
        json={"email": "admin@rheinclean.example", "password": "falsch-falsch-falsch"},
        headers={"X-CSRF-Token": token},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Anmeldung fehlgeschlagen"


def test_login_requires_the_csrf_header(client):
    client.get("/api/v1/admin/session")
    response = client.post(
        "/api/v1/admin/login",
        json={"email": "admin@rheinclean.example", "password": "ein-langes-passwort"},
    )
    assert response.status_code == 403


def test_list_pagination_status_and_delete(client):
    for name in ("Anna Beispiel", "Bert Beispiel", "Clara Beispiel"):
        assert client.post("/api/v1/quote-requests", json=quote_payload(name=name)).status_code == 201
    headers = login(client)

    page = client.get("/api/v1/admin/quote-requests", params={"page": 1, "page_size": 2})
    assert page.status_code == 200
    body = page.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2

    found = client.get("/api/v1/admin/quote-requests", params={"q": "Clara"})
    assert found.json()["total"] == 1
    reference = found.json()["items"][0]["reference"]

    updated = client.patch(
        f"/api/v1/admin/quote-requests/{reference}",
        json={"status": "kontaktiert"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "kontaktiert"

    rejected = client.patch(
        f"/api/v1/admin/quote-requests/{reference}",
        json={"status": "gewonnen"},
        headers=headers,
    )
    assert rejected.status_code == 422

    stats = client.get("/api/v1/admin/stats").json()
    assert stats["total"] == 3
    assert stats["in_progress"] == 1

    deleted = client.delete(f"/api/v1/admin/quote-requests/{reference}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/admin/quote-requests/{reference}").status_code == 404


def test_status_change_without_csrf_is_rejected(client):
    created = client.post("/api/v1/quote-requests", json=quote_payload())
    login(client)
    response = client.patch(
        f"/api/v1/admin/quote-requests/{created.json()['reference']}",
        json={"status": "abgelehnt"},
    )
    assert response.status_code == 403
