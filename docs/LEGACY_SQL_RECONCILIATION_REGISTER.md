# Legacy SQL Reconciliation Register

| File | Decision | Reason |
| --- | --- | --- |
| 01_schema_migration.sql | REPLACED_BY_ORM_BASELINE | Recreates the four ORM baseline tables. |
| 02_schema_migration.sql | CONVERT_TO_POSTGRES_CANDIDATE | Separate users/reward domain; requires schema review. |
| 03_schema_migration_v3.sql | CONFLICT_DO_NOT_RUN | SQLite AUTOINCREMENT. |
| 04_schema_migration_v4.sql | CONFLICT_DO_NOT_RUN | Alters absent prerequisite table. |
| 05_schema_migration_v5.sql | CONFLICT_DO_NOT_RUN | FK references incompatible users key. |
| 06_schema_migration_v6.sql | CONFLICT_DO_NOT_RUN | SQLite syntax and absent prerequisites/tracking table. |
| 07_schema_migration_v7.sql | CONVERT_TO_POSTGRES_CANDIDATE | PostgreSQL-oriented new tables need baseline review. |
| 08_schema_migration_v8.sql | CONVERT_TO_POSTGRES_CANDIDATE | PostgreSQL-oriented new tables need baseline review. |
