-- Bounded, auditable health-record rewards for permanent health essence.
-- Manual apply only after backup, schema preflight, and explicit approval.
CREATE TABLE game_health_rewards (
    activity_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    record_type VARCHAR(30) NOT NULL,
    health_essence_earned INTEGER NOT NULL DEFAULT 0
        CHECK (health_essence_earned BETWEEN 0 AND 8),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT game_health_rewards_activity_fk FOREIGN KEY (activity_id)
        REFERENCES activity_logs(activity_id) ON DELETE RESTRICT,
    CONSTRAINT game_health_rewards_profile_fk FOREIGN KEY (user_id)
        REFERENCES game_profiles(user_id) ON DELETE RESTRICT
);

CREATE INDEX ix_game_health_rewards_user_created
    ON game_health_rewards(user_id, created_at DESC);
