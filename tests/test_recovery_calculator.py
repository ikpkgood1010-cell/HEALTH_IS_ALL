from datetime import datetime, timedelta, timezone

import pytest

from backend.exercise_catalog import EXERCISE_CATALOG, ExerciseCategory
from backend.recovery_calculator import (
    ConditionScore,
    TargetMuscle,
    calculate_muscle_recovery,
)


def test_exercise_catalog_contains_27_unique_codes():
    assert len(EXERCISE_CATALOG) == 27
    assert {item.category for item in EXERCISE_CATALOG} == set(ExerciseCategory)


def test_recovery_formula_applies_all_multipliers():
    now = datetime(2026, 8, 10, tzinfo=timezone.utc)
    result = calculate_muscle_recovery(
        target_muscle=TargetMuscle.CHEST,
        rpe=8,
        condition_score=ConditionScore.POOR,
        frequency_per_week=3,
        age=42,
        performed_at=now - timedelta(hours=24),
        now=now,
    )

    # 48 * 1.2 * 1.25 * 0.85 * 1.1 = 67.32
    assert result.recommended_recovery_hours == 67.3
    assert result.recovery_percent == pytest.approx(35.7, abs=0.1)
    assert result.status == "REST"


def test_recovery_status_thresholds_and_cap():
    now = datetime(2026, 8, 10, tzinfo=timezone.utc)
    result = calculate_muscle_recovery(
        target_muscle=TargetMuscle.ABS,
        rpe=5,
        condition_score=ConditionScore.NORMAL,
        frequency_per_week=2,
        age=35,
        performed_at=now - timedelta(hours=30),
        now=now,
    )

    assert result.recovery_percent == 100.0
    assert result.status == "READY"
