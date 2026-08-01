# HEALTH_GAME_DUAL_BALANCE_SPEC_V4.md

## Purpose
건강 관리(운동, 식단, 생체 데이터)라는 앱의 본질적 목적을 최우선으로 유지하면서, 게임적 몰입 요소(스피릿 육성, 퀘스트, 보상)가 건강 정보 시각화를 방해하거나 가리지 않도록 인터페이스 및 로직 차원의 이중 밸런스(Dual Balance)를 확립한다.

## Scope
본 명세서는 프론트엔드 UI/UX 레이아웃 제어, 백엔드 다변수 건강-게임 연동 엔진, AI 기반 1~3줄 건강/식단 꿀팁 피더, 스피릿 반응형 애니메이션 및 보상 밸런싱 로직 전반에 적용된다.

## SSOT
* **문서 SSOT**: `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V4.md`
* **데이터베이스 SSOT**: `02_DATABASE/DATABASE_SCHEMA_MASTER.mdux` (`user_health_logs`, `spirit_states`, `reward_histories`)
* **실행 엔진 SSOT**: `03_BACKEND/dynamic_health_engine_v11.py`, `03_BACKEND/diet_spirit_engine_v10.py`

## Definitions
* **Dual-Balance Index (DBI)**: 건강 달성 수치와 게임 보상율 간의 상호 균형을 나타내는 지표.
* **HRR (Heart Rate Reserve)**: 심박예비능 ($HRR = HR_{max} - HR_{rest}$).
* **1~3 Line Health Tip Feeder**: 사용자의 실시간 건강/식단 입력 상태에 반응하여 AI 메이트가 전달하는 1~3줄 이내의 즉각적 친화적 꿀팁 소스.
* **Non-Intrusive Overlay**: 건강 데이터를 가리지 않고 화면 하단이나 여백 영역에서 자연스럽게 반응하는 게임 애니메이션 기법.

## Runtime
* **실행 시점**: 모바일 앱 구동 시, 실시간 웨어러블 데이터 수신 시, 식단/운동 기록 등록 시, 스피릿 인터랙션 발생 시 백그라운드 연산 실행.
* **실행주기**: 이벤트 발생 즉시(Event-driven) 연산 수행 및 UI 상태 업데이트.

## Rules
1. **UI 레이아웃 대원칙**: 화면 내 메인 카드의 70% 면적은 건강 데이터(소모 칼로리, 영양소, 수면, 심박수)에 배정하며, 게임 요소(스피릿 캐릭터, EXP 바)는 30% 이하의 비침습적 오버레이로 배치한다.
2. **다변수 동적 운동 EXP 계산식**:
   $$EXP_{workout} = \left( \Delta Cal \times \left(1 + \frac{HR_{avg} - HR_{rest}}{HR_{max} - HR_{rest}}\right) \times \text{Streak}^{0.15} \right) \times \text{Spirit Synergy Factor}$$
   * 심박 데이터 누락 시 오차 차단을 위해 기본 메츠($METs$) 가중치 연산으로 자동 전환한다.
3. **영양소 밸런스 기반 스피릿 상태 연산식**:
   $$\text{Score}_{diet} = 100 \times \left(1 - \frac{|\text{Target}_{carbs} - \text{Actual}_{carbs}|}{\text{Target}_{carbs}}\right) \times \left(1 - \frac{|\text{Target}_{protein} - \text{Actual}_{protein}|}{\text{Target}_{protein}}\right)$$
4. **1~3줄 건강/식단 꿀팁 트리거 규칙**:
   * 식단 기록 완료 시 목표 영양소 대비 오차가 $\pm 20\%$ 이상 발생하거나, 고강도 운동 완료 후 5분 이내에 1~3줄의 이용자 친화적 맞춤 꿀팁 팝업을 자동 생성한다.

## State
* `IDLE`: 기본 대기 상태 (건강 위젯 중심 표시).
* `RECORDING`: 식단 및 운동 입력 모드 (게임 애니메이션 일시 정지 및 정밀 입력 지원).
* `PROCESSING`: 백엔드 다변수 수식 및 AI 꿀팁 피더 연산 진행 중.
* `BALANCED_FEEDBACK`: 1~3줄 건강 꿀팁과 스피릿 육성 보상 모션이 조화롭게 출력되는 상태.

## Event
* `EVENT_HEALTH_LOG_ENTERED`: 운동/식단 데이터 수신 이벤트.
* `EVENT_DYNAMIC_CALC_COMPLETED`: 다변수 수식 연산 완료 이벤트.
* `EVENT_TIP_FEED_GENERATED`: 1~3줄 맞춤 건강 꿀팁 생성 완료 이벤트.
* `EVENT_SPIRIT_ANIMATION_TRIGGERED`: 스피릿 반응형 모션 제어 이벤트.

## Example
사용자가 고강도 수동 활동(예: 세차, 고강도 트레킹) 후 350kcal 소모 데이터를 수신한 경우:
1. 백엔드에서 HRR 가중치와 연속 달성일을 적용해 425 EXP를 산출.
2. 메인 화면 하단 30% 영역의 스피릿이 활력 넘치는 동작 연출.
3. 챗봇 메이트 팝업으로 1~3줄 꿀팁 피드 출력:
   > "오늘 고강도 활동으로 소모량이 높네요! 운동 후 30분 이내에 따뜻한 물과 단백질을 보충해 주시면 근육 피로 회복에 큰 도움이 됩니다."

## Exception
* **웨어러블 센서 오류 발생 시**: 단일 변수 기반 간결 수식으로 자동 전환하여 시스템 안정성을 확보한다.
* **수치 이상치(예: 1시간 소모 칼로리 > 3,000kcal) 감지 시**: 연산을 차단하고 사용자 재확인 팝업을 안내한다.
* **네트워크 미연결 시**: 로컬 캐시 엔진을 통해 꿀팁 피더와 EXP를 임시 처리 후 오프라인 동기화 수행.

## Related Documents
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V10_SPEC.md`
* `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v11.py`
* `HEALTH IS ALL/05_AI/HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V1.md`
* `HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V9.md`
* `HEALTH IS ALL/02_DATABASE/DATABASE_SCHEMA_MASTER.mdux`

## Change History
* **v4.0.0 (2026-07-31)**: 다변수 정밀 연산 수식 구현, 1~3줄 건강/식단 꿀팁 피더 연동 명세 추가, UI 비침습적 이중 밸런스 규격 확립, 필수 12대 표준 작성 구조 100% 준수 및 코드 블록 이스케이프 적용.