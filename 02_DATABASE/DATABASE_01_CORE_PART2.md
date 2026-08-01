# DATABASE_01_CORE (Part 2)

Version: 1.0

---

# Purpose

This document defines all user-facing profile and preference tables.

These tables contain information related to personalization only.

Authentication data must never be stored here.

---

# TABLE : user_profile

## Purpose

Stores the public identity of the Guild Master.

Every account owns exactly one profile.

---

## Responsibilities

- Display profile information
- RPG identity
- Leaderboard information
- Social information

---

## Columns

id (UUID)

account_id (FK)

nickname

avatar_id

current_title_id

guild_name

country_code

language_code

timezone

bio

birthday

gender (optional)

created_at

updated_at

deleted_at

---

## Constraints

Nickname must be unique.

Nickname length

3~20 characters

Guild name optional.

Birthday optional.

---

## Indexes

nickname (Unique)

account_id

country_code

---

## Relationships

1 Account

↓

1 User Profile

↓

1 Avatar

↓

1 Current Title

---

## Business Rules

Nickname changes are limited.

Leaderboard always uses nickname.

Real name is never displayed.

---

## Example Data

Nickname

TowerWalker

Language

ko-KR

Timezone

Asia/Seoul

---

## API Usage

GET /profile

PATCH /profile

GET /leaderboard

---

## Future Expansion

Profile themes

Animated profile

Background customization

Social badges

---

# TABLE : user_setting

## Purpose

Stores user preferences.

---

## Responsibilities

- Theme
- Units
- Accessibility
- Privacy

---

## Columns

id

account_id

theme

language

distance_unit

weight_unit

energy_unit

first_day_of_week

is_dark_mode

accessibility_font_scale

created_at

updated_at

---

## Constraints

One setting per account.

---

## Business Rules

Changing settings must not affect historical data.

---

## API Usage

GET /settings

PATCH /settings

---

# TABLE : notification_preference

## Purpose

Stores all notification preferences.

---

## Columns

id

account_id

exercise_reminder

meal_reminder

quest_notification

tower_notification

leaderboard_notification

event_notification

marketing_notification

created_at

updated_at

---

## Business Rules

All notifications are opt-in except critical security notifications.

---

## API Usage

PATCH /notifications

GET /notifications

---

# TABLE : user_statistics

## Purpose

Stores frequently accessed aggregated values.

These values are derived from other domains.

This table exists only for performance.

---

## Columns

id

account_id

total_exercises

total_exercise_time

total_steps

total_calories_burned

total_tower_floor

current_level

current_exp

health_score

trust_level

last_exercise_at

updated_at

---

## Business Rules

Never update manually.

Updated by background workers.

Used for dashboard and leaderboard.

---

## API Usage

GET /dashboard

GET /leaderboard

---

# TABLE : user_avatar

## Purpose

Stores avatar ownership.

---

## Columns

id

account_id

avatar_master_id

obtained_at

is_equipped

---

## Business Rules

Multiple avatars may be owned.

Only one avatar may be equipped.

---

# TABLE : user_title

## Purpose

Stores title ownership.

---

## Columns

id

account_id

title_master_id

obtained_at

is_equipped

---

## Business Rules

Titles are permanent rewards.

Only one title can be equipped.

---

# Related Domains

RPG

Leaderboard

Quest

Achievement

Reward

Health

---

# Security

No authentication information belongs here.

No password.

No token.

No login history.

---

# Future Expansion

Public profile sharing

Friend profile

Guild profile

Streaming profile

Creator profile

---

# Consistency Checklist

Must remain consistent with

DATABASE_00_OVERVIEW.md

DATABASE_01_CORE.md

MASTER_DATA.md

ENGINE_RULES.md

PRODUCT_VISION.md

Conflict Status

None
