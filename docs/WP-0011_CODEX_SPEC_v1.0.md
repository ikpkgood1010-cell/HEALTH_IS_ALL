# WP-0011 — Disable Automatic Schema Creation

Remove automatic ORM schema creation from ordinary API startup and make readiness check a safe real DB connectivity probe. Never execute migrations or alter Supabase.
