# DATA DICTIONARY

Version: 1.0

Database uses `snake_case`; API and TypeScript use `camelCase`; components use `PascalCase`; constants/enums use `UPPER_SNAKE_CASE`.

Identifiers use UUID. Dates use UTC and `*_at`; booleans use `is_`, `has_`, `can_`, or `should_` in database naming.

Core entities include User, Exercise, Food, body records, Hero, Equipment, Tower, Quest, Achievement, Affinity, AI analysis, Notification, and Settings.

Validation: UUIDs are unique; EXP and points are non-negative; level is at least 1; durability and affinity remain 0–100; duration is positive; food calories are non-negative. Soft delete is the default.

Master Data is the source for enums and balance values.
