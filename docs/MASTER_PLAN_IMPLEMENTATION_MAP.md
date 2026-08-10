# 마스터 기획 구현 대응표

| 기획 항목 | 현재 반영 | 실제 경로 | 다음 확장 |
|---|---|---|---|
| 익명 MVP | 완료 | `lib/anonymous_user_repository.dart`, `lib/main.dart` | 계정 이전 정책 후 소셜 로그인 |
| 5개 하단 탭 | 완료 | `lib/main_navigation_screen.dart` | 없음 |
| 토스형 건강 UI | 1차 완료 | `lib/app_theme.dart`, `lib/home_screen.dart` | 실제 기기 접근성·반응형 QA |
| 운동·식단 진입 | 완료 | `lib/health_tab_screens.dart` | 기록 폼 UX 통합 |
| 익명 마이 화면 | 완료 | `lib/settings_profile_screen.dart` | 설정 영구 저장 |
| HBI 공식 | 완료 | `backend/game_balance_engine.py`, `lib/game_balance.dart` | 수면·스트레스 실측 연결 |
| 건강 기반 길드 미리보기 | 완료 | `lib/guild_screen.dart` | 서버 결과 저장·시설 시각화 |
| 게임 overview API | 완료 | `backend/main.py`, `backend/models.py` | 앱 API 소비·캐시 |
| 낮은 활동 비처벌 | 완료 | 게임 엔진 및 길드/홈 안내 | 전 기능 회귀 검증 |
| 던전 방 가중치·안전 규칙 | 엔진/테스트 완료 | `backend/game_balance_engine.py` | 실제 던전 생성·저장 |
| 오프라인 12시간·70% | 명세/UI 안내 | `docs/GAME_EXPANSION_BALANCE_SPEC.md` | 중복 방지 가능한 서버 작업 |
| 재화 3종 순환 | 명세/예상치 | 게임 엔진·길드 화면 | 원장과 거래 멱등성 |
| 기억의 순환 | 잠금 규칙/예상치 | 게임 엔진·길드 화면 | 실제 초기화·복구 검증 |
| 살아있는 길드/던전/보스 | 방향 확정 | 기획 문서 | 아트·콘텐츠·서버 구현 |
| 농장·낚시·집 꾸미기 | 방향 확정 | 기획 문서 | 단계별 별도 구현 |
| 정령 6속성 | 기존 기획 유지 | 기존 정령 관련 모듈 | 신규 UI와 데이터 통합 |
| 회복 시간 기준 | 기존 기획 유지 | 기존 회복 엔진 | 신체 부위 UX 검증 |
| 운동 27종 Enum·강도 분리 | 완료 | `backend/exercise_catalog.py`, `lib/exercise_catalog.dart` | 전용 DB migration 검토 |
| 다변수 근육 회복 계산 | 계산 API 완료 | `backend/recovery_calculator.py`, `backend/main.py` | 저장·위젯·푸시 연동 |

`완료`는 현재 MVP에서 실행 가능한 범위를 뜻한다. 장기 기획 전체가 구현되었다는
뜻은 아니다.
