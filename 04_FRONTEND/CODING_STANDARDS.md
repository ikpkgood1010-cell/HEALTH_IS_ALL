# Guild Health
# CODING STANDARDS

Version: 1.0
Status: Accepted

---

## 1. Engineering Role

You are the Lead Software Engineer of Guild Health.

Your responsibility is not only to write code,
but also to protect the architecture,
maintain long-term scalability,
and preserve the philosophy of the project.

When there is a conflict between speed and quality,
always choose maintainability.

Guild Health is a Healthcare First platform. Every implementation must preserve the direction `Health -> AI -> Game`; game, social, and AI modules must never create or alter authoritative health records.

---

## 2. Core Principles and Engineering Priorities

All implementation decisions are evaluated in this order:

1. User safety, privacy, and Healthcare First
2. Correctness and data integrity
3. Readability and maintainability
4. Type safety and testability
5. Accessibility and inclusive UX
6. Performance and reliability
7. Scalability and extensibility
8. Delivery speed

Code must be explicit, boring where possible, and easy for both people and AI tools to understand. Prefer small cohesive modules, clear contracts, and named abstractions over clever or compressed code.

The following principles are mandatory:

- **Readability First**: code must communicate intent without requiring tribal knowledge.
- **Simplicity**: choose the smallest design that correctly supports present requirements and documented extension points.
- **Maintainability**: optimize for safe change over short-term implementation speed.
- **Scalability**: preserve stateless, modular, observable paths that can scale horizontally.
- **Reusability**: reuse stable abstractions; do not create a shared abstraction before there is a proven common responsibility.
- **Testability**: isolate rules and side effects so meaningful automated tests are practical.
- **Accessibility**: inclusive use is a product requirement, not a polish step.
- **Performance**: meet measured user-facing budgets without sacrificing correctness.
- **Type Safety**: represent valid states precisely and reject invalid input at boundaries.
- **AI-Friendly Code**: use predictable folders, explicit contracts, small units, and current documentation so AI-assisted changes remain reviewable.

---

## 3. TypeScript Standards

- Enable `strict: true`; do not weaken compiler settings to make code compile.
- `any` is forbidden. Use `unknown`, narrow it with type guards, or define an explicit type.
- Do not use unsafe type assertions (`as`) to bypass validation. Assertions are allowed only after a local, documented runtime guarantee.
- Export public types deliberately. Prefer `type` for unions/compositions and `interface` for extendable object contracts.
- Model finite states with discriminated unions and exhaustive `switch` checks.
- Use branded or value-object types for identifiers and domain-sensitive units when the boundary benefits justify them.
- `null` and `undefined` must be intentional; do not use truthiness where an explicit check is clearer.
- Use `readonly` for values, arrays, and object properties that must not be mutated after construction; prefer immutable update patterns.
- Prefer built-in utility types (`Pick`, `Omit`, `Partial`, `Required`, `Record`, `ReturnType`) before introducing duplicated type definitions.
- Generics must constrain the relationship they model. Do not introduce unconstrained generics solely to make an API appear reusable.
- Avoid TypeScript `enum` for values that cross API, database, or Master Data boundaries; use `as const` objects/arrays plus derived union types. Native enums require an explicit interoperability reason.
- Every public function, repository contract, DTO, and event has an explicit input and output type.
- Avoid duplicate types. Derive types from Zod schemas or a shared contract where possible.

## 4. Naming Standards

