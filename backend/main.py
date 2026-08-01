"""FastAPI application entrypoint."""
from __future__ import annotations

import json
from datetime import timedelta
from uuid import uuid4

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.ai_agent_service import HealthIAgentService
from backend.config import settings, utc_now
from backend.database import (
    ActivityLogModel,
    HealthIProfileModel,
    UserExpLogModel,
    get_db,
    init_db,
)
from backend.health_calculator import DynamicHealthCalculator
from backend.models import HealthIStateResponse, HealthRecordRequest, HealthRecordResponse
from backend.progression_engine import ProgressionEngine

init_db()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="HEALTH IS ALL - Health & Gamification Backend Core API",
)

# 현재 allow_origins=["*"] 로 전체 오리진을 허용 중이다. 웹앱을
# deploy/docker-compose.web.yml 구성(같은 오리진 + nginx /api 프록시)으로
# 배포하면 브라우저 입장에서는 CORS 자체가 발생하지 않으므로 이 설정이
# 실질적으로 쓰이지 않는다. 다만 프론트를 다른 도메인에 별도 배포하거나
# 모바일 앱에서 직접 호출하는 경우에는 계속 필요하다. 프로덕션에서
# 오리진을 좁히고 싶다면 allow_origins를 실제 배포 도메인 목록으로
# 교체할 것 (allow_credentials=True와 "*"를 함께 쓰는 조합은 브라우저에
# 따라 거부될 수 있어 특히 주의).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

progression_engine = ProgressionEngine()
health_calc = DynamicHealthCalculator()
ai_agent = HealthIAgentService()

# record_type별로 ActivityLogModel.value가 어느 오늘자 집계 필드에
# 더해지는지 매핑한다. 새 활동 타입을 추가할 때 이 맵에 한 줄만
# 추가하면 오늘자 상태 집계에도 자동 반영된다 (확장 용이성 목적).
DAILY_AGGREGATE_MAP = {
    "meal_log": "calories",
    "workout_log": "minutes",
    "water_log": "liters",
}


def _today_range():
    """오늘(UTC naive) 00:00:00 ~ 내일 00:00:00 범위를 반환한다.

    SQLite/Postgres 방언 차이가 있는 func.date() 대신, Python 레벨에서
    범위를 계산해 두 DB 모두에서 동일하게 동작하도록 단순화했다.
    """
    now = utc_now()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


def _calc_streak_days(db: Session, user_id: str) -> int:
    """오늘부터 거슬러 올라가며 연속으로 활동 기록이 있는 일수를 계산한다."""
    logs = (
        db.query(ActivityLogModel.logged_at)
        .filter(ActivityLogModel.user_id == user_id)
        .order_by(ActivityLogModel.logged_at.desc())
        .all()
    )
    if not logs:
        return 0

    activity_dates = sorted({row[0].date() for row in logs}, reverse=True)
    today = utc_now().date()

    streak = 0
    expected = today
    for d in activity_dates:
        if d == expected:
            streak += 1
            expected = expected - timedelta(days=1)
        elif d < expected:
            break
    return streak


@app.get("/")
def read_root() -> dict:
    return {"message": "HEALTH IS ALL Backend Core System is Running", "version": settings.APP_VERSION}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok", "service": "HEALTH IS ALL API"}


