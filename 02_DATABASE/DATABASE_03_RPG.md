# DATABASE_03_RPG

Version: 1.0

---

# Purpose

This database stores long-term progression data that motivates healthy habit formation.

These systems visualize personal growth and are always subordinate to the Health Engine.

---

# Domain Structure

Progression

├── Player Profile
├── Level
├── Experience
├── Points
├── Companion
├── Companion Trust
├── Equipment
├── Equipment History
├── Titles
├── Achievements
├── Tower Progress
├── Quest Progress

---

# TABLE : player_progress

Purpose

Stores long-term player progression.

Columns

id

account_id

level

current_exp

total_exp

points

health_habit_grade

created_at

updated_at

Rules

One record per account.

---

# TABLE : companion

Purpose

Stores companion information.

Columns

id

account_id

companion_master_id

nickname

current_trust

trust_level

appearance_version

created_at

---

# TABLE : equipment

Purpose

Stores cosmetic equipment owned by the player.

Columns

id

account_id

equipment_master_id

status

obtained_at

equipped_at

Rules

Equipment never increases health score.

Equipment may visually evolve based on long-term activity.

---

# TABLE : equipment_history

Purpose

Stores equipment changes.

Columns

id

equipment_id

change_type

before_state

after_state

reason

created_at

---

# TABLE : achievement_progress

Purpose

Stores achievement progress.

Columns

id

account_id

achievement_master_id

progress

completed

completed_at

---

# TABLE : title_unlock

Purpose

Stores unlocked titles.

Columns

id

account_id

title_master_id

is_equipped

unlocked_at

---

# TABLE : tower_progress

Purpose

Stores tower progression.

Columns

id

account_id

current_floor

highest_floor

last_cleared_at

---

# TABLE : quest_progress

Purpose

Stores mission progress.

Columns

id

account_id

quest_master_id

status

progress

completed_at

---

# Consistency Checklist

Must remain consistent with:

HEALTH_ENGINE.md

PROGRESSION_ENGINE.md

QUEST_ENGINE.md

MASTER_DATA.md

Conflict Status

None
