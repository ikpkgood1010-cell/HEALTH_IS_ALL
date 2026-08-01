# ADMIN CMS SPEC

Version: 1.0

---

# Purpose

This document defines the administrator management system (CMS) for Guild Health.

The CMS allows operators to manage content, balance, events, rewards, AI prompts, and game systems without modifying application code.

The CMS is a core part of the platform and must support long-term live operations.

---

# Core Principles

- Every configurable feature should be editable through the CMS.
- Business rules should be data-driven whenever possible.
- Changes should not require application deployment.
- Every change must be logged.
- Dangerous operations require confirmation and permission.

---

# Administrator Roles

## Super Admin

Full access.

Can manage every system.

---

## Game Designer

Can edit:

- Exercise Master
- EXP Rules
- Health Score Rules
- Quests
- Rewards
- Equipment
- Monsters
- Tower
- Events

Cannot access user personal information.

---

## Community Manager

Can manage:

- Announcements
- Notices
- Events
- Leaderboards
- Guild Events
- Reports

Cannot modify game balance.

---

## AI Manager

Can manage:

- AI Prompt Templates
- AI Coach Messages
- Health Tips
- Motivation Messages

Cannot modify EXP or rewards.

---

## Customer Support

Can:

- View user accounts
- Restore deleted records
- Correct exercise records
- Respond to reports

Cannot modify Master Data.

---

# CMS Modules

The CMS includes the following modules.

---

## Dashboard

Displays:

- Daily Active Users
- Exercise Count
- New Users
- AI Usage
- Server Status
- Event Status

---

## User Management

Functions

- Search users
- Suspend account
- Restore account
- View activity history
- View Health Score history

---

## Exercise Management

Functions

- Add exercise
- Edit exercise
- Disable exercise
- Configure input fields
- Configure validation
- Configure EXP rule
- Configure Health Score rule
- Configure AI prompt
- Configure animations
- Configure icons

---

## Quest Management

Functions

- Create quests
- Weekly quests
- Daily quests
- Hidden quests
- Seasonal quests
- Reward configuration

---

## RPG Management

Functions

- Hero classes
- Equipment
- Monsters
- Tower floors
- Battle balance
- Companion trust values

---

## Health Management

Functions

- Health Score rules
- Trust rules
- Recovery rules
- Daily summary rules

---

## AI Management

Functions

- Prompt library
- Prompt versioning
- Health advice
- Exercise advice
- Food analysis prompts

---

## Event Management

Functions

- Seasonal events
- Weekend bonus
- EXP events
- Tower events
- Guild events

---

## Feature Flag Management

Functions

Enable

Disable

Beta Only

Internal Only

Percentage Rollout

---

## Master Data Management

Editable

- Exercise Categories
- Equipment Master
- Monster Master
- Item Master
- Achievement Master
- Title Master
- Badge Master
- Avatar Master
- Health Score Formula
- EXP Formula
- Trust Formula

---

## Audit Log

Every CMS action must record:

- Administrator
- Timestamp
- Module
- Action
- Before Value
- After Value
- IP Address

Audit logs are immutable.

---

# Permission Rules

Every API endpoint must validate administrator permissions.

No permission inheritance is assumed.

Least privilege principle applies.

---

# Safety Rules

Deletion of master data is prohibited.

Instead:

- Disable
- Archive
- Version

must be used.

---

# Versioning

Every configurable object supports:

- Version
- Effective Date
- Change Log
- Rollback

---

# Future Expansion

The CMS architecture must support:

- Multi-language management
- A/B testing
- Live balance updates
- AI-assisted content generation
- Analytics dashboards
- Plugin management

without architectural redesign.

---

# Consistency Checklist

Must remain consistent with:

PROJECT_CONSTITUTION.md

ENGINE_OVERVIEW.md

MASTER_DATA.md

DATABASE_02_HEALTH.md

RULE_ENGINE.md

Conflict Status

None
