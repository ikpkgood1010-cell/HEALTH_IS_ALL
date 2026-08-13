-- Rolling automatic-battle state and idempotent settlement audit.
-- Manual apply only after the canonical idle-game migration, backup, and approval.
ALTER TABLE game_profiles
    ADD COLUMN battle_anchor_at TIMESTAMP,
    ADD COLUMN battle_progress_seconds DOUBLE PRECISION NOT NULL DEFAULT 0
        CHECK (battle_progress_seconds >= 0);

ALTER TABLE game_rebirth_logs
    ADD COLUMN star_shards_earned INTEGER NOT NULL DEFAULT 0
        CHECK (star_shards_earned >= 0);

CREATE TABLE game_battle_settlements (
    settlement_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    elapsed_seconds INTEGER NOT NULL CHECK (elapsed_seconds >= 0),
    credited_seconds INTEGER NOT NULL CHECK (credited_seconds >= 0),
    rooms_cleared INTEGER NOT NULL CHECK (rooms_cleared >= 0),
    bosses_cleared INTEGER NOT NULL CHECK (bosses_cleared >= 0),
    gold_earned INTEGER NOT NULL CHECK (gold_earned >= 0),
    result_json TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT game_battle_settlements_profile_fk FOREIGN KEY (user_id)
        REFERENCES game_profiles(user_id) ON DELETE RESTRICT
);

CREATE INDEX ix_game_battle_settlements_user_created
    ON game_battle_settlements(user_id, created_at DESC);
