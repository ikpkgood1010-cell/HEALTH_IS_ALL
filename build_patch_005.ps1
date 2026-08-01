# build_patch_005.ps1
$files = @{
    "00_PROJECT\RELEASE_READINESS_CHECKLIST.md" = @"
# RELEASE_READINESS_CHECKLIST

## Purpose
본 문서는 '헬스 이스 올' 앱의 신규 버전 배포 시 각 단계(MVP, Beta, Production)별 필수 승인 조건을 검증하기 위한 SSOT 체크리스트이다.

## Scope
App Store/Play Store 배포, API, AI Prompt, Formula 검증에 적용된다.

## SSOT
배포 가능 여부(Go / No-Go) 판정 기준의 단일 진실 출처이다.

## Gate 1: MVP Release Criteria
- [ ] 핵심 건강 기록 기능 정상 작동
- [ ] Companion 캐릭터 기본 렌더링 및 상태 피드백
- [ ] Formula Engine 단위 테스트 커버리지 > 85%
- [ ] API p95 < 500ms
- [ ] App Crash Free Rate > 98.0%

## Gate 2: Beta Release Criteria
- [ ] AI 비전 환각률 < 3%
- [ ] Transactional Outbox 지연 시간 < 1.0s
- [ ] Analytics 이벤트 PII 필터링 검증
- [ ] App Crash Free Rate > 99.0%

## Gate 3: Production Release Criteria
- [ ] Security & Privacy 영향평가 완료
- [ ] Performance Budget 충족 (Cold Start < 1.5s, 60 FPS)
- [ ] Trace ID 모니터링 및 P0/P1 Alert 작동
- [ ] DB/S3 백업 및 DR 모의 훈련 통과
- [ ] App Crash Free Rate > 99.8%

## Related Documents
- 06_QA/QA_TEST_STRATEGY.md
- 03_BACKEND/SECURITY_POLICY.md
- 03_BACKEND/PRIVACY_DATA_POLICY.md

## Change History
- v1.0.0 (2026-07-31): Initial Release Readiness Checklist established.
"@

    "06_QA\QA_TEST_STRATEGY.md" = @"
# QA_TEST_STRATEGY

## Purpose
프론트엔드, 백엔드, AI 엔진 및 건강/게이밍 Formula 전반의 테스트 전략 SSOT이다.

## Scope
Flutter 클라이언트, Spring Boot 백엔드, AI 엔진, CI/CD에 적용된다.

## SSOT
테스트 계층 구조 및 자동화 기준의 단일 진실 출처이다.

## Test Layer Specifications
1. Unit Test: Coverage > 85%, Branch > 80%.
2. Widget Test: Coverage > 70%.
3. AI & Formula Precision Test: 오차율 E <= 2% 이내 준수.
4. Regression & Smoke Test: 핵심 API Health Check 100% 자동화.

## Related Documents
- 00_PROJECT/RELEASE_READINESS_CHECKLIST.md

## Change History
- v1.0.0 (2026-07-31): Initial QA Test Strategy defined.
"@

    "06_ANALYTICS\ANALYTICS_EVENT_SPEC.md" = @"
# ANALYTICS_EVENT_SPEC

## Purpose
유저 행동 분석 및 퍼널 측정을 위한 Analytics Event 사양 SSOT이다.

## Scope
Flutter 이벤트 수집기, Firebase Analytics, Mixpanel에 적용된다.

## SSOT
사용자 행동 트래킹 이벤트 규격의 단일 진실 출처이다.

## Rule: Separation from Domain Events
- Domain Event (EVT_DOM_*): DB 트랜잭션 및 비즈니스 결과적 일관성용.
- Analytics Event (evt_app_*): 유저 행동 및 UI 추적용.

## Naming Convention
evt_app_[category]_[action]_[target]

## Related Documents
- 06_ANALYTICS/KPI_DASHBOARD_SPEC.md
- 03_BACKEND/PRIVACY_DATA_POLICY.md

## Change History
- v1.0.0 (2026-07-31): Initial Analytics Event Spec established.
"@

    "06_ANALYTICS\KPI_DASHBOARD_SPEC.md" = @"
# KPI_DASHBOARD_SPEC

## Purpose
건강 달성률 및 게이밍 몰입도를 평가하는 KPI 수식 및 매핑 SSOT이다.

## Scope
운영 대시보드 및 서비스 제품 의사결정에 적용된다.

## SSOT
비즈니스 지표 계산 공식의 단일 진실 출처이다.

## Key Metrics
- Day 1 Retention > 55%, D7 > 30%, D30 > 18%
- Meal Logging Rate > 65%, Workout Logging Rate > 40%
- Companion Interaction Engagement > 50%

## Related Documents
- 06_ANALYTICS/ANALYTICS_EVENT_SPEC.md

## Change History
- v1.0.0 (2026-07-31): KPI Dashboard Spec established.
"@

    "03_BACKEND\FEATURE_FLAG_POLICY.md" = @"
# FEATURE_FLAG_POLICY

## Purpose
안전한 배포, A/B 테스트 및 Kill Switch 제어를 위한 Feature Flag 정책 SSOT이다.

## Scope
백엔드 API, AI 통신, Flutter UI 제어에 적용된다.

## SSOT
Feature Flag 관리 규격의 단일 진실 출처이다.

## Flag Types
1. Kill Switch: 장애 발생 시 기능 즉시 비활성화.
2. Beta Flag: 특정 유저 타겟팅.
3. A/B Flag: 실험 집단 분리.
4. Gradual Flag: 비율 기반 카나리 배포.

## Related Documents
- 00_PROJECT/RELEASE_READINESS_CHECKLIST.md
- 03_BACKEND/OBSERVABILITY_RUNBOOK.md

## Change History
- v1.0.0 (2026-07-31): Feature Flag Policy established.
"@

    "03_BACKEND\SECURITY_POLICY.md" = @"
# SECURITY_POLICY

## Purpose
인증/인가, 데이터 암호화, API Rate Limit 및 보안 표준 규정 SSOT이다.

## Scope
API Gateway, DB, Flutter 토큰 관리에 적용된다.

## SSOT
정보보안 및 암호화 규격의 단일 진실 출처이다.

## Standards
- JWT RS256 + Refresh Token Rotation.
- DB AES-256-GCM 암호화, TLS 1.3 강제.
- Token Bucket Rate Limiting (120 req/min).

## Related Documents
- 03_BACKEND/PRIVACY_DATA_POLICY.md

## Change History
- v1.0.0 (2026-07-31): Security Policy established.
"@

    "03_BACKEND\PRIVACY_DATA_POLICY.md" = @"
# PRIVACY_DATA_POLICY

## Purpose
건강, 생체, 식단 정보 등 민감 개인정보 처리 및 AI 통제 규정 SSOT이다.

## Scope
저장되는 모든 사용자 데이터 및 AI 연산 흐름에 적용된다.

## SSOT
민감 데이터 프라이버시 보호의 단일 진실 출처이다.

## Core Rules
- AI 전달 시 PII 완전 제로화.
- 탈퇴 요청 시 3초 이내 완전 파기.
- 데이터 내보내기(Export) 권리 보장.

## Related Documents
- 03_BACKEND/SECURITY_POLICY.md

## Change History
- v1.0.0 (2026-07-31): Privacy Data Policy established.
"@

    "03_BACKEND\BACKUP_RECOVERY_PLAN.md" = @"
# BACKUP_RECOVERY_PLAN

## Purpose
장애 및 데이터 파손 시 백업 및 재해 복구(DR) 절차 SSOT이다.

## Scope
RDB, S3, Redis, Formula/Prompt 버전 관리에 적용된다.

## SSOT
RPO/RTO 기준 및 DR 실행 가이드의 단일 진실 출처이다.

## Objectives
- RPO < 5분
- RTO < 30분

## Related Documents
- 03_BACKEND/OBSERVABILITY_RUNBOOK.md

## Change History
- v1.0.0 (2026-07-31): Backup Recovery Plan established.
"@

    "02_FRONTEND\PERFORMANCE_BUDGET.md" = @"
# PERFORMANCE_BUDGET

## Purpose
Flutter 클라이언트 성능 예산 및 한계선 규정 SSOT이다.

## Scope
앱 렌더링, 네트워크, 메모리, AI 지연 제어에 적용된다.

## SSOT
성능 한계선 및 대응 방안의 단일 진실 출처이다.

## Targets
- Cold Start < 1.2s (Hard Limit 2.0s)
- 60 FPS (16.6ms) 유지
- API p95 < 300ms, RAM < 180MB

## Related Documents
- 00_PROJECT/RELEASE_READINESS_CHECKLIST.md

## Change History
- v1.0.0 (2026-07-31): Performance Budget established.
"@

    "03_BACKEND\OBSERVABILITY_RUNBOOK.md" = @"
# OBSERVABILITY_RUNBOOK

## Purpose
장애 발생 시 온콜 대응을 위한 장애 등급 및 복구 Runbook SSOT이다.

## Scope
백엔드, API Gateway, Outbox, AI Engine, DB에 적용된다.

## SSOT
장애 대응 절차의 단일 진실 출처이다.

## Severity & Runbooks
- P0 (Critical): 즉시 대응, Kill Switch 발동.
- P1 (Major): 15분 이내 대응, Graceful Fallback.
- Outbox 지연 및 AI 장애 대응 Runbook 제공.

## Related Documents
- 03_BACKEND/FEATURE_FLAG_POLICY.md
- 03_BACKEND/BACKUP_RECOVERY_PLAN.md

## Change History
- v1.0.0 (2026-07-31): Observability Runbook established.
"@
}

Write-Host "Starting file generation..."

foreach ($path in $files.Keys) {
    $dir = Split-Path $path
    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($path, $files[$path], [System.Text.Encoding]::UTF8)
    Write-Host " -> Created: $path"
}

$dirsToZip = @("00_PROJECT", "06_QA", "06_ANALYTICS", "03_BACKEND", "02_FRONTEND")
if (Test-Path "HEALTH_IS_ALL_PATCH_005.zip") {
    Remove-Item "HEALTH_IS_ALL_PATCH_005.zip" -Force
}
Compress-Archive -Path $dirsToZip -DestinationPath "HEALTH_IS_ALL_PATCH_005.zip" -Force

Write-Host "`n[SUCCESS] HEALTH_IS_ALL_PATCH_005.zip created successfully!"