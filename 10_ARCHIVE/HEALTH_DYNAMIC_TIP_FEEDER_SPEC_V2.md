# HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V2.mdux

## Purpose
본 문서는 'HEALTH IS ALL' 시스템 내에서 사용자의 동적 건강 수치(식단, 운동, 수면, 수분, HRV 등)를 정밀 분석하여, 게임 내 정령(Spirit)과 AI 코치가 전달하는 1~3줄 분량의 맞춤형 건강 꿀팁 및 친근한 대화 문구를 생성하는 피더(Feeder)의 작동 명세와 규칙을 정의한다.

## Scope
* AI 피드백 엔진 및 정령 대화 관리 모듈 전체 (`HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V9` 연동)
* 백엔드 동적 건강 계산 엔진 (`dynamic_health_engine_v12`, `diet_spirit_engine_v10`)
* 프론트엔드 홈 팝업 및 대화 인터페이스 화면

## SSOT
* **단일 진실 출처 (SSOT)**: `HEALTH IS ALL/05_AI/HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V2.mdux`
* 건강 계산 공식 SSOT: `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.mdux`
* 게임 통합 엔진 SSOT: `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V11_SPEC.mdux`

## Definitions
* **Dynamic Health Multiplier ($M_{dynamic}$)**: 단순 칼로리 및 운동량을 넘어 HRV, 수분, 식사 간격을 다변수로 조합한 동적 건강 가중치.
* **Friendly Tip Feeder**: 건강 지침을 딱딱하지 않게 1~3줄의 이용자 친화적이고 호감 가는 인터페이스 문구로 변환하는 서브시스템.
* **Fallback Safety Routine**: 다변수 계산 시 변수 누락 또는 범위 초과 오류 발생 시 기본 표준 공식으로 자동 전환하는 안전 로직.

## Runtime
* **실행 시점**: 유저의 건강 데이터(식단 기록, 운동 완료, 수면 측정, 수분 입력) 갱신 시 실시간 이벤트 트리거.
* **응답 시간 목표**: 동적 수식 계산 및 문구 바인딩 완료까지 150ms 이내 처리.

## Rules
1. **게임성과 건강성 동등 유지**: 게임 요소(정령 호감도/경험치)와 건강 안내 문구가 5:5 밸런스를 이루며, 건강 표현보다 게임 팝업이 과도하게 튀지 않도록 조율한다.
2. **다변수 동적 계산식 적용**:
   $$M_{dynamic} = \left(1 + \frac{\text{HRV} - 50}{100}\right) \times \left(1 - 0.05 \times |\text{MealInterval} - 4|\right) \times (1 + 0.1 \times \text{HydrationRatio})$$
3. **1~3줄 핵심 꿀팁 제공**: 문구는 최소 1줄, 최대 3줄을 초과하지 않으며 호감적이고 긍정적인 어조를 유지한다.
4. **언어 규칙**: 프롬프트 및 시스템 인프라 코드를 제외한 모든 사용자 제공 텍스트는 표준 한글을 사용한다.

## State
* `IDLE`: 사용자 데이터 입력 대기 상태.
* `CALCULATING`: 다변수 가중치 및 정령 반응 수치 산출 중.
* `GENERATING_TIP`: 수치 구간별 1~3줄 호감형 팁 및 대화 매핑 중.
* `DELIVERED`: UI 팝업 및 대화창으로 최종 전달 완료.

## Event
* `ON_HEALTH_DATA_UPDATED`: 새로운 건강 관련 데이터 수집 시 발생.
* `ON_TIP_FEED_READY`: 사용자 화면으로 출력 준비 완료 시 발생.
* `ON_CALCULATION_FALLBACK`: 다변수 오류로 단순 계산식 전환 시 발생.

## Example
* **상황**: 수분을 충분히 섭취하고 식사 간격을 4시간으로 유지한 유저에게 정령 '파이론'이 전달하는 팝업 문구.
* **출력 예시**:
  > "오늘 수분 충전과 식사 타이밍이 정말 완벽해요! 정령의 불꽃이 더욱 활기차게 타오르고 있답니다. 이 기세를 몰아 가벼운 산책 한 번 어때요?"

## Exception
* **데이터 누락 예외 (`ERR_MISSING_VARIABLE`)**: HRV 또는 수분 입력값이 없을 경우, 기본값(HRV=50, HydrationRatio=0.5)을 채워 가볍게 계산을 수행하고 예외 로그를 기록함.
* **수식 연산 오류 예외 (`ERR_MATH_OVERFLOW`)**: 다변수 계산 연산 중 오버플로 발생 시 단일 가중치 공식($M_{base} = 1.0$)으로 즉시 전환하여 시스템 중단을 방지함.

## Related Documents
* `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.mdux`
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V11_SPEC.mdux`
* `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V5.mdux`
* `HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V9.mdux`
* `HEALTH IS ALL/03_BACKEND/user_friendly_dialogue_manager_v3.py`

## Change History
| Date | Version | Author | Description |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | V2.0 | AI System Architect | V1 대비 다변수 정밀 계산식 추가, 1~3줄 꿀팁 연동 규칙 세분화, 10_ARCHIVE 정리 반영 |