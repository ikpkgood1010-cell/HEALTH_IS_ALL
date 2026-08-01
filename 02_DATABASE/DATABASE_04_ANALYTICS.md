# DATABASE_04_ANALYTICS

Version: 1.0

---

# Purpose

This database stores aggregated analytics data for dashboards, reports, AI coaching, and long-term trend analysis.

Raw activity data must remain in operational databases.

Analytics tables store derived and summarized information.

---

# Design Principles

Analytics data must:

- Never replace source data.
- Be reproducible from source records.
- Support historical trend analysis.
- Be optimized for read performance.
- Be independent from UI implementation.

---

# TABLE : daily_health_summary

Purpose

Stores daily aggregated health metrics.

Columns

id

account_id

summary_date

health_score

exercise_score

habit_score

recovery_score

sleep_score

nutrition_score

hydration_score

steps

exercise_minutes

active_calories

created_at

updated_at

---

# TABLE : weekly_health_summary

Purpose

Stores weekly aggregated metrics.

Columns

id

account_id

week_start

week_end

average_health_score

exercise_days

habit_completion_rate

average_sleep_hours

average_hydration

average_nutrition_score

created_at

updated_at

---

# TABLE : monthly_health_summary

Purpose

Stores monthly health trends.

Columns

id

account_id

month

average_health_score

best_health_score

habit_consistency

exercise_frequency

recovery_index

created_at

updated_at

---

# TABLE : analytics_insight

Purpose

Stores generated analytics insights.

Columns

id

account_id

insight_type

title

summary

confidence_score

generated_by

generated_at

---

# TABLE : personal_best

Purpose

Stores personal best achievements.

Columns

id

account_id

category

value

unit

record_date

source_reference

created_at

---

# TABLE : analytics_job

Purpose

Stores analytics generation history.

Columns

id

job_type

target_period

status

started_at

completed_at

error_message

---

# Data Retention

Analytics summaries may be regenerated from operational data.

Generated insights should preserve historical context.

---

# Consistency Checklist

Must remain consistent with:

ANALYTICS_ENGINE.md

DATABASE_02_HEALTH.md

AI_ENGINE.md

API_SPECIFICATION.md

Conflict Status

None
