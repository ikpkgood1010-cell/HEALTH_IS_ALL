-- HEALTH IS ALL Database Schema Migration Script
-- SSOT Standard: exp_points, health_i_id
--
-- 2026-08 갱신: backend/database.py (SQLAlchemy 모델)를 단일 소스로 삼아
-- 실제 실행 코드와 정확히 일치하도록 재작성했다. 참고:
--   - init_db()가 Base.metadata.create_all()로 앱 시작 시 테이블을 자동
--     생성하므로, 이 SQL은 필수는 아니다 (Postgres initdb 스크립트로
--     마운트되어 컨테이너 최초 기동 시 한 번 실행되는 보조 스크립트).
--   - 타임스탬프는 SQLAlchemy가 naive UTC(datetime.now(timezone.utc)
--     .replace(tzinfo=None))로 저장하므로, 여기서도 TIMESTAMP
--     (WITHOUT TIME ZONE)로 맞췄다. WITH TIME ZONE으로 두면 두 소스가
--     서로 다른 타입 가정을 하게 되어 향후 tz-aware 마이그레이션 시
--     혼동의 원인이 된다.
--   - workout_logs / meal_logs 테이블은 실제로는 사용되지 않는다.
--     PATCH_008부터 모든 활동(식사/운동/수분/습관)은 범용 activity_logs
--     테이블 하나에 record_type으로 구분되어 기록된다. meal_logs는
--     구버전 호환을 위해 테이블 정의만 남겨두었다 (앱 코드는 참조하지
--     않음). workout_logs는 애초에 SQLAlchemy 모델에 존재한 적이 없어
--     제거했다.

CREATE TABLE IF NOT EXISTS health_i_profiles (
health_i_id VARCHAR(36) PRIMARY KEY,
user_id VARCHAR(36) UNIQUE NOT NULL,
nickname VARCHAR(50) DEFAULT '건강이' NOT NULL,
level INT DEFAULT 1 NOT NULL,
current_exp INT DEFAULT 0 NOT NULL,
equipped_skin_id VARCHAR(50) DEFAULT 'default_skin' NOT NULL,
emotion_state VARCHAR(30) DEFAULT '평온함' NOT NULL,
created_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc') NOT NULL,
updated_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc') NOT NULL
);

CREATE TABLE IF NOT EXISTS user_exp_logs (
log_id VARCHAR(36) PRIMARY KEY,
user_id VARCHAR(36) NOT NULL,
action_type VARCHAR(50) NOT NULL,
exp_gained INT NOT NULL,
daily_accumulated_exp INT NOT NULL,
created_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc') NOT NULL
);

-- 구버전 호환용 보조 테이블 (실제 앱 코드는 activity_logs를 사용).
CREATE TABLE IF NOT EXISTS meal_logs (
meal_id VARCHAR(36) PRIMARY KEY,
user_id VARCHAR(36) NOT NULL,
meal_type VARCHAR(20) NOT NULL,
calories DOUBLE PRECISION NOT NULL,
carbs DOUBLE PRECISION,
protein DOUBLE PRECISION,
fat DOUBLE PRECISION,
logged_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc') NOT NULL
);

-- PATCH_008 신규: 식사/운동/수분/습관 등 모든 활동을 통합 기록하는
-- 범용 테이블. backend/database.py의 ActivityLogModel과 1:1 대응.
CREATE TABLE IF NOT EXISTS activity_logs (
activity_id VARCHAR(36) PRIMARY KEY,
user_id VARCHAR(36) NOT NULL,
record_type VARCHAR(30) NOT NULL,
value DOUBLE PRECISION DEFAULT 0.0 NOT NULL,
detail_json VARCHAR(2000),
exp_gained INT DEFAULT 0 NOT NULL,
logged_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc') NOT NULL
);

-- Index Setups for High Performance
CREATE INDEX IF NOT EXISTS idx_health_i_user ON health_i_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_exp_logs_user_date ON user_exp_logs(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_meal_logs_user ON meal_logs(user_id, logged_at);
CREATE INDEX IF NOT EXISTS idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_type ON activity_logs(record_type);
CREATE INDEX IF NOT EXISTS idx_activity_logs_logged_at ON activity_logs(logged_at);
