from fastapi.testclient import TestClient


def test_register_creates_user(client: TestClient) -> None:
    response = client.post(
        "/auth/register", json={"email": "anna@example.com", "password": "supersecret123"}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "anna@example.com"
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_rejects_duplicate_email(client: TestClient) -> None:
    payload = {"email": "anna@example.com", "password": "supersecret123"}
    client.post("/auth/register", json=payload)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400


def test_login_returns_token_for_correct_credentials(client: TestClient) -> None:
    client.post(
        "/auth/register", json={"email": "anna@example.com", "password": "supersecret123"}
    )

    response = client.post(
        "/auth/token",
        data={"username": "anna@example.com", "password": "supersecret123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_rejects_wrong_password(client: TestClient) -> None:
    client.post(
        "/auth/register", json={"email": "anna@example.com", "password": "supersecret123"}
    )

    response = client.post(
        "/auth/token",
        data={"username": "anna@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_login_rejects_unknown_email(client: TestClient) -> None:
    response = client.post(
        "/auth/token",
        data={"username": "unknown@example.com", "password": "supersecret123"},
    )

    assert response.status_code == 401
