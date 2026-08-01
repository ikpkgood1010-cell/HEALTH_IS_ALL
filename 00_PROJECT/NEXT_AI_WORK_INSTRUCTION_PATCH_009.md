# 다음 작업 계획서 (Next Work Plan) — PATCH_009

## 0. 시작 전 필수 확인사항
- 이번 세션을 시작하기 전, **업로드된 zip 파일을 직접 열어 아래 파일들이
  실제로 존재하는지 먼저 확인**하세요. 대화 로그의 서술과 실제 파일 상태가
  다를 수 있습니다 (`00_PROJECT/NEXT_AI_HANDOFF_GUIDE_PATCH_008.md` §4 참고).
  - `lib/api_client.dart`
  - `lib/api_data_provider.dart`
  - `backend/database.py`의 `ActivityLogModel`
  - `pubspec.yaml`의 `http` 패키지
- 위 항목이 확인되지 않으면, 먼저 `PATCH_008_EXECUTION_REPORT.md`를 읽고
  실제 코드 상태부터 재파악한 뒤 작업을 시작하세요.

## 1. 작업 목표
- `diet_screen.dart`, `workout_screen.dart`를 `home_screen.dart`와 동일한
  패턴으로 `ApiDataProvider` 연동 전환.
- Flutter 실행 가능 환경에서 정적 분석 및 테스트 체계를 복구.
- FastAPI 통합 테스트 3건의 실패 원인을 재현하고 수정.

## 2. 우선순위

### 1순위 — 나머지 화면 API 연동 (신규, 최우선)
- `lib/home_screen.dart`를 레퍼런스로 삼아 `lib/diet_screen.dart`,
  `lib/workout_screen.dart`를 `ApiDataProvider` 연동으로 전환하세요.
- 체크리스트:
  1. `import 'mock_data_provider.dart';` → `import 'api_data_provider.dart';`
  2. `Provider.of<MockDataProvider>(context, listen: false)` →
     `Provider.of<ApiDataProvider>(context, listen: false)`
  3. `provider.logMeal(...)`/`logWorkout(...)`가 이제 `Future<void>`를
     반환하므로, 호출부를 `async`로 감싸고 `await` 처리
  4. 저장 성공/실패에 따라 `provider.lastError`를 확인해 스낵바 분기
  5. 화면 진입 시(`initState`) `refreshStatus()` 호출 여부는 화면 성격에
     따라 판단 (입력 전용 화면이면 생략 가능)
- 전환 후 `home_screen.dart`에서 사용한 것과 동일한 정적 검증(괄호 균형,
  import 경로 실존, provider 메서드/getter 대조)을 반드시 수행하고 로그를
  실행보고서에 남기세요.

### 2순위 — Flutter 환경 복구
- `flutter pub get`
- `flutter analyze`
- `flutter test`
- (신규) `http` 패키지 추가 이후 실제 네트워크 mock을 이용한 `api_data_provider`
  단위 테스트 작성 검토

### 3순위 — 가짜 테스트 6건 실테스트화
- Mock/Fake 의존성 정리
- 실패 재현 후 실제 assertions로 교체

### 4순위 — FastAPI 통합 테스트 3건 복구
- `pytest -q` 기준 실패 케이스 재현
- 라우터/의존성 주입/Mock 수정
- (신규) `activity_logs` 기반 오늘자 집계 로직에 대한 통합 테스트 케이스 추가 검토

### 5순위 — DB 타임존 전략 검토
- Postgres 실환경 기준 tz-aware 마이그레이션 초안 작성
- `created_at`, `updated_at`, `logged_at`(신규 `activity_logs`) 비교 로직 영향도 분석

## 3. 실행 시 주의사항
- 화면 전환 작업은 한 화면씩 완료하고 즉시 정적 검증 후 다음 화면으로
  넘어가세요. 여러 화면을 한 번에 고치고 마지막에 몰아서 검증하면 오류
  원인 추적이 어렵습니다.
- `MockDataProvider`와 관련 화면을 삭제하지 마세요. 전환이 끝날 때까지는
  두 Provider 체계가 공존해야 합니다.
- Flutter/FastAPI는 반드시 실행 가능한 환경에서만 최종 검증하세요. 이 환경
  (컨테이너)에서는 정적 검증까지만 가능합니다.
- 부분 수정 후에는 전체 회귀 테스트와 문서 동기화를 함께 수행하세요.
- 작업 완료 후 실행보고서에는 반드시 "실제 실행 검증 로그"를 원문 그대로
  남겨, 다음 세션이 서술만 보고 오판하지 않도록 하세요.
