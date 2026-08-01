# Guild Health
# README FOR CODEX

Version: 1.5

Guild Health is an AI Healthcare + RPG Gamification platform. Codex protects the project philosophy and writes maintainable code, not merely code that works.

Read project documents in their declared priority order. Preserve Health First, then AI, then Game. Do not put business logic in UI, hard-code business values, break domain boundaries, create cycles, or access databases from UI.

For each feature: inspect the feature/domain/Master Data/event/API/database; implement UI only after these; then test, review accessibility and performance, and update documentation.

Always reuse stable code, validate inputs, emit events, handle errors, test, and consider performance/accessibility. When documents conflict, propose the required document update before implementation.

───
Architecture Review Rule
Before creating, modifying, or deleting any document, Codex must perform an Architecture Review.
1. Consistency Check
Compare the requested change with every existing project document.
Report architectural conflicts before making changes.
Never silently replace established architecture.

2. Health First Principle
Guild Health is a healthcare platform.
Gamification exists only to encourage healthy habits.
Whenever gameplay conflicts with healthcare principles, healthcare always has higher priority.

3. Extension Before Replacement
Prefer extending existing systems over replacing them.
Avoid duplicate concepts.
Reuse existing engines whenever possible.

4. Traceability
Every new or modified document must list related documents.
If a change affects other documents, list them explicitly.
Example:
Affected Documents
HEALTH_ENGINE.md
HABIT_ENGINE.md
RULE_ENGINE.md

5. Conflict Reporting
If conflicts are detected:
1. Explain the conflict.
2. Explain why it exists.
3. Recommend the preferred solution.
4. Wait for user confirmation before applying breaking changes.

6. Backward Compatibility
Avoid breaking existing architecture.
Maintain compatibility whenever possible.
If breaking changes are required, explain the migration path.

7. Document Quality Checklist
Before completing any document, verify:
Health First philosophy is preserved.
Existing architecture remains consistent.
Naming follows project conventions.
Future extensibility is maintained.
Administrative management is considered.
AI integration remains compatible.
Privacy and security are respected.

8. Final Review
Before finalizing any document, internally verify:
✓ No duplicated concepts
✓ No architectural conflicts
✓ Consistent terminology
✓ Consistent naming
✓ Consistent document references
✓ Healthcare-first philosophy maintained
Only after passing this review should the document be considered complete.
End of Patch.

───
Documentation Maintenance Rule
Whenever a document is created, removed, renamed, or reaches Stable status, Codex must also review ARCHITECTURE_INDEX.md.
If the document affects the project structure, Codex must:
1. Update the appropriate category in ARCHITECTURE_INDEX.md.
2. Update the dependency map if relationships changed.
3. Update the document lifecycle if necessary.
4. Report both modified documents in the final response.
This maintenance step is mandatory for every documentation change.
End of Patch.

───
# Error Handling Rule

Every feature must define:

- Failure scenarios
- Recovery strategy
- Offline behavior
- User-facing message
- Logging policy

No feature is considered complete until its error handling has been documented.

End of Patch.

───
# Document Metadata Standard

Every Markdown architecture document should begin with the following metadata:

- Document Name
- Version
- Status
- Owner
- Last Updated
- Purpose

Status values:

Draft

Review

Stable

Deprecated

When creating new documents, always follow this metadata format.

End of Patch.

───
# Terminology Rule

Before introducing a new architectural, technical, gameplay, healthcare, or UX term:

1. Review GLOSSARY.md.
2. Reuse existing official terminology whenever possible.
3. If a new term is required, add it to GLOSSARY.md before using it in any other document.
4. Report terminology conflicts before modifying documents.

This rule is mandatory for all future documentation updates.

End of Patch.