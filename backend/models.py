"""Pydantic request/response models."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

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
