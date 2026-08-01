# API SPECIFICATION

Version: 1.0

---

# Purpose

This document defines the API contract for Guild Health.

The API must remain independent from client implementations.

Clients may include:

- Web
- iOS
- Android
- Smart Watch
- Admin CMS

---

# API Principles

RESTful

Versioned

Stateless

Secure

Consistent

Documented

---

# Authentication

Bearer Token

Refresh Token

Role-based Authorization

Device Validation

---

# Main API Domains

Authentication

User

Health

Exercise

Habit

Analytics

AI

Quest

Progression

Companion

Tower

Notification

Admin

---

# Response Format

Every response contains:

success

data

error

meta

timestamp

request_id

---

# Error Format

Every error contains:

error_code

message

details

request_id

---

# Pagination

Cursor-based pagination is preferred.

Offset pagination may be used for administrative pages.

---

# API Versioning

URI Versioning

Example:

/api/v1/

Future versions:

/api/v2/

Deprecated APIs must remain available during the migration period.

---

# Security

HTTPS only.

Sensitive health data must always be encrypted in transit.

Role validation is required for every protected endpoint.

---

# Performance

Support:

Compression

Caching

Rate Limiting

Idempotency where appropriate

---

# Future Expansion

Support:

GraphQL Gateway

Public API

Partner API

Healthcare Provider API

Webhook

without architectural redesign.

---

# Consistency Checklist

Must remain consistent with:

DOMAIN_DESIGN.md

ENGINE_OVERVIEW.md

DATABASE_01_CORE.md

DATABASE_02_HEALTH.md

DATABASE_03_RPG.md

Conflict Status

None
