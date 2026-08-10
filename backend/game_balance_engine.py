"""Health-first game balance rules for the anonymous MVP.

The game layer is deliberately derived from health activity. It does not award
extra progress for repeatedly opening the app and it never punishes a low score.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import floor, sqrt
from typing import Iterable


ROOM_WEIGHTS = {
    "COMBAT": 50,
    "EVENT": 15,
    "REST": 15,
    "SHOP": 10,
    "ELITE": 10,
}


def _score(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def calculate_hbi(scores: Iterable[float]) -> float:
    """Health Balance Index = minimum * 0.6 + average * 0.4."""
    normalized = [_score(value) for value in scores]
    if not normalized:
        return 0.0
    return round(min(normalized) * 0.6 + (sum(normalized) / len(normalized)) * 0.4, 1)


def dungeon_room_type(roll: int, *, position: int, room_count: int) -> str:
    """Return a room type using the approved distribution and safety guards.

    The first room is COMBAT, the last is BOSS, and the room before the boss is
    a recovery choice (REST/SHOP). ``roll`` is an integer in the 0..99 range so
    callers can provide a deterministic seed.
    """
    if room_count < 3:
        raise ValueError("room_count must be at least 3")
    if position == 0:
        return "COMBAT"
    if position == room_count - 1:
        return "BOSS"
    if position == room_count - 2:
        return "REST" if roll % 2 == 0 else "SHOP"

    cursor = 0
    normalized_roll = roll % 100
    for room_type, weight in ROOM_WEIGHTS.items():
        cursor += weight
        if normalized_roll < cursor:
            return room_type
    return "COMBAT"


@dataclass(frozen=True)
class GameOverview:
    hbi_score: float
    hbi_confidence: str
    health_breakdown: dict[str, float]
    guild_level: int
    guild_stage_name: str
    tower_floor: int
    vitality: int
    guild_coins: int
    memory_shards_preview: int
    environment_type: str
    environment_message: str
    reward_multiplier: float
    offline_cap_hours: int
    prestige_min_floor: int
    prestige_cooldown_days: int

    def to_dict(self) -> dict:
        return asdict(self)


def build_game_overview(
    *,
    level: int,
    current_exp: int,
    calories: float,
    target_calories: float,
    workout_minutes: float,
    target_workout_minutes: float,
    water_liters: float,
    target_water_liters: float,
    streak_days: int,
    sleep_score: float | None = None,
    stress_score: float | None = None,
) -> GameOverview:
    """Build a deterministic, non-punitive overview from existing health data.

    Sleep and stress integrations are not available in the current MVP. Missing
    domains receive a neutral score and lower the confidence label instead of
    silently pretending that measurements exist.
    """
    activity = _score(workout_minutes / max(target_workout_minutes, 1) * 100)
    nutrition = _score(100 - abs(calories - target_calories) / max(target_calories, 1) * 100)
    hydration = _score(water_liters / max(target_water_liters, 0.1) * 100)
    consistency = _score(streak_days / 7 * 100)

    measured = [activity, nutrition]
    if sleep_score is not None:
        measured.append(sleep_score)
    if stress_score is not None:
        measured.append(stress_score)
    confidence = "HIGH" if len(measured) == 4 else "PARTIAL"

    # Until sleep/stress integrations arrive, hydration and consistency are
    # visible MVP proxies. They are returned in the breakdown so the UI can be
    # honest about what was measured.
    balance_inputs = [activity, nutrition, sleep_score if sleep_score is not None else hydration,
                      stress_score if stress_score is not None else consistency]
    hbi = calculate_hbi(balance_inputs)

    vitality = min(
        200,
        floor(activity * 0.8 + nutrition * 0.35 + hydration * 0.25 + min(streak_days, 7) * 5),
    )
    guild_coins = floor(vitality * (1.0 + hbi / 500.0))
    tower_floor = max(1, level * 3 + floor(hbi / 20))
    memory_shards = 0 if tower_floor < 30 else floor(sqrt(tower_floor) * 10 * (0.8 + hbi / 500.0))

    if level >= 100:
        stage_name = "전설 길드"
    elif level >= 50:
        stage_name = "유명 길드"
    elif level >= 30:
        stage_name = "모험가 길드"
    elif level >= 10:
        stage_name = "견습 길드"
    else:
        stage_name = "작은 캠프"

    if hbi >= 80:
        environment = "STARLIGHT_GROVE"
        environment_message = "별빛 정원이 열리고 희귀 정령의 흔적이 보여요."
        multiplier = 1.15
    elif hbi >= 60:
        environment = "SUNLIT_PATH"
        environment_message = "햇살길이 열렸어요. 균형 잡힌 하루가 길드를 밝힙니다."
        multiplier = 1.08
    elif hbi >= 40:
        environment = "QUIET_FOREST"
        environment_message = "고요한 숲에서 천천히 다음 모험을 준비하고 있어요."
        multiplier = 1.03
    else:
        environment = "RESTING_MIST"
        environment_message = "회복의 안개가 길드를 감싸고 있어요. 쉬어도 성장은 사라지지 않아요."
        multiplier = 1.0

    return GameOverview(
        hbi_score=hbi,
        hbi_confidence=confidence,
        health_breakdown={
            "activity": round(activity, 1),
            "nutrition": round(nutrition, 1),
            "hydration_proxy": round(hydration, 1),
            "consistency_proxy": round(consistency, 1),
        },
        guild_level=max(level, 1),
        guild_stage_name=stage_name,
        tower_floor=tower_floor,
        vitality=vitality,
        guild_coins=guild_coins,
        memory_shards_preview=memory_shards,
        environment_type=environment,
        environment_message=environment_message,
        reward_multiplier=multiplier,
        offline_cap_hours=12,
        prestige_min_floor=30,
        prestige_cooldown_days=7,
    )