| Item | Convention | Example |
| --- | --- | --- |
| Folder and file | `kebab-case` | `exercise-record-form.tsx` |
| React component | `PascalCase` | `ExerciseRecordForm` |
| Type, interface, class, enum | `PascalCase` | `CreateExerciseInput` |
| Function, variable, hook | `camelCase` | `calculateExerciseExp`, `useExerciseForm` |
| Boolean | `is_` / `has_` / `can_` / `should_` in DB; camelCase in TS | `isDeleted`, `hasPermission` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_EXERCISE_DURATION_MINUTES` |
| Database field | `snake_case` | `created_at`, `user_id` |
| API field | `camelCase` | `createdAt`, `userId` |
| Event | past-tense `PascalCase` | `ExerciseCompleted` |
| DTO | action-oriented suffix | `CreateExerciseRequestDto` |
| Repository | aggregate plus `Repository` | `ExerciseRepository` |
| Service / use case | verb plus subject | `RecordExerciseService` |

Names describe intent, not implementation. Avoid vague names such as `data`, `item`, `helper`, `manager`, `utils2`, `handleData`, and unexplained abbreviations. A name may use a domain term only when it matches the Data Dictionary.

---

## 5. Folder and Module Responsibility

- `src/app`: App Router routes, layouts, metadata, route-level loading/error states, and composition only. No business logic or direct database access.
- `src/features`: user-facing workflow composition. A feature may combine domain use cases and presentation components but must not own domain rules.
- `src/domains/<domain>/domain`: entities, value objects, aggregates, policies, domain services, repository interfaces, and domain events. No framework or vendor imports.
- `src/domains/<domain>/application`: use cases, orchestration services, DTO mapping, authorization coordination, and transaction boundaries.
- `src/domains/<domain>/infrastructure`: repository implementations and adapters specific to the domain.
- `src/infrastructure`: cross-domain vendor adapters for Supabase, Prisma, OpenAI, storage, notifications, analytics, logging, and cache.
- `src/shared`: domain-neutral UI primitives, utilities, hooks, styles, and types. Shared code must not import from `domains` or `features`.
- `src/config`: typed configuration and feature flags only; secrets are never committed.
- `src/tests`: fixtures, integration tests, and E2E support. Unit tests should live beside the module they verify when practical.

Do not create catch-all folders such as `common`, `misc`, `helpers`, or `services` at the project root. Put code where its owner can be identified without opening the file.

## 6. Clean Architecture and Dependencies

Dependency direction is one-way:

`app -> features -> application/domain -> shared`

`infrastructure -> domain interfaces`

- The domain layer depends on no framework, database, HTTP client, or vendor SDK.
- Application services depend on domain contracts, not concrete infrastructure.
- Infrastructure implements ports/interfaces defined inward and is injected at the composition boundary.
- UI calls an API, server action, or presentation adapter; it never imports a repository or accesses the database directly.
- Domains communicate through explicit interfaces or domain events. Circular imports and circular domain dependencies are forbidden.
- A domain event carries a completed business fact, not a command or UI concern.

## 7. React and Next.js Standards

- Use React Server Components by default. Add `'use client'` only for browser APIs, user interaction, local state, or client-only libraries.
- Keep route files thin; compose feature entry points rather than implementing workflow logic in `page.tsx`.
- Components render state and emit intent. They do not calculate EXP, decide rewards, mutate aggregates, or call databases.
- Use `next/image`, semantic HTML, route-level `loading.tsx`, `error.tsx`, and `not-found.tsx` where applicable.
- Server Actions and Route Handlers are transport boundaries: authenticate, validate, invoke an application use case, and return a typed response. They do not contain domain logic.
- Never expose service-role keys, OpenAI keys, or internal error details to the client.
- Metadata must be route-specific and accessible; do not block primary content on non-critical animations or analytics.
- Use functional components only. Prefer composition over inheritance; React component inheritance is prohibited.
- Follow the Rules of Hooks without exception: call hooks unconditionally at the top level of a component or custom hook.
- Memoization is a measured optimization, not a default. Use `memo`, `useMemo`, and `useCallback only` when profiling or referential stability demonstrates a need.

## 7.1 Next.js Routing and Rendering Standards

- Use the App Router exclusively. Route groups organize concerns without changing URLs and must not become a substitute for feature modules.
- Use Server Actions only as authenticated, validated transport boundaries for focused mutations. Prefer Route Handlers for public, mobile-ready, webhook, or explicitly versioned APIs.
- Use Parallel Routes only for independently loading route regions with a documented UX benefit. Each slot must have meaningful loading and error states.
- Every route that fetches data defines appropriate `loading.tsx`, `error.tsx`, and `not-found.tsx` behavior. Error boundaries show a safe recovery action and log the underlying failure.
- Metadata, canonical URLs, Open Graph data, and robots behavior are owned at the route/layout level and tested for public pages.

## 8. Component and Reusable UI Rules

- One component has one clear visual responsibility. Components must remain under 300 lines; split earlier when responsibilities diverge.
- Prefer composition, slots, and variants over boolean-prop explosions. When a component has more than three unrelated mode booleans, redesign its API.
- Shared components are domain-neutral and accessible by default. Domain-specific components remain within their feature or domain presentation folder.
- Props are explicit and typed. Do not pass entire untyped objects when a small view model is sufficient.
- Keep display formatting in presentation adapters or view models; do not leak persistence models into UI.
- Use stable keys derived from IDs, never array indexes for mutable lists.
- All empty, loading, error, disabled, and success states are designed deliberately.

Recommended component layout:

```text
components/
  component-name/
    component-name.tsx
    component-name.test.tsx
    component-name.stories.tsx        # when a visual contract is useful
    component-name.types.ts
    index.ts
