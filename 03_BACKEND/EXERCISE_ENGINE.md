# EXERCISE ENGINE

Version: 1.0

---

# Purpose

The Exercise Engine is the foundation of Guild Health.

Every exercise is treated as a configurable plugin rather than hard-coded functionality.

The application generates UI, validation, rewards, AI coaching, and progression from exercise definitions.

---

# Core Philosophy

Exercises are data.

Not code.

Adding or modifying an exercise should not require application updates.

Administrators should be able to configure exercise behavior through Master Data.

---

# Exercise Plugin Structure

Each exercise consists of:

- Metadata
- Input Components
- Validation Rules
- EXP Rules
- Health Score Rules
- AI Prompt Template
- Quest Mapping
- Achievement Mapping
- Battle Reward Mapping
- Leaderboard Rule
- Animation
- Sound Effect

---

# Metadata

Contains:

- Exercise ID
- Name
- Category
- Difficulty
- Intensity
- Default Icon
- Display Order
- Active Status

---

# Input Components

Input UI is generated dynamically.

Supported Components:

- Number Input
- Decimal Input
- Time Picker
- Date Picker
- Distance Picker
- Step Counter
- Altitude Input
- Weight Input
- Repetition Input
- Dropdown
- Multi Select
- Toggle
- Text Input
- Image Upload
- GPS Route
- Heart Rate
- Calories
- Custom Component

---

# Validation Rules

Each field supports:

- Required
- Minimum Value
- Maximum Value
- Default Value
- Placeholder
- Unit
- Tooltip
- Error Message

Validation rules are configurable.

---

# Dynamic UI Generation

Exercise Form

↓

Read Exercise Definition

↓

Generate Components

↓

Apply Validation

↓

Save Data

No exercise screen should be hard-coded.

---

# Reward Rules

Each exercise defines:

Base EXP

Bonus EXP

Health Score Contribution

Trust Contribution

Point Bonus (Special Events Only)

---

# AI Integration

Each exercise defines:

Completion Prompt

Recovery Prompt

Motivation Prompt

Warning Prompt

Educational Tip

AI prompts are configurable.

---

# Battle Integration

Exercise completion may trigger:

Battle Progress

Tower Progress

Quest Progress

Companion Trust

Equipment Experience

Event Progress

---

# Seasonal Support

Each exercise may define:

Season Bonus

Event Bonus

Weekend Bonus

Challenge Bonus

---

# Future Support

Exercise Plugins must support:

- Smart Watch
- Wear OS
- Apple Watch
- Bluetooth Devices
- AI Detection
- Motion Recognition
- Voice Input

without architecture changes.

---

# Consistency Checklist

Must remain consistent with:

ENGINE_OVERVIEW.md

MASTER_DATA.md

DATABASE_02_HEALTH.md

PRODUCT_VISION.md

ENGINE_RULES.md

Conflict Status:
None
