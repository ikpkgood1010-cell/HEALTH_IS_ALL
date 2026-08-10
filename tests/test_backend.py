import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import Base, get_db
from backend.main import app


@pytest.fixture(scope="module")
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    testing_session = sessionmaker(bind=engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_db, None)
    engine.dispose()


def test_health_check(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "HEALTH IS ALL API"}


def test_default_health_i_status(client):
    response = client.get("/api/v1/health-i/status/test_user")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "건강이"
    assert data["level"] == 1


def test_record_health_activity(client):
    payload = {"user_id": "test_user_1", "record_type": "meal_log", "value": 550.0, "detail_data": {"carbs": 60}}
    response = client.post("/api/v1/health/record", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "exp_gained" in data


def test_calculate_recovery_endpoint(client):
    response = client.post(
        "/api/v1/recovery/calculate",
        json={
            "userId": "anon_test",
            "performedAt": "2026-08-09T00:00:00Z",
            "age": 35,
            "condition": {"sleepHours": 7.5, "conditionScore": "NORMAL"},
            "workoutLogs": [
                {
                    "targetMuscle": "CHEST",
                    "rpe": 6,
                    "frequencyPerWeek": 2,
                }
            ],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "anon_test"
    assert data["results"][0]["recommended_recovery_hours"] == 48.0
    assert data["results"][0]["target_muscle"] == "CHEST"


def test_automatic_adventure_is_idempotent_and_claims_once(client):
    payload = {"user_id": "adventure_test_user"}
    first = client.post("/api/v1/game/adventures/settle", json=payload)
    second = client.post("/api/v1/game/adventures/settle", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["adventure_id"] == second.json()["adventure_id"]
    assert first.json()["claimed"] is False

    adventure_id = first.json()["adventure_id"]
    first_claim = client.post(
        f"/api/v1/game/adventures/{adventure_id}/claim",
        json=payload,
    )
    retry_claim = client.post(
        f"/api/v1/game/adventures/{adventure_id}/claim",
        json=payload,
    )

    assert first_claim.status_code == 200
    assert retry_claim.status_code == 200
    assert first_claim.json()["claim_id"] == retry_claim.json()["claim_id"]
    assert first_claim.json()["already_claimed"] is False
    assert retry_claim.json()["already_claimed"] is True
    assert (
        first_claim.json()["guild_coins_received"]
        + first_claim.json()["facility_invested"]
        == first_claim.json()["gross_guild_coins"]
    )

    settled_again = client.post("/api/v1/game/adventures/settle", json=payload)
    assert settled_again.json()["claimed"] is True


def test_training_grounds_reports_facility_and_balance(client):
    response = client.get(
        "/api/v1/game/facilities/training-grounds/adventure_test_user"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "TRAINING_GROUNDS"
    assert data["name"] == "훈련장"
    assert data["level"] >= 1
    assert 0 <= data["progress_ratio"] < 1


def test_adventure_claim_rejects_another_user(client):
    settled = client.post(
        "/api/v1/game/adventures/settle",
        json={"user_id": "adventure_owner"},
    ).json()
    response = client.post(
        f"/api/v1/game/adventures/{settled['adventure_id']}/claim",
        json={"user_id": "different_user"},
    )
    assert response.status_code == 403
