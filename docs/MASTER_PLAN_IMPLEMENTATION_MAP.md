# 마스터 기획 구현 대응표

| 기획 항목 | 현재 상태 | 실제 경로 | 다음 확장 |
|---|---|---|---|
| 익명 MVP | 완료 | `lib/anonymous_user_repository.dart`, `lib/main.dart` | 계정 이전 정책 확정 후 로그인 |
| 하단 탭 5개 | 완료 | `lib/main_navigation_screen.dart` | 없음 |
| 토스형 건강 UI | 1차 완료 | `lib/app_theme.dart`, `lib/home_screen.dart` | 실기기 접근성 QA |
| 운동·식단 기록 | 완료 | `lib/health_tab_screens.dart`, `lib/diet_screen.dart`, `backend/main.py` | 수분 전용 입력 UX 고도화 |
| 건강 기록 멱등성 | 완료 | `lib/idempotency_key.dart`, `backend/data_idempotency_engine.py`, `backend/main.py` | 앱 재시작을 넘는 오프라인 큐 연동 |
| HBI 공식 | 완료 | `backend/game_balance_engine.py`, `lib/game_balance.dart` | 수면·스트레스 데이터 연동 |
| 운동 27종·강도 분리 | 완료 | `backend/exercise_catalog.py`, `lib/exercise_catalog.dart` | 필요 시 DB 카탈로그화 |
| 근육 회복 계산 | 완료 | `backend/recovery_calculator.py`, `backend/main.py` | 저장·위젯 연동 |
| 건강 기반 길드 | 3차 완료 | `lib/guild_screen.dart` | 3D 이미지 적용·장기 이벤트 |
| 자동 모험 12시간·70% | 완료 | `backend/adventure_service.py`, `backend/main.py` | 과거 구간 누적 정책 검토 |
| 보상 중복 방지 | 완료 | `backend/adventure_service.py` | 운영 동시성 관측 |
| 훈련장 1종 | 외형 성장 포함 완료 | `backend/adventure_service.py`, `lib/guild_screen.dart` | 시설 효과는 경제 검증 후 추가 |
| 던전 가중치·안전 규칙 | 결과 다양화 완료 | `backend/game_balance_engine.py`, `backend/adventure_service.py`, `lib/guild_screen.dart` | 장기 전투 애니메이션·보스 패턴 |
| 이야기 용사 합류 | 첫 용사 완료 | `backend/adventure_service.py`, `backend/main.py`, `lib/guild_screen.dart` | 스테이지·Quest·이벤트 용사 확장 |
| 제작·인벤토리 | 수집형 MVP 완료 | `backend/guild_workshop_service.py`, `lib/guild_screen.dart` | 장식 적용·장기 제작법 |
| 용사 파티 배치 | 선봉 1슬롯 완료 | `backend/guild_workshop_service.py`, `lib/guild_screen.dart` | 추가 용사 합류 후 다중 슬롯 |
| 게임 UI 아트 방향 | 기준 확정 | `docs/GAME_UI_ART_DIRECTION.md`, `lib/guild_screen.dart` | 실제 SD 3D 캐릭터·장면 교체 |
| 모험 회상 | 최근 5개 완료 | `backend/adventure_service.py`, `backend/main.py`, `lib/guild_screen.dart` | 앨범·상세 이야기 확장 |
| 기억 조각·환생 | 수식·해금 기준만 반영 | 게임 엔진·길드 화면 | 초기화·복구 검증 후 실행 기능 |
| 살아있는 길드·보스 | 방향 확정 | 기획 문서 | 전투·콘텐츠·서버 구현 |
| 광장·날씨·지역 탐험 | 방향 확정 | 기획 문서 | 단계별 구현 |

`완료`는 현재 익명 MVP에서 실행 가능한 범위를 뜻하며 장기 기획 전체가 끝났다는 뜻은 아니다. 마스터 프롬프트를 우선 기준으로 삼고, 없는 항목은 개발기획 1~42와 검토 자료를 따른다.
