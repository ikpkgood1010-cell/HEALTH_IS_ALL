# Database Migration Safety Audit

## 위험 요약

- V3와 V6는 SQLite `AUTOINCREMENT`를 사용해 PostgreSQL/Supabase에 CONFLICT다.
- V4는 `user_health_profiles`, V6는 `daily_health_logs`와 `schema_migrations`를 전제하지만 현재 ORM baseline에 없다.
- V5는 `users(user_id)`를 참조하지만 V2의 `users` primary key는 `id`다.
- 감사된 SQL에는 DROP, DELETE, TRUNCATE, 또는 데이터 UPDATE 구문은 없다. 그러나 CREATE/ALTER/INSERT의 선행조건 충돌은 적용을 막는다.

## Current baseline

ORM startup previously created `health_i_profiles`, `user_exp_logs`, `meal_logs`, and `activity_logs`. `migration_runner.py --dry-run` only lists files and has no applied-migration tracking or execution path. Therefore no SQL file is safe to apply without baseline comparison.

| SQL file | Purpose/target | Risk | Decision |
| --- | --- | --- | --- |
| `01_schema_migration.sql` | Creates four ORM-overlapping tables plus indexes | CREATE/INDEX; column/default comparison required | BASELINE_REQUIRED |
| `02_schema_migration.sql` | Creates users, masters, progression, rewards | CREATE/INDEX | APPLY_CANDIDATE only after baseline approval |
| `03_schema_migration_v3.sql` | Dynamic state/evolution/guild tables | CREATE; SQLite AUTOINCREMENT | CONFLICT |
| `04_schema_migration_v4.sql` | Formula log and alters user_health_profiles | CREATE/ALTER/INDEX; prerequisite absent | CONFLICT |
| `05_schema_migration_v5.sql` | Health dynamic/evolution tables | CREATE/INDEX; FK references users(user_id) mismatch | CONFLICT |
| `06_schema_migration_v6.sql` | Alters logs and inserts tracking version | ALTER/CREATE/INSERT; SQLite syntax and prerequisites absent | CONFLICT |
| `07_schema_migration_v7.sql` | Telemetry and guild tables | CREATE/INDEX | APPLY_CANDIDATE only after baseline approval |
| `08_schema_migration_v8.sql` | Formula/synergy tables | CREATE/INDEX | APPLY_CANDIDATE only after baseline approval |

No file is an APPLY_CANDIDATE until each CREATE/ALTER/INSERT/DROP/DELETE/UPDATE statement is reconciled against the live schema. Any DROP, DELETE, UPDATE, or destructive ALTER must be treated as CONFLICT until explicitly approved.
