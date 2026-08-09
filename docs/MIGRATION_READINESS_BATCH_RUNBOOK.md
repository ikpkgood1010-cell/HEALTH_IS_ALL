# Migration Readiness Batch Runbook

Run once in PowerShell after setting `DATABASE_URL` only for that process: `./scripts/run_migration_readiness.ps1 -OutputDirectory <local folder>`. Confirm `pg_dump --version` first. Review backup and JSON report; MATCH still requires separate migration approval. No apply command exists.
