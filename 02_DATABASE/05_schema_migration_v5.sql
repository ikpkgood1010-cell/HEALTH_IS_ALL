-- HEALTH IS ALL DATABASE SCHEMA MIGRATION V5
-- Migration Date: 2026-07-31
-- Description: Dynamic formula metrics, Spirit evolution states, and granular meal macro logs.

BEGIN TRANSACTION;

-- 1. Dynamic Health Log Table (Multi-Variable Support)
CREATE TABLE IF NOT EXISTS user_health_dynamic_logs (
    log_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    recorded_date DATE NOT NULL,
    weight_kg DECIMAL(5, 2) NOT NULL,
    height_cm DECIMAL(5, 2) NOT NULL,
    daily_steps INT DEFAULT 0,
    active_workout_minutes INT DEFAULT 0,
    hrv_ms DECIMAL(6, 2) NULL,
    baseline_hrv_ms DECIMAL(6, 2) NULL,
    sleep_quality_score DECIMAL(4, 1) NULL,
    calculated_bmr DECIMAL(7, 2) NOT NULL,
    calculated_tdee DECIMAL(7, 2) NOT NULL,
    calculation_mode VARCHAR(30) DEFAULT 'PRECISION_MODE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Index for daily query optimization
CREATE INDEX IF NOT EXISTS idx_user_health_date ON user_health_dynamic_logs(user_id, recorded_date);

-- 2. Spirit Evolution Table Upgrade
CREATE TABLE IF NOT EXISTS spirit_evolution_logs (
    evolution_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    current_stage INT DEFAULT 0,
    element_type VARCHAR(20) DEFAULT 'NEUTRAL',
    total_exp INT DEFAULT 0,
    affinity_score INT DEFAULT 1,
    catalyst_inventory JSON NULL,
    last_evolved_at TIMESTAMP NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Index for spirit lookup
CREATE INDEX IF NOT EXISTS idx_spirit_user ON spirit_evolution_logs(user_id);

COMMIT;