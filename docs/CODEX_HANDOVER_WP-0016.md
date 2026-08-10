# Codex Handover — WP-0016

DATABASE_URL stays process-only; batch stops on backup failure or non-MATCH preflight.

The ORM baseline registration was approved and completed on 2026-08-10 after a local backup and MATCH preflight. Version `202608090001` is registered in `schema_migrations`. Future migration work must preserve the existing four application tables and must not run legacy `/02_DATABASE` SQL.
