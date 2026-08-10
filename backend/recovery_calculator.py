"""Deterministic muscle recovery calculator based on the supplied spec."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum


class ConditionScore(str, Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    NORMAL = "NORMAL"
    POOR = "POOR"
    CRITICAL = "CRITICAL"


class TargetMuscle(str, Enum):
    CHEST = "CHEST"
    BACK = "BACK"
    SHOULDERS = "SHOULDERS"
    BICEPS = "BICEPS"
    TRICEPS = "TRICEPS"
    FOREARMS = "FOREARMS"
    ABS = "ABS"
    CORE = "CORE"
    GLUTES = "GLUTES"
    THIGHS = "THIGHS"


BASE_RECOVERY_HOURS = {
    TargetMuscle.ABS: 24.0,
    TargetMuscle.CORE: 24.0,
    TargetMuscle.BICEPS: 36.0,
    TargetMuscle.TRICEPS: 36.0,
    TargetMuscle.FOREARMS: 36.0,
    TargetMuscle.CHEST: 48.0,
    TargetMuscle.SHOULDERS: 48.0,
    TargetMuscle.BACK: 72.0,
    TargetMuscle.GLUTES: 72.0,
    TargetMuscle.THIGHS: 72.0,
}

CONDITION_MULTIPLIERS = {
    ConditionScore.EXCELLENT: 0.85,
    ConditionScore.GOOD: 0.95,
    ConditionScore.NORMAL: 1.0,
    ConditionScore.POOR: 1.25,
    ConditionScore.CRITICAL: 1.4,
}


def intensity_multiplier(rpe: int) -> float:
    if not 1 <= rpe <= 10:
        raise ValueError("rpe must be between 1 and 10")
    if rpe <= 4:
        return 0.8
    if rpe <= 7:
        return 1.0
    if rpe <= 9:
        return 1.2
    return 1.4


def frequency_multiplier(frequency_per_week: int, *, is_beginner: bool) -> float:
    if frequency_per_week < 1:
        raise ValueError("frequency_per_week must be at least 1")
    if is_beginner:
        return 1.25
    if frequency_per_week >= 3:
        return 0.85
    return 1.0


def age_multiplier(age: int) -> float:
    if age <= 0:
        raise ValueError("age must be positive")
    if age < 30:
        return 0.95
    if age < 40:
        return 1.0
    if age < 50:
        return 1.1
    return 1.2


@dataclass(frozen=True)
class MuscleRecoveryResult:
    target_muscle: str
    base_recovery_hours: float
    recommended_recovery_hours: float
    elapsed_hours: float
    recovery_percent: float
    status: str
    estimated_ready_at: str

    def to_dict(self) -> dict:
        return asdict(self)


def calculate_muscle_recovery(
    *,
    target_muscle: TargetMuscle,
    rpe: int,
    condition_score: ConditionScore,
    frequency_per_week: int,
    age: int,
    performed_at: datetime,
    is_beginner: bool = False,
    now: datetime | None = None,
) -> MuscleRecoveryResult:
    if performed_at.tzinfo is None:
        performed_at = performed_at.replace(tzinfo=timezone.utc)
    reference_time = now or datetime.now(timezone.utc)
    if reference_time.tzinfo is None:
        reference_time = reference_time.replace(tzinfo=timezone.utc)

    base_hours = BASE_RECOVERY_HOURS[target_muscle]
    recommended_hours = base_hours
    recommended_hours *= intensity_multiplier(rpe)
    recommended_hours *= CONDITION_MULTIPLIERS[condition_score]
    recommended_hours *= frequency_multiplier(
        frequency_per_week, is_beginner=is_beginner
    )
    recommended_hours *= age_multiplier(age)
    recommended_hours = round(recommended_hours, 1)

    elapsed_hours = max(
        0.0, (reference_time - performed_at).total_seconds() / 3600.0
    )
    recovery_percent = min(100.0, elapsed_hours / recommended_hours * 100.0)
    if recovery_percent >= 90.0:
        status = "READY"
    elif recovery_percent >= 50.0:
        status = "RECOVERING"
    else:
        status = "REST"

    return MuscleRecoveryResult(
        target_muscle=target_muscle.value,
        base_recovery_hours=base_hours,
        recommended_recovery_hours=recommended_hours,
        elapsed_hours=round(elapsed_hours, 1),
        recovery_percent=round(recovery_percent, 1),
        status=status,
        estimated_ready_at=(
            performed_at + timedelta(hours=recommended_hours)
        ).isoformat(),
    )
