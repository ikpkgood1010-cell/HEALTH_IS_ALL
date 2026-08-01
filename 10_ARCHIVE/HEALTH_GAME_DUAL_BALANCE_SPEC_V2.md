# HEALTH_GAME_DUAL_BALANCE_SPEC_V2.md

## Purpose
본 문서는 앱 내 '건강 관리' 기능과 'RPG 게임 요소' 간의 완벽한 이중 밸런스(Dual Balance) 기준을 정의합니다. 게임 요소가 화면을 지나치게 가리거나 건강 관리 본연의 목적을 저해하지 않도록 통제하면서, 독창적인 RPG 재미를 최고 수준으로 제공합니다.

## Scope
* 건강 수치(식단, 수면, 운동)의 게임 속성(정령 능력치, 던전 진행, EXP) 매핑
* 어뷰징 방지 및 억제 메카닉 (Anti-Grind Policy)
* 화면 레이아웃 상 건강 지표와 게임 UI의 시각적 배분 가이드라인

## SSOT
* **경로**: `HEALTH IS ALL/03_GAME_SYSTEM/HEALTH_GAME_DUAL_BALANCE_SPEC_V2.md`
* **소유팀**: Game Balance & Health Design Team

## Definitions
* **Dual-Balance Ratio**: 화면 UI 영역에서 건강 정보(60%)와 게임 비주얼(40%)의 최적 배분 비율.
* **Spirit Synergy**: 사용자가 건강한 식단과 규칙적인 운동을 이행할 때 정령이 발동하는 특수 능률 보너스.

## Runtime
* **실행 환경**: 게임 세션 실행 및 건강 데일리 리셋 타임(매일 00:00:00)

## Rules
1. 게임 보상을 얻기 위해 허위 건강 데이터를 입력하는 어뷰징을 시스템적으로 방지한다.
2. 메인 화면 첫 진입 시 당일의 식단 및 운동 달성 현황이 가장 먼저 명확히 보여야 한다.
3. 정령 비주얼과 이펙트는 고급스럽게 연출하되 건강 수치 확인을 방해하지 않는다.

## State
* `BALANCED`: 건강과 게임 수치가 균형을 이루는 정상 상태
* `HEALTH_FOCUSED`: 건강 수치 입력이 시급한 상태 (식단 미기록 등)
* `REWARD_READY`: 건강 목표 달성으로 게임 보상 수령 가능한 상태

## Event
* `ON_MEAL_LOGGED`: 식단 등록 시 정령 속성 파워 업 이벤트 발동
* `ON_EXERCISE_COMPLETED`: 운동 달성 시 보스 레이드 데미지 환산 적용

## Example
* 사용자가 건강한 스팀/찜 위주의 양질의 식단을 작성하면, 정령 '아이리스'의 방어력과 친밀도가 상승하며 감사의 대화 팝업이 노출됨.

## Exception
* 연속 3일 이상 무리한 과운동 감지 시: 게임 EXP 획득 제한 및 휴식 권장 모드로 자동 전환.

## Related Documents
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V9_SPEC.md`
* `HEALTH IS ALL/03_GAME_SYSTEM/ANTI_GRIND_POLICY.mdux`

## Change History
* **v2.0.0 (2026-07-31)**: V1 대비 UI 6:4 황금비율 적용, 정령 시너지 보너스 수식 재설계.