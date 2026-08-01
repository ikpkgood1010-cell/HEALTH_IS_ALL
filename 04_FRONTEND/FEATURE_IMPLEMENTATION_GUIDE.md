# FEATURE IMPLEMENTATION GUIDE

Document Name: FEATURE_IMPLEMENTATION_GUIDE.md
Version: 1.0
Status: Draft
Owner: Guild Health Architecture
Last Updated: 2026-07-28
Purpose: Define the official step-by-step implementation workflow for developers and AI collaborators when creating or modifying feature modules in Guild Health, aligned with FLUTTER_PROJECT_STRUCTURE.md and STATE_MANAGEMENT_GUIDE.md.

---

# 1. Feature Creation Order

To maintain Clean Architecture boundaries and avoid circular code dependencies, every new feature must be implemented in the following strict order:

1. Domain Layer (Entities, Value Objects, Repository Interfaces)
2. Data Layer (DTOs, Isar Schemas, Datasources, Concrete Repositories)
3. Application Layer (UseCases, State Controllers / AsyncNotifiers)
4. Presentation Layer (UI Screens, Widgets, Design System integration)
5. Integration & Tests (Analytics, AI, Push Notifications, Unit/Widget Tests)

---

# 2. Folder Creation

Create the standard Clean Architecture directory template under `lib/features/<feature_name>/`:

```text
lib/features/<feature_name>/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
├── data/
│   ├── datasources/
│   ├── models/
│   └── repositories/
├── application/
│   └── controllers/
└── presentation/
    ├── screens/
    ├── widgets/
    └── state/