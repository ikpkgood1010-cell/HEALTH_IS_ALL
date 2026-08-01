# ORPHAN_MODULE_REGISTER

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: 미연결 또는 활성 경로가 불분명한 모듈을 삭제하지 않고 분류한다.

## Classification Rule
- `Active`: 현재 메인 플로우 또는 테스트에서 참조됨
- `Roadmap`: 설계는 유효하나 메인 플로우 미연결
- `Archive Candidate`: 중복/구버전/유지 필요성 낮음

| Module | Current State | Reason | Recommended Bucket | Next Action |
|---|---|---|---|---|
| `lib/diet_screen.dart` | 구현 존재, 메인 네비게이션 미연결 | 화면 품질은 회복됐지만 진입점 없음 | Roadmap | 라우팅 연결 여부 제품 결정 |
| `lib/workout_screen.dart` | 구현 존재, 메인 네비게이션 미연결 | 화면 품질은 회복됐지만 진입점 없음 | Roadmap | 라우팅 연결 여부 제품 결정 |
| `lib/settings_profile_screen.dart` | 구현 존재, 메인 네비게이션 미연결 | Riverpod 기반이나 진입점 없음 | Roadmap | 설정 진입 플로우 정의 |
| `lib/spirit_interactive_widget.dart` | 참조 0건 | 대체 위젯(`health_i_widget.dart`) 존재 | Archive Candidate | 사용처 없으면 archive 이동 |
| `lib/heartrate_spirit_widget.dart` | 참조 미약 | 웨어러블 연동 기능 후보 | Roadmap | wearable 플로우 설계 확정 |
| `lib/wearable_sync_widget.dart` | 참조 미약 | 연결 경로 미확인 | Roadmap | sync 화면/버튼 설계 |
| `lib/audio_coaching_widget.dart` | 참조 미약 | AI 오디오 기능 미연결 | Roadmap | feature flag 아래 연결 검토 |
| `lib/monthly_report_widget.dart` | 참조 미약 | 리포트 기능 미연결 | Roadmap | 월간 리포트 런칭 시 연결 |
| `lib/guild_challenge_widget.dart` | 참조 미약 | 소셜 기능 미연결 | Archive Candidate | 범위 축소 시 archive 우선 |
| `backend/guild_challenge_engine.py` | 직접 참조 미확인 | 소셜 기능 백엔드 | Roadmap | API 계약 정의 전까지 비활성 유지 |
| `backend/guild_synergy_engine.py` | 직접 참조 미확인 | 소셜 기능 백엔드 | Roadmap | 동일 |
| `backend/raid_quest_engine.py` | 직접 참조 미확인 | 레이드 기능 미연결 | Archive Candidate | 범위 재평가 |
| `backend/monthly_report_engine.py` | 직접 참조 미확인 | 월간 리포트 경로 미연결 | Roadmap | scheduled report 요구 확정 |
| `backend/audio_coaching_engine.py` | 직접 참조 미확인 | 오디오 코칭 미연결 | Roadmap | AI audio rollout 전까지 대기 |
| `backend/spirit_album_engine.py` | 직접 참조 미확인 | Memory/album 후보 | Roadmap | F-004 연결 여부 결정 |
| `backend/spirit_evolution_engine.py` | 직접 참조 미확인 | 진화 기능 미연결 | Archive Candidate | naming 정렬 후 필요성 재평가 |
| `backend/offline_sync_engine.py` | 직접 참조 미확인 | 엔진 파일은 있으나 활성 루트 미확인 | Roadmap | sync 이벤트 체인 설계 |
| `backend/wearable_sync_engine.py` | 직접 참조 미확인 | 웨어러블 수집 미연결 | Roadmap | 디바이스 전략 이후 연결 |

## PATCH-005 Note
- 현재 패치에서는 분류 문서화까지 수행했다.
- 실제 archive 이동은 제품 결정 및 참조 재검사 후 수행한다.

## PATCH-006 확인 사항 (2026-08-01)
- `backend/heart_rate_calorie_engine.py`와 `backend/heartrate_calorie_engine.py`는
  이름이 비슷해 중복/오타로 오인하기 쉽지만, 실제로는 서로 다른 SSOT 문서가 각각
  명시적으로 가리키는 별개 모듈이다.
  - `backend/heart_rate_calorie_engine.py` → `01_ARCHITECTURE/HEART_RATE_CALORIE_SPEC.md`
    (Keytel 공식 기반 DAB 칼로리 계산)
  - `backend/heartrate_calorie_engine.py` → `01_ARCHITECTURE/WEARABLE_HEARTRATE_SPEC.md`
    (Tanaka 공식 기반 HR Zone/EPOC 계산)
  - 둘 다 클래스명이 `HeartRateCalorieEngine`으로 동일해 향후 import 충돌이나 혼동
    가능성이 있다. 다음 패치에서 클래스명 분리 또는 파일명 재정렬을 검토할 것을 권고한다.
  - 이번 세션에서는 로직을 건드리지 않고 사실 확인만 했다 (두 파일 모두 정상 import,
    정상 인스턴스화 확인됨).
