# DATABASE OVERVIEW

Version: 1.0

---

# Purpose

This document defines the overall database architecture of Guild Health.

It explains the responsibilities of each domain,
the relationships between domains,
and the principles that every database table must follow.

This document does NOT define individual tables.

Individual schemas are maintained in separate documents.

---

# Database Philosophy

Guild Health is designed using Domain Driven Design (DDD).

Every table belongs to exactly one domain.

Business logic should never be mixed across domains.

Cross-domain communication should occur only through well-defined services.

---

# Database Domains

The database consists of the following domains.

## Core

Users

Profiles

Authentication

Settings

Notification

Devices

Sessions

---

## Health

Exercises

Exercise Records

Meals

Foods

Nutrition

Body Records

Health Score

AI Food Analysis

---

## RPG

Heroes

Hero Stats

Equipment

Inventory

Tower

Battle

Monster

Quest

Achievement

Title

---

## Progression

Experience

Level

Point

Trust

Daily Quest

Weekly Quest

Mission

Reward

Season

---

## Community

Leaderboard

Friend

Guild

Guild Member

Guild Quest

Raid

World Event

---

## AI

AI Coach

Emotion Log

Recommendation

Prompt History

AI Conversation

Analytics

---

# General Rules

Every table must

- Have UUID Primary Key
- Have created_at
- Have updated_at
- Use soft delete whenever possible
- Use UTC timestamps
- Be fully normalized unless performance requires otherwise

---

# Naming Convention

Tables

snake_case

Columns

snake_case

Primary Key

id

Foreign Key

{table_name}_id

Booleans

is_xxx

has_xxx

Dates

xxx_at

---

# Relationship Rules

One-to-One

Only when absolutely necessary.

One-to-Many

Preferred.

Many-to-Many

Always use junction tables.

Never store arrays of foreign keys.

---

# Index Strategy

Index

Foreign Keys

Frequently searched columns

Sorting columns

Leaderboard columns

Season columns

---

# Soft Delete Policy

Use deleted_at.

Never physically delete user data unless legally required.

---

# Security

Personal information must be isolated.

Sensitive data should never be duplicated.

Health data requires strict ownership validation.

---

# Scalability

The database must support

10 million users

100 million exercise records

Unlimited tower floors

Unlimited seasons

Unlimited quests

Unlimited achievements

Unlimited AI logs

without requiring architectural redesign.

---

# Consistency Checklist

Must remain consistent with

PROJECT_CONSTITUTION.md

PRODUCT_VISION.md

ENGINE_RULES.md

MASTER_DATA.md

LORE.md

Conflict Status

None
