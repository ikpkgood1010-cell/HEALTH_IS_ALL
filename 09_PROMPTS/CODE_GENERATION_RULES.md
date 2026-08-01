# CODE GENERATION RULES

Document Name: CODE_GENERATION_RULES.md
Version: 1.0
Status: Draft
Owner: Guild Health Architecture
Last Updated: 2026-07-28
Purpose: Define mandatory code generation rules, execution order, architectural compliance, forbidden practices, and self-review checklists for AI assistants and human developers writing code for Guild Health.

---

# 1. Required Documents to Read Before Coding

Before generating or modifying any source code, AI assistants and developers must inspect the following foundation documents in order:

1. `PROJECT_CONSTITUTION.md` - Core project principles and Health First priority.
2. `README_FOR_CODEX.md` - Architecture review rules, metadata standards, and terminology rules.
3. `TECH_STACK.md` - Approved technology choices and vendor lock-in policies.
4. `FLUTTER_PROJECT_STRUCTURE.md` - Clean Architecture boundaries and directory layout.
5. `STATE_MANAGEMENT_GUIDE.md` - Riverpod state controller patterns and rules.
6. `FEATURE_IMPLEMENTATION_GUIDE.md` - Step-by-step feature creation order.
7. `API_SPECIFICATION.md` - REST endpoints, payloads, and error codes.
8. `GLOSSARY.md` - Official terminology reference.

---

# 2. Code Generation Order

When writing feature code, ALWAYS generate layers in this strict sequence:

1. **Domain Layer**: Entities -> Value Objects -> Repository Interfaces.
2. **Data Layer**: DTOs -> Isar Schemas -> Datasources -> Concrete Repositories.
3. **Application Layer**: UseCases -> Riverpod State Controllers (`AsyncNotifier`).
4. **Presentation Layer**: UI Screens -> Widgets -> Design System Integration.
5. **Testing**: Unit tests -> Widget/Integration tests.

---

# 3. Clean Architecture Compliance

- **Domain Independence**: Domain code must have zero dependencies on Flutter, Dio, Isar, NestJS, or third-party libraries.
- **Data Encapsulation**: Data source entities or HTTP DTOs must never leak into the Presentation layer.
- **Dependency Inversion**: High-level domain modules must depend on abstract repository interfaces, not concrete data implementations.

---

# 4. Flutter Coding Rules

- Use declarative, strongly-typed widgets.
- Do not put business logic or state mutation inside `build()` methods.
- UI components must wrap foundational components from `lib/core/widgets/` following `DESIGN_SYSTEM.md`.
- No hardcoded UI strings; all user-facing text must use `AppLocalizations.of(context)!.<key>`.
- Colors must be dynamically referenced via `Theme.of(context).colorScheme`.

---

# 5. Backend Coding Rules

- NestJS controllers must handle request validation via DTO class-validators.
- Business logic must reside in NestJS domain services, not inside controllers.
- Access database entities using Prisma ORM schemas.
- Implement proper REST HTTP status codes (200, 201, 400, 401, 403, 404, 500) aligned with `API_SPECIFICATION.md`.

---

# 6. Riverpod Compliance

- Always use `@riverpod` annotations for code generation.
- Do not use deprecated `StateNotifier` or manual provider declarations.
- Use `ref.watch` for reactive state binding inside widget build methods.
- Use `ref.read` exclusively inside event callbacks.
- Always wrap async states in `AsyncValue<T>`.

---

# 7. Repository Pattern Compliance

- Every data interaction must pass through a repository interface defined in the domain layer.
- Repositories must handle error catching and map raw network/database exceptions into `Failure` domain objects.
- Repositories must encapsulate local Isar persistence and remote API synchronization logic.

---

# 8. Naming Conventions

