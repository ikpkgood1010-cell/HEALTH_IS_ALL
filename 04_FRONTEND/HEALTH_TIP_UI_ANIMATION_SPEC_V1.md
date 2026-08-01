[여기부터 복사]
# HEALTH_TIP_UI_ANIMATION_SPEC_V1.mdux

## Purpose
본 문서는 'HEALTH IS ALL' 앱 내 1~3줄 맞춤형 건강 꿀팁 피딩 시 나타나는 말풍선(Dialogue Bubble) 및 정령(Spirit) 리액션, 마이크로 보상 연출의 시각적 인터랙션 및 애니메이션 스펙을 정의한다.

## Scope
본 규격은 프론트엔드 UI 컴포넌트(`04_FRONTEND`), 정령 애니메이션 레이어, 마이크로 보상 이펙트 시스템에 적용된다.

## SSOT
* 본 문서는 팁 피더 UI 연출 및 애니메이션 프레임워크의 단일 진실 공급원(SSOT)이다.
* 연동 표준: `HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V3.mdux`, `user_friendly_dialogue_manager_v3.py`.

## Definitions
1. **Dialogue Pop Engine**: 팁 텍스트를 3줄 이내 말풍선 형태로 부드럽게 팝업시키는 애니메이션 트랜지션.
2. **Spirit Mood Reaction**: 팁 카테고리 및 사용자 회복 지수에 맞춰 정령 모션(바운스, 반짝임, 따뜻한 파동)이 동기화되는 연출.
3. **Reward Particle System**: 팁 확인 클릭 시 정령 친밀도(+2) 및 마이크로 골드(+5)가 정령 머리 위로 떠오르며 사라지는 파티클 이펙트.

## Runtime Specs
* **프레임 레이트**: 60 fps (가변 주율 대응)
* **팝업 등장 애니메이션 시간**: 250ms (Ease-Out Back 커브)
* **텍스트 타자기(Typewriter) 효과**: 글자당 15ms (최대 3줄, 전체 출력 < 600ms)
* **보상 파티클 유지 시간**: 800ms (Ease-In Quad 이동 후 Fade-Out)

## Rules
1. **가독성 최우선**: 최대 3줄 한계를 준수하며, 줄바꿈은 의미 단위로 자연스럽게 단절되도록 가공한다.
2. **게임성 결합**: 팁 터치 해제 시 보상 파티클 애니메이션이 필수 발생해야 하며, 정령 친밀도 게이지에 수치 증가 효과가 즉시 반영된다.
3. **방해 금지(Non-Intrusive)**: 주요 게임 플레이(전투/미니게임) 중에는 팝업을 차단하고, IDLE 화면 및 식단/운동 기록 완료 화면에서만 팝업을 승인한다.

## State Transitions
* `HIDDEN`: 화면에 표시되지 않음.
* `ENTERING`: Ease-Out 커브로 말풍선 확대 및 정령 반짝임 연출.
* `READING`: 텍스트 노출 완료, 사용자 터치 입력 대기.
* `REWARDING`: 팁 확인 터치 시 보상 파티클 Floating 연출.
* `EXITING`: 말풍선 Fade-Out 및 초기화.

## Event Handlers
* `ON_TIP_RECEIVE`: API 데이터 수신 완료 시 `ENTERING` 상태로 전환.
* `ON_BUBBLE_TAP`: 사용자가 말풍선 터치 시 `REWARDING` 이벤트 트리거 및 보상 수령.
* `ON_AUTO_DISMISS`: 8초 간 반응 없을 시 자동 `EXITING`.

## Exception
* **E_ANIMATION_LAG**: 프레임 드랍 발생 시 타자기 효과를 스킵하고 텍스트 전체를 즉시 출력 (`ENTERING` -> `READING` 50ms 내 강제 전환).

## Related Documents
* `HEALTH IS ALL/05_AI/HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V3.mdux`
* `HEALTH IS ALL/03_BACKEND/api_tip_feeder_router_v3.py`
* `HEALTH IS ALL/04_FRONTEND/user_friendly_dialogue_manager_v3.py`

## Change History
* **v1.0.0 (Current)**:
  * 1~3줄 팁 말풍선 트랜지션 및 타자기 효과 규격 제정.
  * 정령 리액션 연출 및 마이크로 보상 파티클 인터랙션 통합.
[여기까지 복사]