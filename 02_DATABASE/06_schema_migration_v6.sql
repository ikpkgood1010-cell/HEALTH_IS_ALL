-- 파일 저장 경로: HEALTH IS ALL/02_DATABASE/06_schema_migration_v6.sql
-- SSOT: HEALTH IS ALL/02_DATABASE/06_schema_migration_v6.sql
-- Related Documents: HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V6_SPEC.md
-- Change History: Patch 006 V6 마이그레이션 스크립트 작성

BEGIN TRANSACTION;

-- 1. 일일 건강 기록 테이블에 V6 동적 변수 칼럼 추가
ALTER TABLE daily_health_logs ADD COLUMN hrv_norm REAL DEFAULT 0.5;
ALTER TABLE daily_health_logs ADD COLUMN sleep_hours REAL DEFAULT 7.0;
ALTER TABLE daily_health_logs ADD COLUMN bmr_dynamic REAL DEFAULT 0.0;
ALTER TABLE daily_health_logs ADD COLUMN tdee_dynamic REAL DEFAULT 0.0;

-- 2. 정령 상호작용 로그 테이블 신설
CREATE TABLE IF NOT EXISTS spirit_interaction_logs_v6 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    interaction_type TEXT NOT NULL,
    balance_score REAL NOT NULL,
    exp_gained INTEGER NOT NULL,
    is_fallback INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 스키마 버전 기록 업데이트
INSERT INTO schema_migrations (version, applied_at) 
VALUES ('6.0.0', CURRENT_TIMESTAMP);

COMMIT;