"""Pydantic request/response models."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HealthRecordRequest(BaseModel):
    user_id: str = Field(..., examples=["user_test_001"])
    record_type: str = Field(..., examples=["meal_log"])
    value: float = Field(..., examples=[550.0])
    detail_data: Optional[Dict[str, Any]] = Field(default=None)


class HealthRecordResponse(BaseModel):
    success: bool
    record_id: str
    exp_gained: int
    current_daily_exp: int
    message: str


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
