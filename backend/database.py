"""SQLAlchemy database setup and ORM models."""
from __future__ import annotations

from typing import Generator

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.config import settings, utc_now

engine = None
SessionLocal = None
if settings.database_url:
    engine = create_engine(settings.database_url, pool_pre_ping=True, future=True, connect_args={"sslmode": "require"})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


class HealthIProfileModel(Base):
    __tablename__ = "health_i_profiles"

    health_i_id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), unique=True, nullable=False, index=True)
    nickname = Column(String(50), default="건강이")
    level = Column(Integer, default=1)
    current_exp = Column(Integer, default=0)
    equipped_skin_id = Column(String(50), default="default_skin")
    emotion_state = Column(String(30), default="평온함")
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)


class UserExpLogModel(Base):
    __tablename__ = "user_exp_logs"

    log_id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    action_type = Column(String(50), nullable=False)
    exp_gained = Column(Integer, nullable=False)
    daily_accumulated_exp = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=utc_now)


class MealLogModel(Base):
    __tablename__ = "meal_logs"

    meal_id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    meal_type = Column(String(20), nullable=False)
    calories = Column(Float, nullable=False)
    carbs = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    logged_at = Column(DateTime, default=utc_now)


class ActivityLogModel(Base):
    """범용 활동 로그 테이블.

    식사(meal_log)/운동(workout_log)/수분(water_log)/습관(habit_complete) 등
    모든 record_type을 하나의 테이블에 통합 기록한다. 새로운 활동 타입을
    추가할 때도 이 테이블 스키마를 바꿀 필요 없이 record_type 문자열과
    detail_data(JSON 문자열)만 추가하면 되도록 설계했다 (확장 용이성 목적).
    """

    __tablename__ = "activity_logs"

    activity_id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    record_type = Column(String(30), nullable=False, index=True)
    # value의 의미는 record_type에 따라 달라진다:
    #   meal_log     -> 칼로리(kcal)
    #   workout_log  -> 운동 시간(분)
    #   water_log    -> 수분 섭취량(L)
    #   habit_complete -> 1.0(완료 플래그) 등 자유롭게 확장
    value = Column(Float, nullable=False, default=0.0)
    detail_json = Column(String(2000), nullable=True)
    exp_gained = Column(Integer, nullable=False, default=0)
    logged_at = Column(DateTime, default=utc_now, index=True)


def init_db() -> bool:
    if engine is None:
        return False
    Base.metadata.create_all(bind=engine)
    return True


def database_configured() -> bool:
    return engine is not None


def get_db() -> Generator:
    if SessionLocal is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="database is not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
