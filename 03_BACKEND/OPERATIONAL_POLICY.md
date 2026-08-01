# OPERATIONAL\_POLICY.md

## Purpose

본 문서는 'HEALTH IS ALL' 서비스 운영 중 발생하는 데이터 리셋, 서비스 점검, 동기화 정책 및 예외 처리 기준을 정의하여 백엔드 Engine 및 DDD Domain Logic과의 충돌을 방지함을 목적으로 한다.

## Scope

* 백엔드 API 서버, 백그라운드 스케줄러, 오프라인 클라이언트 동기화 엔진 전체
* 일일/주간 리셋 정책, 서비스 점검 시 트랜잭션 처리, 이상 데이터 탐지 정책

## SSOT

* **SSOT Document**: `HEALTH IS ALL/03\_BACKEND/OPERATIONAL\_POLICY.md`
* **Authority**: Backend Core Architecture Team

## Definitions

* **Daily Reset**: 매일 KST 04:00:00에 실행되는 일일 일퀘 및 상태 수치 초기화 배치 작업
* **Grace Period**: 오프라인 상태에서 생성된 클라이언트 데이터의 동기화 유효 인정 시간 (최대 72시간)
* **Soft Ban**: 부정행위 탐지 시 계정 차단 대신 보상 획득률을 0으로 고정하는 운영 조치

## Runtime

* **Execution Environment**: FastAPI Async Scheduler / Celery Worker
* **Timezone Standard**: UTC+9 (KST)

## Rules

1. **일일 리셋 일관성**: KST 04:00:00 기준 미완료 퀘스트는 실패 처리되며, 정령 상태 보정 계산식은 아래 다변수 공식을 따른다.
$$S\_{health} = \\max\\left(0, S\_{prev} - \\left(10 \\times \\delta\_{idle} \\times \\left(1 + \\frac{\\text{UnmetQuests}}{\\text{TotalQuests}}\\right)\\right)\\right)$$
2. **DDD 도메인 규칙 준수**: 운영 정책에 의한 데이터 변경은 반드시 Aggregate Root를 통해서만 수행되며 DB 직접 수정(Direct SQL Write)은 금지한다.
3. **오프라인 데이터 허용 한도**: 서버 타임스탬프 대비 72시간 이상 차이나는 오프라인 기록은 Validation Fail로 처리하여 배그라운드 로그에 기록 후 기각한다.

## State

* `NORMAL`: 정상 운영 상태
* `MAINTENANCE`: 서비스 점검 상태 (읽기 전용 모드 전환)
* `EMERGENCY\_SHUTDOWN`: 심각한 데이터 오염 발생 시 트랜잭션 차단 상태

## Event

* `OPERATIONAL\_RESET\_COMPLETED`: 일일 리셋 완료 시 발행되는 도메인 이벤트
* `SUSPICIOUS\_ACTIVITY\_DETECTED`: 이상 동작 감지 시 보안 및 분석 시스템으로 전달되는 이벤트

## Example

```json
{
  "event\_name": "OPERATIONAL\_RESET\_COMPLETED",
  "timestamp": "2026-07-31T04:00:00+09:00",
  "affected\_users": 14250,
  "reset\_metrics": \["daily\_quests", "water\_intake\_counter", "spirit\_fatigue"]
}



Exception

점검 중 수신된 클라이언트 요청: HTTP Status Code 503 Service Unavailable 반환 및 Retry-After 헤더 명시.



리셋 작업 중 DB Deadlock 발생 시: 최대 3회 재시도 후 실패 시 관리자 PagerDuty 알림 발송.



Related Documents

HEALTH IS ALL/01\_ARCHITECTURE/DOMAIN\_DESIGN.md



HEALTH IS ALL/03\_BACKEND/DDD/AGGREGATE\_BOUNDARY.md



Change History

v1.0.0 (2026-07-31): PATCH-005 최초 제정.

