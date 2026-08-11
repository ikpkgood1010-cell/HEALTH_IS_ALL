"""FastAPI application entrypoint."""
from __future__ import annotations

from datetime import timedelta
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.ai_agent_service import HealthIAgentService
from backend.config import settings, utc_now
from backend.database import (
    ActivityLogModel,
    HealthIProfileModel,
    UserExpLogModel,
    database_configured,
    get_db,
    engine,
)
from backend.health_calculator import DynamicHealthCalculator
from backend.data_idempotency_engine import (
    DUPLICATE_RECORD_MESSAGE,
    canonical_detail_json,
    matches_health_record,
)
from backend.models import (
    AdventureClaimRequest,
    AdventureClaimResponse,
    AdventureResponse,
    AdventureSettleRequest,
    GameOverviewResponse,
    HealthIStateResponse,
    HealthRecordRequest,
    HealthRecordResponse,
    RecoveryCalculateRequest,
    RecoveryCalculateResponse,
    TrainingGroundsResponse,
)
from backend.game_balance_engine import build_game_overview
from backend.adventure_service import (
    AdventureNotFoundError,
    AdventureOwnershipError,
    adventure_window,
    claim_adventure,
    settle_adventure,
    training_grounds_status,
)
from backend.progression_engine import ProgressionEngine
from backend.recovery_calculator import (
    ConditionScore,
    TargetMuscle,
    calculate_muscle_recovery,
)


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
        .filter(
            ActivityLogModel.user_id == user_id,
            ActivityLogModel.record_type.in_(tuple(DAILY_AGGREGATE_MAP)),
        )
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


def _daily_exp_total(db: Session, user_id: str) -> int:
    today_start, _ = _today_range()
    return int(
        db.query(func.coalesce(func.sum(UserExpLogModel.exp_gained), 0))
        .filter(
            UserExpLogModel.user_id == user_id,
            UserExpLogModel.created_at >= today_start,
        )
        .scalar()
        or 0
    )


def _duplicate_health_record_response(
    db: Session,
    *,
    existing: ActivityLogModel,
    req: HealthRecordRequest,
    detail_json: str | None,
) -> HealthRecordResponse:
    if not matches_health_record(
        existing,
        user_id=req.user_id,
        record_type=req.record_type,
        value=req.value,
        detail_json=detail_json,
    ):
        raise HTTPException(
            status_code=409,
            detail="Idempotency key was already used for a different health record",
        )
    return HealthRecordResponse(
        success=True,
        record_id=existing.activity_id,
        exp_gained=existing.exp_gained,
        current_daily_exp=_daily_exp_total(db, req.user_id),
        message=DUPLICATE_RECORD_MESSAGE,
        duplicate=True,
    )


@app.get("/")
def read_root() -> dict:
    return {"message": "HEALTH IS ALL Backend Core System is Running", "version": settings.APP_VERSION}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok", "service": "HEALTH IS ALL API"}


@app.get("/readyz")
def readyz() -> dict:
    if not database_configured():
        return {"status": "not_ready", "database": "not_configured"}
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        return {"status": "not_ready", "database": "unavailable"}
    return {"status": "ready", "database": "connected"}


