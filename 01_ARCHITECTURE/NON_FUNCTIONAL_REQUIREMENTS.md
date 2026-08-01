# NON-FUNCTIONAL REQUIREMENTS

Version: 1.0

Targets: home initial load ≤2 seconds; exercise/food save ≤300ms; AI food analysis ≤5 seconds; AI advice ≤2 seconds; leaderboard ≤500ms; statistics ≤1 second; animations target 60 FPS.

The service targets 99.9% availability and scales from 1,000 to 1,000,000 users with stateless services, horizontal scaling, CDN, caching, and pooling.

Required: RLS, TLS, secure authentication, privacy/data export/deletion, offline-first records with automatic sync, WCAG 2.2 AA, PWA, monitoring/logging/backup, test coverage, and safe AI wellness guidance.
