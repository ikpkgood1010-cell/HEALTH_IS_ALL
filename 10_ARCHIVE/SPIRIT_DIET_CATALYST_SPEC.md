# SPIRIT_DIET_CATALYST_SPEC.md

## Purpose
본 문서는 사용자가 기록한 식단의 영양성분(탄수화물, 단백질, 지방, 식이섬유, 정제당 등)을 다변수 수식으로 평가하여, 사용자 건강 지표 개선과 정령(Spirit)의 성장 촉진제(Growth Catalyst) 산출 로직을 정의한다.

## Scope
1. 매크로/미크로 영양소 밸런스 점수(Nutrient Balance Score, NBS) 산출
2. 정제당, 알코올, 과도한 나트륨에 대한 감점 및 정령 감정 상태(Mood) 변화 규칙
3. 식단 기록 기반 '정령 성장 촉진제(Spirit Growth Catalyst)' 획득 수식
4. 영양 정보 미비 시 열량 기반 간이 계산법(Fallback) 전환 로직

## SSOT
본 문서는 백엔드 영양 평가 엔진(`backend/diet_spirit_engine.py`) 및 프론트엔드 정령 인터랙션 위젯(`lib/spirit_diet_interactive_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **NBS (Nutrient Balance Score)**: 영양소 비율, 식이섬유 비중, 정제당 유무를 종합 평가한 0~100점 영양 점수.
- **Catalyst Essence**: 정령의 급속 성장에 사용되는 핵심 재화.
- **Spirit Mood**: 식단 품질에 따라 달라지는 정령의 반응 상태 (JOYFUL, SATISFIED, SLUGGISH, DISTRESSED).

## Runtime
- 프론트엔드(Flutter): 식단 입력 시 즉시 정령 반응 애니메이션 및 대사 출력.
- 백엔드(FastAPI/Python): 영양 DB 검증 및 일일 정령 촉진제 최종 지급 확정.

## Rules
1. **건강-게임 주객전도 방지**: 게임 보상을 위해 부실한 식단을 기록하는 부정행위를 방지하고, 클린 식단(자연식, 고단백, 저정제당)일수록 정령 성장이 비선형적으로 대폭 증가한다.
2. **동적 미세 변동**: 동일한 식단을 입력하더라도 일일 연속 클린 식단 달성일(Clean Streak)과 미세 변동 난수($0.95 \sim 1.05$)가 적용되어 항상 유기적인 보상 수치를 제공한다.
3. **Fallback 정책**: 상세 영양 성분(식이섬유, 당류 등) 데이터가 누락된 경우, 기본 탄단지 비율 기반의 간이 평가식으로 자동 전환되어 시스템 중단이나 계산 오류를 방지한다.

## State
- `protein_g`, `carbs_g`, `fat_g`, `fiber_g`, `added_sugar_g`
- `clean_diet_streak`: 연속 클린 식단 유지 일수
- `spirit_mood_state`: 정령의 현재 감정 상태

## Event
- `ON_DIET_LOGGED`: 식단 등록 시 영양 평가 및 정령 대사/보상 연동
- `ON_CATALYST_GAINED`: 정령 촉진제 에센스 획득 및 정령 친밀도 상승
- `ON_FALLBACK_DIET_TRIGGERED`: 영양 정보 부족 시 간이 수식 전환

## Example
$$\text{Base NBS} = \left( \frac{\text{Protein(g)} \times 4}{\text{Total Cal}} \times 40 \right) + \left( \frac{\text{Fiber(g)}}{\text{Target Fiber}} \times 30 \right) + 30$$
$$\text{Sugar Penalty} = \max\left(0, \frac{\text{Added Sugar(g)} \times 4}{\text{Total Cal}} - 0.1\right) \times 100$$
$$\text{Final NBS} = \text{Clamp}\left(\text{Base NBS} - \text{Sugar Penalty}, 10, 100\right)$$

## Exception
- 식단 칼로리가 0kcal 이하로 입력되거나, 1회 식단이 3,000kcal를 초과하는 비정상 데이터는 안전 기준치(400kcal, 표준 비율)로 자동 교정 후 계산한다.

## Related Documents
- `01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY.md`
- `03_BACKEND/DIET_ENGINE.mdux`
- `03_GAME_SYSTEM/SPIRIT_GROWTH.mdux`

## Change History
- 2026-07-31 (PATCH_007): 식단 동적 영양 평가 및 정령 성장 촉진제 연동 명세 신규 작성 (SSOT 규격 준수).