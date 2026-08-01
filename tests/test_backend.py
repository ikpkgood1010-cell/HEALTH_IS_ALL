from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "HEALTH IS ALL API"}


def test_default_health_i_status():
    response = client.get("/api/v1/health-i/status/test_user")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "건강이"
    assert data["level"] == 1


def test_record_health_activity():
    payload = {"user_id": "test_user_1", "record_type": "meal_log", "value": 550.0, "detail_data": {"carbs": 60}}
    response = client.post("/api/v1/health/record", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "exp_gained" in data
