import pytest
from datetime import timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.adventure_service import adventure_window
from backend.config import utc_now
from backend.database import (
    ActivityLogModel,
    Base,
    GameConstellationNodeModel,
    GameHeroModel,
    GameProfileModel,
    get_db,
    get_optional_db,
)
from backend.main import app
from backend.main import nutrition_data_service


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
    app.dependency_overrides[get_optional_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_optional_db, None)
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
    previous_optional_override = app.dependency_overrides.get(get_optional_db)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_optional_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client, testing_session
    if previous_override is None:
        app.dependency_overrides.pop(get_db, None)
    else:
        app.dependency_overrides[get_db] = previous_override
    if previous_optional_override is None:
        app.dependency_overrides.pop(get_optional_db, None)
    else:
        app.dependency_overrides[get_optional_db] = previous_optional_override
    engine.dispose()


def test_health_check(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "HEALTH IS ALL API"}


def test_official_nutrition_search_and_unknown_meal_cards(client, monkeypatch):
    candidate = {
        "provider": "MFDS_PRODUCT_DB", "food_id": "P1", "name": "테스트 제품",
        "brand": "테스트사", "basis_g": 100, "serving_g": 150,
        "kcal": 300, "carbs_g": 50, "protein_g": 10, "fat_g": 8,
        "fiber_g": 2, "source_label": "식품의약품안전처 식품영양성분DB",
    }
    monkeypatch.setattr(nutrition_data_service, "mfds_api_key", "test-key")
    monkeypatch.setattr(nutrition_data_service, "search", lambda query, limit=5: [candidate])

    searched = client.get("/api/v1/nutrition/foods/search", params={"q": "테스트 제품"})
    assert searched.status_code == 200
    assert searched.json()["items"][0]["food_id"] == "P1"

    analyzed = client.post("/api/v1/health/text/analyze", json={
        "user_id": "official_lookup_user", "record_type": "meal_log",
        "meal_type": "간식", "text": "테스트 제품 한 봉지 먹었어",
    })
    assert analyzed.status_code == 200
    assert analyzed.json()["confirmation_cards"][0]["id"] == "external_candidate_index"


def test_canonical_idle_game_direction(client):
    response = client.get("/api/v1/game/direction")
    assert response.status_code == 200
    data = response.json()
    assert data["official_name"] == "HEALTH IS ALL : 건강이 전부다 !!"
    assert data["health_tabs"] == ["홈", "운동", "식단", "마이"]
    assert data["party_roles"] == ["탱커", "전사", "마법사", "궁수", "도적", "치유사"]
    assert data["normal_rooms_per_floor"] == 5
    assert data["boss_rooms_per_floor"] == 1
    assert data["constellation_layers"] == 7
    assert data["large_nodes_per_layer"] == 6
    assert data["deterministic_spirit_hatching"] is True
    assert data["random_gacha"] is False
    assert data["equipment_inventory"] is False
    assert "small_nodes" in data["rebirth_resets"]
    assert "medium_nodes" in data["rebirth_resets"]
    assert "job_advancement_tiers" in data["rebirth_retains"]
    assert "advancement_appearance" in data["rebirth_retains"]


