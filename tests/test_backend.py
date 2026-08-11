import pytest
from datetime import timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.adventure_service import adventure_window
from backend.config import utc_now
from backend.database import ActivityLogModel, Base, get_db
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


@pytest.fixture()
def journey_runtime():
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

    previous_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client, testing_session
    if previous_override is None:
        app.dependency_overrides.pop(get_db, None)
    else:
        app.dependency_overrides[get_db] = previous_override
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


def test_health_record_retry_is_persistently_idempotent(journey_runtime):
    client, testing_session = journey_runtime
    payload = {
        "user_id": "idempotency_user",
        "record_type": "meal_log",
        "value": 550.0,
        "detail_data": {"meal_type": "점심", "protein": 30},
        "idempotency_key": "11111111-1111-4111-8111-111111111111",
    }

    first = client.post("/api/v1/health/record", json=payload)
    retry = client.post("/api/v1/health/record", json=payload)

    assert first.status_code == 200
    assert retry.status_code == 200
    assert first.json()["record_id"] == payload["idempotency_key"]
    assert retry.json()["record_id"] == payload["idempotency_key"]
    assert first.json()["duplicate"] is False
    assert retry.json()["duplicate"] is True
    assert retry.json()["exp_gained"] == first.json()["exp_gained"]

    with testing_session() as db:
        assert db.query(ActivityLogModel).filter(
            ActivityLogModel.user_id == payload["user_id"],
            ActivityLogModel.record_type == "meal_log",
        ).count() == 1

    conflicting = client.post(
        "/api/v1/health/record",
        json={**payload, "value": 900},
    )
    assert conflicting.status_code == 409


def test_health_record_to_adventure_and_training_ground_journey(journey_runtime):
    client, testing_session = journey_runtime
    user_id = "journey_user"
    records = [
        ("meal_log", 1000.0, "21111111-1111-4111-8111-111111111111"),
        ("workout_log", 30.0, "31111111-1111-4111-8111-111111111111"),
        ("water_log", 1.0, "41111111-1111-4111-8111-111111111111"),
    ]
    for record_type, value, key in records:
        response = client.post(
            "/api/v1/health/record",
            json={
                "user_id": user_id,
                "record_type": record_type,
                "value": value,
                "idempotency_key": key,
            },
        )
        assert response.status_code == 200

    status = client.get(f"/api/v1/health-i/status/{user_id}").json()
    assert status["today_consumed_calories"] == 1000.0
    assert status["today_workout_minutes"] == 30.0
    assert status["today_water_liters"] == 1.0

    overview = client.get(f"/api/v1/game/overview/{user_id}").json()
    assert overview["hbi_score"] > 0
    assert overview["vitality"] > 0

    window_start, _ = adventure_window(utc_now())
    with testing_session() as db:
        health_logs = db.query(ActivityLogModel).filter(
            ActivityLogModel.user_id == user_id,
            ActivityLogModel.record_type.in_({"meal_log", "workout_log", "water_log"}),
        ).all()
        for log in health_logs:
            log.logged_at = window_start + timedelta(hours=1)
        db.commit()

    settled = client.post(
        "/api/v1/game/adventures/settle",
        json={"user_id": user_id},
    )
    assert settled.status_code == 200
    adventure = settled.json()
    assert adventure["hbi_score"] > 0
    assert adventure["gross_guild_coins"] > 0
    assert len(adventure["rooms"]) == 5
    assert adventure["rooms"][0]["room_type"] == "COMBAT"
    assert adventure["rooms"][-2]["room_type"] in {"REST", "SHOP"}
    assert adventure["rooms"][-1]["room_type"] == "BOSS"

    claimed = client.post(
        f"/api/v1/game/adventures/{adventure['adventure_id']}/claim",
        json={"user_id": user_id},
    )
    assert claimed.status_code == 200
    assert claimed.json()["facility_invested"] > 0

    facility = client.get(
        f"/api/v1/game/facilities/training-grounds/{user_id}"
    ).json()
    assert facility["total_invested"] == claimed.json()["facility_invested"]
    assert facility["guild_coin_balance"] == claimed.json()["guild_coins_received"]
    assert facility["stage_name"] == "들판 훈련터"

    history = client.get(
        f"/api/v1/game/adventures/history/{user_id}?limit=5"
    )
    assert history.status_code == 200
    assert len(history.json()["items"]) == 1
    assert history.json()["items"][0]["adventure_id"] == adventure["adventure_id"]
    assert history.json()["items"][0]["claimed"] is True


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
