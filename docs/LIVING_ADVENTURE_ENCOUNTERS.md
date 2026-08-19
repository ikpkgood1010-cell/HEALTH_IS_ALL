> **SUPERSEDED:** 첫 용사 아루와 과거 자동 모험 규칙은 새 6인 구조에 포함하지 않는다.

# 살아있는 모험 결과와 첫 용사 합류 (레거시 기록)

## 구현 범위

- 같은 모험 ID는 항상 같은 방 종류와 이야기 결과를 반환한다.
- 각 방은 `result_code`, 결과 제목, 결과 문장을 갖는다.
- 과거 저장 모험도 보상값을 바꾸지 않고 결정론적으로 새 결과 문장을 복원한다.
- 건강 기록으로 활력이 1 이상 생긴 첫 모험 보상을 수령하면 `새싹 길잡이 아루`가
  확정 합류한다. 기록 없는 0 활력 모험만 반복해서는 합류하지 않는다.
- 용사는 뽑기나 구매가 아니라 이야기 마일스톤으로만 합류한다.
- 아루는 MVP에서 보상 배율·전투력·재화 획득량을 바꾸지 않는 서사 동료다.

## 저장과 중복 방지

기존 `activity_logs`의 append-only 이벤트 구조를 사용한다.

- `game_adventure`: 정산된 모험과 방 결과
- `game_adventure_claim`: 한 번만 가능한 보상 수령
- `game_facility_investment`: 훈련장 자동 투자
- `game_hero_join`: 이야기 기반 용사 합류

사용자와 용사 코드를 포함한 안정 ID를 사용하므로 같은 사용자가 아루를 여러 번
획득할 수 없다. 이번 변경에는 DB migration과 실제 운영 DB 쓰기가 없다.

## API

- `POST /api/v1/game/adventures/settle`
- `POST /api/v1/game/adventures/{adventure_id}/claim`
- `GET /api/v1/game/adventures/history/{user_id}`
- `GET /api/v1/game/heroes/{user_id}`

합류 응답의 `gameplay_effect`는 `NONE`이다. 경제 효과는 별도 밸런스 검증과 명시적
승인 전까지 추가하지 않는다.
