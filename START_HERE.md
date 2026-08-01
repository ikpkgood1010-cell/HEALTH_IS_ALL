START_HERE - HEALTH IS ALL 개발자 가이드

Purpose
본 문서는 HEALTH IS ALL 프로젝트에 새로 참여하는 모든 개발자, 기획자, AI 엔지니어를 위한 최상위 온보딩 단일 진실 출처(SSOT) 가이드이다.

Scope
• 전체 폴더 구조, 시스템 아키텍처, 문서 읽는 순서, 개발 착수 전 필수 숙지 사항

SSOT
본 문서는 신규 개발자 온보딩 및 문서 탐색 경로의 최상위 안내서이다.

Definitions
• HEALTH IS ALL: 사용자의 건강 증진을 최우선으로 하되, 뛰어난 게임 완성도를 결합한 차세대 헬스케어 플래너 앱.

Rules
1. 필수 탐색 및 문맥 파악 순서: 
A. START_HERE.md (본 문서)
B. 00_PROJECT/CANONICAL_NAMING.md (용어 표준 및 금지 용어 숙지)
C. 03_GAME_SYSTEM/GAMEPLAY_LOOP_MASTER.md (코어 서비스 루프 파악)
D. 03_GAME_SYSTEM/ECONOMY_MASTER.md (Exp 및 Point 경제 체계 이해)
E. 00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.md (의존성 연관 분석)

1. 디렉토리 구조 요약: 
◦ 00_PROJECT/: 프로젝트 표준, 용어집, 패치 이력 (PATCH_HISTORY/)
◦ 02_DATABASE/: DB 마이그레이션 및 SQL 스크립트
◦ 03_GAME_SYSTEM/: 게임플레이, 경제, 퀘스트, 규칙 SSOT
◦ backend/: Python 백엔드 및 정밀 엔진 소스 코드
◦ lib/: Flutter 프론트엔드 위젯 및 화면 소스 코드

1. 개발 착수 전 금지 사항: 
◦ CANONICAL_NAMING.md에 정의된 금지 용어(XP, Spirit, Pet 등)를 소스 코드나 문서에 절대 사용하지 말 것.

Runtime
• 프로젝트에 새 기능이나 버그 수정을 반영하기 전, 관련 도메인의 SSOT 문서를 먼저 검토하고 변경 사항을 기록한다.

Examples
• 신규 백엔드 개발자는 EXP_RULE.md를 읽고 backend/progression_engine.py 모듈을 수정해야 한다.

Forbidden
• SSOT 문서 검토 없이 독자적인 용어나 수식으로 코드를 작성하는 행위.

Related Documents
• 00_PROJECT/CANONICAL_NAMING.md
• 00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.md

Change History
• 2026-07-31: PATCH-001 기준 신규 작성 (Gemini)