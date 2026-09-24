from fastapi.testclient import TestClient


def _auth_headers(client: TestClient, email: str = "anna@example.com") -> dict[str, str]:
    password = "supersecret123"
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post("/auth/token", data={"username": email, "password": password})
    token: str = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_job_returns_created_job(client: TestClient) -> None:
    headers = _auth_headers(client)

    response = client.post(
        "/jobs",
        json={"title": "KI-Engineer", "raw_text": "Gesucht: FastAPI-Entwickler"},
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "KI-Engineer"
    assert "embedding" not in body


def test_create_job_without_token_is_unauthorized(client: TestClient) -> None:
    response = client.post("/jobs", json={"title": "KI-Engineer", "raw_text": "Text"})

    assert response.status_code == 401


def test_list_my_jobs_returns_only_own_jobs(client: TestClient) -> None:
    headers_anna = _auth_headers(client, "anna@example.com")
    headers_bob = _auth_headers(client, "bob@example.com")

    client.post(
        "/jobs", json={"title": "Annas Job", "raw_text": "Text A"}, headers=headers_anna
    )
    client.post("/jobs", json={"title": "Bobs Job", "raw_text": "Text B"}, headers=headers_bob)

    response = client.get("/jobs", headers=headers_anna)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Annas Job"
