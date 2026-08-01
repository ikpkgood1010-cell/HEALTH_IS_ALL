# Architecture Decision Records (ADR)

## Overview
This document logs all key Architectural Decisions (ADRs) for the project. Each record captures the context, decision, status, consequences, and compliance guidelines.

---

## Table of Contents
1. [ADR-001: Adoption of Modular Monolith Architecture](#adr-001-adoption-of-modular-monolith-architecture)
2. [ADR-002: Primary Database Selection (PostgreSQL)](#adr-002-primary-database-selection-postgresql)
3. [ADR-003: Asynchronous Event Messaging via Redis Streams](#adr-003-asynchronous-event-messaging-via-redis-streams)
4. [ADR-004: JWT with Refresh Token Rotation for Authentication](#adr-004-jwt-with-refresh-token-rotation-for-authentication)
5. [ADR-005: Containerization & CI/CD Pipeline Standardization](#adr-005-containerization--cicd-pipeline-standardization)

---

## ADR-001: Adoption of Modular Monolith Architecture

* **Status:** Accepted
* **Date:** 2026-07-28
* **Authors:** Software Architecture Team

### Context
We need to design a system architecture that supports rapid feature development, high maintainability, clear domain boundaries, and simple deployment while keeping operational overhead low in early-to-mid scale stages.

### Decision
We choose a **Modular Monolith** architecture over a distributed Microservices approach at this stage. 
- High cohesion and low coupling within domain modules.
- Strict interface boundaries enforced at code/package levels.
- Shared database instance with separate schemas per domain.

### Consequences
* **Positive:**
  - Simplified deployment (single artifact / container).
  - Fast local development and test setup without complex service mocking.
  - No distributed tracing overhead or RPC network latency.
* **Negative:**
  - Requires discipline to prevent cross-module dependency leaks.
  - Scaling is monolithic (entire application scales together), though memory footprint remains modest.

---

## ADR-002: Primary Database Selection (PostgreSQL)

* **Status:** Accepted
* **Date:** 2026-07-28
* **Authors:** Database Architecture Team

### Context
The application handles structured transactional data with strong consistency requirements, complex relational queries, and needs support for JSON document structures and geospatial data.

### Decision
Use **PostgreSQL** as the primary relational database management system (RDBMS).

### Consequences
* **Positive:**
  - ACID compliance and robust transactional integrity.
  - Excellent support for JSONB, indexing (GIN/GiST), and extension ecosystem (e.g., PostGIS).
  - Strong community support and managed cloud platform availability.
* **Negative:**
  - Vertical scaling limitations for extreme write loads (mitigated by read-replicas and partitioning when needed).

---

## ADR-003: Asynchronous Event Messaging via Redis Streams

* **Status:** Accepted
* **Date:** 2026-07-28
* **Authors:** Backend Engineering Team

### Context
To keep domain modules decoupled, asynchronous events (e.g., notification triggers, log ingestion, background task processing) need to be published and consumed reliably without blocking HTTP request threads.

### Decision
Utilize **Redis Streams** for lightweight, in-memory asynchronous message queuing and event pub/sub.

### Consequences
* **Positive:**
  - Reuses existing Redis infrastructure (low cost and operational overhead).
  - Supports consumer groups, message persistence, and offset management.
  - Minimal latency for real-time task distribution.
* **Negative:**
  - Not designed for multi-year immutable event sourcing compared to Kafka (short-to-medium retention period configured).

---

## ADR-004: JWT with Refresh Token Rotation for Authentication

* **Status:** Accepted
* **Date:** 2026-07-28
* **Authors:** Security & Auth Team

### Context
User authorization across client applications (Web, Mobile) requires secure, stateless request verification with token revoke capabilities for compromised sessions.

### Decision
Implement **Short-lived Access Tokens (JWT)** combined with **Refresh Tokens stored in HTTP-only, Secure Cookies** using a Refresh Token Rotation strategy backed by Redis blacklisting.

### Consequences
* **Positive:**
  - Microservices/API routes can verify requests statelessly using public keys.
  - Mitigates XSS vulnerabilities via HttpOnly cookie storage.
  - Detects token reuse attacks automatically by invalidating token families upon unauthorized refresh attempts.
* **Negative:**
  - Requires server state management in Redis for active refresh token verification and invalidation.

---

## ADR-005: Containerization & CI/CD Pipeline Standardization

* **Status:** Accepted
* **Date:** 2026-07-28
* **Authors:** DevOps Team

### Context
Deployment environments must be consistent across local development, staging, and production to eliminate "works on my machine" issues and enable automated testing.

### Decision
Standardize application packaging using **Docker** containers and automate delivery using **GitHub Actions** with strict linting, security scanning, and unit/integration test gates.

### Consequences
* **Positive:**
  - Reproducible builds across environments.
  - Automated quality assurance preventing broken builds from reaching main branch.
  - Seamless integration with Kubernetes / Cloud Run container runners.
* **Negative:**
  - Image size optimization and caching strategies must be maintained in Dockerfiles.
