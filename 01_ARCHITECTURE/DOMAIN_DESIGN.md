# DOMAIN DESIGN

Version: 1.0

Guild Health applies DDD. Health activity is the sole authoritative source of game growth.

Domains: Authentication, User, Healthcare, AI, RPG, Social, Reward, and System.

Dependencies flow Authentication → User → Healthcare → AI → Reward → RPG → Social → System. Healthcare produces events; Reward, RPG, Social, and System independently consume them.

Domains remain independently deployable/testable, avoid direct database coupling, communicate through services, interfaces, or events, and never form circular dependencies. AI analyzes and recommends; it does not alter health records.