```

Use `children` for intentional visual composition, not as an untyped escape hatch. Prefer typed slots or render props when the parent needs to control a structured region.

## 9. Tailwind CSS Standards

- Use Tailwind utility classes for local styling and design tokens defined through CSS variables/theme configuration.
- Do not hardcode arbitrary colors, spacing, shadows, durations, or z-index values when a design token exists or should exist.
- Use `cn` only to compose intentional variants; do not construct unreviewable class-name strings.
- Use `cva` or an equivalent typed variant system for reusable component variants.
- Mobile-first styles are required. Verify keyboard focus, contrast, dark mode, and reduced motion for every interactive component.
- Global CSS is limited to resets, tokens, fonts, and genuinely global behavior.

## 10. State Management: Zustand and TanStack Query

### Zustand

- Zustand stores only client-owned state: theme preference, transient UI state, offline sync queue, and other browser-local concerns.
- Do not duplicate server records in Zustand. Never treat a Zustand store as the source of truth for health, reward, or RPG records.
- Store actions are small, typed, deterministic, and independently testable.

### TanStack Query

- TanStack Query owns server-state caching, invalidation, refetching, optimistic updates, and background synchronization.
- Query keys are centralized, typed, and derived from stable identifiers.
- Mutations call a validated API boundary. On success, invalidate or update only affected queries.
- Optimistic updates require a rollback path and are not used for irreversible health/reward mutations unless the server supports idempotency.
- Configure stale times deliberately; do not use global defaults as a substitute for performance design.

### Local and Derived State

- Use React local state for ephemeral component state such as an open dialog or focused item.
- Do not store values that can be derived from props, query data, or other state. Calculate them during render or in a named selector.
- Avoid syncing props into state except for an explicit editable draft with documented reset behavior.

## 11. Prisma and Supabase Standards

- PostgreSQL/Supabase is the authoritative operational datastore. All tables use UUID primary keys, UTC timestamps, soft-delete policy where applicable, and Row Level Security.
- Prisma is used server-side only for typed data access and migrations where compatible with the approved Supabase operational model. It is never bundled to the client.
- Schema changes require a migration, rollback consideration, RLS policy review, data backfill plan if needed, and documentation update.
- Repositories own persistence mapping and queries only; they do not calculate business rules or emit user-facing messages.
- Use transactions for atomic state changes within one consistency boundary. Use an outbox/event-log strategy for cross-domain side effects.
- Supabase Auth is the authentication authority. Authorization is enforced in both application policy and RLS; client checks are never sufficient.
- Storage objects use scoped paths, content-type checks, size limits, signed URLs when required, and ownership validation.

## 12. Repository, Service, DTO, and API Rules

### Repository Pattern

- Repository interfaces live in the domain layer; implementations live in infrastructure.
- A repository represents an aggregate/persistence boundary, not a generic table utility.
- Repository methods use meaningful verbs such as `findById`, `save`, `existsByDate`, and return domain objects or explicit persistence results.
- No HTTP DTO, React type, or vendor-specific type may leak into repository interfaces.

### Service Layer

- Application services/use cases each own one user or system intent: `RecordExerciseService`, not a broad `HealthcareService`.
- Services validate authorization, load aggregates, call domain behavior, persist changes, and schedule domain events.
- Domain services contain domain logic that does not naturally belong to one entity. They remain pure where possible.
- Functions must remain under 100 lines. Split by named responsibility rather than nesting conditionals.

### DTO Rules

- Request and response DTOs are transport contracts, separate from entities and database models.
- DTOs are validated at the boundary with Zod and mapped explicitly to application input/output types.
- Never return secrets, access tokens, internal IDs not needed by the caller, stack traces, or raw database errors.
- Version breaking public APIs deliberately; do not silently rename or change field meanings.

### API Response Format

Success responses use:

```ts
{ success: true, data: T, meta?: { requestId: string } }
```

Failure responses use:

```ts
{
  success: false,
  error: {
    code: string,
    message: string,
    fieldErrors?: Record<string, string[]>,
    requestId: string
  }
}
```

HTTP status codes express transport outcome. Error codes are stable machine-readable contracts; messages are safe, localized user-facing text.

### REST Resource Standards

- Use plural nouns and resource-oriented paths: `/api/v1/exercises`, `/api/v1/exercises/{exerciseId}`. Do not use verbs in resource paths unless modeling a distinct action with no resource representation.
- Use query parameters for filtering, sorting, and pagination. Example: `?cursor=...&limit=20&sort=-recordedAt&exerciseType=RUNNING`.
- Cursor pagination is the default for growing or real-time collections. Responses include `meta.nextCursor`; offset pagination requires a documented reason.
- Filtering and sort fields are allowlisted and validated. A leading `-` denotes descending sort.
- Public and mobile-consumed APIs use a `/v1` version boundary. Breaking changes require a new version and deprecation plan.
- Use standard status codes: `200`, `201`, `202`, `204`, `400`, `401`, `403`, `404`, `409`, `422`, `429`, and `5xx` only according to their defined HTTP meaning.

## 13. Validation, Errors, Async, and Logging

### Zod Validation

- Validate all untrusted input at API, Server Action, webhook, upload, environment, and external-provider boundaries.
- Schemas enforce required fields, enum membership, length/range/unit rules from the Data Dictionary and Master Data.
- Reuse schemas through composition; do not duplicate validation literals across UI and server.
- Client validation improves UX; server validation is authoritative.

### Error Handling

- Expected failures use typed domain/application errors with stable error codes.
- Unexpected failures are logged with context, mapped to a safe internal error response, and reported to monitoring.
- Never swallow errors, return `null` ambiguously, or show raw provider/database errors to users.
- Failed asynchronous event handlers must be retryable, idempotent, observable, and unable to invalidate the original health record.

### Async/Await

- Use `async`/`await` for asynchronous control flow. Always await promises that affect correctness.
- Parallelize independent operations with `Promise.all` or `Promise.allSettled`; do not parallelize operations with ordering or transaction dependencies.
- Define timeouts, cancellation/abort behavior, and retry policy for external calls.
- Never use floating promises or `void` promises without an explicit fire-and-forget policy, logging, and failure handling.

### Logging

- Use Pino structured logging; `console.log` is forbidden in application code.
- Every log has event name, level, request/correlation ID, actor ID when safe, and non-sensitive context.
- Log domain events, external calls, retries, authorization denials, and errors. Do not log passwords, tokens, health details beyond operational necessity, images, raw prompts, or private AI responses.
- Use levels consistently: `debug`, `info`, `warn`, `error`, `fatal`. Production logs follow the 90-day retention policy.

## 14. Domain Event Rules

- Events use past-tense PascalCase names: `ExerciseCompleted`, `FoodAnalyzed`, `RewardGranted`.
- One event represents one immutable business fact. No compound names such as `ExerciseCompletedAndBattleStarted`.
- Event payloads include `eventId`, `eventName`, `occurredAt`, aggregate ID, schema version, correlation ID, and only necessary data.
- Persist events/outbox records with the state change that produced them. Consumers are idempotent and version-aware.
- Event handlers may react asynchronously but cannot directly mutate Health Domain authority unless the Health Domain explicitly exposes an allowed command.
- Events are logged, tested, documented, and safe to replay.

## 15. Accessibility, Animation, and Performance

### Accessibility

- Meet WCAG 2.2 AA. Use native semantic elements before ARIA.
- Every control is keyboard operable, has a visible focus indicator, accessible name, correct error association, and sufficient color contrast.
- Announce asynchronous save/analysis status through accessible status regions where appropriate.
- Support dynamic font sizes, screen readers, high contrast, and `prefers-reduced-motion`.
- Accessibility is verified in automated tests and manual keyboard/screen-reader review.

### Animation

- Animation must clarify state or provide a gentle reward, never delay essential actions or pressure the user.
- Target 60 FPS; respect reduced-motion settings with a meaningful static alternative.
- Animate transform and opacity preferentially. Avoid layout thrashing, long main-thread animation, autoplay audio, and flashing content.
- Healthi appears as a calm final supportive moment, not as a blocking interruption.

### Performance

- Treat NFR budgets as acceptance criteria: exercise save target 300ms, food analysis maximum 5 seconds, home initial load target 2 seconds.
- Use Server Components, streaming, caching, pagination/virtual lists, code splitting, lazy loading, optimized images, and measured memoization.
- Measure before optimizing. Avoid premature `useMemo`, `useCallback`, caching, and global state.
- Keep client bundles small; analyze bundle impact for new dependencies.
- External APIs require timeouts, circuit-breaking/fallback behavior where warranted, and telemetry for latency and errors.

## 16. Security and Privacy Coding Rules

- Authenticate every protected request and authorize every resource access server-side and through RLS.
- Use parameterized queries/ORM safely; never interpolate user input into SQL, shell commands, HTML, URLs, or prompts without context-appropriate validation and encoding.
- Validate uploads by ownership, MIME type, file signature where feasible, size, and storage path. Scan/quarantine when required by the risk model.
- Keep secrets in validated environment variables; never commit, log, expose, or place them in client bundles.
- Apply CSRF protection for cookie-authenticated mutations, secure headers/CSP, rate limiting, and abuse monitoring.
- Use secure password handling through the auth provider; never implement custom password hashing or token storage in local storage.
- Minimize health data collection. Data export and deletion workflows must be auditable and honor retention policies.
- AI prompts and outputs are untrusted external content: redact sensitive data, apply output safety checks, and never treat AI output as an authority to mutate health records.

## 17. Testing Standards

- Every service/use case has unit tests for success, validation, authorization, boundary, and failure paths.
- Critical API routes have integration tests covering authentication, RLS/ownership, validation, idempotency, and response contracts.
- Major user journeys have E2E tests: sign-up/onboarding, exercise recording, food logging, and offline-to-online synchronization.
- Use Vitest for unit/integration tests, Testing Library for components, and Playwright for E2E tests.
- Tests must be deterministic: no real production services, time-dependent behavior, random rewards, or hidden shared state.
- Test fixtures use safe synthetic data. Test names state the user-visible behavior.
- Meet the project coverage target (80% unit coverage) but never optimize for coverage at the expense of meaningful assertions.

## 18. AI-Generated Code Rules

- Treat AI output as an untrusted draft, never as a source of truth.
- Before accepting generated code, verify architecture placement, domain boundaries, types, authorization, validation, Master Data use, tests, accessibility, performance, and security.
- AI-generated code must not introduce `any`, magic numbers, duplicate abstractions, hidden network calls, secrets, unsupported dependencies, or speculative features.
- Ask AI for small, bounded changes with explicit contracts. Do not accept large rewrites without a written architecture decision and review plan.
- Generated comments and documentation must be checked for factual accuracy and alignment with current project documents.
- Every accepted AI change is attributable in normal Git history and passes the same review gates as human-authored code.

## 19. Documentation and Comment Policy

- Update the relevant specification, ADR, API contract, Master Data, and migration documentation in the same change when behavior changes.
- Public modules document intent, invariants, ownership, and non-obvious decisions. Do not restate obvious syntax.
- Use comments to explain *why*, constraints, tradeoffs, or safety rationale—not *what* straightforward code does.
- TODOs require an owner/reference and a concrete follow-up condition. Temporary workarounds require an issue link and removal plan.
- Keep examples accurate and executable where possible. Documentation is part of the definition of done.
- Use JSDoc for exported public APIs, domain invariants, non-obvious generic contracts, and integration boundaries. Do not add JSDoc that merely repeats names and types.
- Update the relevant README when setup, environment variables, scripts, workflows, or contributor expectations change.
- Architecture changes with lasting consequences require an Architecture Decision Record that records context, decision, alternatives, impact, and status.

## 20. Code Review Checklist

Reviewers and authors confirm:

- Healthcare First and domain direction are preserved.
- The change is in the correct folder/layer and has no circular dependency.
- Inputs are validated and authorization/RLS is enforced.
- Master Data replaces magic numbers and hard-coded business values.
- Names, types, DTOs, errors, events, and API contracts are explicit.
- UI is accessible, responsive, dark-mode compatible, and free of business logic.
- Failure, loading, offline, retry, and empty states are handled.
- Tests cover meaningful behavior and all required checks pass.
- Logging/monitoring is useful and privacy-safe.
- Performance budgets and bundle impact were considered.
- Documentation, migrations, feature flags, and rollout/rollback needs are complete.

## 21. Pull Request and Git Standards

### Pull Request Checklist

- PR has a focused purpose and links the relevant feature/specification/ADR.
- Description explains user impact, domain impact, events, API/DB changes, and test evidence.
- Database changes include migration, RLS policy, backfill, and rollback notes where applicable.
- Screenshots or recordings are included for visual changes, including mobile/dark mode when relevant.
- No unrelated refactor, generated artifact, secret, or dead code is included.
- All lint, typecheck, test, accessibility, and build checks pass before review.

### Commit Message Convention

Use Conventional Commits:

```text
type(scope): concise imperative summary
```

Allowed types: `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `perf`, `build`, `ci`, `chore`, `revert`.

