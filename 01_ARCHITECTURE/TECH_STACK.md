# TECH STACK

Document Name: TECH_STACK.md
Version: 1.1
Status: Review
Owner: Guild Health Architecture
Last Updated: 2026-07-28
Purpose: Define the official technology stack for Guild Health as the single source of truth across frontend, backend, infrastructure, AI, testing, and deployment.

---

# Architecture Principles

Technology choices must:

- Support long-term maintainability.
- Be scalable.
- Be testable.
- Minimize vendor lock-in where practical.
- Prioritize reliability for healthcare services.

---

# Frontend

- **Framework**: Flutter
- **Language**: Dart
- **State Management**: Riverpod
- **Routing**: GoRouter
- **Networking**: Dio
- **Local Database**: Isar (Offline Caching & Local Storage)
- **Dependency Injection**: Riverpod Providers

---

# Backend

- **Framework**: NestJS
- **Language**: TypeScript
- **Database**: PostgreSQL
- **Cache**: Redis
- **ORM**: Prisma
- **API**: REST (GraphQL may be evaluated in the future)

---

# AI

- **Provider**: OpenAI (through an abstraction layer)
- **Requirement**: AI providers must be replaceable without changing business logic.

---

# Notifications

- **Service**: Firebase Cloud Messaging (FCM)

---

# Analytics

- **External Analytics**: Firebase Analytics
- **Internal Storage**: Internal Analytics Database

---

# Authentication

- **Mechanism**: JWT (JSON Web Tokens)
- **Session Control**: Refresh Token Strategy
- **Extension**: OAuth expansion support (Apple / Google Auth)

---

# File Storage

- **Storage Type**: S3-compatible Object Storage

---

# Monitoring

- **Crash Reporting**: Firebase Crashlytics
- **Observability**: See OBSERVABILITY.md for telemetry, tracing, and log metrics.

---

# CI/CD

- **Automation**: GitHub Actions
- **Containerization**: Docker

---

# Testing

- Unit Test
- Integration Test
- Widget Test
- End-to-End Test

---

# Vendor Lock-in Policy

Third-party services should be replaceable whenever practical.

Business logic must not directly depend on vendor-specific SDKs.

Prefer abstraction layers for AI, Storage, Analytics, and Notification providers whenever feasible.

---

# Technology Adoption Criteria

Before adopting any new technology evaluate:

- Community maturity
- Long-term maintenance
- Documentation quality
- Testing support
- Performance impact
- Security considerations
- Healthcare compliance impact

Technology decisions should be documented before adoption.

---

# Technology Review Policy

Technology changes must be reviewed before adoption and reflected in this document.

---

# Related Documents

- FLUTTER_PROJECT_STRUCTURE.md
- BACKEND_PROJECT_STRUCTURE.md
- API_SPECIFICATION.md
- OBSERVABILITY.md
- ARCHITECTURE_INDEX.md