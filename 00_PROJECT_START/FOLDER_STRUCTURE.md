# FOLDER STRUCTURE

Version: 1.0

`src/app` contains routes and layouts; `src/domains` owns business modules; `src/features` composes UI workflows; `src/shared` holds domain-neutral code; `src/infrastructure` owns vendor adapters; `src/assets`, `src/tests`, `src/types`, and `src/config` have explicit supporting roles.

Dependency direction is `app → features → domains → shared`, while infrastructure implements inward-facing domain interfaces. No reverse dependency, UI business logic, circular domain reference, or direct database access from the UI is allowed.

Folders/files are kebab-case; components/types/events use PascalCase; hooks use camelCase; constants use UPPER_SNAKE_CASE. Features are controlled by feature flags.
