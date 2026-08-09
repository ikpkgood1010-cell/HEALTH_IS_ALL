# Supabase Free Backup and Pause Policy

Treat the stated one-week inactivity pause as an operational risk to validate in the selected Supabase dashboard before launch. The current repository has no automated backup or pause-recovery procedure.

- Before any expected inactivity period, the developer manually exports an approved database backup through Supabase Dashboard and stores it in an approved access-controlled location outside Git.
- After pause/resume or database unavailability, verify database reachability and health before accepting writes. Do not run migrations or schema changes as a recovery shortcut.
- Current FastAPI route code has no confirmed database-unavailable response policy; safe API error behavior is **UNKNOWN** and needs an implementation WP with tests.
- User GUI steps: create Supabase project in Singapore, obtain the approved session-pooler connection details without copying them to Git, configure Render runtime variable, test `/healthz`, then perform and record a manual backup procedure.
