# OBSERVABILITY_RUNBOOK

## Purpose
본 문서는 서비스 운영 중 발생하는 시스템 장애, AI 통신 이상, DB Deadlock 및 Outbox 지연 상황에서 온콜(On-Call) 담당자가 신속히 대응하기 위한 장애 등급, 알림(Alert) 및 복구 Runbook의 SSOT이다.

## Scope
백엔드 서버, API Gateway, Outbox Relayer, AI Engine, DB 모니터링 시스템 전반에 적용된다.

## SSOT
장애 등급 분류, 알림 임계치, 담당자 역할 및 항목별 긴급 대응 절차의 단일 진실 출처이다.

## Incident Severity Matrix

| Severity | Definition | Response SLA | Target Actions |
| :--- | :--- | :--- | :--- |
| **P0 (Critical)** | 전면 서비스 불능, DB Down, AI 통신 100% 장애 | 즉시 (5분 이내) | 긴급 조치팀 소집, Kill Switch 발동 |
| **P1 (Major)** | 주요 기능(식단/운동 저장) 에러율 $> 5\%$ 발생 | 15분 이내 | Fallback 서버 전환, Outbox 재시도 |
| **P2 (Minor)** | 특정 통계 조회 지연, 성능 예산 경미 도과 | 2시간 이내 | Read Model 캐시 Refresh, 로그 분석 |
| **P3 (Info)** | 단순 UI 표시 오류, 오탈자 | 24시간 이내 | 정기 배포 시 반영 |

## Emergency Response Runbooks

### 1. AI Engine Failure Runbook (AI 장애 대응)
1. PagerDuty / Slack Alert 통지 수신 (`AI_TIMEOUT_RATE > 10%`).
2. `FEATURE_FLAG_POLICY`에 따라 `AI_VISION_KILL_SWITCH`를 `OFF`로 전환.
3. 앱 화면에 "현재 AI 정밀 분석 지연 중입니다. 수동 영양소 입력 모드로 전환합니다" 문구 자동 노출 확인.
4. AI 서빙 서버 인스턴스 헬스체크 및 재부팅.

### 2. Outbox Relayer Lag Runbook (이벤트 정체 대응)
1. Outbox 테이블 내 `PENDING` 상태 건수가 $> 1,000$건 초과 시 Alert 발생.
2. Relayer 프로세스 Memory & DB Lock 상태 점검.
3. DLQ(Dead Letter Queue)로 이관된 메시지 원인 파악 및 `retry_count` 초기화 스크립트 실행.

## Runtime Impact
- 장애 발생 시 우왕좌왕하는 시간을 없애고 5분 이내에 명확한 절차에 따라 장애를 복구한다.

## Related Documents
- `03_BACKEND/LOGGING_AND_OBSERVABILITY.md`
- `03_BACKEND/FEATURE_FLAG_POLICY.md`
- `03_BACKEND/BACKUP_RECOVERY_PLAN.md`

## Change History
- v1.0.0 (2026-07-31): Observability Runbook initial release.