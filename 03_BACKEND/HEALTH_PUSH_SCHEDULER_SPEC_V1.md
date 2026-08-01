[여기부터 복사]
# HEALTH_PUSH_SCHEDULER_SPEC_V1.mdux

## Purpose
본 문서는 'HEALTH IS ALL' 시스템에서 앱 비활성화(백그라운드/종료) 상태 시 사용자의 생활 패턴 및 건강 결핍 상태에 맞춰 1~3줄 정밀 꿀팁 푸시 알림을 동적으로 발송하는 스케줄러 모듈의 표준 규격을 정의한다.

## Scope
본 규격은 백엔드 푸시 모듈(`03_BACKEND`), AI 동적 피더 연동 모듈(`05_AI`), 외부 FCM(Firebase Cloud Messaging) / APNs 알림 게이트웨이에 적용된다.

## SSOT
* 본 문서는 동적 푸시 알림 타이밍 및 1~3줄 푸시 문구 가공 시스템의 단일 진실 공급원(SSOT)이다.
* 연동 표준: `HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V3.mdux`, `api_tip_feeder_router_v3.py`.

## Definitions
1. **Dynamic Trigger Slot**: 사용자의 수분 결핍, 수면 패턴, 식사 시간을 고려해 알림을 트리거하는 동적 시간대(오전 08:30, 점심 12:30, 오후 15:30, 저녁 21:30).
2. **Push Dialogue Filter**: 알림창 글자 수 제한(최대 2~3줄, 80자 이내)에 맞춰 팁 메시지를 최적화하는 필터.
3. **Quiet Hours**: 수면 및 휴식을 방해하지 않기 위해 알림을 강제 차단하는 방해 금지 시간대(22:30 ~ 07:00).

## Runtime
* **실행 주기**: 매시 정각/30분 단위 백그라운드 크론(Cron) 스케줄러 감시.
* **알림 발송 지연**: Trigger 이벤트 발생 후 < 5초 이내 FCM/APNs 전달.

## Rules
1. **야간 방해 금지**: Quiet Hours(22:30 ~ 07:00) 동안에는 모든 일반 팁 푸시 발송을 차단하며, 필요 시 내일 아침 첫 슬롯으로 이월한다.
2. **최적화 문구 적용**: 알림창 특성에 맞춰 최대 3줄(80자)을 넘지 않도록 자동 줄바꿈 및 강조 이모지를 포함한다.
3. **알림 클릭 보상 연동**: 알림을 통해 앱에 진입할 경우 정령 친밀도 보상(+2)이 즉시 활성화된다.

## State
* `SCHEDULING`: 사용자별 다음 푸시 슬롯 및 가중치 계산 중.
* `SLEEP_MUTE`: 방해 금지 시간대로 인한 발송 대기.
* `DISPATCHED`: FCM/APNs 게이트웨이로 푸시 메시지 전달 완료.

## Event
* `EVENT_SCHEDULE_CHECK`: 푸시 주기 스케줄 체크 트리거.
* `EVENT_PUSH_SENT`: 푸시 알림 정상 발송 완료.
* `EVENT_PUSH_CLICKED`: 사용자가 알림을 클릭하여 앱 진입.

## Exception
* **E_GATEWAY_TIMEOUT**: 외부 푸시 서버 응답 지연 시 -> 3분 후 1회 재시도 후 실패 시 당회 슬롯 취소.

## Related Documents
* `HEALTH IS ALL/05_AI/HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V3.mdux`
* `HEALTH IS ALL/03_BACKEND/health_dynamic_tip_feeder_v3.py`
* `HEALTH IS ALL/04_FRONTEND/HEALTH_TIP_UI_ANIMATION_SPEC_V1.mdux`

## Change History
* **v1.0.0 (Current)**:
  * 백그라운드 1~3줄 동적 팁 푸시 스케줄러 규정 최초 제정.
  * 야간 방해 금지 시간대(Quiet Hours) 및 알림 클릭 연동 보상 스펙 포함.
[여기까지 복사]