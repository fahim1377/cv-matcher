import uuid

from fastapi.testclient import TestClient

from cv_matcher.core.security import create_access_token


def _register_and_login(client: TestClient, email: str = "anna@example.com") -> str:
    password = "supersecret123"
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post("/auth/token", data={"username": email, "password": password})
    token: str = response.json()["access_token"]
    return token


def test_read_me_returns_current_user(client: TestClient) -> None:
    token = _register_and_login(client)

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["email"] == "anna@example.com"


def test_read_me_without_token_is_unauthorized(client: TestClient) -> None:
    response = client.get("/users/me")

    assert response.status_code == 401


def test_read_me_with_invalid_token_is_unauthorized(client: TestClient) -> None:
    response = client.get("/users/me", headers={"Authorization": "Bearer not-a-real-token"})

    assert response.status_code == 401


def test_read_me_with_token_for_unknown_user_is_unauthorized(client: TestClient) -> None:
    token = create_access_token(subject=uuid.uuid4())

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
