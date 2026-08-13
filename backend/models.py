"""Pydantic request/response models."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import UUID4, BaseModel, Field


class HealthRecordRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36, examples=["user_test_001"])
    record_type: Literal["meal_log", "workout_log", "water_log", "habit_complete"] = Field(
        ..., examples=["meal_log"]
    )
    value: float = Field(..., gt=0, examples=[550.0])
    detail_data: Optional[Dict[str, Any]] = Field(default=None)
    idempotency_key: Optional[UUID4] = Field(
        default=None,
        description="Client-generated UUID reused when the same record request is retried.",
    )


class HealthRecordResponse(BaseModel):
    success: bool
    record_id: str
    exp_gained: int
    current_daily_exp: int
    message: str
    duplicate: bool = False


class HealthIStateResponse(BaseModel):
    name: str = Field(default="건강이")
    level: int
    current_exp: int
    daily_exp_cap: int = Field(default=300)
    emotion_state: str
    dialogue: str
    equipped_skin: str
    last_updated: datetime
    # 오늘자 실측 집계값 (ActivityLogModel 기반). 앱이 더 이상 로컬 목업이
    # 아닌 실제 서버 데이터를 그려줄 수 있도록 상태 응답에 포함한다.
    today_consumed_calories: float = Field(default=0.0)
    today_workout_minutes: float = Field(default=0.0)
    today_water_liters: float = Field(default=0.0)
    streak_days: int = Field(default=0)


class GameOverviewResponse(BaseModel):
    hbi_score: float
    hbi_confidence: str
    health_breakdown: Dict[str, float]
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


class GameDirectionResponse(BaseModel):
    """Read-only canonical contract for the new idle game foundation."""

    official_name: str
    status: Literal["FOUNDATION"] = "FOUNDATION"
    health_tabs: List[str]
    game_entry: str
    party_roles: List[str]
    full_auto_battle: bool
    normal_rooms_per_floor: int
    boss_rooms_per_floor: int
    constellation_layers: int
    large_nodes_per_layer: int
    deterministic_spirit_hatching: bool
    random_gacha: bool
    equipment_inventory: bool
    rebirth_resets: List[str]
    rebirth_retains: List[str]


class GameInitializeRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)


class InitialHeroSelectionRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    hero_code: Literal["TANKER", "WARRIOR", "MAGE", "ARCHER", "ROGUE", "HEALER"]
    expected_revision: int = Field(..., ge=0)


class GameHeroStateResponse(BaseModel):
    hero_code: str
    role_name: str
    recruited: bool
    advancement_tier: int
    appearance_code: str
    active_skill_slots: int


class CanonicalGameStateResponse(BaseModel):
    initialized: bool
    phase: Literal["ONBOARDING", "IDLE_BATTLE"]
    user_id: str
    revision: int
    run_number: int
    tower_floor: int
    highest_floor: int
    room_position: int
    rooms_per_floor: int
    gold: int
    health_essence: int
    star_shards: int
    transcendence_points: int
    initial_hero_selected: bool
    large_node_slots_by_layer: Dict[str, int]
    heroes: List[GameHeroStateResponse]
    node_counts: Dict[str, int]


class RebirthPreviewResponse(BaseModel):
    user_id: str
    revision: int
    can_rebirth: bool
    next_run_number: int
    reset: Dict[str, int]
    retain: Dict[str, Any]


class RebirthExecuteRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    expected_revision: int = Field(..., ge=0)
    idempotency_key: UUID4
    confirm: Literal[True]


class RebirthExecuteResponse(BaseModel):
    rebirth_id: str
    already_executed: bool
    state: CanonicalGameStateResponse


class AdventureSettleRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)


class AdventureRoomResponse(BaseModel):
    position: int
    room_type: str
    title: str
    result_code: str
    result_title: str
    outcome: str


class AdventureResponse(BaseModel):
    adventure_id: str
    user_id: str
    window_start: datetime
    window_end: datetime
    vitality: int
    gross_guild_coins: int
    offline_efficiency: float
    hbi_score: float
    tower_floor: int = 1
    rooms: List[AdventureRoomResponse] = Field(default_factory=list)
    claimed: bool


class AdventureHistoryResponse(BaseModel):
    items: List[AdventureResponse] = Field(default_factory=list)


class AdventureClaimRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)


class HeroResponse(BaseModel):
    hero_code: str
    name: str
    title: str
    role: str
    element: str
    rarity: str
    join_source: str
    join_message: str
    gameplay_effect: str
    joined_at: datetime
    source_adventure_id: str


class HeroRosterResponse(BaseModel):
    items: List[HeroResponse] = Field(default_factory=list)


class AdventureClaimResponse(BaseModel):
    adventure_id: str
    claim_id: str
    already_claimed: bool
    gross_guild_coins: int
    facility_invested: int
    guild_coins_received: int
    joined_hero: Optional[HeroResponse] = None


class TrainingGroundsResponse(BaseModel):
    code: str
    name: str
    level: int
    total_invested: int
    current_level_progress: int
    next_level_cost: int
    progress_ratio: float
    guild_coin_balance: int
    description: str
    stage_code: str
    stage_name: str
    stage_message: str
    next_milestone_level: Optional[int] = None


class RecoveryConditionRequest(BaseModel):
    sleep_hours: Optional[float] = Field(default=None, alias="sleepHours", ge=0, le=24)
    condition_score: str = Field(alias="conditionScore")

    model_config = {"populate_by_name": True}


class RecoveryWorkoutLogRequest(BaseModel):
    target_muscle: str = Field(alias="targetMuscle")
    rpe: int = Field(ge=1, le=10)
    frequency_per_week: int = Field(default=1, alias="frequencyPerWeek", ge=1)
    is_beginner: bool = Field(default=False, alias="isBeginner")

    model_config = {"populate_by_name": True}


class RecoveryCalculateRequest(BaseModel):
    user_id: str = Field(alias="userId")
    performed_at: datetime = Field(alias="performedAt")
    condition: RecoveryConditionRequest
    workout_logs: List[RecoveryWorkoutLogRequest] = Field(alias="workoutLogs", min_length=1)
    age: int = Field(default=30, ge=1, le=120)

    model_config = {"populate_by_name": True}


class MuscleRecoveryResponse(BaseModel):
    target_muscle: str
    base_recovery_hours: float
    recommended_recovery_hours: float
    elapsed_hours: float
    recovery_percent: float
    status: str
    estimated_ready_at: datetime


class RecoveryCalculateResponse(BaseModel):
    user_id: str
    results: List[MuscleRecoveryResponse]
