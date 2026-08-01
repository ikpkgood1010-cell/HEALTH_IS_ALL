# SPIRIT_DIET_CATALYST_SPEC_V2.md

## Purpose
본 문서는 정령(Spirit)의 성장이 사용자의 건강한 식습관 및 운동 이행에 의해 촉매(Catalyst) 작용을 받아 다차원적으로 진화하는 아키텍처 스펙 v2를 정의합니다.

## Scope
* 식단 클린 지수(Clean Diet Index)와 정령 속성(불, 물, 바람, 대지) 간의 매핑
* 정령 진화 및 감정 상태 변화 알고리즘
* 백엔드 엔진 연동 수식 및 상태 보정

## SSOT
* **경로**: `HEALTH IS ALL/01_ARCHITECTURE/SPIRIT_DIET_CATALYST_SPEC_V2.md`
* **소유팀**: Spirit System Logic Team

## Definitions
* **Clean Diet Index (CDI)**: 가공식품, 정제당, 튀김류를 피하고 건강한 식단을 이행했을 때 부여되는 보정 스코어.
* **Spirit Affinity**: 정령과 유저 간의 친밀도 수준.

## Runtime
* **실행 환경**: 백엔드 식단 처리 엔진 및 프론트엔드 정령 애니메이션 레이어

## Rules
1. 건강한 식단을 이행할수록 정령의 스킬 쿨타임 감소 및 비주얼 이펙트가 화려해진다.
2. 불균형 식단 시 정령이 아파하거나 슬퍼하는 모션을 취하여 자연스러운 식습관 개선을 유도한다.
3. 연산 수식은 정적 수치에 머물지 않고 당일 활동량과 수면 효율 변수를 동적으로 반영한다.

## State
* `NORMAL`: 일반 성장 상태
* `BOOSTED`: 클린 식단 연속 달성으로 경험치 촉매 증폭 상태
* `DORMANT`: 식단 미입력으로 정령 휴면 상태

## Event
* `ON_CLEAN_MEAL_EVALUATED`: 식단 클린 지수 측정 완료
* `ON_SPIRIT_EVOLVED`: 정령 단계별 진화 발동

## Example
* 사용자가 찜 요리 중심의 영양식단을 기록하면 CDI 가중치가 최고 수치(1.5x)로 산출되어, 정령 '아이리스'가 대지 속성 진화 폼으로 한 단계 성장함.

## Exception
* 식단 데이터 미입력 시: 정령이 배고파하는 유저 친화적 알림 다이얼로그 출력.

## Related Documents
* `HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v9.py`
* `HEALTH IS ALL/01_ARCHITECTURE/SPIRIT_EVOLUTION_SPEC.mdux`

## Change History
* **v2.0.0 (2026-07-31)**: V1 대비 CDI 인덱스 세분화, 정령 진화 수식 동적 다변수화 적용.