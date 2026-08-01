# SYSTEM ARCHITECTURE

Version: 1.0

Guild Health uses DDD, Clean Architecture, and Event-Driven Architecture.

Layers: Presentation, Application, Domain, Infrastructure, Database. Presentation contains UI only; Application executes use cases; Domain owns rules and interfaces; Infrastructure adapts Supabase, OpenAI, storage, auth, analytics, and notifications.

Health events initiate downstream work: a completed exercise is validated and saved; independent handlers calculate health/progression, update quests and achievements, resolve RPG presentation, update statistics/leaderboard, create notifications, and generate supportive guidance.

Health Score evaluates exercise, nutrition, recovery, hydration, and consistency through Master Data. Overtraining reduces efficiency and recovery is rewarded. AI is an encouraging wellness coach, never a judge or medical authority.
