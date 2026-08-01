# IMPLEMENTATION_GUIDELINES

- Document Name: IMPLEMENTATION_GUIDELINES.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 실제 구현 단계에서 개발자별 편차를 줄이고, 실행 코드·설계 문서·리뷰 기준을 하나의 구현 표준으로 묶는다.
- Implementation Status: Implemented
- Source of Truth: Documentation + Runtime Code
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: Manual review, compile baseline, targeted file scan

## Scope
- 루트 실행 코드(`backend/`, `lib/`)
- 설계/표준 문서(`00_PROJECT/`, `03_BACKEND/`, `04_FRONTEND/`, `03_GAME_SYSTEM/`)
- 신규 기능 구현, 리팩터링, 버그 수정, 테스트 작성

## Core Principle
문서는 설명서가 아니라 **코드와 함께 검증되는 SSOT**다. 신규 구현은 “각자 편한 방식”이 아니라 본 문서의 규칙을 따라야 한다.

## Folder Rule
1. 실행 가능한 백엔드 코드는 `backend/`에 둔다.
2. 실행 가능한 Flutter 앱 코드는 `lib/`에 둔다.
3. `03_BACKEND/`, `04_FRONTEND/`는 기본적으로 설계 문서·표준 문서·참고 샘플 영역으로 취급한다.
4. `10_ARCHIVE/`는 참조용 보관 영역이며 신규 구현의 기준으로 삼지 않는다.
5. 같은 책임의 파일을 문서 폴더와 런타임 폴더에 중복 생성하지 않는다.

## Naming Rule
1. 사용자 표시 용어의 표준은 `Exp`, 역할명은 `정령`, 기본 이름은 `건강이`다.
2. 코드 변수는 소문자 카멜 케이스를 사용한다. 예: `currentExp`, `dailyExpCap`, `defaultSpiritName`.
3. Python 파일은 `snake_case.py`, Dart 파일은 `snake_case.dart`를 사용한다.
4. 클래스는 `PascalCase`, 상수는 언어 표준을 따르되 중앙 상수는 `CANONICAL_CONSTANTS.md`를 먼저 갱신한다.
5. 금지 용어(`XP`, `EXP`, `Spirit`를 canonical 명칭으로 쓰는 행위)는 신규 구현에서 금지한다. 단, 레거시 호환은 기술 부채로 등록 후 단계적으로 제거한다.

## Engine Rule
1. Engine은 순수 계산·판정·도메인 규칙을 담당한다.
2. Engine은 I/O, HTTP 응답, UI 상태 변경을 직접 수행하지 않는다.
3. Engine 입력과 출력은 문서화 가능한 구조체/딕셔너리/모델로 고정한다.
4. Formula, cap, reward, recommendation 규칙은 Engine 문서와 테스트를 함께 가진다.

## Service Rule
1. Service는 Engine 조합, 외부 의존성 호출, orchestration을 담당한다.
2. FastAPI route는 Service/Engine을 호출하되 직접 복잡한 도메인 계산을 넣지 않는다.
3. AI 관련 서비스는 프롬프트·fallback·사용자 메시지 정책을 분리해 관리한다.

## Dependency Rule
1. 방향은 UI -> Application/Service -> Engine/Repository -> Config 순으로 유지한다.
2. 하위 레이어가 상위 레이어를 import하지 않는다.
3. Engine은 Flutter UI, FastAPI app 객체, DB 세션에 의존하지 않는다.
4. 설계 문서는 실행 코드의 import 대상이 되지 않는다.

## Import Rule
1. Python은 `backend.*` 절대 import를 우선한다.
2. Dart는 상대경로 난립을 피하고 기능 단위 import를 유지한다.
3. 미사용 import는 허용하지 않는다.
4. orphan 후보 파일은 메인 라우트나 API에서 import하지 않으면 활성 모듈로 간주하지 않는다.

## Async Rule
1. 네트워크, DB, 파일, sync 작업은 비동기 또는 background task로 분리한다.
2. Flutter 상태는 loading -> success/error -> retry 흐름을 명시한다.
3. 재시도 가능 작업은 최대 재시도 횟수와 backoff 정책을 문서화한다.
4. 오프라인 동기화는 낙관적 UI와 충돌 해결 정책을 함께 정의한다.

## Exception Rule
1. 사용자 메시지와 내부 예외를 분리한다.
2. 예외는 삼키지 말고 분류한다: validation, business, integration, runtime.
3. fallback이 있으면 이유와 범위를 로그로 남긴다.
4. 문서와 코드가 충돌하면 즉시 hotfix하지 말고 SSOT 결정 -> 동기화 계획 -> 테스트까지 한 패치로 처리한다.

## Logging Rule
1. 요청 ID, 사용자 ID, 엔진명, 주요 상수 버전, fallback 여부를 로그에 포함한다.
2. 개인건강정보 원문은 마스킹 없이 남기지 않는다.
3. warning은 “운영 추적 필요”, error는 “사용자 영향 가능” 기준으로 분리한다.
4. 상수 불일치·orphan 감지·route 미연결은 운영성 이슈로 기록한다.

## Implementation Workflow
1. 관련 SSOT 문서 확인
2. 상수/용어/계약 영향 범위 확인
3. 코드 수정
4. 테스트 추가 또는 갱신
5. 리뷰 체크리스트 통과
6. 기술 부채·운영 영향 기록

## Definition of Ready
- 관련 SSOT가 식별되었는가
- 기준 상수가 확정되었는가
- API/상태/UI 영향 범위가 정리되었는가
- orphan/legacy 여부가 판별되었는가

## Definition of Done
- 구현 코드, 문서, 테스트가 같은 기준을 본다
- 런타임 경로에 hard-coded 상수 drift가 없다
- 리뷰 체크리스트와 검증 항목이 갱신되었다

## Related Source Files
- `backend/main.py`
- `backend/config.py`
- `backend/progression_engine.py`
- `lib/main.dart`
- `lib/main_navigation_screen.dart`
- `00_PROJECT/CANONICAL_NAMING.md`

## Validation Method
- Manual Review
- Compile Check
- Runtime Verification
- Contract Review
