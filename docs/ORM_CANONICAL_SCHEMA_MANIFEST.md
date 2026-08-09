# ORM Canonical Schema Manifest

`backend/database.py` is the official schema source. Existing Supabase baseline tables are `health_i_profiles`, `user_exp_logs`, `meal_logs`, and `activity_logs`.

| Table | PK | Key columns/defaults | Index/nullable baseline |
| --- | --- | --- | --- |
| health_i_profiles | health_i_id string | user_id unique; level/current_exp defaults; timestamps | user_id indexed, nullable defaults per ORM |
| user_exp_logs | log_id string | user_id, action_type, exp/daily totals, timestamp | user_id indexed |
| meal_logs | meal_id string | user_id, meal type, calories/macros, timestamp | user_id indexed; macro fields nullable |
| activity_logs | activity_id string | user_id, record_type, value, detail JSON text, exp, timestamp | user_id/record_type/logged_at indexed; detail nullable |

Any live-schema difference is drift only; it must not be changed by this WP.
