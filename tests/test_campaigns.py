# tests/test_campaigns.py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone


@pytest.fixture
def auth_token(client: TestClient):
    # Enroll the user
    client.post("/users/enroll", json={
        "email": "campaign@test.com",
        "password": "pass123"
    })

    # Login to get access token
    login_res = client.post(
        "/users_Login",
        data={"username": "campaign@test.com", "password": "pass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    return login_res.json()["access_token"]


def test_create_campaign(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "name": "Test Campaign",
        "description": "A test campaign",
        "start_date": "2025-10-26T00:00:00",
        "end_date": "2025-12-26T00:00:00",
        "budget": 1000.0
    }
    response = client.post("/api/campaigns/", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "campaign" in data
    assert data["campaign"]["name"] == "Test Campaign"
    assert "id" in data["campaign"]


def test_get_campaigns(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/campaigns/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    # Assuming response returns {"campaigns": [...]}
    assert "campaigns" in data or isinstance(data, list)


def test_get_campaign_by_id(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Create campaign first
    payload = {
        "name": "Test Campaign",
        "description": "A test campaign",
        "start_date": "2025-10-26T00:00:00",
        "end_date": "2025-12-26T00:00:00",
        "budget": 1000.0
    }
    response = client.post("/api/campaigns/", json=payload, headers=headers)
    assert response.status_code == 200
    campaign_id = response.json()["campaign"]["id"]

    get_res = client.get(f"/api/campaigns/{campaign_id}", headers=headers)
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["id"] == campaign_id


def test_update_campaign(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Create a campaign first
    create_payload = {
        "name": "Test Campaign",
        "description": "A test campaign",
        "start_date": "2025-10-26T00:00:00",
        "end_date": "2025-12-26T00:00:00",
        "budget": 1000.0
    }
    response = client.post("/api/campaigns/", json=create_payload, headers=headers)
    assert response.status_code == 200
    campaign_id = response.json()["campaign"]["id"]

    # Partial update
    update_payload = {
        "name": "Updated Campaign",
        "budget": 1200.0
    }
    update_res = client.put(f"/api/campaigns/{campaign_id}", json=update_payload, headers=headers)
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["campaign"]["name"] == "Updated Campaign"
    assert data["campaign"]["budget"] == 1200.0


def test_delete_campaign(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Create campaign to delete
    create_payload = {
        "name": "Delete Campaign",
        "description": "Delete test",
        "start_date": "2025-10-26T00:00:00",
        "end_date": "2025-12-26T00:00:00",
        "budget": 500.0
    }
    response = client.post("/api/campaigns/", json=create_payload, headers=headers)
    assert response.status_code == 200
    campaign_id = response.json()["campaign"]["id"]

    # Delete campaign
    delete_res = client.delete(f"/api/campaigns/{campaign_id}", headers=headers)
    assert delete_res.status_code == 200
    assert "deleted successfully" in delete_res.json()["message"]
