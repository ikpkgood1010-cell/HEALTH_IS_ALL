# FLUTTER PROJECT STRUCTURE

Document Name: FLUTTER_PROJECT_STRUCTURE.md
Version: 1.1
Status: Review
Owner: Guild Health Architecture
Last Updated: 2026-07-28
Purpose: Define the official Flutter project architecture for Guild Health. This document is the single source of truth for Flutter project organization, directory layout, Clean Architecture boundaries, and coding conventions, following TECH_STACK.md.

---

# 1. Project Directory Structure

Guild Health Flutter applications adopt a **Feature-First + Clean Architecture** hybrid layout under the `lib/` directory.

```text
lib/
├── app/                      # Application root configuration & bootstrap
│   ├── app.dart              # MaterialApp / Riverpod root configuration
│   ├── bootstrap.dart        # Async initializations (Isar, FCM, Hydrated State)
│   ├── router/               # GoRouter configuration & routes
│   └── theme/                # Global Theme & Design System integration
├── core/                     # Shared core utilities, base classes, network & storage
│   ├── constants/            # Global constants & keys
│   ├── error/                # Exception types & Failure models
│   ├── logging/              # Logging infrastructure (Talker / Logger)
│   ├── network/              # Dio client, Interceptors, API endpoints
│   ├── storage/              # Isar database instances & helpers
│   ├── utils/                # Date, string, math helpers
│   └── widgets/              # Reusable generic UI components (Design System wrappers)
├── features/                 # Domain-driven feature modules
│   ├── health/               # Health feature domain (Vitals, Sleep, Activity)
│   ├── habit/                # Habit engine & tracking UI
│   ├── quest/                # Gamified Quest & RPG elements
│   ├── progression/          # Guild & Progression UI
│   ├── ai_coach/             # AI Insight & Chat interface
│   ├── profile/              # User profile & settings
│   └── auth/                 # Authentication & onboarding
├── l10n/                     # Internationalization (ARB files)
└── main.dart                 # Application entry point