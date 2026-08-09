# Render Deployment Implementation Guide

- Service type: Web Service; branch: `main`; service name: `health-is-all-api`; region: Singapore; plan: Free.
- Root directory: repository root. Runtime: Docker. Build command: Render Docker build from root `Dockerfile`. Start command: Docker `CMD` invoking `uvicorn backend.main:app` on `0.0.0.0` and Render `PORT`.
- Health check path: `/healthz`; it does not run migrations or query the DB.
- In Render Dashboard, the user enters only `DATABASE_URL` as a runtime Environment Variable. Do not enter a value in source, build args, `render.yaml`, or documentation.
- User actions: connect GitHub repository, select `main`, confirm Docker service settings, add `DATABASE_URL`, deploy, then verify `/healthz`.
