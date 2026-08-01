# QA_TEST_STRATEGY

## Purpose
본 문서는 프론트엔드, 백엔드, AI 엔진 및 건강/게이밍 계산 공식(Formula) 전반의 품질을 검증하기 위한 테스트 레이어, 자동화 범위 및 커버리지 목표를 정의하는 SSOT이다.

## Scope
Flutter 클라이언트 애플리케이션, Spring Boot 백엔드, Python AI 분석 엔진 및 CI/CD 파이프라인에 적용된다.

## SSOT
프로젝트 전체의 테스트 계층 구조, 자동화 기준 및 수락 테스트 조건의 단일 진실 출처이다.

## Testing Pyramid & Automation Coverage Targets

```
           / \
          /   \        [E2E / Release Test] (Manual + Cypress/Appium: 10%)
         /     \      -------------------------------------------------------
        / Integration \    [Integration & Contract Test] (Backend & AI: 20%)
       /---------------\  ---------------------------------------------------
      /   Widget Test   \  [Flutter Component & Screen Test] (Coverage > 70%)
     /-------------------\---------------------------------------------------
    /      Unit Test      \ [Domain Model, Formula, Utility Test] (Coverage > 85%)
   /-----------------------\
```

## Test Layer Specifications

### 1. Unit Test (단위 테스트)
- **Target**: DDD Aggregate Domain Logic, Formula Engine 수식 계산, DTO Mapper.
- **Coverage Goal**: Code Coverage $> 85\%$, Branch Coverage $> 80\%$.
- **Rule**: 외부 I/O(DB, Network)는 Mocking 처리하며 단일 테스트 실행 시간은 $10\text{ms}$ 이하여야 한다.

### 2. Widget Test (플러터 위젯 테스트)
- **Target**: UI Component, Custom Gauge Widget, Companion Motion Component.
- **Coverage Goal**: Widget Coverage $> 70\%$.

### 3. AI & Formula Precision Test
- **Target**: AI 비전 영양소 추정 오차 범위, 복합 건강 점수(Health Score) 다변수 수식 검증.
- **Assertion Formula**: 계산된 표준 오차율 $E$가 임계치 이하여야 한다.
  $$E = \frac{|\text{Calculated\_Score} - \text{Expected\_Score}|}{\text{Expected\_Score}} \le 0.02 \quad (2\% \text{ 이내})$$

### 4. Regression & Smoke Test
- **Smoke Test**: CI/CD 배포 직후 핵심 API 10종에 대한 Health Check (자동화 100%).
- **Regression Test**: 신규 기능 추가 시 기존 게이밍 Quest/Reward 및 건강 기록 기능 영향도 평가.

## Runtime Impact
- 코드 수정 시 기존 계산식 및 게이밍 로직 부작용(Side Effect)이 즉시 감지되어 시스템 안정성이 보장된다.

## Related Documents
- `00_PROJECT/RELEASE_READINESS_CHECKLIST.md`
- `03_BACKEND/DDD/APPLICATION_SERVICE_GUIDE.md`

## Change History
- v1.0.0 (2026-07-31): Initial QA Test Strategy defined.