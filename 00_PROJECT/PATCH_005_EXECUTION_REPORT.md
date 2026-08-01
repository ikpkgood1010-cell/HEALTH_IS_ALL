# PATCH_005_EXECUTION_REPORT

- Last Updated: 2026-08-01
- Scope: PATCH-005 Verification & Traceability Layer

## Executed Verification
1. scripts/check_canonical_constants.py
Canonical constant check PASSED

2. scripts/check_patch005_integrity.py
PATCH-005 integrity check PASSED

3. pytest -q
.........                                                                [100%]
=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
  /home/user/patch005/work/HEALTH IS ALL/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

test/progression_engine_test.py::test_anti_farming_10min_rule
  /home/user/patch005/work/HEALTH IS ALL/test/progression_engine_test.py:16: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    recent_time = datetime.utcnow() - timedelta(minutes=5)

test/progression_engine_test.py::test_anti_farming_10min_rule
tests/test_backend.py::test_record_health_activity
  /home/user/patch005/work/HEALTH IS ALL/backend/progression_engine.py:29: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    time_diff = datetime.utcnow() - last_action_time

test/progression_engine_test.py::test_dynamic_workout_calorie_calculation
test/progression_engine_test.py::test_dynamic_workout_calorie_calculation
test/system_integration_test.py::test_full_health_to_game_pipeline
  /home/user/patch005/work/HEALTH IS ALL/backend/health_calculator.py:39: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    current_hour = datetime.utcnow().hour

test/system_integration_test.py::test_full_health_to_game_pipeline
  /home/user/patch005/work/HEALTH IS ALL/backend/diet_calculator.py:29: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    current_hour = datetime.utcnow().hour

test/system_integration_test.py::test_full_health_to_game_pipeline
  /home/user/patch005/work/HEALTH IS ALL/backend/ai_agent_service.py:45: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    "timestamp": datetime.utcnow().isoformat(),

tests/test_backend.py::test_default_health_i_status
  /home/user/patch005/work/HEALTH IS ALL/backend/main.py:123: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    last_updated=datetime.utcnow(),

tests/test_backend.py::test_record_health_activity
  /home/user/patch005/work/HEALTH IS ALL/backend/main.py:66: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
9 passed, 11 warnings in 0.51s
