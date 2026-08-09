# Supabase Free Backup Runbook

Before migration work, create a manual backup through Supabase Dashboard export or Supabase CLI using credentials supplied outside Git. Store it in an approved access-controlled location, verify restoration procedure, and record only backup metadata—not connection data—in the change record. Free-tier operational pause/backup risk means no automatic-backup assumption is permitted.
