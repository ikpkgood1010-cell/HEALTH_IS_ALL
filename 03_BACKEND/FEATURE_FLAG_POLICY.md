# FEATURE_FLAG_POLICY

## Purpose
본 문서는 신규 기능의 안전한 배포, A/B 테스트, 긴급 차단(Kill Switch) 및 점진적 노출(Gradual Rollout)을 제어하기 위한 Feature Flag 운영 정책의 SSOT이다.

## Scope
백엔드 API, AI 서비스 통신, Flutter UI 구성 요소 제어 전반에 적용된다.

## SSOT
Feature Flag 생성, 평가 수식, Rollout 알고리즘 및 만료 관리 표준의 단일 진실 출처이다.

## Flag Taxonomy & Life Cycle

| Flag Type | Purpose | Target Scope | Default State | Max TTL |
| :--- | :--- | :--- | :--- | :--- |
| **Kill Switch** | 시스템 장애 시 특정 기능 긴급 비활성화 | Global / API / AI | `ENABLED` | Permanent |
| **Beta Flag** | 신규 기능 테스터 그룹 사전 공개 | Specific User IDs | `DISABLED` | 60 Days |
| **A/B Flag** | UX/게이밍 밸런스 실험 비교 | Randomized Cohort | `EVALUATED` | 30 Days |
| **Gradual Flag**| % 비율 기반 카나리 배포 | Percentage Hash | `0% -> 100%` | 14 Days |

## Consistent Hash Rollout Formula
사용자 ID 기반의 일관된 퍼센티지 롤아웃 평가 수식:
$$\text{UserHash} = \text{MurmurHash3}(\text{UserId} + \text{FlagKey}) \pmod{100}$$
$$\text{IsEligible} = \begin{cases} \text{true} & \text{if } \text{UserHash} < \text{TargetPercentage} \\ \text{false} & \text{otherwise} \end{cases}$$

## Operational Rules
1. **Kill Switch Priority**: Kill Switch Flag가 `OFF`로 전환되면 하위 모든 비즈니스 로직 및 AI 연산은 즉시 Graceful Fallback(기본 기능 응답)으로 전환된다.
2. **Flag Cleanup (만료 정책)**: 배포 완료 후 30일이 지난 실험 플래그는 코드베이스에서 완전히 제거(Refactoring)해야 한다.

## Runtime Impact
- 앱 재배포 없이 서버 측 설정만으로 장애 기능을 0.1초 이내에 차단하고 유저 리스크를 최소화한다.

## Related Documents
- `00_PROJECT/RELEASE_READINESS_CHECKLIST.md`
- `03_BACKEND/OBSERVABILITY_RUNBOOK.md`

## Change History
- v1.0.0 (2026-07-31): Feature Flag Policy established.