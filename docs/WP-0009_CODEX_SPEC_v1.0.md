# WP-0009 — Supabase Database Connection

Implement a safe, `DATABASE_URL`-based Supabase PostgreSQL connection path, a dry-run-only migration runner, tests, and implementation guidance. Do not connect to Supabase, run SQL against a real DB, deploy Render, or disclose secrets.

The app must support a Supabase session-pooler URL with TLS, return safe readiness information when DB configuration or connection fails, and never auto-run migrations at startup.
