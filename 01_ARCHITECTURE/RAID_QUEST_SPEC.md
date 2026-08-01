# RAID_QUEST_SPEC.md

## Purpose
본 문서는 사용자의 일주일 간 누적 운동 수행량, 평균 영양소 밸런스 점수(NBS), 클린 식단 연속 달성일을 종합 평가하여 동적 보스 레이드 난이도 및 레이드 딜량을 산출하는 주간 레이드 퀘스트 로직을 정의한다.

## Scope
1. 주간 건강 데이터 기반 레이드 보스 체력(HP) 및 방어력 동적 생성 수식
2. 사용자의 일일 건강 행동(운동/식단) 시 발생되는 레이드 타격 딜량($D_{\text{raid}}$) 산출
3. 건강 달성률 저하 시 보스 광폭화(Enrage) 및 보상 감쇄 로직
4. 건강 기록 누락 시 간이 평균 기반 Fallback 수식 연동

## SSOT
본 문서는 백엔드 레이드 엔진(`backend/raid_quest_engine.py`) 및 프론트엔드 대시보드 위젯(`lib/raid_quest_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Weekly Health Score (WHS)**: 주간 운동 달성률, 평균 NBS, 식단 연속성이 합성된 0~100점 지표.
- **Raid Boss HP**: 사용자의 평균 건강 수준에 맞춰 매주 월요일 생성되는 동적 보스 체력.
- **Raid Damage ($D_{\text{raid}}$)**: 당일 수행한 운동 강도와 식단 밸런스 점수가 조합된 타격 수치.

## Runtime
- 프론트엔드(Flutter): 주간 레이드 보스 체력바, 실시간 딜량 연출 및 건강 미션 달성 현황 출력.
- 백엔드(FastAPI/Python): 매주 월요일 00:00 UTC 보스 스탯 생성, 일일 건강 기록 수신 시 레이드 딜량 적용 및 보상 확정.

## Rules
1. **건강 목표 우선**: 순수 게임 단순 반복 플레이(노가다)로는 보스에게 딜량을 넣을 수 없으며, 실제 운동 수행과 클린 식단 기록만이 유일한 공격 수단이다.
2. **동적 다변수 난수 적용**: 보스 공격 시 단순 고정값이 아닌 당일 유산소/무산소 비율, 수면/수분 섭취 가중치 및 난수($0.92 \sim 1.08$)가 결합되어 매번 정밀하게 변동된다.
3. **Fallback 정책**: 주간 운동/식단 데이터 중 일부가 미입력된 경우, 최근 3주간의 이동 평균(Moving Average) 값으로 자동 대체하여 계산 중단을 방지한다.

## State
- `weekly_workout_min`, `avg_nbs_score`, `clean_streak_days`
- `boss_max_hp`, `boss_current_hp`, `boss_phase` (NORMAL, ENRAGED, DEFEATED)
- `weekly_raid_reward_tier`

## Event
- `ON_WEEKLY_RAID_RESET`: 매주 월요일 신규 보스 생성
- `ON_HEALTH_ACTION_LOGGED`: 운동/식단 입력 시 레이드 타격 발생
- `ON_BOSS_DEFEATED`: 보스 토벌 및 주간 성취 보상 지급
- `ON_FALLBACK_CALCULATION`: 데이터 미비 시 이동 평균 수식 전환

## Example
$$\text{WHS} = (\text{Workout Completion Ratio} \times 40) + (\text{Avg NBS} \times 0.4) + (\text{Streak Days} \times 2)$$
$$\text{Boss Max HP} = 10,000 \times \left(1 + \log_{10}(1 + \frac{\text{Historical WHS}}{100})\right)$$
$$D_{\text{raid}} = \text{BaseDamage} \times \left(1 + \ln(1 + \text{WorkoutMin})\right) \times \left(\frac{\text{Today NBS}}{100}\right) \times \text{Jitter}$$

## Exception
- 주간 건강 달성률이 20% 미만으로 극도로 저조한 경우, 보스가 광폭화(Enraged) 상태에 진입하여 보상 감소 경고를 표시하되 사용자의 건강 동기 부여를 위한 '구원 미션(Quick Rescue Mission)'을 즉시 발동한다.

## Related Documents
- `01_ARCHITECTURE/SPIRIT_DIET_CATALYST_SPEC.md`
- `01_ARCHITECTURE/OFFLINE_SYNC_SPEC.md`
- `03_BACKEND/RAID_ENGINE.mdux`

## Change History
- 2026-07-31 (PATCH_009): 동적 레이드 던전 및 주간 건강 퀘스트 연동 명세 신규 작성 (SSOT 규격 준수).