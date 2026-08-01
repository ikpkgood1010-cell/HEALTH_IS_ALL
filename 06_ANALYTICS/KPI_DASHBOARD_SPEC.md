# KPI_DASHBOARD_SPEC

## Purpose
본 문서는 '헬스 이스 올' 프로젝트의 건강 달성률 및 게이밍 몰입도를 평가하는 핵심 성과 지표(KPI)의 수식, 목표치 및 Analytics Event 매핑 구조를 정립하는 SSOT이다.

## Scope
운영 모니터링 대시보드, 데이터 분석가 리포트 및 제품 의사결정에 적용된다.

## SSOT
시스템 전체 비즈니스 지표 계산 공식 및 목표 수치의 단일 진실 출처이다.

## Key Performance Indicators & Formulas

### 1. Retention Indicators
- **Day 1 Retention**:
  $$R_{D1} = \frac{\text{Users Active on Day 1 after Signup}}{\text{Total Signups on Day 0}} \times 100 \quad (\text{Goal: } > 55\%)$$
- **Day 7 / Day 30 Retention**: $R_{D7} > 30\%$, $R_{D30} > 18\%$ 목표.

### 2. Health Logging Engagement Rates
- **Meal Logging Rate (식단 기록율)**:
  $$\text{MLR} = \frac{\text{DAU performing } \ge 1 \text{ meal log}}{\text{Total DAU}} \times 100 \quad (\text{Goal: } > 65\%)$$
- **Workout Logging Rate (운동 기록율)**: $\text{WLR} > 40\%$ 목표.

### 3. Gaming & Companion Interaction Metrics
- **Companion Touch Engagement Rate**:
  $$\text{CER} = \frac{\text{DAU triggering } \text{evt\_app\_companion\_interact}}{\text{Total DAU}} \times 100 \quad (\text{Goal: } > 50\%)$$
- **Habit Completion Rate**: 일일 활성 습관의 평균 달성 비율 ($> 75\%$ 목표).

## KPI to Analytics Event Mapping Table

| KPI Name | Source Analytics Events | Target Metric | Calculation Window |
| :--- | :--- | :--- | :--- |
| **DAU / WAU / MAU** | `evt_app_session_start` | Unique User Count | Daily / Weekly / Monthly |
| **D1 / D7 Retention** | `evt_app_onboarding_complete` $\rightarrow$ `evt_app_session_start` | Cohort Ratio | Rolling 1 / 7 Days |
| **Meal Logging Rate**| `evt_app_meal_analyzed` | User Ratio | Daily |
| **Habit Completion** | `evt_app_habit_check` | Completion Ratio | Daily |

## Runtime Impact
- 건강과 게임 요소 간의 균형 잡힌 성장을 수치화하여 특정 요소 편중 현상을 조기에 감지하고 피드백한다.

## Related Documents
- `06_ANALYTICS/ANALYTICS_EVENT_SPEC.md`

## Change History
- v1.0.0 (2026-07-31): KPI Dashboard Specification established.