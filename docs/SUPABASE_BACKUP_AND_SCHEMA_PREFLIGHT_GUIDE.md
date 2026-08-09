# Supabase Backup and Schema Preflight Guide

1. Set `DATABASE_URL` only in the current PowerShell process; never paste it into files or chat.
2. Run `scripts/backup_supabase.ps1 -OutputPath <local backup path>`; it stops if `pg_dump` is unavailable.
3. Run `python scripts/schema_preflight.py`; review its secret-free fingerprint report.
4. Request migration apply approval only after backup and schema comparison are accepted.

The backup tool writes only to the chosen local path. The preflight tool must use only information-schema/catalog reads when driver support is enabled. MATCH means ORM baseline matches fingerprint; DRIFT means a difference; UNKNOWN means insufficient comparison evidence.
