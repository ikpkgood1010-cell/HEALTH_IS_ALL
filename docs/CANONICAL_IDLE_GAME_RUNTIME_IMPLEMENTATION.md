# Canonical 방치형 게임 상태 구현

상태: **CODE COMPLETE / DATABASE NOT APPLIED / 2026-08-13**

## 구현 범위

- 익명 사용자별 게임 프로필과 현재 회차 저장 구조
- 탱커·전사·마법사·궁수·도적·치유사 6개 고정 슬롯의 멱등 초기화
- 영입 여부, 최고 전직 차수, 전직 외형, 활성 스킬 슬롯 저장 구조
- 별자리 소형·중형·대형 해금 노드 저장 구조
- 환생 전 초기화/보존 수량 read-only 미리보기
- revision 확인과 idempotency key를 사용하는 환생 트랜잭션
- 환생 감사 로그와 영구 보존 스냅샷
- Flutter 게임 허브의 실제 서버 상태·환생 미리보기 연결
- 서버 시간 기반 지속 자동전투와 UUID 멱등 정산
- 1~5번 일반방·6번 보스방 진행 및 회차 골드 저장
- Flutter 자동전투 실제 상태·정산 결과 화면

## API

| 메서드 | 경로 | 쓰기 여부 | 역할 |
|---|---|---:|---|
| POST | `/api/v1/game/state/initialize` | 빈 상태 최초 1회 | 6개 고정 용사 슬롯과 1회차 생성 |
| POST | `/api/v1/game/heroes/select-initial` | 있음 | 6직업 중 첫 용사 1명 무료 확정 영입 |
| POST | `/api/v1/game/battle/settle` | 있음 | 서버 경과시간을 한 번만 방·층·골드로 정산 |
| POST | `/api/v1/game/constellation/unlock` | 있음 | 다음 소형·중형 노드 해금 또는 경로 완료 용사 확정 영입 |
| GET | `/api/v1/game/state/{user_id}` | 없음 | 현재 탑·회차·재화·용사·노드 조회 |
| GET | `/api/v1/game/rebirth/preview/{user_id}` | 없음 | 환생 시 초기화/보존될 실제 수량 확인 |
| POST | `/api/v1/game/rebirth/execute` | 있음 | 명시 확인·revision·멱등 키를 거친 환생 |

Flutter 화면에는 환생 실행 버튼을 아직 노출하지 않는다. 사용자가 보존 범위를 실제
미리보기로 충분히 확인하고, 운영 DB migration과 복구 절차가 검증된 뒤에만 노출한다.

## 환생 트랜잭션

```text
요청의 idempotency_key 확인
→ 사용자 게임 프로필 행 잠금
→ expected_revision 비교
→ 초기화/보존 수량 재계산
→ SMALL/MEDIUM 노드 삭제
→ 탑·방·골드 초기화, 회차·revision 증가
→ LARGE 노드·용사·전직·외형·영구 재화 유지
→ 보존 스냅샷과 환생 감사 로그 저장
→ 단일 트랜잭션 commit
```

같은 idempotency key를 재전송하면 다시 초기화하지 않고 최초 결과를 반환한다. 다른
요청이 먼저 상태를 바꾸면 HTTP 409로 차단한다. 초기화할 회차 진행이 전혀 없어도
HTTP 409로 차단한다.

## DB migration

파일: `migrations/202608130001_canonical_idle_game_state.sql`,
`migrations/202608140001_idle_battle_runtime.sql`

추가 대상:

- `game_profiles`
- `game_heroes`
- `game_constellation_nodes`
- `game_rebirth_logs`
- `game_battle_settlements`와 프로필의 전투 기준시각·현재 방 경과시간

현재 Supabase에는 적용하지 않았다. 기존 migration runner의 generic apply는 계속
차단돼 있으며 dry-run에서 baseline 뒤 후속 후보로만 표시된다. 실제 적용에는 다음이
모두 필요하다.

1. PR 병합과 Render 배포 순서 승인
2. 적용 직전 Supabase 수동 백업
3. 기존 4개 테이블 fingerprint 확인
4. 새 SQL의 staging 또는 임시 PostgreSQL 검증
5. 적용 명령과 승인자 기록
6. 적용 후 전체 ORM fingerprint `MATCH`
7. `/readyz`, 게임 초기화, 재시도·rollback 검증

## 아직 구현하지 않은 것

- 0계층: 용사별 소형 6·중형 2 경로와 5개 확정 영입 노드 구현, 비용은 후보값
- 자동 전투·0계층 경제: 30회 환생 시뮬레이션 완료, 전직 경제 연결 후 재검증 필요
- 1~6계층 별자리 노드 비용과 해금 API: 전직·건강 정수·별 조각 소비처와 함께 구현
- 실제 환생 버튼: DB 적용과 사용자 확인 UX 검증 후 노출
- 스킬·아바타·정령 테이블: 해당 콘텐츠 세로 단면과 함께 추가
