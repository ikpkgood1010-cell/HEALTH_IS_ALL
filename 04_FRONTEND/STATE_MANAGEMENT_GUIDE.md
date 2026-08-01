# STATE MANAGEMENT GUIDE

Document Name: STATE_MANAGEMENT_GUIDE.md
Version: 1.0
Status: Draft
Owner: Guild Health Architecture
Last Updated: 2026-07-28
Purpose: Define the official Riverpod state management rules, provider lifecycle patterns, asynchronous state handling, and testing strategies for Guild Health, aligned with TECH_STACK.md and FLUTTER_PROJECT_STRUCTURE.md.

---

# Provider Usage Rules

- Always use Riverpod 2.0+ / 3.0+ Code Generation syntax (`@riverpod` annotation) instead of legacy manual provider definitions.
- Prefer `autoDispose` providers by default (`@riverpod`) to ensure unused state resources are freed automatically.
- Keep state immutable using `Freezed` data classes for view states.
- Mutating state outside of Notifier classes is strictly forbidden.
- Avoid passing `WidgetRef` or `Ref` into business logic classes or UI widgets as function arguments; use provider bindings instead.

---

# Notifier & StateNotifier Usage

- **`Notifier<T>`**: Used for synchronous state management (e.g., local UI filters, theme mode, multi-step form steps).
- **Legacy `StateNotifier`**: Deprecated. Do not write new code using `StateNotifier`; migrate to `Notifier` or `AsyncNotifier`.
- Notifier state must always be initialized synchronously in the `build()` method.

---

# AsyncNotifier Usage

- **`AsyncNotifier<T>` / `AutoDisposeAsyncNotifier<T>`**: Primary state container for asynchronous operations (REST API, Isar DB reads).
- Replaces raw `FutureBuilder` or stateful manual async handling.
- Operations modifying state must set state to `AsyncLoading()` before executing, and update to `AsyncData(newData)` or `AsyncError(failure, stackTrace)` upon completion.

---

# FutureProvider Usage

- Reserved for read-only asynchronous requests that do not require state mutation methods (e.g., fetching application config, initial user profile metadata).
- If state mutation (refresh, patch, update) is required later, convert the `FutureProvider` to an `AsyncNotifierProvider`.

---

# StreamProvider Usage

- Used for reactive data streams such as Isar database live queries, WebSocket health metrics, or SSE (Server-Sent Events) from the AI Engine.
- Ensure streams automatically unsubscribe when no longer listened to via `autoDispose`.

---

# Dependency Injection

- All application dependencies (Repositories, Datasources, Services) must be registered and injected using Riverpod Providers.
- Root singletons (Dio client, Isar instance, Storage) are initialized during startup (`bootstrap.dart`) and injected into the root `ProviderScope` via provider overrides.

---

# Repository Pattern Integration

- Repositories are exposed through read-only functional providers (e.g., `@riverpod HealthRepository healthRepository(Ref ref)`).
- Application Controllers / Notifiers read repositories via `ref.watch` or `ref.read` to execute data operations.

---

# UseCase Interaction

- UseCases contain single-responsibility domain logic.
- Controllers invoke UseCases in their mutation methods rather than executing raw repository operations directly.
- UseCases return `Either<Failure, SuccessType>` domain models, which the Controller handles to emit appropriate `AsyncValue` states.

---

# Naming Conventions

### State Naming
- View states must use `PascalCase` ending with `State`.
- Example: `HealthDashboardState`, `HabitListState`.

### File Naming
- Provider/Controller files must use `lower_snake_case` ending with `_controller.dart` or `_provider.dart`.
- Example: `health_dashboard_controller.dart`, `user_profile_provider.dart`.

### Provider Naming
- Generated providers use `camelCase` appended with `Provider` automatically by `riverpod_generator`.
- Example: `@riverpod class HealthDashboardController` generates `healthDashboardControllerProvider`.

---

# Error Handling

- Async errors must be wrapped in custom `Failure` objects (defined in `core/error/failures.dart`).
- UI layers read error states using `AsyncValue.when` or `ref.listen(provider, (prev, next) => ...)` to display user-friendly snackbars or alert dialogs.
- Raw HTTP or database stack traces must never be exposed directly to the user interface.

---

# Loading State

- UI elements must handle loading gracefully using `AsyncValue.when` or `AsyncValue.maybeWhen`.
- Continuous background updates should preserve previous data using `AsyncValue.preserveState` or `AsyncValue.copyWithPrevious` during re-fetching to prevent UI flickering.

---

# Offline Synchronization

- Offline state transitions must update local Isar state synchronously and trigger an asynchronous background sync task.
- Controllers watch local Isar streams using `StreamProvider` to guarantee instant UI response upon local write.

---

# Cache Invalidation

- Use `ref.invalidate(provider)` or `ref.refresh(provider)` to invalidate stale provider state when mutations occur in related domains.
- Example: Completing a habit invalidates both `habitListControllerProvider` and `healthScoreProvider`.

---

# Testing Strategy

- **Unit Testing Controllers**: Test controllers independently by mocking Repositories/UseCases using `mocktail` or `mockito`.
- Override dependencies in `ProviderContainer`:
  ```dart
  final container = ProviderContainer(
    overrides: [
      healthRepositoryProvider.overrideWithValue(mockHealthRepository),
    ],
  );