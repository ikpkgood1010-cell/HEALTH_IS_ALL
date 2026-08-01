# SYSTEM_INTEGRATION_GOVERNANCE_MASTER_V2.md

## Purpose
본 문서는 '헬스 이스 올(HEALTH IS ALL)' 프로젝트 전체의 시스템 통합, 건강 및 게임 요소의 이중 밸런스 유지, 동적 계산 수식 제어, 그리고 문서/코드 버전 정합성을 관리하는 최상위 거버넌스 명세서이다[cite: 9].

## Scope
* 백엔드, 프론트엔드, AI, 데이터베이스, 게임 시스템, UI/UX 전 영역[cite: 9]
* 사용자 건강 데이터 기반 동적 계산 알고리즘 및 예외 처리(Fallback) 메커니즘[cite: 9]
* 프로젝트 내 파일 배치 표준 및 버전 아카이빙 규칙[cite: 9]

## SSOT
`HEALTH IS ALL/00_PROJECT/SYSTEM_INTEGRATION_GOVERNANCE_MASTER_V2.md`[cite: 9]

## Definitions
* **Dual Balance**: 건강 관리의 목적성을 손상시키지 않으면서 게임의 몰입감을 최상으로 유지하는 상호 보완적 시스템 균형 구조[cite: 9].
* **Dynamic Formula Engine**: 동일한 입력값에 일률적인 결과가 출력되지 않도록 심박수, 환경, 연속 달성도 등 다변수를 조합하여 매번 정밀하게 변동하는 수식 엔진[cite: 9].
* **Fallback Rule**: 다변수 계산에 필요한 센서/외부 데이터 누락 또는 오류 발생 시, 시스템 중단 없이 안전하게 작동하는 간결형 계산식 전환 규칙[cite: 9].

## Runtime
* **Execution Environment**: Flutter Frontend / Python FastAPI Backend / SQLite & PostgreSQL[cite: 9]
* **Cycle**: 실시간 웨어러블 데이터 연동 및 일일 리셋(00:00 KST) 주기 작동[cite: 9]

## Rules
1. **이중 밸런스 준수**: 게임 요소가 화려하다고 해서 운동/식단 데이터의 명확성이 가려져서는 안 되며, 반대로 건강 표현이 너무 경직되어 게임적 재미를 저해해서는 안 된다[cite: 9].
2. **동적 계산 적용**: 모든 경험치, 칼로리, 스피릿 진화 수치 계산에는 다변수 정밀 공식을 우선 적용하며, 데이터 이상 발생 시 즉시 간결 수식으로 자동 이행한다[cite: 9].
3. **단일 버전 관리**: 중복 문서는 덮어쓰거나 통합하며, 대폭 구조 개편 시 최신 버전을 새로 작성하고 구버전은 `10_ARCHIVE/` 폴더로 즉시 격리 이동한다[cite: 9].

## State
```json
{
  "system_status": "INTEGRATED_ACTIVE",
  "governance_version": "2.0.0",
  "dual_balance_health_weight": 0.5,
  "dual_balance_game_weight": 0.5,
  "formula_engine_mode": "DYNAMIC_WITH_FALLBACK",
  "archive_policy": "STRICT_ISOLATION"
}
```

## Event
* `ON_HEALTH_DATA_RECEIVED`: 웨어러블/식단 입력 시 동적 수식 계산 엔진 트리거[cite: 9]
* `ON_FORMULA_ERROR`: 변수 누락 감지 시 Fallback 수식으로 즉시 전환[cite: 9]
* `ON_VERSION_UPGRADE`: 문서/코드 사양 업그레이드 시 아카이브 프로세스 자동 실행[cite: 9]

## Example
### 동적 칼로리 및 경험치 연산 예시
```python
# 다변수 정밀 계산 모드
dynamic_calorie = calculate_dynamic_calorie(
    bmr=1650, 
    hr_avg=135, 
    hr_rest=65, 
    hr_max=185, 
    temp_delta=2.5, 
    fatigue_factor=0.95
)

# 데이터 부족 시 Fallback 연산 예시
fallback_calorie = calculate_simple_calorie(
    bmr=1650, 
    met=6.0, 
    hours=1.0
)
```

## Exception
```json
{
  "exception_code": "ERR_FORMULA_VARIABLE_MISSING",
  "severity": "WARNING",
  "action": "FALLBACK_TO_SIMPLE_FORMULA",
  "user_message": "일부 데이터가 부족하여 기본 정밀 모드로 안전하게 계산되었습니다."
}
```

## Related Documents
* `HEALTH IS ALL/00_PROJECT/CANONICAL_NAMING.md`[cite: 9]
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V11_SPEC.md`[cite: 9]
* `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md`[cite: 9]
* `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V5.md`[cite: 9]
* `HEALTH IS ALL/10_ARCHIVE/`[cite: 9]

## Change History
| Date | Version | Author | Description |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | V1.0 | Core Engine Team | 최초 시스템 통합 거버넌스 문서 작성[cite: 9] |
| 2026-07-31 | V2.0 | Gemini AI Collaborator | 건강-게임 이중 밸런스, 다변수 동적 수식 및 아카이브 이동 규칙 전면 재정립[cite: 9] |