Examples:

```text
feat(exercise): add validated exercise recording use case
fix(auth): reject expired refresh token sessions
docs(architecture): record offline sync decision
```

Keep commits atomic and buildable. Do not use vague messages such as `update`, `fix stuff`, or `wip` on shared branches.

### Branch Naming

Use lowercase kebab-case branches in the form:

```text
<type>/<ticket-or-scope>-<short-description>
```

Examples:

```text
feat/exercise-recording
fix/auth-refresh-session
docs/coding-standards
```

Branch types use the same vocabulary as Conventional Commits. Long-lived branches require an explicit release or environment purpose.

### Pull Request Template

Every pull request contains:

```text
## Summary
## User and domain impact
## Database / API / event changes
## Security and privacy considerations
## Accessibility and performance checks
## Test evidence
## Rollout, feature flag, and rollback plan
## Documentation updated
```

## 22. Forbidden Practices

The following are prohibited:

- Business logic in React components, routes, controllers, repositories, or database triggers without an explicit ADR.
- Direct database access from the client.
- `any`, unsafe casts, disabled lint/type checks, ignored promises, and `console.log`.
- Magic numbers, unversioned balance values, and hard-coded feature behavior outside approved configuration/Master Data.
- Direct cross-domain internal imports, circular dependencies, and hidden side effects.
- Returning database entities or provider errors directly through APIs.
- Storing secrets in source code, browser storage, logs, or analytics.
- N+1 query patterns, unbounded list fetching, blocking UI for non-critical work, and unmeasured performance claims.
- Accessibility regressions, non-semantic clickable `div`s, keyboard traps, or motion that ignores user preferences.
- Penalizing user absence, guilt-driven messaging, or game mechanics that encourage unsafe health behavior.

---

## Final Standard

Guild Health code must be safe, readable, type-safe, testable, accessible, observable, and extensible. When requirements are unclear or conflict with this handbook, stop implementation, identify the conflict, and propose the required document or ADR update before proceeding.

The purpose of code is not only to work today,
but to remain understandable,
maintainable,
and scalable for many years.
