# BALANCE_CHANGE_PROCESS

- Document Name: BALANCE_CHANGE_PROCESS.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 게임 밸런스 변경을 문서·코드·테스트와 함께 통제한다.
- Implementation Status: Implemented
- Source of Truth: Documentation + Code + Config
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: formula/unit/integration validation

## Change Scope
- Formula 변경
- Exp 변경
- Point 변경
- Quest 변경
- Reward 변경
- Shop 변경

## Standard Process
1. 변경 요청 등록
2. 변경 사유와 목표 지표 명시
3. 영향 상수/문서/코드/테스트 식별
4. SSOT 결정
5. 문서/코드 동시 수정
6. 테스트 및 시뮬레이션
7. 리뷰 승인
8. 릴리스 후 모니터링

## Formula 변경
- 입력값, 계수, cap, fallback을 명시한다.
- 같은 의미의 숫자를 여러 파일에 하드코딩하지 않는다.
- 기존 유저 영향(성장 속도, 인플레이션, grind 유도)을 평가한다.

## Exp 변경
- 일일 cap, 주간 cap, streak bonus, anti-farming 규칙을 함께 본다.
- PATCH-004 기준 canonical 제안은 `300 soft cap`이다.
- 300 초과 행동은 기록/통계/배지 반영을 유지하되 성장 보상은 감쇄 구조를 우선 검토한다.

## Point 변경
- Exp와 Point를 같은 역할로 쓰지 않는다.
- 상점 소비/획득 루프의 순환 속도를 측정한다.

## Quest 변경
- 기본 보상, 난이도, 재롤, 반복 악용 가능성을 함께 본다.
- streak/day-part/location 같은 맥락 데이터 사용 시 개인정보/설명 가능성도 검토한다.

## Reward 변경
- reward는 사용자 행동을 왜곡하지 않아야 한다.
- 건강 목표보다 게임 보상이 과도하게 앞서면 거절한다.

## Shop 변경
- skin/item 가격은 예상 일간/주간 획득량과 함께 평가한다.
- 신규 상품은 pay-to-win 또는 건강행동 왜곡 요소가 없어야 한다.

## A/B 테스트 여부
1. 고영향 밸런스 변경은 A/B 테스트를 우선 검토한다.
2. 실험군/대조군 차이는 문서화한다.
3. 실험 종료 후 canonical 값으로 승격할지 결정한다.
4. 실험 중 상수를 SSOT처럼 오인하지 않도록 feature flag와 구분한다.

## Related Source Files
- `03_GAME_SYSTEM/EXP_RULE.md`
- `03_GAME_SYSTEM/POINT_RULE.md`
- `backend/progression_engine.py`
- `backend/quest_engine.py`
- `lib/shop_screen.dart`

## Validation Method
- Formula Test
- Integration Test
- A/B Review
- Runtime Verification