- **Folders & Files**: `lower_snake_case` (e.g., `health_record_repository.dart`).
- **Classes**: `PascalCase` (e.g., `HealthRecordRepository`).
- **Variables & Functions**: `camelCase` (e.g., `fetchHealthSummary()`).
- **Constants**: `lowerCamelCase` or `UPPER_SNAKE_CASE` (for global constants).
- Follow official terminology from `GLOSSARY.md`.

---

# 9. Error Handling Requirements

- Every generated feature must handle:
  - Failure scenarios.
  - Recovery strategies / Fallback options.
  - Offline behaviors.
  - User-facing error messages (masked, non-technical).
  - Structured error logging.

---

# 10. Logging Requirements

- Log all major state transitions, API calls, and errors using structured loggers (`Talker` or NestJS Logger).
- Mandatory log tags: `[DEBUG]`, `[INFO]`, `[WARNING]`, `[ERROR]`, `[NETWORK]`.
- **Privacy Rule**: Sensitive personal health data (PHI/PII) must be masked before logging, adhering to `HEALTH_DATA_GOVERNANCE.md`.

---

# 11. Analytics Requirements

- Instrument event tracking calls for feature usage and habit completion via `AnalyticsService`.
- Use event names and key parameters specified in `DATABASE_04_ANALYTICS.md`.

---

# 12. AI Integration Requirements

- AI interactions must pass through abstract AI service interfaces (`AiRepository`).
- Code must not bind business logic directly to vendor-specific SDKs (e.g., direct OpenAI imports in domain logic).

---

# 13. Testing Requirements

- Generated code must include unit tests for UseCases and Riverpod Controllers.
- Mock external dependencies using `mocktail` or `mockito`.
- Ensure tests verify both success states and error/failure recovery states.

---

# 14. Documentation Update Requirements

If new features introduce new terminology, endpoints, or dependencies:
- Update `GLOSSARY.md` for new terms.
- Update `API_SPECIFICATION.md` for new REST endpoints.
- Update `ARCHITECTURE_INDEX.md` and `DOCUMENT_DEPENDENCY_MAP.md` if folder or file dependencies changed.

---

# 15. Pull Request Requirements

When submitting code for review:
- Freezed and Riverpod code generation must build without errors (`build_runner`).
- All unit and widget tests must pass.
- No warnings or linting errors in Dart/TypeScript analyzers.

---

# 16. Forbidden Practices

- ❌ **NO Game-First Priority**: Gamification mechanics must never override healthcare validity or user health safety.
- ❌ **NO Logic in UI**: Never place database queries, API calls, or business rules in UI widgets or build methods.
- ❌ **NO Direct Cross-Feature Imports**: Features must communicate via Core or domain interfaces, not by directly importing other private feature files.
- ❌ **NO Hardcoded Values**: Hardcoding API URLs, secret keys, or UI text is strictly forbidden.
- ❌ **NO Direct Vendor SDK Binding**: Do not couple core business code directly to third-party SDKs without abstraction layers.

---

# 17. AI Self-Review Checklist

Before delivering generated code, the AI collaborator must verify:
- [ ] Read `PROJECT_CONSTITUTION.md` and verified Health First priority.
- [ ] Checked `GLOSSARY.md` to ensure correct terminology.
- [ ] Code follows Clean Architecture layer dependencies (Domain -> Data -> Application -> Presentation).
- [ ] Riverpod code generation syntax (`@riverpod`) is used.
- [ ] UI contains zero business logic and uses Design System widgets.
- [ ] Error handling and structured logging are implemented.
- [ ] Sensitive health data is masked in logs.
- [ ] Unit test code is generated alongside feature logic.

---

# 18. Related Documents

- `PROJECT_CONSTITUTION.md`
- `README_FOR_CODEX.md`
- `TECH_STACK.md`
- `FLUTTER_PROJECT_STRUCTURE.md`
- `STATE_MANAGEMENT_GUIDE.md`
- `FEATURE_IMPLEMENTATION_GUIDE.md`
- `API_SPECIFICATION.md`
- `GLOSSARY.md`