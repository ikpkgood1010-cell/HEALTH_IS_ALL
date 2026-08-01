DOCUMENT_DEPENDENCY_MATRIX

Purpose
본 문서는 프로젝트 내 모든 문서 간의 참조 관계 및 수정 시 파급 효과(Impact Range)를 정의한다.

Scope
• SSOT 문서, 하위 기능 문서, 구현 사양서 간의 상호 연결 구조 표기

SSOT
본 문서는 문서 수정 영향도 분석의 단일 진실 출처(SSOT)이다.

Rules
1. 문서 의존성 체계 표:


최상위 SSOT 문서
하위 참조 문서
영향을 받는 시스템
수정 시 점검 사항

GAMEPLAY_LOOP_MASTER.md
QUEST_SYSTEM.md, HABIT_SYSTEM.md
UX 흐름, AI 피드백, Flutter 메인
루프 파손 및 이벤트 누락 여부

ECONOMY_MASTER.md
EXP_RULE.md, POINT_RULE.md
Backend DB, 상점, 보상 엔진
인플레이션 및 재화 교차 오류

CANONICAL_NAMING.md
프로젝트 내 모든 .md 및 Source Code
전체 시스템, AI Prompt
금지 용어 잔재 여부 검수

ANTI_GRIND_POLICY.md
EXP_RULE.md, POINT_RULE.md
Backend Interceptor
정상 유저 경험 저해 여부



1. 문서 수정 시 필수 절차: 
◦ 상위 SSOT 변경 시 하위 참조 문서를 반드시 동일 Patch 내에서 동시 업데이트해야 한다.

Runtime
• 문서 수정 작업 시 본 매트릭스를 확인하여 영향을 받는 문서 목록을 Change Log에 명시한다.

Examples
• EXP_RULE.md 수식이 변경되면 ECONOMY_MASTER.md 및 Backend 계산 모듈에 영향이 미치므로 동시 검수 필요.

Forbidden
• 상위 SSOT 수정 후 하위 의존 문서를 업데이트하지 않고 남겨두어 문서 간 충돌을 야기하는 행위.

Related Documents
• START_HERE.md
• 00_PROJECT/PATCH_HISTORY/PATCH_001_CHANGELOG.md

Change History
• 2026-07-31: PATCH-001 최초 매트릭스 수립 (Gemini)