def test_canonical_game_state_and_rebirth_api(journey_runtime):
    client, testing_session = journey_runtime
    user_id = "canonical_game_user"
    initialized = client.post(
        "/api/v1/game/state/initialize",
        json={"user_id": user_id},
    )
    assert initialized.status_code == 200
    assert initialized.json()["phase"] == "ONBOARDING"
    assert len(initialized.json()["heroes"]) == 6
    assert initialized.json()["large_node_slots_by_layer"] == {
        "0": 5,
        "1": 6,
        "2": 6,
        "3": 6,
        "4": 6,
        "5": 6,
        "6": 6,
    }
    assert client.post(
        "/api/v1/game/state/initialize",
        json={"user_id": user_id},
    ).json() == initialized.json()

    starter = client.post(
        "/api/v1/game/heroes/select-initial",
        json={
            "user_id": user_id,
            "hero_code": "TANKER",
            "expected_revision": 0,
        },
    )
    assert starter.status_code == 200
    assert starter.json()["phase"] == "IDLE_BATTLE"
    assert starter.json()["revision"] == 1
    assert starter.json()["starter_hero_code"] == "TANKER"
    assert starter.json()["node_counts"]["LARGE"] == 0
    assert sum(hero["recruited"] for hero in starter.json()["heroes"]) == 1
    assert starter.json()["constellation_layers"][0]["node_count"] == 5
    assert starter.json()["constellation_layers"][1]["node_count"] == 6

    conflicting_starter = client.post(
        "/api/v1/game/heroes/select-initial",
        json={
            "user_id": user_id,
            "hero_code": "MAGE",
            "expected_revision": 1,
        },
    )
    assert conflicting_starter.status_code == 409

    with testing_session() as db:
        profile = db.query(GameProfileModel).filter_by(user_id=user_id).one()
        profile.battle_anchor_at = utc_now() - timedelta(minutes=10)
        db.commit()

    battle_payload = {
        "user_id": user_id,
        "idempotency_key": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
    }
    battle = client.post("/api/v1/game/battle/settle", json=battle_payload)
    battle_retry = client.post("/api/v1/game/battle/settle", json=battle_payload)
    assert battle.status_code == 200
    assert battle.json()["rooms_cleared"] > 0
    assert battle.json()["gold_earned"] > 0
    assert battle.json()["state"]["battle"]["status"] == "RUNNING"
    assert battle_retry.json()["already_settled"] is True
    assert battle_retry.json()["gold_earned"] == battle.json()["gold_earned"]

    with testing_session() as db:
        profile = db.query(GameProfileModel).filter_by(user_id=user_id).one()
        profile.tower_floor = 109
        profile.room_position = 5
        profile.gold = 900
        hero = db.query(GameHeroModel).filter_by(
            user_id=user_id, hero_code="TANKER"
        ).one()
        hero.recruited = True
        hero.advancement_tier = 2
        hero.appearance_code = "TANKER_TIER_2"
        db.add_all(
            [
                GameConstellationNodeModel(
                    user_id=user_id,
                    node_code="SMALL_API_TEST",
                    layer=1,
                    node_size="SMALL",
                    unlocked_run_number=1,
                ),
                GameConstellationNodeModel(
                    user_id=user_id,
                    node_code="L2_TANKER",
                    layer=2,
                    node_size="LARGE",
                    hero_code="TANKER",
                    unlocked_run_number=1,
                ),
            ]
        )
        db.commit()

    preview = client.get(f"/api/v1/game/rebirth/preview/{user_id}")
    assert preview.status_code == 200
    assert preview.json()["reset"]["small_nodes"] == 1
    assert preview.json()["retain"]["large_nodes"] == 1

    payload = {
        "user_id": user_id,
        "expected_revision": battle.json()["state"]["revision"],
        "idempotency_key": "44444444-4444-4444-8444-444444444444",
        "confirm": True,
    }
    rebirth = client.post("/api/v1/game/rebirth/execute", json=payload)
    assert rebirth.status_code == 200
    assert rebirth.json()["already_executed"] is False
    state = rebirth.json()["state"]
    assert state["tower_floor"] == 1
    assert state["gold"] == 0
    assert state["node_counts"] == {"SMALL": 0, "MEDIUM": 0, "LARGE": 1}
    tanker = next(hero for hero in state["heroes"] if hero["hero_code"] == "TANKER")
    assert tanker["advancement_tier"] == 2
    assert tanker["appearance_code"] == "TANKER_TIER_2"

    retry = client.post("/api/v1/game/rebirth/execute", json=payload)
    assert retry.status_code == 200
    assert retry.json()["already_executed"] is True


def test_layer_zero_unlock_api_spends_once_and_rejects_skipping(journey_runtime):
    client, testing_session = journey_runtime
    user_id = "constellation_api_user"
    client.post("/api/v1/game/state/initialize", json={"user_id": user_id})
    selected = client.post(
        "/api/v1/game/heroes/select-initial",
        json={
            "user_id": user_id,
            "hero_code": "MAGE",
            "expected_revision": 0,
        },
    ).json()
    with testing_session() as db:
        profile = db.query(GameProfileModel).filter_by(user_id=user_id).one()
        profile.gold = 10_000
        db.commit()
    state = client.get(f"/api/v1/game/state/{user_id}").json()
    branch = next(
        item for item in state["recruitment_branches"]
        if item["hero_code"] == "TANKER"
    )
    payload = {
        "user_id": user_id,
        "node_code": branch["next_node"]["node_code"],
        "expected_revision": selected["revision"],
    }
    unlocked = client.post(
        "/api/v1/game/constellation/unlock",
        json=payload,
    )
    assert unlocked.status_code == 200
    assert unlocked.json()["gold"] == 8_500
    assert unlocked.json()["node_counts"]["SMALL"] == 1

    retry = client.post("/api/v1/game/constellation/unlock", json=payload)
    assert retry.status_code == 200
    assert retry.json()["gold"] == 8_500

    skipped = client.post(
        "/api/v1/game/constellation/unlock",
        json={
            "user_id": user_id,
            "node_code": "L0_TANKER_S03",
            "expected_revision": unlocked.json()["revision"],
        },
    )
    assert skipped.status_code == 409


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


