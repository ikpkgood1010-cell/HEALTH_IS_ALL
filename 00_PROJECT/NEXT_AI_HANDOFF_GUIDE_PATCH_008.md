# AI 인수인계서 (Handoff Guide) — PATCH_008

## 1. 현재 진행 상태 및 작업 요약
- **앱-백엔드 연동을 실제 파일 레벨에서 구현 완료**했습니다. (이전 세션은 대화로만
  서술되고 실제 파일에는 반영되지 않은 상태였습니다 — §4 참고)
- 백엔드에 범용 `ActivityLogModel`을 추가해 식사/운동/수분 등을 통합 기록하고,
  상태 조회 시 오늘자 실측 집계값(칼로리/운동시간/수분/streak)을 반환하도록
  확장했습니다.
- Flutter에 `api_client.dart` + `api_data_provider.dart`를 신규 작성하고,
  `home_screen.dart`를 실제 서버 연동 레퍼런스 구현으로 전환했습니다.
- 기존 `MockDataProvider`와 `diet_screen.dart`/`workout_screen.dart`는 건드리지
  않았습니다 (안전한 점진적 전환 방식).

## 2. 이번 패치에서 실제 수정/신규한 파일
**신규**
- `lib/api_client.dart`
- `lib/api_data_provider.dart`
- `API_REFERENCE.md` (루트)
- `00_PROJECT/PATCH_008_EXECUTION_REPORT.md`

**수정**
- `backend/database.py` (ActivityLogModel 추가)
- `backend/models.py` (HealthIStateResponse에 오늘자 필드 추가)
- `backend/progression_engine.py` (water_log EXP 매핑 추가)
- `backend/main.py` (activity_logs 저장, 오늘자 집계, streak 계산 반영)
- `pubspec.yaml` (http 패키지 추가)
- `lib/main.dart` (ApiDataProvider 등록)
- `lib/home_screen.dart` (전면 재작성 — ApiDataProvider 연동)

## 3. 미완료 및 이관된 작업

### 최우선 (0순위)
1. **`diet_screen.dart`, `workout_screen.dart`를 `home_screen.dart`와 동일한
   패턴으로 `ApiDataProvider` 연동 전환.**
   - 현재 이 두 화면은 여전히 `MockDataProvider`만 사용합니다.
   - `home_screen.dart`를 참고해서: import를 `mock_data_provider.dart` →
     `api_data_provider.dart`로 교체, `Provider.of<MockDataProvider>` →
     `Provider.of<ApiDataProvider>`(또는 `context.read/watch`)로 교체,
     `provider.logMeal(...)`/`provider.logWorkout(...)`이 이제 `Future<void>`를
     반환하므로 `await` 처리 및 에러 핸들링(`provider.lastError`) 추가가 필요합니다.
2. **Flutter 실행 환경에서의 실제 컴파일 검증.** 이번 패치는 정적 검증(괄호 균형,
   import 경로 실존, 파라미터 시그니처 대조)만 수행했습니다. `flutter pub get` →
   `flutter analyze` → `flutter run`으로 실제 빌드 확인이 필요합니다.
3. **`user_id` 처리 방식 결정.** 현재 `ApiDataProvider`는
   `userId = 'user_test_001'` 하드코딩 기본값을 사용합니다. 실제 로그인/유저
   식별 체계가 생기면 `ApiDataProvider(userId: ...)`로 주입하도록 교체해야 합니다.

### 기존 패치007에서 이관된 항목 (여전히 미해결)
4. Flutter 6개 가짜 테스트 재작성 (Flutter 실행 환경 부재로 검증 불가)
5. FastAPI 통합 테스트 3건 복구 (통합 실행 환경 부재로 검증 불가)
6. DB tz-aware 전환 (실제 DB 통합 검증 전까지 보류)

## 4. 다음 작업자를 위한 주의사항
- **대화 로그와 실제 파일 상태가 다를 수 있음에 각별히 주의하세요.** 이번 패치의
  시작점이 된 이전 세션은 "구현했다"고 서술했지만 실제로는 파일에 반영되지
  않은 채 대화가 끊긴 상태였습니다. 새 세션을 시작할 때는 항상 **업로드된 zip
  파일을 직접 열어 코드 존재 여부를 확인**하고, 이전 대화 서술을 그대로 신뢰하지
  마세요.
- `record_type`에 새 활동 타입을 추가할 때는 `API_REFERENCE.md`의 "새 활동
  타입을 추가하려면" 섹션 절차를 따르세요. `ActivityLogModel` 스키마 변경은
  필요 없습니다.
- `ApiDataProvider`의 API 서버 주소(`baseUrl`)는 Android 에뮬레이터 기준
  `http://10.0.2.2:8000`으로 하드코딩되어 있습니다. iOS/실기기/배포 환경에서는
  `HealthIApiClient(baseUrl: '...')`로 명시적으로 교체해야 합니다.
- `MockDataProvider`는 삭제하지 말고 오프라인/개발/UI 테스트용으로 유지하세요.
- naive UTC 저장 구조(`backend/config.py`의 `utc_now()`)를 전제로 새 시간 관련
  로직을 작성할 때는 반드시 `utc_now()`를 사용하세요.
- 문서상 완료 처리와 실제 코드 상태가 어긋나지 않도록, 다음 패치에서도
  컴파일/정적 검증 로그를 실행보고서에 함께 남기세요.
