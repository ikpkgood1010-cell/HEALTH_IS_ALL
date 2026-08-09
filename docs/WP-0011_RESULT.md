# WP-0011 Result

Automatic schema creation is removed from API startup. `/healthz` is unchanged. `/readyz` returns configured DB connectivity states without exposing URLs or exceptions. No migration or real database action occurred.
