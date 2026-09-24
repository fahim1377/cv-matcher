from fastapi.testclient import TestClient


def _auth_headers(client: TestClient, email: str = "anna@example.com") -> dict[str, str]:
    password = "supersecret123"
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post("/auth/token", data={"username": email, "password": password})
    token: str = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_cv_returns_created_cv(client: TestClient) -> None:
    headers = _auth_headers(client)

    response = client.post(
        "/cv", json={"raw_text": "Python-Entwickler mit FastAPI"}, headers=headers
    )

    assert response.status_code == 201
    body = response.json()
    assert body["raw_text"] == "Python-Entwickler mit FastAPI"
    assert "embedding" not in body


def test_create_cv_without_token_is_unauthorized(client: TestClient) -> None:
    response = client.post("/cv", json={"raw_text": "Python-Entwickler"})

    assert response.status_code == 401


def test_list_my_cvs_returns_only_own_cvs(client: TestClient) -> None:
    headers_anna = _auth_headers(client, "anna@example.com")
    headers_bob = _auth_headers(client, "bob@example.com")

    client.post("/cv", json={"raw_text": "Annas CV"}, headers=headers_anna)
    client.post("/cv", json={"raw_text": "Bobs CV"}, headers=headers_bob)

    response = client.get("/cv", headers=headers_anna)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["raw_text"] == "Annas CV"
