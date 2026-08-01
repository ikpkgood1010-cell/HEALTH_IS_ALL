[코드 다운로드: 08_schema_migration_v8.sql]
[코드 복사]
<!-- 여기부터 복사 -->
-- Purpose: Dynamic Formula Registry V8 및 건강-게임 듀얼 밸런스 이력을 저장하기 위한 데이터베이스 스키마 마이그레이션 v8.
-- Scope: health_formula_logs, spirit_synergy_logs 테이블 생성 및 신규 인덱스 추가.
-- SSOT: HEALTH IS ALL/02_DATABASE/08_schema_migration_v8.sql
-- Related Documents: HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md
-- Change History: 2026-07-31 - v8 스키마 신규 제정.

BEGIN TRANSACTION;

-- 1. dynamic_formula 연산 이력 및 폴백 트래킹 테이블
CREATE TABLE IF NOT EXISTS health_formula_logs (
    log_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    formula_tier VARCHAR(20) NOT NULL, -- 'Tier-2 Dynamic' OR 'Tier-1 Simple'
    calculated_score NUMERIC(5, 2) NOT NULL,
    fallback_reason TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. 식단-정령 시너지 및 다변수 수식 로그 테이블
CREATE TABLE IF NOT EXISTS spirit_synergy_logs (
    synergy_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    calories NUMERIC(7, 2) NOT NULL,
    synergy_multiplier NUMERIC(4, 2) NOT NULL,
    earned_exp NUMERIC(8, 2) NOT NULL,
    spirit_mood VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. 빠른 조회를 위한 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_formula_logs_user_date ON health_formula_logs(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_synergy_logs_user_date ON spirit_synergy_logs(user_id, created_at);

COMMIT;
<!-- 여기까지 복사 -->