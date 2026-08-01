-- HEALTH IS ALL Database Schema Migration V7
-- Description: V8 Multi-variable Telemetry and Guild Synergy Logging Tables

BEGIN;

-- 1. 다변수 건강 계산 로그 테이블
CREATE TABLE IF NOT EXISTS health_telemetry_logs_v7 (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    activity_type VARCHAR(32) NOT NULL,
    raw_calories DOUBLE PRECISION NOT NULL,
    precision_calories DOUBLE PRECISION NOT NULL,
    heart_rate_avg INT,
    sleep_score INT,
    formula_used VARCHAR(32) NOT NULL, -- 'PRECISION_V8' or 'FALLBACK_V1'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. 길드 레이드 시너지 기여도 테이블
CREATE TABLE IF NOT EXISTS guild_synergy_contributions_v7 (
    id BIGSERIAL PRIMARY KEY,
    guild_id VARCHAR(64) NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    health_score_contribution DOUBLE PRECISION NOT NULL,
    synergy_multiplier DOUBLE PRECISION DEFAULT 1.0,
    logged_date DATE NOT NULL,
    UNIQUE(guild_id, user_id, logged_date)
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_telemetry_user_date ON health_telemetry_logs_v7(user_id, calculated_at);
CREATE INDEX IF NOT EXISTS idx_guild_synergy_guild ON guild_synergy_contributions_v7(guild_id, logged_date);

COMMIT;