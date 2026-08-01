Database Schema Master (PostgreSQL DDL)

1. 기본 원칙 (SSOT & Dual-Excellence)
• 경험치는 exp_points (Exp. 표기 연동)로 저장한다.
• 정령 및 파트너 캐릭터 정보는 health_i_profiles 및 **health_i_states**로 통합 관리한다.
• 건강 기록 테이블(식단, 운동, 습관)과 게임 보상 테이블은 분리되어 데이터 독립성을 유지한다.

───

2. 핵심 테이블 구조

2.1 건강이 프로필 및 상태 (health_i_profiles)
sql
CREATE TABLE health_i_profiles (
    health_i_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL UNIQUE,
    nickname VARCHAR(50) DEFAULT '건강이',
    level INT DEFAULT 1,
    current_exp INT DEFAULT 0,
    equipped_skin_id VARCHAR(50) DEFAULT 'default_skin',
    emotion_state VARCHAR(30) DEFAULT '평온함',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


2.2 Exp. 획득 및 사용 이력 (user_exp_logs)
sql
CREATE TABLE user_exp_logs (
    log_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    action_type VARCHAR(50) NOT NULL, -- meal_log, workout_log, habit_complete
    exp_gained INT NOT NULL,
    daily_accumulated_exp INT NOT NULL, -- 당일 누적 Exp. (상한선 300 관리)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


2.3 건강 데이터: 식단 기록 (meal_logs)
sql
CREATE TABLE meal_logs (
    meal_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    meal_type VARCHAR(20) NOT NULL, -- breakfast, lunch, dinner, snack
    calories FLOAT NOT NULL,
    carbs FLOAT,
    protein FLOAT,
    fat FLOAT,
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


2.4 건강 데이터: 운동 기록 (workout_logs)
sql
CREATE TABLE workout_logs (
    workout_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    workout_type VARCHAR(50) NOT NULL,
    duration_minutes INT NOT NULL,
    calories_burned FLOAT NOT NULL,
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);