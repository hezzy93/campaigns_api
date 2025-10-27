# tests/test_users.py
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client_fixture(client: TestClient):
    return client

def test_enroll_user(client: TestClient):
    response = client.post("/users/enroll", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_login_user(client: TestClient):
    # Ensure the user is enrolled first
    client.post("/users/enroll", json={
        "email": "login@test.com",
        "password": "pass123"
    })

    # Use form data (OAuth2PasswordRequestForm expects this)
    response = client.post(
        "/users_Login",
        data={"username": "login@test.com", "password": "pass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"

    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"
