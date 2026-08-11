# Anonymous MVP Identity

The MVP creates one random `anon_` user ID per device and keeps it in local Hive storage. Existing health-record API calls use that ID instead of the shared `user_test_001` value. The identifier is exactly 36 characters (`anon_` + 31 hexadecimal characters) so it fits the canonical PostgreSQL `VARCHAR(36)` contract. Earlier 37-character local IDs are truncated once and saved back to Hive before any API call.

This is a no-login MVP convenience, not authentication. It must not be treated as account security or used for a public multi-user launch. A future Supabase Auth migration will replace the anonymous ID with an authenticated user ID.

Deleting browser/app storage creates a new anonymous identity and the previous records cannot be recovered through the app.