@app.post("/api/v1/health/record", response_model=HealthRecordResponse)
def log_health_activity(req: HealthRecordRequest, db: Session = Depends(get_db)) -> HealthRecordResponse:
    profile = db.query(HealthIProfileModel).filter(HealthIProfileModel.user_id == req.user_id).first()
    if not profile:
        profile = HealthIProfileModel(
            health_i_id=f"hi_{uuid4().hex[:12]}",
            user_id=req.user_id,
            nickname=settings.SSOT_CHARACTER_NAME,
            level=1,
            current_exp=0,
            emotion_state="평온함",
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    today_start, _ = _today_range()
    current_daily_exp = (
        db.query(func.coalesce(func.sum(UserExpLogModel.exp_gained), 0))
        .filter(UserExpLogModel.user_id == req.user_id, UserExpLogModel.created_at >= today_start)
        .scalar()
    ) or 0

    latest_log = (
        db.query(UserExpLogModel)
        .filter(UserExpLogModel.user_id == req.user_id)
        .order_by(UserExpLogModel.created_at.desc())
        .first()
    )

    streak_days = _calc_streak_days(db, req.user_id)

    engine_res = progression_engine.calculate_exp_gain(
        action_type=req.record_type,
        current_daily_exp=int(current_daily_exp),
        last_action_time=latest_log.created_at if latest_log else None,
        streak_days=max(streak_days, 1),
    )

    exp_gained = int(engine_res["exp_gained"])

    # 활동 기록은 Exp 획득 여부와 무관하게 항상 activity_logs에 저장한다.
    # (안티파밍으로 Exp가 0이어도 사용자가 실제로 한 행동은 기록되어야
    #  오늘자 칼로리/운동/수분 집계가 정확하게 유지된다.)
    db.add(
        ActivityLogModel(
            activity_id=f"act_{uuid4().hex[:12]}",
            user_id=req.user_id,
            record_type=req.record_type,
            value=req.value,
            detail_json=json.dumps(req.detail_data, ensure_ascii=False) if req.detail_data else None,
            exp_gained=exp_gained,
        )
    )

    if exp_gained > 0:
        db.add(
            UserExpLogModel(
                log_id=f"log_{uuid4().hex[:12]}",
                user_id=req.user_id,
                action_type=req.record_type,
                exp_gained=exp_gained,
                daily_accumulated_exp=int(engine_res["current_daily_exp"]),
            )
        )
        profile.current_exp += exp_gained
        profile.level = (profile.current_exp // 300) + 1
        profile.updated_at = utc_now()

    db.commit()

    return HealthRecordResponse(
        success=True,
        record_id=f"rec_{uuid4().hex[:12]}",
        exp_gained=exp_gained,
        current_daily_exp=int(engine_res["current_daily_exp"]),
        message=engine_res["reason"],
    )


@app.get("/api/v1/health-i/status/{user_id}", response_model=HealthIStateResponse)
def get_health_i_status(user_id: str, db: Session = Depends(get_db)) -> HealthIStateResponse:
    profile = db.query(HealthIProfileModel).filter(HealthIProfileModel.user_id == user_id).first()
    if not profile:
        return HealthIStateResponse(
            name=settings.SSOT_CHARACTER_NAME,
            level=1,
            current_exp=0,
            daily_exp_cap=settings.DAILY_EXP_CAP,
            emotion_state="평온함",
            dialogue="오늘 하루도 차근차근 시작해볼까요?",
            equipped_skin="default_skin",
            last_updated=utc_now(),
            today_consumed_calories=0.0,
            today_workout_minutes=0.0,
            today_water_liters=0.0,
            streak_days=0,
        )

    today_start, today_end = _today_range()
    today_logs = (
        db.query(ActivityLogModel)
        .filter(
            ActivityLogModel.user_id == user_id,
            ActivityLogModel.logged_at >= today_start,
            ActivityLogModel.logged_at < today_end,
        )
        .all()
    )

    today_calories = 0.0
    today_minutes = 0.0
    today_water = 0.0
    for log in today_logs:
        field = DAILY_AGGREGATE_MAP.get(log.record_type)
        if field == "calories":
            today_calories += log.value
        elif field == "minutes":
            today_minutes += log.value
        elif field == "liters":
            today_water += log.value

    streak_days = _calc_streak_days(db, user_id)

    feedback = ai_agent.generate_feedback(
        consumed_calories=int(today_calories),
        target_calories=2000,
        workout_minutes=int(today_minutes),
        water_liters=today_water,
        streak_days=max(streak_days, 1),
    )
    return HealthIStateResponse(
        name=profile.nickname,
        level=profile.level,
        current_exp=profile.current_exp,
        daily_exp_cap=settings.DAILY_EXP_CAP,
        emotion_state=feedback["emotion_state"],
        dialogue=feedback["dialogue"],
        equipped_skin=profile.equipped_skin_id,
        last_updated=profile.updated_at,
        today_consumed_calories=today_calories,
        today_workout_minutes=today_minutes,
        today_water_liters=today_water,
        streak_days=streak_days,
    )
