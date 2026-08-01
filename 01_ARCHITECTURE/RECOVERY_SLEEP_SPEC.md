# RECOVERY_SLEEP_SPEC.md

## Purpose
본 문서는 유저의 수면 시간, 수면 효율, 심박 변이도(HRV) 데이터를 정밀 분석하여 일일 회복 지수($Recovery Score, RS$)를 산출하고, 이에 맞춰 정령의 상태 및 익일 운동 난이도를 최적화하는 수면·회복 시스템 규격을 정의한다.

## Scope
1. 수면 단계(깊은 수면, 렘수면, 얕은 수면) 및 HRV 기반 회복 지수($RS$) 정밀 공식 정의
2. 회복 지수에 따른 정령의 '휴식 슬럼버(Slumber)' 상태 연출 및 다정한 리포트 생성
3. 회복 지수 저조 시 익일 퀘스트 자동 하향 조정 연동
4. 수면 부족 유저를 위한 정령의 힐링 사운드/수면 케어 인터랙션 제공
5. 수면 데이터 미입력 시 평균 회복 수치를 적용하는 보정 Fallback 로직

## SSOT
본 문서는 수면 분석 백엔드 엔진(`backend/recovery_sleep_engine.py`) 및 프론트엔드 수면 리포트 위젯(`lib/recovery_sleep_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Recovery Score ($RS$)**: $0 \sim 100$점 범위의 유저 일일 회복 상태 수치.
- **Sleep Efficiency**: 총 침대 체류 시간 대비 실제 수면 시간의 비율($\%$).

## Runtime
- 프론트엔드(Flutter): 수면 회복 리포트 시각화, 정령의 밤 인사 팝업 및 힐링 인터페이스 제공.
- 백엔드(FastAPI/Python): 수면 바이오 데이터 파싱, $RS$ 정밀 계산 및 정령 상태 업데이트.

## Rules
1. **건강 중심 본위 원칙**: 수면이 부족한 상태($RS < 50$)에서는 고강도 운동 미션을 완전히 제한하고 가벼운 스트레칭과 명상 퀘스트로 자동 대체한다.
2. **다정하고 안심을 주는 표현**: "수면 점수 낙제"와 같은 자극적 표현 대신 "오늘 밤은 정령과 함께 깊은 휴식을 취해볼까요? 🌙"와 같은 힐링형 메시지를 제공한다.
3. **정밀 계산식**: 수면 시간뿐만 아니라 HRV 지수, 수면 효율, 그리고 $0.96 \sim 1.04$ 난수 변수를 종합 적용한다.

## State
- `total_sleep_minutes`, `deep_sleep_minutes`, `hrv_ms`, `sleep_efficiency`
- `recovery_score` ($0.0 \sim 100.0$)
- `slumber_mode_active` (True / False)

## Event
- `ON_SLEEP_DATA_SYNC`: 수면 센서/앱 데이터 동기화
- `ON_RECOVERY_SCORE_CALCULATED`: 회복 지수 산출 및 정령 반응 갱신
- `ON_HEALING_SOUND_REQUESTED`: 수면 케어 힐링 사운드 요청

## Example
$$RS = \left( \text{SleepEff} \times 0.4 + \frac{\text{DeepSleepMin}}{\text{TotalSleepMin}} \times 100 \times 0.35 + \frac{\text{HRV}}{120} \times 100 \times 0.25 \right) \times \text{Jitter}$$

## Exception
- 수면 수치가 비정상적으로 높거나 저조할 경우($RS > 100$ or $RS < 10$), 물리적 한계값 적용 후 사용자 확인 인터페이스를 띄운다.

## Related Documents
- `01_ARCHITECTURE/SPIRIT_EVOLUTION_SPEC.md`
- `01_ARCHITECTURE/NUTRITION_QUEST_SPEC.md`

## Change History
- 2026-07-31 (PATCH_014): 수면·회복 지수 정밀 분석 시스템 명세 신규 작성 (SSOT 규격 준수).