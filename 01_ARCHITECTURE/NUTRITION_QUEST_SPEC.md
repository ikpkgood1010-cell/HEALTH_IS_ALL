# NUTRITION_QUEST_SPEC.md

## Purpose
본 문서는 유저가 매일 지루함 없이 건강 습관을 유지할 수 있도록, 개별 유저의 대사량 및 수면 상태에 맞춰 매일 변동되는 동적 식단-운동 통합 퀘스트 엔진의 규격과 보상 산출 체계를 정의한다.

## Scope
1. 유저 맞춤형 일일 식단(탄단지 밸런스, 클린 식단 인증) 및 운동(걸음 수, 유산소/근력) 퀘스트 생성
2. 퀘스트 난이도 산출 알고리즘 및 난이도별 정령 성장 골드/경험치 보상 계산
3. 퀘스트 완료 시 유저 호감형 축하 팝업 메시지 연동
4. 유저 피로도 고려 오버퀘스트 방지 및 가벼운 퀘스트 전환 옵션
5. 네트워크 장애 시 Local Storage 기반 퀘스트 달성 현황 임시 동기화 Fallback

## SSOT
본 문서는 퀘스트 생성 백엔드 엔진(`backend/nutrition_quest_engine.py`) 및 프론트엔드 퀘스트 위젯(`lib/nutrition_quest_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Dynamic Quest**: 유저의 당일 수면 상태 및 피로도에 따라 목표치(예: 10,000보 $\rightarrow$ 6,000보)가 자동 조정되는 스마트 건강 미션.
- **Affinity Reward**: 퀘스트 달성 시 정령 친밀도를 올려주는 특수 경험치.

## Runtime
- 프론트엔드(Flutter): 일일 퀘스트 카드 목록, 달성률 프로그레스 바, 호감형 보상 수령 팝업 출력.
- 백엔드(FastAPI/Python): 유저 컨디션 분석, 일일 퀘스트 3종 자동 추천, 달성 검증 및 보상 계산.

## Rules
1. **건강 중심 본위 원칙**: 회복 지수가 저조한 날에는 "무리하지 않고 20분 가볍게 산책하기"와 같이 건강 회복을 우선하는 퀘스트를 발행하여 유저의 몸을 보호한다.
2. **친근하고 다정한 인터페이스**: 퀘스트 미달성 시 "실패"라는 단어를 절대 사용하지 않으며, "오늘도 최선을 다하셨어요! 내일 정령과 다시 즐겁게 시작해봐요 🌱"라는 호감형 문구를 표시한다.
3. **변수 세분화 수식**: 기본 보상에 유저의 연속 달성일(Streak), 정령 친밀도, 미세 난수를 승산 적용하여 매번 새로운 보상 수치를 지급한다.

## State
- `daily_quests` (List of Quest objects)
- `quest_completion_status` (Map<String, Bool>)
- `total_reward_gold`, `total_affinity_exp`

## Event
- `ON_QUEST_GENERATED`: 자정 또는 컨디션 갱신 시 맞춤형 퀘스트 발행
- `ON_QUEST_PROGRESS_UPDATE`: 걸음 수/식단 기록 입력 시 실시간 달성률 업데이트
- `ON_QUEST_COMPLETED`: 퀘스트 완료 및 축하 팝업 트리거

## Example
$$\text{Reward}_{\text{Gold}} = \text{BaseGold} \times (1.0 + (\text{Streak} \times 0.03)) \times (1.0 + (\text{AffinityLvl} \times 0.01)) \times \text{Jitter}$$

## Exception
- 유저 데이터 수집 센서에 오류가 발생한 경우, 식단 인증 단독 퀘스트 중심의 간이 퀘스트 세트로 자동 전환한다.

## Related Documents
- `01_ARCHITECTURE/SPIRIT_EVOLUTION_SPEC.md`
- `01_ARCHITECTURE/DYNAMIC_NUTRITION_FORMULA_SPEC.md`

## Change History
- 2026-07-31 (PATCH_013): 식단-운동 통합 퀘스트 엔진 명세 신규 작성 (SSOT 규격 준수).