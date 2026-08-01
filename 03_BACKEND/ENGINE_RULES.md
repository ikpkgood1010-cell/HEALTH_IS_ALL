# ENGINE RULES

Version: 1.0

Health → AI → Game is mandatory. RPG and Social cannot modify Health; AI only analyzes and recommends. Business logic belongs in domain/application services; repositories only access persistence.

Core events are single-fact, past-tense records such as `ExerciseCompleted`, `QuestCompleted`, and `TowerCleared`.

Health Score uses only health factors. EXP is earned from healthy actions, not battle. Points never buy equipment. Heroes grow automatically from real health activity. Rest is progress and must never be treated as failure.

All APIs are validated and return a consistent success/error envelope. UUIDs, UTC, soft deletes, logging, RLS, rate limiting, offline exercise support, WCAG 2.2 AA, and automated testing are required.
