# BACKEND PROJECT STRUCTURE

Document Name: BACKEND_PROJECT_STRUCTURE.md
Version: 1.0
Status: Draft
Owner: Guild Health Architecture
Last Updated: 2026-07-28
Purpose: Define the official NestJS backend project architecture for Guild Health. This document serves as the single source of truth for backend project organization, Clean Architecture boundaries, Prisma/Redis integrations, shared infrastructure modules, and module dependencies, following TECH_STACK.md.

---

# 1. Project Directory Structure

Guild Health NestJS applications follow a **Modular Monolith** pattern organized under `src/`:

```text
src/
├── main.ts                   # Application bootstrap & entry point
├── app.module.ts             # Root application module orchestrating sub-modules
├── common/                   # Global shared utilities, guards, pipes, interceptors
│   ├── decorators/           # Custom NestJS decorators (@CurrentUser, @Public)
│   ├── dto/                  # Common request/response pagination & wrapper DTOs
│   ├── exceptions/           # Domain & infrastructure exception types
│   ├── filters/              # Global Exception Filters
│   ├── interceptors/         # Global Logging & Response Transformation Interceptors
│   ├── middleware/           # HTTP Request Middleware (Correlation ID, Rate Limiting)
│   └── pipes/                # Global Validation Pipes
├── core/                     # Core infrastructure modules (Shared Singleton Services)
│   ├── auth/                 # JWT Authentication & OAuth strategies
│   ├── config/               # Environment configuration with Zod validation
│   ├── database/             # Prisma Service & Database Connection Lifecycle
│   ├── events/               # Event Emitter & Event Bus infrastructure
│   ├── logging/              # Structured Logger Module (Winston / Pino)
│   ├── queue/                # Redis BullMQ Queue configuration
│   └── redis/                # Redis Cache Service & Client Lifecycle
├── modules/                  # Domain-driven feature modules
│   ├── health/               # Health Vitals & Daily Record domain
│   ├── habit/                # Habit tracking & engine domain
│   ├── quest/                # RPG Quests & Gamification domain
│   ├── progression/          # Guild & Progression domain
│   ├── ai_coach/             # AI Coach & Insight Generation domain
│   └── user/                 # User Profile & Identity domain
└── test/                     # End-to-End (E2E) testing suite