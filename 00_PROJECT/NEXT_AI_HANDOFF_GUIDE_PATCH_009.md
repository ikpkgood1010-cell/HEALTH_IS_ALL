# AI 인수인계서 (Handoff Guide) — PATCH_009

## 1. 현재 진행 상태 및 작업 요약
- **웹 런칭 대응을 실제 파일 레벨에서 구현 완료**했습니다. (직전 세션은
  "web/ 생성, api_client.dart 플랫폼 인식형 개선, Dockerfile/nginx 구성"까지
  대화로만 서술되고 실제 파일에는 전혀 반영되지 않은 상태였습니다 — §4 참고)
- `api_client.dart`의 `10.0.2.2` 하드코딩 baseUrl을 제거하고, 플랫폼별
  자동 감지(`api_config.dart` + 조건부 import)로 교체했습니다. 웹에서는
  접속 중인 브라우저 origin을 그대로 API 주소로 사용합니다.
- Flutter web 빌드에 필요한 `web/` 골격, PWA `manifest.json`, 배포용
  `Dockerfile.web`/`nginx.conf`/`docker-compose.web.yml`을 신규 추가했습니다.
- `diet_screen.dart`, `workout_screen.dart`를 `home_screen.dart`와 동일한
  패턴으로 `ApiDataProvider` 연동 전환 완료했습니다 (PATCH_009 지시서
  1순위 완료).
- 사용자의 실제 목표("스토어 없이 웹에서 APK 배포")에 대해 PWA 방식을
  권장하는 이유와 배포 방법을 담은 `WEB_DEPLOYMENT_GUIDE.md`를 작성했습니다.

## 2. 이번 패치에서 실제 수정/신규한 파일

**신규**
- `lib/api_config.dart` — baseUrl 결정 진입점 (환경변수 오버라이드 → 플랫폼 자동감지)
- `lib/api_config_io.dart` — 비웹 환경 기본값 (Android: 10.0.2.2, 그 외: localhost)
- `lib/api_config_web.dart` — 웹 환경 기본값 (`package:web`으로 origin 감지)
- `web/index.html`, `web/manifest.json`, `web/icons/README.md`
- `deploy/Dockerfile.web`, `deploy/nginx.conf`, `deploy/docker-compose.web.yml`
- `WEB_DEPLOYMENT_GUIDE.md` (루트)
- `PATCH_009_EXECUTION_REPORT.md` (루트)

**수정**
- `lib/api_client.dart` (baseUrl 하드코딩 제거, api_config.dart 사용)
- `lib/diet_screen.dart` (ApiDataProvider 연동 전환)
- `lib/workout_screen.dart` (ApiDataProvider 연동 전환)
- `pubspec.yaml` (`description` 웹 대응 반영, `web: ^0.5.1` 의존성 추가)
- `backend/main.py` (CORS 설정에 프로덕션 주의사항 주석 추가)
- `02_DATABASE/01_schema_migration.sql` (실제 SQLAlchemy 모델과 재동기화 —
  `activity_logs` 추가, 실존하지 않는 `workout_logs` 제거, naive UTC로 통일)
- `API_REFERENCE.md` (baseUrl 설명을 자동 감지 방식으로 갱신)

## 3. 미완료 및 이관된 작업

### 최우선 (0순위) — 신규 발견 이슈
1. **`DietScreen`/`WorkoutScreen`이 앱 어디에서도 네비게이션되지 않는 고아
   화면입니다.** `main_navigation_screen.dart`의 하단 탭은 홈/퀘스트/상점
   3개뿐이고 두 화면으로 진입할 경로가 없습니다. 이번 패치에서 API 연동
   자체는 완료했지만, 실제 사용자가 이 화면에 도달할 방법이 없어 기능이
   죽어 있는 상태입니다. `home_screen.dart`의 "빠른 기록하기" 버튼처럼
   즉시 기록하는 방식으로 이미 홈에서 커버되고 있어 의도적으로 뺀 것인지,
   아니면 원래 계획에 있었는데 누락된 것인지 확인 후 (a) 네비게이션
   경로를 연결하거나 (b) 화면 자체가 불필요하면 정리하는 결정이 필요합니다.
