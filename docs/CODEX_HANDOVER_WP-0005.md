# Codex Handover — WP-0005

Work only on `codex/wp-0005-runtime-secret-governance`. The only allowed changes are the two WP control documents and the three WP-0005 result documents.

For each variable or variable group, record: use location, loading actor, precedence, local-development provision, production provision, owner, evidence, and confidence. Distinguish a code lookup from a `.env` loader, a compose declaration, and a deployment secret-injection mechanism.

If CI files are absent, record “CI not configured or no repository evidence” and do not create them. If production injection is unproven, list only possible choices and the role required to decide; do not select or implement a tool.
