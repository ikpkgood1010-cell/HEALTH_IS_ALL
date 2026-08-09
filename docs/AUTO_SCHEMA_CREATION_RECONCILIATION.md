# Auto Schema Creation Reconciliation

`health_i_profiles`, `user_exp_logs`, `meal_logs`, and `activity_logs` were previously auto-created by ORM metadata creation. WP-0011 removes the ordinary `init_db()` startup call; `Base.metadata.create_all()` is no longer on the API startup path.

`/02_DATABASE` SQL remains unapplied. Before any migration application, approve ordering, applied-migration tracking, an external backup, and a restore plan. This WP deletes, changes, or executes no Supabase table, data, or SQL.
