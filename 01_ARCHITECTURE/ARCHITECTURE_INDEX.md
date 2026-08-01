ARCHITECTURE_INDEX

Purpose
본 문서는 HEALTH IS ALL 프로젝트 전체 문서와 실행 코드 간의 최상위 내비게이션 지도이다. 개발자와 AI가 "이 폴더/문서가 왜 있고, 지금도 유효한지"를 판단할 수 있게 한다.

Scope
• 전체 최상위 폴더(00~10) 목적, 상태(Active/Legacy/Archive), 실제 실행 코드 위치, 읽기 순서를 정의한다.

SSOT
본 문서는 "문서 지도"의 단일 진실 출처이다. 개별 도메인 규칙(용어, 경제, DB 스키마 등)의 SSOT는 각 도메인 문서(`CANONICAL_NAMING.md`, `ECONOMY_MASTER.md` 등)에 있다.

Status: Stable
Version: 2.0 (PATCH-002)
Last Updated: 2026-08-01
Owner: Architecture

---

Rules

1. 신규 참여자 읽기 순서 (5분 온보딩)
   1) /START_HERE.md
   2) /00_PROJECT/CANONICAL_NAMING.md — 용어 표준(필독, 금지 용어 확인)
   3) /03_GAME_SYSTEM/GAMEPLAY_LOOP_MASTER.md
   4) /03_GAME_SYSTEM/ECONOMY_MASTER.md
   5) /00_PROJECT_START/DOCUMENT_DEPENDENCY_MAP.md
   6) 본 문서(ARCHITECTURE_INDEX.md)로 돌아와 작업할 도메인 폴더로 이동

