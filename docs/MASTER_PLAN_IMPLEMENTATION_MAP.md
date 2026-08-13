# 마스터 기획 구현 대응표

기준일: 2026-08-13

| 기획 항목 | 현재 상태 | 실제 경로 | 다음 확장 |
|---|---|---|---|
| 익명 MVP | 완료 | `lib/anonymous_user_repository.dart`, `lib/main.dart` | 이전·복구 정책 뒤 로그인 |
| 건강 하단 4탭 | 완료 | `lib/main_navigation_screen.dart` | 실기기 QA |
| 홈 상단 게임 입장 | 완료 | `lib/home_screen.dart` | 최종 배너 에셋 연결 |
| 게임 내부 허브 | 기능·배치 1차 | `lib/game_screen.dart` | 실제 상태·전투 연결 |
| 6인 직군·자동 전투 규칙 | 계약 완료 | `backend/main.py`, `backend/models.py` | 전투 엔진·저장 모델 |
| 별자리 7층·대형 노드 6개 | 화면·계약 기준 완료 | `lib/game_screen.dart`, canonical 문서 | 노드 그래프·비용 구현 |
| 정령 확정 부화 | 화면 기준 완료 | `lib/game_screen.dart` | 부화 진행·저장 구현 |
| 스킬·아바타 확정 제작 | 화면 기준 완료 | `lib/game_screen.dart` | 제작식·재료 구현 |
| 환생 초기화·보존 | 화면·계약 기준 완료 | `lib/game_screen.dart`, `/api/v1/game/direction` | 복구 테스트 뒤 실행 |
| 건강 기록·HBI | 기존 완료 | `backend/main.py`, `backend/game_balance_engine.py` | 게임 파생 정수 어댑터 |
| 기존 길드·12시간 모험 | SUPERSEDED | deprecated API와 미사용 `lib/guild_screen.dart` | 데이터 보존 확인 뒤 제거 |
| 최종 게임 아트 | 미적용 | `docs/GAME_ASSET_AUDIT.md` | Stitch P0 에셋 제작·검수 |

`완료`는 전체 게임 완성을 뜻하지 않는다. 현재는 새 방향이 기존 실행 구조와 다시
충돌하지 않도록 정보구조, 표시 규칙, 읽기 전용 API 계약을 고정한 단계다.
