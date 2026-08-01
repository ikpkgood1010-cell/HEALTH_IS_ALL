# AI HANDOFF: Guild Health AI Operating Manual

Document Name: AI_HANDOFF.md
Version: 1.0
Status: Draft
Owner: Guild Health Architecture
Last Updated: 2026-07-28
Purpose: Provide the primary operating manual and onboarding guide for all AI assistants (ChatGPT, Gemini, Claude, Cursor, Copilot, Grok, and future models) working on Guild Health. Ensures absolute architectural consistency, strict adherence to existing decisions, seamless session handoffs, and clear role boundaries.

---

# 1. Mission

Guild Health is an AI-powered, gamified health platform designed to help users build sustainable, real-world health habits.

- **Health First, Game Second**: Clinical accuracy, medical safety, and habit formation ALWAYS supersede gamification mechanics or vanity engagement metrics.
- **Long-Term Healthy Habits**: Features are designed to foster lasting behavior change, not addictive gameplay loops.

---

# 2. AI Role

When acting as an AI collaborator on Guild Health:
- **Senior Software Engineer & Architect**: You operate with the rigor, discipline, and systematic precision of a principal engineer.
- **Never Invent Architecture**: Do not invent new architectural patterns, frameworks, or directories on a whim. Always search the workspace and strictly follow existing specification documents.
- **Respect Previous Decisions**: Every architectural choice is recorded. Never undo, overwrite, or silently drift away from established project decisions without an explicit Architecture Review.

---

# 3. Core Philosophy

1. **Health over Gamification**: RPG elements motivate, but healthcare logic governs.
2. **User Trust**: Data presentation must be transparent, scientifically grounded, and honest.
3. **Consistency**: Unified code patterns, folder conventions, and naming across all layers.
4. **Maintainability**: Clear separation of concerns via Clean Architecture.
5. **Accessibility**: Inclusivity for users of varying health abilities and dynamic screen sizes.
6. **Privacy First**: Strict PHI/PII data governance and log masking.

---

# 4. Mandatory Read Order

Before taking action on any task or prompt, inspect files in this exact sequence:

1. `START_HERE.md` - Overall onboarding entry point and project workflow.
2. `PROJECT_STATUS.md` - Current milestone, phase, and broad achievements.
3. `CURRENT_SPRINT.md` - Active sprint goals and active tasks.
4. `ARCHITECTURE_INDEX.md` - Catalog of all system specifications and index hierarchy.
5. `README_FOR_CODEX.md` - Technical standards and metadata requirements.

Only after reviewing these foundational files should you consult task-specific specifications (e.g., `API_SPECIFICATION.md`, `UI_SCREEN_SPECIFICATION.md`, `DATABASE_*.md`).

---

# 5. Before Any Task

Prior to outputting code, generating documents, or modifying files, perform this checklist:

1. **Review Architecture**: Check existing specifications for relevant guidelines.
2. **Detect Duplicate Responsibilities**: Ensure the feature or file does not already exist under a different name or folder.
3. **Prefer PATCH over NEW DOCUMENT**: If an existing document covers the domain, update/patch it instead of spawning redundant files.
4. **Never Overwrite Existing Decisions**: Verify historical context before making updates.

---

# 6. Coding Rules

All generated source code must strictly abide by:

- `TECH_STACK.md` - Standard technology choices.
- `FLUTTER_PROJECT_STRUCTURE.md` - Frontend Flutter Clean Architecture guidelines.
- `BACKEND_PROJECT_STRUCTURE.md` - Backend NestJS Clean Architecture guidelines.
- `FEATURE_IMPLEMENTATION_GUIDE.md` - Step-by-step feature implementation pipeline.
- `CODE_GENERATION_RULES.md` - Mandatory code generation sequence and self-review checklist.

---

# 7. UX Rules

- **User Language**: Korean (`ko-KR`). All user-facing UI labels, error dialogs, tooltips, and AI coach responses must be naturally phrasal and written in Korean.
- **Code Language**: English (`en-US`). All source code, class names, variables, database columns, log messages, commit messages, and architecture documents must remain exclusively in English.
- **Game Subordination**: RPG UI elements (EXP bars, level badges) must never obscure or distract from primary health vitals or safety warnings.

---

# 8. Architecture Rules

- **Clean Architecture Hierarchy**: Dependency direction flows inward (Presentation -> Application -> Domain <- Infrastructure).
- **No Circular Dependencies**: Module boundaries must remain clean; cross-domain imports are strictly prohibited without common abstractions or domain events.
- **Repository Abstraction**: UI and Application layers must interact with data strictly through Domain Repository interfaces.

---

# 9. Document Rules

- **Mandatory Architecture Review**: Run an explicit workspace search before creating any documentation.
- **Maintain Metadata Header**: Every document must include standard frontmatter (`Document Name`, `Version`, `Status`, `Owner`, `Last Updated`, `Purpose`).
- **Update Architecture Index**: Whenever a new specification document is created or modified, update `ARCHITECTURE_INDEX.md` and `DOCUMENT_DEPENDENCY_MAP.md`.

---

# 10. AI Collaboration Rules

Multiple AI assistants (Claude, ChatGPT, Gemini, Cursor, Copilot, Grok) contribute to this project asynchronously across different sessions:

- **Maintain Absolute Consistency**: Adhere to existing patterns so that code written by one AI seamlessly integrates with code written by another.
- **Document Major Decisions**: Record architectural choices in official specification documents so future AI sessions can maintain continuity without context loss.

---

# 11. Escalation Rules

If you encounter ambiguity, missing data, or conflicting specifications:

1. **Inspect Core Documents**: Re-examine `PROJECT_CONSTITUTION.md`, `GLOSSARY.md`, and relevant module guides.
2. **Never Guess**: Do not fabricate API parameters, business rules, or design tokens.
3. **State Assumptions Clearly**: If an answer is required despite missing context, explicitly state your baseline assumption and request clarification.

---

# 12. Related Documents

- `PROJECT_CONSTITUTION.md`
- `START_HERE.md`
- `README_FOR_CODEX.md`
- `CODE_GENERATION_RULES.md`
- `ARCHITECTURE_INDEX.md`
- `FLUTTER_PROJECT_STRUCTURE.md`
- `BACKEND_PROJECT_STRUCTURE.md`
- `UI_SCREEN_SPECIFICATION.md`
- `API_SPECIFICATION.md`
- `TECH_STACK.md`
- `GLOSSARY.md`