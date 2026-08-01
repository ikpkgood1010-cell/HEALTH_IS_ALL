# RULE ENGINE

Version: 1.0

---

# Purpose

The Rule Engine is responsible for evaluating every configurable game and health rule within Guild Health.

Business logic must not be hard-coded whenever possible.

Rules are evaluated dynamically using Master Data and engine configuration.

---

# Core Philosophy

Rules are data.

Not code.

Every calculation should be configurable.

Every rule should support versioning.

Every rule should support rollback.

---

# Supported Rule Types

- EXP Rule
- Health Score Rule
- Trust Rule
- Quest Rule
- Battle Rule
- Reward Rule
- Event Rule
- Leaderboard Rule
- AI Trigger Rule
- Achievement Rule

---

# Rule Structure

Every rule contains:

- Rule ID
- Rule Name
- Rule Category
- Version
- Status
- Priority
- Effective Date
- Expiration Date
- Created By
- Updated By

---

# Rule Evaluation Order

1. Validate Input

↓

2. Load Rule

↓

3. Evaluate Conditions

↓

4. Execute Formula

↓

5. Apply Modifiers

↓

6. Save Result

↓

7. Trigger Events

---

# Formula Support

The engine supports:

Addition

Subtraction

Multiplication

Division

Percentage

Clamp

Minimum

Maximum

Round

Ceiling

Floor

Conditional

Nested Formula

---

# Variables

Formula may access:

Exercise Duration

Exercise Distance

Exercise Difficulty

Exercise Intensity

Heart Rate

Calories

Tower Floor

Player Level

Health Score

Trust

Season Bonus

Weekend Bonus

Guild Bonus

Equipment Bonus

Event Bonus

---

# Rule Priority

Highest

Emergency Override

↓

Season Event

↓

Weekend Event

↓

Special Event

↓

Exercise Rule

↓

Default Rule

---

# Versioning

Each rule has:

Version

Effective From

Effective To

Rollback Support

Rules used for historical calculations must never be modified.

---

# Rule Execution

Rules must be deterministic.

The same input must always produce the same output.

---

# Rule Logging

Every evaluation stores:

Rule Version

Input

Output

Execution Time

Success

Failure Reason

---

# Performance

Frequently used rules should be cached.

Rule cache must refresh automatically after updates.

---

# Future Expansion

Support:

AI Generated Rules

Rule Simulation

Rule Testing

A/B Rule Comparison

Live Rule Switching

without architecture redesign.

---

# Consistency Checklist

Must remain consistent with:

MASTER_DATA.md

ENGINE_OVERVIEW.md

DATABASE_02_HEALTH.md

ADMIN_CMS_SPEC.md

PROJECT_CONSTITUTION.md

Conflict Status

None
