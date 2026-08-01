# RECOVERY_BALANCE_SPEC_V3.md

## Purpose
사용자의 수면 및 휴식 데이터를 바탕으로 생체 회복 지수를 측정하고, 스피릿(Spirit) 캐릭터의 상태 및 게임 활동력 버프를 산출하는 명세입니다.

## Scope
* 수면 효율성 분석 및 HRV 기반 피로도 복원 알고리즘
* 스피릿 컨디션 및 유저 스테미나 회복 수식

## SSOT
* 회복 지수 및 휴식 밸런스 연산에 관한 최상위 규격 문서.

## Definitions
* **Recovery Score ($RS$)**: $0 \sim 100$점 범위의 일일 회복 지수.
* **HRV Normalization**: 사용자의 평균 HRV 대비 당일 회복 비율.

## Runtime
* 매일 아침 수면 데이터 동기화 시 수면 엔진에서 자동 트리거.

## Rules
1. **회복 점수 계산식**:
   $$RS = Clamp((Sleep_{eff} \times 0.4) + (HRV_{norm} \times 0.4) + (Rest_{min} \times 0.2), 0, 100)$$
   * $Sleep_{eff}$: 수면 점수 ($0 \sim 100$)
   * $HRV_{norm}$: 평균 대비 HRV 비율 지수 ($0 \sim 100$)
   * $Rest_{min}$: 휴식 점수 ($0 \sim 100$)
2. $RS \ge 80$: 스피릿 '최상' 상태, 경험치 $1.2\times$ 버프.
3. $RS < 50$: 스피릿 '휴식 필요' 상태, 따뜻한 응원 팝업 표시 및 과도한 운동 자제 권고.

## State
* States: RECOVERY_EXCELLENT, RECOVERY_NORMAL, RECOVERY_REST_NEEDED

## Event
* `EVENT_RECOVERY_SCORE_UPDATED`: 회복 점수 신규 업데이트.

## Example
* 수면 점수 85점, HRV 지수 90점 반영 시 회복 점수 87점 달성.

## Exception
* 수면 측정 기기 부재 시 유저의 주관적 컨디션 입력 3단계(좋음/보통/피곤)로 자동 점수 부여.

## Related Documents
* `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v7.py`
* `HEALTH IS ALL/05_AI/HEALTH_FEEDBACK_INTELLIGENCE_SPEC_V7.md`

## Change History
| 날짜 | 버전 | 작성자 | 변경 내용 |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | V3.0.0 | Health Domain | V3 삼각 생체 회복 알고리즘 및 스피릿 감정 연동 정의 |