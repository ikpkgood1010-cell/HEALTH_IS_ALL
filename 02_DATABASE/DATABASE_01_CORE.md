# DATABASE_01_CORE

Version: 1.0

---

# Purpose

This document defines the Core Domain of Guild Health.

The Core Domain manages account identity,
authentication,
devices,
sessions,
and user profile information.

Every other domain depends on this domain.

---

# Design Principles

The Core Domain must remain independent from Health, RPG, AI, and Community domains.

Core tables should never contain business-specific fields.

Authentication and Profile are separated.

Every table uses UUID as the primary key.

Soft Delete is used whenever possible.

---

# Entity Relationship

Account
 ├── Authentication
 ├── OAuthAccount
 ├── Session
 ├── Device
 ├── UserProfile
 ├── UserSetting
 └── NotificationPreference

---

# TABLE : account

Purpose

Represents the root identity of a Guild Health member.

This table owns authentication,
subscription,
device,
and profile information.

Primary Key

id (UUID)

Columns

id

email

email_verified_at

status

role

last_login_at

created_at

updated_at

deleted_at

Indexes

email (Unique)

status

last_login_at

Rules

Email must be unique.

Email cannot be changed without verification.

Physical deletion is prohibited.

Relationships

1 Account

↓

Many Sessions

Many Devices

Many OAuth Accounts

1 User Profile

1 User Setting

1 Notification Preference

---

# TABLE : authentication

Purpose

Stores authentication credentials.

Separated from account for future extensibility.

Primary Key

id (UUID)

Columns

id

account_id

password_hash

password_updated_at

failed_login_count

locked_until

created_at

updated_at

Indexes

account_id

Rules

Never store plain passwords.

Passwords must be hashed using Argon2id.

---

# TABLE : oauth_account

Purpose

Stores external login providers.

Supported Providers

Google

Apple

Kakao

Future providers

Columns

id

account_id

provider

provider_user_id

provider_email

connected_at

created_at

Indexes

(provider, provider_user_id)

account_id

Rules

One provider account cannot belong to multiple Guild Health accounts.

---

# TABLE : session

Purpose

Tracks active login sessions.

Columns

id

account_id

device_id

access_token_version

refresh_token_version

ip_address

user_agent

last_activity_at

expires_at

created_at

Indexes

account_id

expires_at

last_activity_at

Rules

Expired sessions are invalid.

Support multiple simultaneous devices.

---

# TABLE : device

Purpose

Stores trusted user devices.

Columns

id

account_id

device_type

platform

os_version

app_version

device_name

last_active_at

is_trusted

created_at

Indexes

account_id

platform

last_active_at

Rules

Users may own multiple devices.

Unknown devices require verification.

---

# Common Columns

Every table must contain

id

created_at

updated_at

deleted_at (if applicable)

---

# Timestamp Standard

All timestamps use UTC.

Application layer converts to local time.

---

# Soft Delete Policy

Use deleted_at.

Never physically delete account-related records.

---

# Index Strategy

Unique indexes

email

provider + provider_user_id

Search indexes

account_id

status

expires_at

last_activity_at

---

# Constraints

Email must be unique.

OAuth provider identity must be unique.

Session must belong to one account.

Device must belong to one account.

---

# Security Principles

Passwords are never reversible.

Tokens are never stored in plain text.

Authentication data is isolated from profile data.

Least privilege principle applies.

---

# Future Expansion

This schema supports

- Premium subscriptions
- Multi-factor authentication
- Passkeys
- Enterprise accounts
- Family accounts
- Multi-language profiles
- Cross-platform synchronization

without schema redesign.

---

# Consistency Checklist

This document must remain consistent with

- PROJECT_CONSTITUTION.md
- PRODUCT_VISION.md
- DATABASE_00_OVERVIEW.md
- ENGINE_RULES.md
- MASTER_DATA.md
- LORE.md

Conflict Status

None
