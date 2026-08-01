# SPIRIT EVOLUTION EXPANSION V2 SPECIFICATION

## Purpose
본 문서는 사용자 건강 습관 달성에 따라 스피릿(Spirit)이 4단계 진화(알 -> 아기 스피릿 -> 성장기 스피릿 -> 수호정령)를 이루고, 건강 속성(체력/유산소/클린영양)과 공명하는 아키텍처 구조를 명시한다.

## Scope
- 스피릿 단계별 진화 경험치(EXP) 임계치 및 속성 수치
- 식단/운동 클린 스트릭(Streak)에 따른 촉매(Catalyst) 연성 시스템
- 스피릿 비주얼 및 이펙트 연동 규칙

## SSOT (Single Source of Truth)
- 본 문서는 스피릿 진화, 속성 변경 및 촉매 아이템 생성 로직의 유일한 SSOT이다.

## Definitions
- **Spirit Stage**: Phase 0 (Egg) -> Phase 1 (Baby) -> Phase 2 (Growth) -> Phase 3 (Guardian Spirit).
- **Catalyst Item**: 클린 식단 및 운동 연속 달성 시 획득하여 진화 속성을 결정짓는 연성 재료.

## Runtime
- 백엔드 `spirit_evolution_engine.py` 및 프론트엔드 `spirit_evolution_widget.dart` 제어.

## Rules
1. **건강 중심 진화 법칙**: 스피릿의 진화는 현질이나 인게임 과금이 아닌, 오직 사용자의 실질적 건강 행동(걸음 수, 영양 균형, 수면)으로만 가능하도록 제한한다.
2. **시각적 만족감 제공**: 스피릿 진화 시 그래픽 이펙트 및 감성적 대화 팝업을 배치하여 호감도를 높인다.

## State
- `SpiritState`: `stage` (0~3), `element` (FIRE | WATER | EARTH | WIND), `affinity_level` (1~100), `evolution_ready` (boolean).

## Event
- `ON_SPIRIT_EXP_GAINED`: 경험치 획득 및 레벨업 체크.
- `ON_SPIRIT_EVOLVED`: 진화 조건 만족 시 속성 선택 및 애니메이션 재생.

## Example
- **Phase 1 -> Phase 2 진화**:
  - 조건: 누적 경험치 5,000 XP 이상 + 클린 식단 스트릭 7일 연속.
  - 보상: '바른 영양의 촉매' 획득 및 수호정령 외형 오픈.

## Exception
- 연속 스트릭이 깨지더라도 스피릿의 레벨이나 진화 단계가 하락하지 않으며, 친밀도만 소폭 감소 후 회복 퀘스트가 제공된다.

## Related Documents
- `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V5.md`
- `HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v5.py`

## Change History
- v2.0.0 (2026-07-31): 스피릿 4단계 진화 트리 명세 및 건강 연동 속성 시스템 추가.