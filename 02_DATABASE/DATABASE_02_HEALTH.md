# DATABASE_02_HEALTH

Version: 1.0

---

# Purpose

This domain manages every health-related activity performed by the Guild Master.

The Health Domain is responsible for recording activities, analyzing them, calculating Health Score, and providing structured data to other engines.

Health data is immutable whenever possible.

Derived values are calculated separately.

---

# Domain Structure

Health Domain

├── Health Activity
├── Exercise Session
├── Exercise Activity
├── Exercise Field Value
├── Meal
├── Food
├── Water
├── Sleep
├── Body Record
├── Recovery
├── Health Score History
└── Daily Summary

---

# Core Principle

Every user action becomes a Health Activity.

Examples

Exercise

Meal

Water

Sleep

Recovery

Stretching

Meditation

Walking

Future activities may be added without schema redesign.

---

# TABLE : health_activity

Purpose

Represents every health-related event.

Columns

id

account_id

activity_type

started_at

ended_at

source

status

created_at

updated_at

Rules

Every activity has one type.

Activities are immutable after completion except administrator correction.

Relationships

One Health Activity

↓

One Exercise Session (optional)

One Meal (optional)

One Sleep Record (optional)

One Water Record (optional)

---

# TABLE : exercise_session

Purpose

Represents one workout session.

A session may contain multiple exercise activities.

Columns

id

health_activity_id

started_at

ended_at

duration_seconds

location_type

gps_enabled

memo

weather_snapshot

created_at

---

# TABLE : exercise_activity

Purpose

Represents one exercise inside a session.

Columns

id

exercise_session_id

exercise_master_id

display_order

started_at

ended_at

duration_seconds

calories

average_heart_rate

max_heart_rate

created_at

---

# TABLE : exercise_field_value

Purpose

Stores dynamic exercise input values.

Columns

id

exercise_activity_id

field_master_id

value_text

value_number

value_boolean

value_datetime

unit

created_at

Rules

Only one value type may be populated per row.

The field definition determines which value column is used.

---

# TABLE : body_record

Purpose

Stores body measurements.

Columns

id

account_id

weight

body_fat_percentage

skeletal_muscle_mass

bmi

height

recorded_at

---

# TABLE : water_record

Purpose

Stores water intake.

Columns

id

health_activity_id

amount_ml

recorded_at

---

# TABLE : sleep_record

Purpose

Stores sleep information.

Columns

id

health_activity_id

sleep_start

sleep_end

duration_minutes

quality_score

---

# TABLE : recovery_record

Purpose

Stores recovery activities.

Examples

Stretching

Massage

Foam Rolling

Meditation

Sauna

Cold Bath

---

# TABLE : health_score_history

Purpose

Stores Health Score changes.

Columns

id

account_id

score_before

score_after

reason

engine_version

calculated_at

---

# TABLE : daily_summary

Purpose

Stores aggregated daily values.

Columns

id

account_id

date

exercise_minutes

calories

steps

water_ml

sleep_minutes

health_score

exp

created_at

Rules

Generated automatically.

Never manually edited.

---

# Consistency Checklist

Must remain consistent with

ENGINE_OVERVIEW.md

EXERCISE_ENGINE.md

MASTER_DATA.md

ENGINE_RULES.md

Conflict Status

None
