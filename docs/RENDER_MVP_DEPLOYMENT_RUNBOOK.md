# Render MVP Deployment Runbook

## User-performed GUI steps

1. In Render Dashboard, create a new Web Service and connect the GitHub repository.
2. Select the approved deployment branch and repository root.
3. Select Docker runtime using the root Dockerfile; confirm the backend application target and health check `/healthz`.
4. Choose Render PostgreSQL or an approved external PostgreSQL provider before adding DB variables.
5. In Render Dashboard Environment Variables, enter only approved runtime variable names and values. Do not use GitHub Secrets while CI is absent.
6. Deploy, use the Render service URL to check `/healthz`, and record the service owner/audit location outside source control.

## Preconditions and UNKNOWNs

- Render account/project, branch, region, plan, service name, custom domain, database provider, and production port adaptation are UNKNOWN.
- A separate implementation WP is required for any port-code, CORS, DB migration, render.yaml, CI, frontend hosting, or production verification change.
