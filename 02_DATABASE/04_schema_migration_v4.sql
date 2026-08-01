-- File Path: HEALTH IS ALL/02_DATABASE/04_schema_migration_v4.sql
-- Description: 동적 계산식 기록 및 클린 식단/회복 데이터 저장을 위한 DB 마이그레이션 V4

BEGIN;

-- 동적 수식 로그 테이블 생성
CREATE TABLE IF NOT EXISTS dynamic_formula_logs (
    log_id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    formula_version VARCHAR(16) NOT NULL,
    input_variables JSONB NOT NULL,
    calculated_result NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 클린 식단 및 회복 지수 확장 컬럼 추가
ALTER TABLE user_health_profiles 
ADD COLUMN IF NOT EXISTS clean_diet_streak INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS recovery_index NUMERIC(5, 2) DEFAULT 100.00,
ADD COLUMN IF NOT EXISTS last_activity_type VARCHAR(64);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_dynamic_formula_user_id ON dynamic_formula_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_health_profiles_streak ON user_health_profiles(clean_diet_streak);

COMMIT;