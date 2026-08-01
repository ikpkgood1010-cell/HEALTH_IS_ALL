# HEART_RATE_CALORIE_SPEC.md

## Purpose
본 문서는 유저의 심박 변이도 및 실시간 심박수 수준을 바탕으로 정밀 소모 칼로리를 산출하고, 이를 수호 정령의 속성 별 에너지(불꽃/바람/빛 속성)로 변환하는 동적 수식 구조를 정의한다.

## Scope
1. 심박수 기반 동적 칼로리($Dynamic Active Burn, DAB$) 계산 알고리즘
2. 유저 나이, 체중, 성별, 평균 심박수를 변수로 하는 정밀 수식 적용
3. 소모 칼로리의 정령 속성 기여도(불꽃: 고강도 유산소, 바람: 중강도 유산소, 빛: 안정/회복) 분배
4. 단조로운 칼로리 표기를 지양하고 매번 변화하는 세분화 공식 유지

## SSOT
본 문서는 심박 기반 칼로리 백엔드 엔진(`backend/heart_rate_calorie_engine.py`) 및 프론트엔드 워치 위젯(`lib/wearable_sync_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Dynamic Active Burn ($DAB$)**: 단순 걸음 수가 아닌, 실시간 심박수 변동폭을 반영하여 산출된 고정밀 소모 칼로리(kcal).
- **Element Energy Conversion**: 운동으로 얻은 열량을 정령의 불/바람/빛 속성 에너지를 채우는 수치로 환산하는 시스템.

## Runtime
- 프론트엔드(Flutter): 동적 소모 칼로리 게이지, 속성 에너지 전환 게이지 및 정령 기뻐함 모션.
- 백엔드(FastAPI/Python): 실시간 심박 패킷 파싱, Keytel 수식 기반 칼로리 및 정령 속성 경험치 계산.

## Rules
1. **정밀 계산과 게임 요소의 유기적 조합**: 단순 소모 칼로리 숫자보다 유저의 심장이 뛴 만큼 정령의 에너지가 채워지는 시각적 기쁨을 우선 제공한다.
2. **과도한 운동 유도 금지**: 안전 심박수 구역(Zone 2~3)에서 정령의 속성 성장 효율을 최대로 설정하여 무리한 과운동을 방지한다.
3. **세분화 동적 수식**: 남성/여성 표준 생체 공식, 심박 예비율($HRR$), 활동 시간 및 $0.96 \sim 1.04$ 미세 난수 적용.

## State
- `user_age`, `user_weight_kg`, `gender`
- `avg_heart_rate`, `duration_minutes`
- `calculated_dab_kcal`, `flame_spirit_energy`

## Event
- `ON_WORKOUT_SESSION_COMPLETED`: 운동 완료 시 동적 칼로리 최종 정산
- `ON_ELEMENT_ENERGY_GAINED`: 정령 속성 에너지 부여 및 진화 반영

## Example
$$DAB = \left[ \left( \text{Age} \times 0.2017 \right) + \left( \text{Weight} \times 0.1988 \right) + \left( HR_{avg} \times 0.6309 \right) - 55.0969 \right] \times \frac{\text{Time}}{4.184} \times \text{Jitter}$$

## Exception
- 체중이나 나이 정보가 누락된 경우 기본 표준 성인 기준 데이터(30세, 65kg)를 안전하게 적용한다.

## Related Documents
- `01_ARCHITECTURE/WEARABLE_SYNC_SPEC.md`
- `01_ARCHITECTURE/MONTHLY_REPORT_SPEC.md`

## Change History
- 2026-07-31 (PATCH_017): 심박수 기반 동적 칼로리 및 정령 에너지 전환 명세서 신규 작성 (SSOT 규격 준수).