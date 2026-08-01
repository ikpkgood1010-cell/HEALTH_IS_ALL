# ENGINE_INTEGRATION_GUIDE

- Document Name: ENGINE_INTEGRATION_GUIDE.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 프로젝트 내 여러 Engine의 입력/출력/소비자 관계를 통합 관점에서 정리한다.
- Implementation Status: Implemented
- Source of Truth: Documentation + Code
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: backend file audit

## Integration Principle
엔진은 독립적으로 계산하되, 입력과 출력 계약이 명확해야 하며 consumer가 누구인지 추적 가능해야 한다.

## Engine Matrix
| Engine | Input | Output | Consumer |
|---|---|---|---|
| Progression | `action_type`, `current_daily_exp`, `last_action_time`, `streak_days` | `exp_gained`, `current_daily_exp`, `is_capped`, `reason` | `backend/main.py`, tests |
| Health | workout type, duration, weight, intensity, heart rate | calories, reward detail | health APIs, future analytics |
| Recommendation | calories, water, workout, streak | emotion, dialogue, health score | `HealthIAgentService`, status API |
| Analytics | meal/nutrition/workout aggregates | insight, summary, category analysis | analytics screens, reports |
| Emotion | health score, sleep, streak, recovery context | emotion state, dialogue | status API, UI widget |
| Memory | achievement / streak / milestone data | unlock snapshots, affinity data | future album UI, archive review |
| Reward | quest completion, activity reward, shop spend | exp/point/item reward | quest UI, shop UI, progression |
| Quest | streak days, behavior patterns | daily quest list, reward_exp | quest screen, backend reward flow |
| Shop | current exp/point, inventory, item catalog | unlock state, spend result | `lib/shop_screen.dart`, future commerce API |
| Runtime | DB/session/config/env/timezone | initialized app state, persistence, schedules | FastAPI app, sync managers |

## Active vs Orphan Note
- Active core: `progression_engine.py`, `health_calculator.py`, `quest_engine.py`, `ai_agent_service.py`
- Candidate orphan/roadmap: `spirit_album_engine.py`, `spirit_evolution_engine.py`, `guild_challenge_engine.py`, 일부 widget
- Orphan 후보는 본 문서만으로 활성 모듈이 되지 않는다. 연결 경로가 확인되어야 한다.

## Integration Rules
1. Engine output field는 consumer가 의존하는 최소 필드로 고정한다.
2. consumer는 engine 내부 구현 세부사항에 의존하지 않는다.
3. 같은 비즈니스 의미의 상수는 모든 engine이 중앙 상수를 참조해야 한다.
4. engine 간 chaining 시 입력 정규화 계층을 둔다.

## Runtime Notes
1. `backend/main.py`는 Progression + AI feedback 조합의 현재 진입점이다.
2. 상태 조회 API는 이름/레벨/감정/대사를 UI에 공급한다.
3. route 연결이 없는 engine은 활성 서비스로 간주하지 않는다.

## Related Source Files
- `backend/main.py`
- `backend/progression_engine.py`
- `backend/health_calculator.py`
- `backend/quest_engine.py`
- `backend/ai_agent_service.py`
- `backend/spirit_album_engine.py`
- `backend/spirit_evolution_engine.py`

## Validation Method
- Manual Review
- Runtime Verification
- Integration Test
