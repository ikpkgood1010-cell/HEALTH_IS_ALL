-- [중복문서-덮어쓰기, 교체] Database Schema Migration V3
-- Purpose: 다변수 동적 계산식 결과, 정령 진화 촉매 데이터, 길드 협력 미션 저장을 위한 스키마 확장.
-- SSOT: 데이터베이스 구조 정의의 표준.

BEGIN TRANSACTION;

-- 1. 사용자 동적 상태 및 연속 달성 테이블 확장
CREATE TABLE IF NOT EXISTS user_dynamic_states (
    user_id TEXT PRIMARY KEY,
    streak_days INTEGER DEFAULT 0,
    fatigue_index REAL DEFAULT 0.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 정령 촉매 및 진화 이력 테이블
CREATE TABLE IF NOT EXISTS spirit_evolution_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    spirit_tier INTEGER NOT NULL,
    clean_diet_score REAL NOT NULL,
    resonance_bonus INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 길드(VMTC) 미션 기여도 테이블
CREATE TABLE IF NOT EXISTS guild_contributions (
    contribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    activity_points REAL NOT NULL,
    recorded_date TEXT NOT NULL
);

COMMIT;

-- Related Documents:
-- - HEALTH IS ALL/02_DATABASE/DATABASE_01_CORE.md
-- Change History:
-- - v3.0 (2026-07-31): 동적 상태, 정령 촉매, 길드 기여도 테이블 추가