DOCUMENT_DEPENDENCY_MAP

Purpose
본 문서는 프로젝트의 문서와 실행 코드가 실제로 어떤 파일을 가리키는지 계층별로 매핑한 지도이다.
`/00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.md`가 "상위 문서 변경 시 영향 범위"를 다룬다면, 본 문서는
"이 레벨에서는 어떤 파일들이 실재하는가"를 다룬다.

Scope
• Level 0(거버넌스) ~ Level 4(테스트)까지 실제로 저장소에 존재하는 파일 경로만 기재한다.

SSOT
본 문서는 문서-코드 매핑 지도의 단일 진실 출처이다. 개별 도메인 규칙 자체의 SSOT는 아니다.

---

Rules

1. Level 0 — 최상위 거버넌스
   • /00_PROJECT_START/PROJECT_CONSTITUTION.md
   • /00_PROJECT_START/PRODUCT_VISION.md
   • /01_ARCHITECTURE/ADR_001_PHILOSOPHY_AND_SSOT_RULES.md

2. Level 1 — 제품 표준 및 도메인 구조
   • 용어 표준(최상위 권한): /00_PROJECT/CANONICAL_NAMING.md — Exp., 건강이 등 표준 용어 및 금지 용어(XP, Spirit, Pet, Energy, Coin/Gold, Mission) 정의
   • 보조 용어집: /07_PRODUCT/MASTER_CANONICAL_GLOSSARY.md, /07_PRODUCT/Product Language Guide.md
     (CANONICAL_NAMING.md와 내용이 충돌할 경우 CANONICAL_NAMING.md가 우선한다)
   • 도메인 설계: /01_ARCHITECTURE/DOMAIN_DESIGN.md (Legacy 표기 — ARCHITECTURE_INDEX.md 참고 후 사용)

3. Level 2 — 코드 및 실행 에셋 (실제 저장소 경로로 검증됨)

   Backend (Python / FastAPI) — 실행 실체
   • 엔트리포인트: /backend/main.py
   • 설정: /backend/config.py
   • DB 세션: /backend/database.py
   • ORM 모델: /backend/models.py
   • 성장/경험치 엔진: /backend/progression_engine.py
   • AI 코칭('건강이') 서비스: /backend/ai_agent_service.py
   • 식단 계산: /backend/diet_calculator.py
   • 건강 점수/칼로리 계산: /backend/health_calculator.py
   • 수면/습관 계산: /backend/habit_sleep_calculator.py
   • 퀘스트 엔진: /backend/quest_engine.py
   • 규칙 문서(코드와 같은 폴더에 위치): /backend/DAILY_RESET_POLICY.md,
     /backend/OFFLINE_FIRST_POLICY.md, /backend/SYNC_CONFLICT_POLICY.md
   • 사양서만 존재(코드 아님, Legacy): /03_BACKEND/ 하위 *.md, *.mdux 및 일부 시안 .py(v3/v7/v10 등).
     실제 구현 시 /backend/의 코드를 기준으로 하고 이 폴더는 아이디어 참고용으로만 사용한다.

   Frontend (Flutter / Dart) — 실행 실체
   • 진입점: /lib/main.dart
   • 홈/메인 내비게이션: /lib/home_screen.dart, /lib/main_navigation_screen.dart
   • 상태/모의데이터: /lib/mock_data_provider.dart, /lib/offline_cache_repository.dart
   • 사양서: /04_FRONTEND/ 하위 *.md, *.mdux (FLUTTER_PROJECT_STRUCTURE.md, STATE_MANAGEMENT_GUIDE.md 등)
   • 빈 폴더(무시): /02_FRONTEND/

   Database (PostgreSQL)
   • 스키마 마스터: /02_DATABASE/DATABASE_SCHEMA_MASTER.md
   • 마이그레이션(순번대로 적용): /02_DATABASE/01_schema_migration.sql ~ 08_schema_migration_v8.sql
   • 도메인별 스펙: /02_DATABASE/DATABASE_01_CORE.md, DATABASE_02_HEALTH.md, DATABASE_03_RPG.md, DATABASE_04_ANALYTICS.md

4. Level 3 — 게임 시스템 / 경제 규칙 (/03_GAME_SYSTEM/)
   • 코어 루프: GAMEPLAY_LOOP_MASTER.md
   • 경제: ECONOMY_MASTER.md, EXP_RULE.md, POINT_RULE.md
   • 어뷰징 방지: ANTI_GRIND_POLICY.md
   • 이 레벨의 문서가 변경되면 /backend/progression_engine.py, /backend/quest_engine.py 재검토 필수
     (상세 영향 범위는 /00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.md 참고)

5. Level 4 — 테스트
   • /test/progression_engine_test.py — 성장 엔진 단위 테스트
   • /test/system_integration_test.py — 건강기록→계산→Exp 부여→AI 코칭→퀘스트 보상 End-to-End 테스트
   • /tests/test_backend.py — 백엔드 API/모듈 통합 테스트
   • 실행: `pytest test/ tests/`

Runtime
• 새 파일을 추가하면 해당 Level 섹션에 실제 경로를 추가한다. 존재하지 않는 파일 경로를 기재하지 않는다.
• 파일을 이동/삭제하면 본 문서와 /01_ARCHITECTURE/ARCHITECTURE_INDEX.md를 동시에 갱신한다.

Examples
• 백엔드 개발자가 성장 공식을 바꾸려면: /03_GAME_SYSTEM/EXP_RULE.md 확인 → /backend/progression_engine.py 수정
  → /test/progression_engine_test.py 갱신 → /00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.md 기준 영향 문서 점검.

Forbidden
• 존재하지 않는 파일이나 깨진 참조(예: 이전 버전의 `span_0span_0` 같은 인용 잔재, `HEALTH ALL/`처럼 오타난
  프로젝트명)를 경로로 남겨두는 행위.

Related Documents
• /01_ARCHITECTURE/ARCHITECTURE_INDEX.md
• /00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.md
• /00_PROJECT/CANONICAL_NAMING.md

Change History
• 2026-07-31: PATCH-001 최초 작성 — 문서 붙여넣기 과정에서 발생한 인용 잔재(`span_0span_0`)로 인해
  본문이 중간에 손상됨 (Gemini 추정)
• 2026-08-01: PATCH-002 — 손상된 인용 잔재 전량 제거, 실제 저장소 파일 존재 여부 전수 검증 후
  전면 재작성 (Claude)