2. **web/icons/의 실제 PNG 아이콘 4종 + web/favicon.png 채우기.** 텍스트
   전용 작업 환경이라 바이너리 이미지를 생성할 수 없었습니다.
   `web/icons/README.md`에 채우는 방법을 안내해 두었습니다.
3. **Flutter SDK가 설치된 실제 환경에서 검증.** `flutter pub get` →
   `flutter analyze` → `flutter build web` → `flutter run -d chrome`
   순서로 실제 빌드/실행을 확인해야 합니다. 이번 패치는 정적 검증까지만
   수행했습니다 (`PATCH_009_EXECUTION_REPORT.md` §4 참고).
4. **실제 서버(도메인) 확보 후 `docker compose -f deploy/docker-compose.web.yml
   up --build`로 실배포 검증 + HTTPS 적용.** 이 컨테이너는 Docker 데몬과
   네트워크가 없어 빌드 자체를 실행해보지 못했습니다.

### PATCH_009 작업지시서에서 이관된 항목 (여전히 미착수)
5. Flutter 6개 가짜 테스트 재작성 (Flutter 실행 환경 부재로 착수 못 함)
6. FastAPI 통합 테스트 3건 복구 (통합 실행 환경 부재로 착수 못 함)
7. DB tz-aware 전환 검토 (실제 DB 통합 검증 전까지 보류)

### PATCH_008에서 이관되었던 항목 (해결됨)
- ~~diet_screen.dart, workout_screen.dart API 연동 전환~~ → 이번 패치에서 완료
- ~~ApiDataProvider의 baseUrl 하드코딩~~ → 이번 패치에서 플랫폼 자동감지로 해결

## 4. 다음 작업자를 위한 주의사항
- **대화 로그와 실제 파일 상태가 다를 수 있음에 각별히 주의하세요.** 이번
  패치의 시작점이 된 세션도 "web/ 생성, Dockerfile 구성 진행하겠다"고
  서술했지만 실제로는 파일에 반영되지 않은 채 끊긴 상태였습니다. 새 세션을
  시작할 때는 항상 **업로드된 zip 파일을 직접 열어 코드 존재 여부를
  확인**하고, 이전 대화 서술을 그대로 신뢰하지 마세요.
- `HealthIApiClient`의 `baseUrl`은 더 이상 하드코딩이 아닙니다. 명시적으로
  넘기지 않으면 `api_config.dart`가 플랫폼별로 자동 결정합니다. 로컬
  개발처럼 프론트/백엔드 포트가 다른 경우에는
  `--dart-define=API_BASE_URL=http://localhost:8000`으로 오버라이드하세요.
- 웹 관련 신규 파일(`api_config_web.dart`)은 `dart:html`이 아닌
  `package:web`을 사용합니다. `dart:html`은 deprecated 상태이니 앞으로도
  웹 관련 코드를 추가할 때 `dart:html`을 다시 쓰지 마세요.
- `record_type`에 새 활동 타입을 추가할 때는 `API_REFERENCE.md`의 "새 활동
  타입을 추가하려면" 섹션 절차를 따르세요. `ActivityLogModel` 스키마 변경은
  필요 없습니다.
- `MockDataProvider`는 삭제하지 말고 오프라인/개발/UI 테스트용으로 계속
  유지하세요 (diet_screen/workout_screen 전환 후에도 `main.dart`에 두
  Provider가 함께 등록된 상태를 유지했습니다).
- naive UTC 저장 구조(`backend/config.py`의 `utc_now()`)를 전제로 새 시간
  관련 로직을 작성할 때는 반드시 `utc_now()`를 사용하세요.
- `02_DATABASE/01_schema_migration.sql`을 이번에 실제 모델과 재동기화했지만,
  `init_db()`의 `Base.metadata.create_all()`이 여전히 단일 진실 소스입니다.
  이 SQL 파일은 Postgres 최초 기동 시 initdb 스크립트 용도일 뿐이니, 앞으로
  SQLAlchemy 모델을 바꿀 때는 이 SQL 파일도 함께 갱신하는 습관을 유지하세요.
- 문서상 완료 처리와 실제 코드 상태가 어긋나지 않도록, 다음 패치에서도
  컴파일/정적 검증 로그를 실행보고서에 원문 그대로 남기세요.
