# ENGINE OVERVIEW

Version: 1.0

---

# Purpose

This document defines the core engine architecture of Guild Health.

Every gameplay, health, AI, and progression system is implemented through independent engines.

Each engine has a single responsibility and communicates through well-defined interfaces.

---

# Engine Philosophy

Guild Health follows a Data-Driven Architecture.

The application should not hard-code business logic whenever possible.

Rules, UI behavior, rewards, AI prompts, and balancing should be configurable through data.

---

# Core Engines

1. Exercise Engine
2. Progression Engine
3. Health Engine
4. Quest Engine
5. Battle Engine
6. AI Engine

---

# Engine Dependencies

Exercise Engine
    ↓
Health Engine
    ↓
Progression Engine
    ↓
Quest Engine
    ↓
Battle Engine

AI Engine can communicate with every engine.

---

# General Rules

Each engine must:

- Have a single responsibility.
- Be independently testable.
- Never directly access another engine's internal state.
- Communicate only through services or events.
- Be configurable without code changes whenever possible.

---

# Event-Driven Architecture

Engines communicate through events.

Example:

ExerciseCompleted
↓

HealthScoreUpdated
↓

ExpGranted
↓

QuestProgressUpdated
↓

BattleProgressUpdated

---

# Engine Configuration

Every engine must support external configuration through database or master data.

Business logic must not depend on hard-coded values.

---

# Scalability

New engines may be added without changing existing engines.

Examples:

- Guild Engine
- Economy Engine
- Achievement Engine
- Event Engine

---

# Consistency Checklist

Must remain consistent with:

- PROJECT_CONSTITUTION.md
- PRODUCT_VISION.md
- ENGINE_RULES.md
- MASTER_DATA.md

Conflict Status:
None
