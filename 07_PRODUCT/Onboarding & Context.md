Onboarding & Context (개발자 및 AI 에이전트 단일 진입점 명세)

1. 개요 (Overview)
본 문서는 HEALTH IS ALL 프로젝트에 처음 참여하는 사람 신규 개발자 및 AI 에이전트(Codex, Claude, GPT 등)를 위한 단일 통합 온보딩 및 컨텍스트 가이드(Single Entry Point) 입니다. 기존의 START_HERE.md, README_FOR_CODEX.md, AI_HANDOFF.md에 파편화되어 있던 안내를 하나로 일원화하여 개발 진입점 혼선을 제거합니다.

───

2. 프로젝트 핵심 철학 (Core Philosophy)

• Health-First & Positive Psychology: 단순한 게임성(Gamification)이나 수치 달성을 위해 사용자의 신체적·정신적 건강을 해치는 설계를 엄격히 금지합니다.
• Single Source of Truth (SSOT) : 데이터, UI 명세, 용어, 연쇄 영향도는 정의된 문서와 매트릭스를 절대적 기준으로 삼습니다.
• Non-Punitive Design: 목표 미달성, 연속 달성(Streak) 끊김 시 사용자를 질책하거나 불이익을 주지 않고, 휴식의 가치를 인정하며 따뜻하게 맞이합니다.

───

3. 디렉토리 구조 및 레이어 아키텍처 (Directory & Layering)

프로젝트는 4대 핵심 레이어 아키텍처를 따릅니다.

text
[ 01_ARCHITECTURE ]  → 도메인 규칙, SSOT 마스터 문서, 헬스 데이터 거버넌스
[ 02_DATABASE ]      → Core, Health, Spirit, Progression DB 스키마 및 ReadModel
[ 03_BACKEND ]       → Health, Exercise, Meal, Spirit, Progression 핵심 엔진
[ 04_FRONTEND ]      → Screen Specification Master, Component Catalog (Flutter)
[ 05_AI_AGENTS ]     → System Prompts, Context Sync, Product Language Rules