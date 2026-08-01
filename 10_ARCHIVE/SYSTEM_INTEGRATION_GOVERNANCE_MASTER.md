# SYSTEM INTEGRATION GOVERNANCE MASTER

## Purpose
본 문서는 'HEALTH IS ALL' 시스템 전체의 기본 로직, 건강-게임 이중 밸런스(Dual Balance), 동적 정밀 계산식, 디렉터리 체계 및 예외 처리 규정을 통합 제어하고 최선의 운영 상태를 유지하기 위해 작성되었습니다.

## Scope
* 'HEALTH IS ALL' 프로젝트의 전체 폴더 및 파일 구조 (`00_PROJECT` ~ `13_ARCHIVE`)
* 프론트엔드(Flutter), 백엔드(Python), AI 에이전트, 게임 시스템 및 분석 엔진 간 데이터 흐름
* 운동, 식단, 수면, 정령(Spirit) 성장, 리워드 동적 계산식 및 안전 폴백 시스템

## SSOT
* **SSOT 문서 위치**: `HEALTH IS ALL/00_PROJECT/SYSTEM_INTEGRATION_GOVERNANCE_MASTER.md`
* **시스템 구동 원칙**: 본 문서에 정의된 통합 규정과 규칙이 프로젝트 내 모든 사양서 및 코드 구현의 최상위 기준(Single Source of Truth)이 됩니다.

## Definitions
1. **Health-Game Dual Balance**: 건강 증진이라는 본래 목적을 최우선으로 하되, 게임 요소의 완성도 또한 최고 수준으로 유지하여 상호 시너지를 내는 시스템 설계 원칙.
2. **Dynamic Multi-Variable Formula**: 정적 상수가 아닌 사용자의 실시간 신체 수치, 환경 변화, 정령 친밀도, 연속 달성일 등 다양한 변수를 반영하여 매회 정밀하게 달라지는 계산 체계.
3. **Safety Fallback Mechanism**: 복잡한 수식 연산 중 데이터 누락, 0 분모 연산, 타임아웃 발생 시 시스템 오류 없이 안전한 기본 계산 체계로 자동 전환되는 보호 로직.

## Runtime
* **프론트엔드 엔진**: Flutter / Dart SDK v3.x (경로: `04_FRONTEND/lib/`)
* **백엔드/AI 엔진**: Python 3.11+ / FastAPI (경로: `backend/`, `03_BACKEND/`)
* **데이터베이스**: PostgreSQL / SQLite (동기화) (경로: `02_DATABASE/`)

## Rules
1. **화면 및 UX 주도권 규정**:
   * 메인 대시보드 및 전체 UX에서 건강 데이터(오늘의 칼로리, 탄단지, 운동량, 수면 등)가 주 표기되며, 게임 요소(정령, 퀘스트, 아이템)는 이를 직관적이고 친근하게 보조/시각화하는 역할로 동작한다.
2. **동적 정밀 계산 체계**:
   * **칼로리 소모 수식**:
     $$Calorie_{Burn} = MET \times Weight(kg) \times Time(hr) \times \left(1 + \frac{HeartRate_{Avg} - HeartRate_{Rest}}{HeartRate_{Max}} \times 0.2\right) \times SpiritSynergy$$
   * **정령 성장 경험치(EXP) 수식**:
     $$EXP_{Gained} = \left(NutrientScore \times 0.4 + WorkoutScore \times 0.4 + SleepScore \times 0.2\right) \times StreakBonus \times RandomFactor(0.95 \sim 1.05)$$
   * 수식 내 모든 무작위성(RandomFactor)은 사용자의 지루함을 방지하는 미세 변량으로 작동하되, 밸런스를 저해하지 않는다.
3. **폴백 규칙**:
   * 계산 변수 중 필수 심박수 데이터나 특수 수치가 누락된 경우, 즉시 기본 단편 수식($Calorie = MET \times Weight \times Time$)으로 안전 전환(Fallback)한다.

## State
* `INIT`: 전체 엔진 초기화 및 DB/동기화 상태 확인
* `SYNCING`: 오프라인 기기 데이터 및 웨어러블 데이터 동기화 중
* `COMPUTING`: 다변수 동적 계산식 적용 및 건강-게임 통합 점수 산출 중
* `FALLBACK`: 수식 오류/데이터 결손에 따른 안전 기본 수식 적용 상태
* `STEADY`: 대시보드 표기 및 유저 상호작용 완료 상태

## Event
* `ON_HEALTH_DATA_INPUT`: 유저의 식단/운동/수면 입력 이벤트 발생
* `ON_WEARABLE_SYNC`: 웨어러블 장치 실시간 데이터(심박수 등) 수신
* `ON_CALCULATION_ERROR`: 수식 연산 예외 감지 시 폴백 이벤트를 발생시켜 전환
* `ON_SPIRIT_EVOLUTION`: 건강 점수 누적에 따른 정령 성장 및 팝업 이벤트

## Example
* **유저 시나리오**:
  1. 유저가 점심 식단 사진 등록 및 30분 산책 입력 (`ON_HEALTH_DATA_INPUT`).
  2. 시스템이 영양 밸런스 점수(88점) 및 심박 반영 산책 소모 칼로리(142 kcal)를 동적 연산 (`COMPUTING`).
  3. 계산된 결과가 정령 친밀도 경험치(+35 EXP)로 동시 전환되며 친절하고 호감 있는 팝업 멘트 출력 ("오늘 점심 영양 밸런스가 정말 훌륭해요! 정령이 활력을 얻었습니다!").

## Exception
내부 시스템 예외 발생 시 시스템 정지를 방지하기 위해 아래 예외 로직을 실행합니다:

```json
{
  "exception_handler": {
    "error_code": "ERR_CALCULATION_OVERFLOW_OR_NULL",
    "trigger_condition": "Division by zero or missing wearable heart rate data",
    "fallback_action": "APPLY_PRIMARY_SIMPLE_FORMULA",
    "user_notification": "정밀 데이터 수신 대기 중입니다. 기본 건강 지표로 안전하게 계산되었습니다.",
    "log_level": "WARNING"
  }
}
```

## Related Documents
* `HEALTH IS ALL/00_PROJECT_START/DEVELOPMENT_ROADMAP_V9.md`
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V11_SPEC.mdux`
* `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.mdux`
* `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V5.mdux`
* `HEALTH IS ALL/04_FRONTEND/UI_SCREEN_SPECIFICATION_V3.mdux`

## Change History
* **2026-07-31**: 전체 프로젝트 압축파일 검토 반영, 프론트엔드/백엔드 디렉터리 번호 중복 해소, 건강-게임 이중 밸런스 규격 및 동적 예외 처리 로직을 포함한 시스템 마스터 문서 통합 제정. [중복문서-덮어쓰기]