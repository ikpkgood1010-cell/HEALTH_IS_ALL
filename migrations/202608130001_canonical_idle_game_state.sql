-- Canonical idle-game persistence. Manual apply only after backup and approval.
CREATE TABLE game_profiles (
    user_id VARCHAR(36) PRIMARY KEY,
    tower_floor INTEGER NOT NULL DEFAULT 1 CHECK (tower_floor >= 1),
    highest_floor INTEGER NOT NULL DEFAULT 1 CHECK (highest_floor >= 1),
    room_position INTEGER NOT NULL DEFAULT 1 CHECK (room_position BETWEEN 1 AND 6),
    gold INTEGER NOT NULL DEFAULT 0 CHECK (gold >= 0),
    run_number INTEGER NOT NULL DEFAULT 1 CHECK (run_number >= 1),
    health_essence INTEGER NOT NULL DEFAULT 0 CHECK (health_essence >= 0),
    star_shards INTEGER NOT NULL DEFAULT 0 CHECK (star_shards >= 0),
    transcendence_points INTEGER NOT NULL DEFAULT 0 CHECK (transcendence_points >= 0),
    revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE game_heroes (
    user_id VARCHAR(36) NOT NULL,
    hero_code VARCHAR(30) NOT NULL,
    role_name VARCHAR(20) NOT NULL,
    recruited BOOLEAN NOT NULL DEFAULT FALSE,
    advancement_tier INTEGER NOT NULL DEFAULT 0 CHECK (advancement_tier BETWEEN 0 AND 6),
    appearance_code VARCHAR(50) NOT NULL DEFAULT 'BASE',
    active_skill_slots INTEGER NOT NULL DEFAULT 0 CHECK (active_skill_slots BETWEEN 0 AND 6),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, hero_code),
    CONSTRAINT game_heroes_profile_fk FOREIGN KEY (user_id)
        REFERENCES game_profiles(user_id) ON DELETE CASCADE
);

CREATE TABLE game_constellation_nodes (
    user_id VARCHAR(36) NOT NULL,
    node_code VARCHAR(80) NOT NULL,
    layer INTEGER NOT NULL CHECK (layer BETWEEN 0 AND 6),
    node_size VARCHAR(10) NOT NULL CHECK (node_size IN ('SMALL', 'MEDIUM', 'LARGE')),
    hero_code VARCHAR(30),
    unlocked_run_number INTEGER NOT NULL CHECK (unlocked_run_number >= 1),
    unlocked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, node_code),
    CONSTRAINT game_nodes_profile_fk FOREIGN KEY (user_id)
        REFERENCES game_profiles(user_id) ON DELETE CASCADE,
    CONSTRAINT game_nodes_hero_fk FOREIGN KEY (user_id, hero_code)
        REFERENCES game_heroes(user_id, hero_code) ON DELETE CASCADE,
    CONSTRAINT game_large_node_hero_required CHECK (
        node_size <> 'LARGE' OR hero_code IS NOT NULL
    )
);

CREATE TABLE game_rebirth_logs (
    rebirth_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    from_run_number INTEGER NOT NULL CHECK (from_run_number >= 1),
    to_run_number INTEGER NOT NULL CHECK (to_run_number = from_run_number + 1),
    previous_highest_floor INTEGER NOT NULL CHECK (previous_highest_floor >= 1),
    reset_small_nodes INTEGER NOT NULL CHECK (reset_small_nodes >= 0),
    reset_medium_nodes INTEGER NOT NULL CHECK (reset_medium_nodes >= 0),
    retained_snapshot_json TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT game_rebirth_profile_fk FOREIGN KEY (user_id)
        REFERENCES game_profiles(user_id) ON DELETE RESTRICT
);

CREATE INDEX ix_game_constellation_nodes_user_size
    ON game_constellation_nodes(user_id, node_size);
CREATE INDEX ix_game_rebirth_logs_user_created
    ON game_rebirth_logs(user_id, created_at DESC);