def test_text_analysis_save_copy_and_daily_review(journey_runtime):
    client, _ = journey_runtime
    user_id = "detailed_food_user"
    client.post("/api/v1/game/state/initialize", json={"user_id": user_id})
    lunch_text = (
        "양배추 한줌을 먹고 10분 후 햇반에 시금치1큐브, 마늘 4개, 생강 반개, "
        "냉동표고 10개, 산수유 10알, 우엉 손가락 한마디, 닭가슴살 1개랑 "
        "생양파 1개 같이 먹었어."
    )
    analyzed = client.post(
        "/api/v1/health/text/analyze",
        json={
            "user_id": user_id, "record_type": "meal_log", "meal_type": "점심",
            "text": lunch_text,
            "answers": {"grams_cooked_rice": 210, "grams_chicken_breast": 120},
        },
    )
    assert analyzed.status_code == 200
    analysis = analyzed.json()
    assert analysis["estimated"]["meal_score"] == 90
    saved = client.post(
        "/api/v1/health/record",
        json={
            "user_id": user_id, "record_type": "meal_log", "value": analysis["value"],
            "detail_data": analysis["storage_detail"],
            "idempotency_key": "81111111-1111-4111-8111-111111111111",
        },
    )
    assert saved.status_code == 200

    copied = client.post(
        "/api/v1/health/text/analyze",
        json={
            "user_id": user_id, "record_type": "meal_log", "meal_type": "저녁",
            "text": "오늘 점심이랑 똑같이 먹었어",
        },
    )
    assert copied.status_code == 200
    assert copied.json()["estimated"]["totals"] == analysis["estimated"]["totals"]
    assert copied.json()["storage_detail"]["copied_from_meal"] is True

    review = client.get(f"/api/v1/health/review/daily/{user_id}")
    assert review.status_code == 200
    assert review.json()["meal_count"] == 1
    assert review.json()["nutrition"]["protein_g"] > 40
    assert review.json()["exp_earned"] == saved.json()["exp_gained"]
    assert review.json()["health_essence_earned"] == 1


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


def test_health_records_award_bounded_idempotent_game_essence(journey_runtime):
    client, _ = journey_runtime
    user_id = "health_essence_user"
    initialized = client.post(
        "/api/v1/game/state/initialize",
        json={"user_id": user_id},
    )
    assert initialized.status_code == 200

    workout = {
        "user_id": user_id,
        "record_type": "workout_log",
        "value": 30,
        "idempotency_key": "51111111-1111-4111-8111-111111111111",
    }
    first = client.post("/api/v1/health/record", json=workout)
    retry = client.post("/api/v1/health/record", json=workout)
    assert first.status_code == 200
    assert first.json()["health_essence_earned"] == 2
    assert retry.json()["health_essence_earned"] == 2
    assert retry.json()["duplicate"] is True

    for index in range(10):
        response = client.post(
            "/api/v1/health/record",
            json={
                "user_id": user_id,
                "record_type": "meal_log",
                "value": 500,
                "idempotency_key": f"6{index:07d}-1111-4111-8111-111111111111",
            },
        )
        assert response.status_code == 200
    state = client.get(f"/api/v1/game/state/{user_id}").json()
    assert state["health_essence"] == 8


def test_game_initialization_backfills_earlier_health_records(journey_runtime):
    client, _ = journey_runtime
    user_id = "health_backfill_user"
    recorded = client.post(
        "/api/v1/health/record",
        json={
            "user_id": user_id,
            "record_type": "workout_log",
            "value": 60,
            "idempotency_key": "71111111-1111-4111-8111-111111111111",
        },
    )
    assert recorded.status_code == 200
    assert recorded.json()["health_essence_earned"] == 0

    initialized = client.post(
        "/api/v1/game/state/initialize",
        json={"user_id": user_id},
    )
    assert initialized.status_code == 200
    assert initialized.json()["health_essence"] == 3


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
    assert all(room["result_title"] for room in adventure["rooms"])

    claimed = client.post(
        f"/api/v1/game/adventures/{adventure['adventure_id']}/claim",
        json={"user_id": user_id},
    )
    assert claimed.status_code == 200
    assert claimed.json()["facility_invested"] > 0
    assert claimed.json()["joined_hero"]["name"] == "아루"
    assert claimed.json()["joined_hero"]["gameplay_effect"] == "NONE"

    roster = client.get(f"/api/v1/game/heroes/{user_id}")
    assert roster.status_code == 200
    assert [item["hero_code"] for item in roster.json()["items"]] == [
        "FOREST_SCOUT_ARU"
    ]

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
    assert first_claim.json()["joined_hero"] is None
    assert client.get(
        "/api/v1/game/heroes/adventure_test_user"
    ).json()["items"] == []
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
