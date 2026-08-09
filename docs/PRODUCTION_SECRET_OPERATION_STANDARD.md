# Production Secret Operation Standard

## Operating standard

| Stage | Secret storage and provision | Status |
| --- | --- | --- |
| Local development | Developers provide values outside Git (for example, their local process environment). `.env.example` is a placeholder-only reference when available; automatic `.env` loading remains UNKNOWN. | CONFIRMED boundary / UNKNOWN loader |
| CI | Use GitHub Secrets only when CI is actually configured and a CI job requires a value. Do not create or populate GitHub Secrets while CI is absent. | CONFIRMED policy / CI 미구성 또는 저장소 근거 없음 |
| MVP production | Immediately before deployment, select exactly one of Render, Railway, AWS, or GCP. Store required MVP values in that selected platform's Environment Variables. | CONFIRMED policy / platform UNKNOWN until selection |
| Long-term production | Use AWS Secrets Manager or GCP Secret Manager, chosen with the long-term deployment platform and ownership model. | CONFIRMED target / provider selection UNKNOWN |

## Access rules

- Apply least privilege: grant access only to the person or workload that needs a secret for its approved task.
- Never commit actual secrets, tokens, passwords, or connection strings to Git, documentation, issues, PRs, logs, or `.env.example`.
- Keep local, CI, and production values separate. A value approved for one environment must not be reused in another without an explicit security decision.
- Record access grants, revocations, and production configuration changes in the selected platform's approved audit trail when a platform is chosen.

## Platform-selection gate

Before MVP deployment, the current developer must choose Render, Railway, AWS, or GCP and record: the selected platform, environment boundary, service identities, required secret names, access roles, audit location, and rollback owner. Until then, all of those implementation details are **UNKNOWN**.

## Required implementation WP before deployment

A separate approved implementation WP must configure the selected platform's environment variables, least-privilege access, deployment documentation, audit/rotation procedure, and production verification. This WP does not configure any platform or secret.