2. 최상위 폴더 상태표 (실제 저장소 기준으로 검증됨)

   [ACTIVE — 실제 실행 코드 / 현재 SSOT]
   - /backend/           : FastAPI+SQLAlchemy 실행 코드. 서비스의 유일한 백엔드 실체.
   - /lib/                : Flutter 프론트엔드 실행 코드.
   - /test/, /tests/      : pytest 테스트. 실행: `pytest test/ tests/`
   - /00_PROJECT/         : 용어 표준, 문서 영향도 매트릭스, 패치 이력(PATCH_HISTORY/)
   - /00_PROJECT_START/   : 프로젝트 헌장, 로드맵, 문서 의존성 맵, 폴더 구조 설명
   - /03_GAME_SYSTEM/     : 게임플레이 루프·경제·퀘스트 규칙 SSOT (Exp./Point/Habit/Quest 표준 용어 사용)
   - /02_DATABASE/        : DB 스키마 마스터 및 마이그레이션 SQL(01~08)
   - /07_PRODUCT/         : 용어집(MASTER_CANONICAL_GLOSSARY.md), 제품 언어 가이드
   - /06_DESIGN/          : 브랜드, 디자인 시스템, UI 스펙(단, 06_DESIGN/UI/*/*_Spec.md 8개는 본문 비어있음 — 작성 필요)
   - /09_PROMPTS/         : AI 어시스턴트별(Claude/Codex/Gemini/ChatGPT) 작업 프롬프트 규칙

   [LEGACY — 참고용, 코드/신규 문서 작성 시 인용 금지]
   - /01_ARCHITECTURE/    : "Guild Health" 프로젝트명·NestJS/Prisma 스택 시절 설계 문서 다수 포함.
     실제 코드(Python/FastAPI)와 스택이 다름. START_HERE.md는 Deprecated 처리됨(루트로 리다이렉트).
     이 폴더의 개별 스펙 문서(TECH_STACK.md, SYSTEM_ARCHITECTURE.md 등)를 인용하기 전 반드시
     /backend/ 실제 구현과 대조할 것.
   - /03_BACKEND/         : 코드가 아닌 "백엔드 사양서 + 샘플 코드 혼합" 폴더. 일부 파일은 실제 서비스에
     반영되지 않은 시안(v3/v7/v10 등 버전 넘버링)이다. 실행 실체는 /backend/ 이다.
   - /02_FRONTEND/        : 빈 폴더(내용 없음). 실제 프론트엔드 사양은 /04_FRONTEND/, 실행 코드는 /lib/.

   [ARCHIVE — 이력 보존용]
   - /10_ARCHIVE/         : 이전 버전(v2~v10 등) 스펙·코드 백업. 신규 작업에서 참조하지 말 것.

   [기타]
   - /04_FRONTEND/, /05_AI/, /06_ANALYTICS/, /06_QA/, /08_ASSETS/ : 각 도메인 스펙 문서. Active로 간주하되,
     06_ 접두사가 06_ANALYTICS / 06_DESIGN / 06_QA 세 곳에 중복 부여되어 있음(번호 체계 미정비 상태,
     기능상 문제는 없으나 향후 정리 대상 — 아래 "알려진 구조적 부채" 참고).

3. 문서 상태(Status) 표기 규칙
   - Draft: 작업 중, 대규모 변경 가능
   - Review: 검토 중
   - Stable: 승인되어 실제로 참조되는 규격
   - Deprecated: 폐기, 대체 문서로 리다이렉트만 유지

4. 알려진 구조적 부채 (다음 정리 단계 후보, 이번 패치에서는 미수정 — 아래 사유 참고)
   a) 최상위 폴더 번호 중복: 06_ANALYTICS / 06_DESIGN / 06_QA 세 폴더가 "06" 접두사를 공유함.
      → 폴더명 변경은 프로젝트 전역 수백 개 문서의 상대 경로 참조를 깨뜨릴 수 있어, 전체 링크
      검증 없이 이번 패치 범위에서 일괄 변경하지 않았다. 별도 작업으로 문서 내 참조 스캔 후 진행 권장.
   b) 루트에 빌드 산출물(`HEALTH_IS_ALL_PATCH_005.zip`, `build_patch_005.ps1`)이 소스와 함께 커밋되어 있음.
      → `.gitignore`로 제외하거나 별도 릴리스 저장소로 이동 권장.
   c) `00_PROJECT/`와 `00_PROJECT_START/`가 폴더명이 유사해 혼동 소지가 있음(역할은 다름: 전자는 표준/용어,
      후자는 헌장/로드맵). 이름 통합은 부채 (a)와 함께 다음 리네이밍 작업에서 함께 처리 권장.

Runtime
• 새 문서를 작성하거나 기존 문서를 옮길 때는 본 문서의 상태표를 갱신한다.
• AI/개발자는 코드를 작성하기 전 해당 도메인이 Active 폴더 문서를 기준으로 하는지 반드시 확인한다.
  Legacy/Archive 폴더의 문서를 실행 코드의 근거로 사용하지 않는다.

Examples
• 백엔드 신규 엔진을 추가할 때: `/03_GAME_SYSTEM/`에서 규칙을 확인하고, `/backend/`에 구현하며,
  `/03_BACKEND/`의 시안 문서는 참고만 하고 실행 근거로 삼지 않는다.

Forbidden
• Legacy로 표시된 `/01_ARCHITECTURE/` 문서(START_HERE.md 등)를 신규 온보딩 경로로 안내하는 행위.
• Archive(`/10_ARCHIVE/`) 코드를 그대로 복사해 `/backend/`에 반영하는 행위.

Related Documents
• /START_HERE.md
• /00_PROJECT_START/DOCUMENT_DEPENDENCY_MAP.md
• /00_PROJECT/CANONICAL_NAMING.md
• /00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.md

Change History
• 2026-07-28: v1.4 최초 작성 (Guild Health/NestJS 기준, Gemini 추정)
• 2026-08-01: PATCH-002 — 실제 저장소 구조 전수 조사 후 전면 재작성. Active/Legacy/Archive 상태 표기
  도입, 기술 스택 불일치 명시, 알려진 구조적 부채 섹션 추가 (Claude)
