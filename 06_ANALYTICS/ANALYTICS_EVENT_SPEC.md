# ANALYTICS_EVENT_SPEC

## Purpose
본 문서는 사용자 행동 분석, 퍼널(Funnel) 측정, UX 개선 및 비즈니스 KPI 산출을 위해 트래킹하는 Analytics Event의 사양, 명명 규칙 및 PII 제외 정책을 정의하는 SSOT이다.

## Scope
Flutter 클라이언트 이벤트 수집기, Firebase Analytics, Mixpanel 및 백엔드 로깅 파이프라인에 적용된다.

## SSOT
사용자 행동 트래킹 이벤트명, 속성(Property) 규격의 단일 진실 출처이다.

## CRITICAL RULE: Separation from Domain Events
- **Domain Event (`03_BACKEND/DDD/DOMAIN_EVENT_CATALOG.md`)**: DB 트랜잭션, 비즈니스 결과적 일관성, 시스템 상태 변경용 (`EVT_DOM_*`).
- **Analytics Event (본 문서)**: 유저 행동 추적, 화면 전환, UX 클릭, 클라이언트 추적용 (`evt_app_*`).
- 두 이벤트는 절대로 혼용되거나 동일한 네이밍 파이프라인을 공유하지 않는다.

## Analytics Event Naming Convention
- Format: `evt_app_[category]_[action]_[target]` (예: `evt_app_meal_click_camera`)

## Core Analytics Event Specification

| Category | Event Name | Trigger Condition | Properties Included | User Properties Set |
| :--- | :--- | :--- | :--- | :--- |
| **Onboarding** | `evt_app_onboarding_complete` | 온보딩 마지막 단계 통과 시 | `duration_sec, goal_type` | `user_goal, is_onboarded` |
| **Workout** | `evt_app_workout_submit` | 운동 기록 저장 버튼 클릭 시 | `workout_type, duration_min, cal` | `last_workout_date` |
| **Meal** | `evt_app_meal_analyzed` | AI 식단 분석 결과 확인 시 | `meal_type, photo_used, score` | `total_meals_logged` |
| **Companion**| `evt_app_companion_interact`| 건강이 터치 또는 대화 시 | `interaction_type, emotion_state` | `companion_level` |
| **Habit** | `evt_app_habit_check` | 습관 체크박스 완료 시 | `habit_id, current_streak` | `active_habit_count` |

## PII Exclusion & Security Filter
- Analytics Property에는 **사용자 이름, 이메일, GPS 위경도 좌표, 프라이빗 메모, 생체 데이터 원본**을 포함하는 것을 엄격히 금지한다.
- 모든 ID는 단방향 해시(SHA-256) 처리된 `analytics_id`를 사용한다.

## Runtime Impact
- 개인정보 리스크 없이 완벽하게 격리된 유저 행동 데이터를 수집하여 서비스 성장 지표를 정밀 측정한다.

## Related Documents
- `06_ANALYTICS/KPI_DASHBOARD_SPEC.md`
- `03_BACKEND/PRIVACY_DATA_POLICY.md`

## Change History
- v1.0.0 (2026-07-31): Initial Analytics Event Specification established.