@app.post("/api/v1/health/record", response_model=HealthRecordResponse)
def log_health_activity(req: HealthRecordRequest, db: Session = Depends(get_db)) -> HealthRecordResponse:
    record_id = str(req.idempotency_key) if req.idempotency_key else f"act_{uuid4().hex[:12]}"
    detail_json = canonical_detail_json(req.detail_data)
    if len((detail_json or "").encode("utf-8")) > 2000:
        raise HTTPException(status_code=422, detail="detail_data is too large")

    existing_record = db.query(ActivityLogModel).filter(
        ActivityLogModel.activity_id == record_id
    ).first()
    if existing_record is not None:
        return _duplicate_health_record_response(
            db,
            existing=existing_record,
            req=req,
            detail_json=detail_json,
        )

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
        try:
            db.commit()
            db.refresh(profile)
        except IntegrityError:
            # Two first requests for one anonymous ID may race. The unique
            # user_id constraint chooses one profile; the other request reuses it.
            db.rollback()
            profile = db.query(HealthIProfileModel).filter(
                HealthIProfileModel.user_id == req.user_id
            ).one()

    current_daily_exp = _daily_exp_total(db, req.user_id)

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
            activity_id=record_id,
            user_id=req.user_id,
            record_type=req.record_type,
            value=req.value,
            detail_json=detail_json,
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

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing_record = db.query(ActivityLogModel).filter(
            ActivityLogModel.activity_id == record_id
        ).first()
        if existing_record is None:
            raise
        return _duplicate_health_record_response(
            db,
            existing=existing_record,
            req=req,
            detail_json=detail_json,
        )

    return HealthRecordResponse(
        success=True,
        record_id=record_id,
        exp_gained=exp_gained,
        current_daily_exp=int(engine_res["current_daily_exp"]),
        message=engine_res["reason"],
        duplicate=False,
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


@app.get("/api/v1/game/overview/{user_id}", response_model=GameOverviewResponse)
def get_game_overview(user_id: str, db: Session = Depends(get_db)) -> GameOverviewResponse:
    """Return a read-only game projection from the user's current health data."""
    status = get_health_i_status(user_id, db)
    overview = build_game_overview(
        level=status.level,
        current_exp=status.current_exp,
        calories=status.today_consumed_calories,
        target_calories=2000,
        workout_minutes=status.today_workout_minutes,
        target_workout_minutes=45,
        water_liters=status.today_water_liters,
        target_water_liters=2.0,
        streak_days=status.streak_days,
    )
    return GameOverviewResponse(**overview.to_dict())


@app.post("/api/v1/game/adventures/settle", response_model=AdventureResponse)
def settle_automatic_adventure(
    request: AdventureSettleRequest,
    db: Session = Depends(get_db),
) -> AdventureResponse:
    """Settle one deterministic automatic adventure per 12-hour UTC window."""
    window_start, window_end = adventure_window(utc_now())
    window_logs = db.query(ActivityLogModel).filter(
        ActivityLogModel.user_id == request.user_id,
        ActivityLogModel.record_type.in_(tuple(DAILY_AGGREGATE_MAP)),
        ActivityLogModel.logged_at >= window_start,
        ActivityLogModel.logged_at < window_end,
    ).all()
    totals = {"calories": 0.0, "minutes": 0.0, "liters": 0.0}
    for log in window_logs:
        totals[DAILY_AGGREGATE_MAP[log.record_type]] += log.value

    profile = db.query(HealthIProfileModel).filter(
        HealthIProfileModel.user_id == request.user_id
    ).first()
    overview = build_game_overview(
        level=profile.level if profile else 1,
        current_exp=profile.current_exp if profile else 0,
        calories=totals["calories"],
        target_calories=1000,
        workout_minutes=totals["minutes"],
        target_workout_minutes=22.5,
        water_liters=totals["liters"],
        target_water_liters=1.0,
        streak_days=_calc_streak_days(db, request.user_id),
    )
    result = settle_adventure(
        db,
        user_id=request.user_id,
        vitality=overview.vitality,
        hbi_score=overview.hbi_score,
        guild_coins=overview.guild_coins,
        tower_floor=overview.tower_floor,
    )
    return AdventureResponse(**result)


@app.post(
    "/api/v1/game/adventures/{adventure_id}/claim",
    response_model=AdventureClaimResponse,
)
def claim_automatic_adventure(
    adventure_id: str,
    request: AdventureClaimRequest,
    db: Session = Depends(get_db),
) -> AdventureClaimResponse:
    """Claim a settled adventure exactly once, even when a request is retried."""
    try:
        result = claim_adventure(db, user_id=request.user_id, adventure_id=adventure_id)
    except AdventureNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Adventure not found") from exc
    except AdventureOwnershipError as exc:
        raise HTTPException(status_code=403, detail="Adventure belongs to another user") from exc
    return AdventureClaimResponse(**result)


@app.get(
    "/api/v1/game/facilities/training-grounds/{user_id}",
    response_model=TrainingGroundsResponse,
)
def get_training_grounds(
    user_id: str,
    db: Session = Depends(get_db),
) -> TrainingGroundsResponse:
    return TrainingGroundsResponse(**training_grounds_status(db, user_id=user_id))


@app.post("/api/v1/recovery/calculate", response_model=RecoveryCalculateResponse)
def calculate_recovery(
    request: RecoveryCalculateRequest,
) -> RecoveryCalculateResponse:
    """Calculate recovery without writing health or game data."""
    try:
        condition = ConditionScore(request.condition.condition_score)
        results = [
            calculate_muscle_recovery(
                target_muscle=TargetMuscle(log.target_muscle),
                rpe=log.rpe,
                condition_score=condition,
                frequency_per_week=log.frequency_per_week,
                is_beginner=log.is_beginner,
                age=request.age,
                performed_at=request.performed_at,
            ).to_dict()
            for log in request.workout_logs
        ]
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return RecoveryCalculateResponse(user_id=request.user_id, results=results)
