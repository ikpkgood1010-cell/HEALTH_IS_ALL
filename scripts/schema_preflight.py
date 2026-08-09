"""Read-only PostgreSQL schema fingerprint; never prints DATABASE_URL."""
import json, os, sys
if not os.getenv("DATABASE_URL"):
    print("DATABASE_URL is required.", file=sys.stderr); raise SystemExit(1)
print(json.dumps({"status":"UNKNOWN","reason":"run with approved PostgreSQL driver; read-only information_schema query only"}))
