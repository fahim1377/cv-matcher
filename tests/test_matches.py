import uuid

from fastapi.testclient import TestClient


def _auth_headers(client: TestClient, email: str = "anna@example.com") -> dict[str, str]:
    password = "supersecret123"
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post("/auth/token", data={"username": email, "password": password})
    token: str = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_match_between_own_cv_and_job_returns_score(client: TestClient) -> None:
    headers = _auth_headers(client)
    cv_id = client.post(
        "/cv", json={"raw_text": "Python-Entwickler mit FastAPI"}, headers=headers
    ).json()["id"]
    job_id = client.post(
        "/jobs",
        json={"title": "KI-Engineer", "raw_text": "Gesucht: Python-Entwickler mit FastAPI"},
        headers=headers,
    ).json()["id"]

    response = client.get(f"/matches/{cv_id}/{job_id}", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["cv_id"] == cv_id
    assert body["job_id"] == job_id
    assert -1.0 <= body["score"] <= 1.0


def test_match_with_someone_elses_job_is_not_found(client: TestClient) -> None:
    headers_anna = _auth_headers(client, "anna@example.com")
    headers_bob = _auth_headers(client, "bob@example.com")

    cv_id = client.post(
        "/cv", json={"raw_text": "Annas CV"}, headers=headers_anna
    ).json()["id"]
    job_id = client.post(
        "/jobs", json={"title": "Bobs Job", "raw_text": "Bobs Job Text"}, headers=headers_bob
    ).json()["id"]

    response = client.get(f"/matches/{cv_id}/{job_id}", headers=headers_anna)

    assert response.status_code == 404


def test_match_with_unknown_cv_is_not_found(client: TestClient) -> None:
    headers = _auth_headers(client)
    job_id = client.post(
        "/jobs", json={"title": "Job", "raw_text": "Text"}, headers=headers
    ).json()["id"]

    response = client.get(f"/matches/{uuid.uuid4()}/{job_id}", headers=headers)

    assert response.status_code == 404
