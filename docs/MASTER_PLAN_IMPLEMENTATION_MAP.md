# 마스터 기획 구현 대응표

기준일: 2026-08-13

| 기획 항목 | 현재 상태 | 실제 경로 | 다음 확장 |
|---|---|---|---|
| 익명 MVP | 완료 | `lib/anonymous_user_repository.dart`, `lib/main.dart` | 이전·복구 정책 뒤 로그인 |
| 건강 하단 4탭 | 완료 | `lib/main_navigation_screen.dart` | 실기기 QA |
| 홈 상단 게임 입장 | 완료 | `lib/home_screen.dart` | 최종 배너 에셋 연결 |
| 게임 내부 허브 | 실제 상태 연결 | `lib/game_screen.dart`, `lib/api_data_provider.dart` | 콘텐츠별 실제 기능 확장 |
| 6인 직군·자동 전투 규칙 | 서버시간·멱등 정산·Flutter 상태 완료(DB 미적용) | `backend/idle_battle_engine.py`, `backend/idle_game_service.py`, `lib/game_screen.dart` | 노드 비용 연결 후 30회 환생 경제 검증 |
| 별자리 7계층·0계층 영입 노드 5개·1~6계층 전직 노드 6개 | 0계층 경로·확정 영입과 1~6계층 개별 전직 완료(DB 미적용) | `backend/constellation_economy.py`, `backend/advancement_economy.py`, `lib/game_screen.dart` | 세부 전직 경로·스킬 효과 연결 |
| 정령 확정 부화 | 화면 기준 완료 | `lib/game_screen.dart` | 부화 진행·저장 구현 |
| 스킬·아바타 확정 제작 | 화면 기준 완료 | `lib/game_screen.dart` | 제작식·재료 구현 |
| 환생 초기화·보존 | 100층 조건·별의 파편 감사·30회 후보 시뮬레이션 완료 | `backend/idle_game_service.py`, `scripts/simulate_rebirth_economy.py` | DB 적용 후 실행 UI 승인 |
| 건강 기록→영구 성장 | 기록별·일별 상한, 멱등 감사, 과거 기록 소급 완료(DB 미적용) | `backend/health_essence_service.py`, `migrations/202608140002_health_essence_rewards.sql` | 실제 스키마 적용·운영 수치 검증 |
| 건강 기록·HBI | 기존 완료 | `backend/main.py`, `backend/game_balance_engine.py` | 게임 파생 정수 어댑터 |
| 기존 길드·12시간 모험 | SUPERSEDED | deprecated API와 미사용 `lib/guild_screen.dart` | 데이터 보존 확인 뒤 제거 |
| 최종 게임 아트 | 미적용 | `docs/GAME_ASSET_AUDIT.md` | Stitch P0 에셋 제작·검수 |

`완료`는 전체 게임 완성을 뜻하지 않는다. 현재는 새 방향이 기존 실행 구조와 다시
충돌하지 않도록 정보구조, 표시 규칙, 읽기 전용 API 계약을 고정한 단계다.
