# 다음 작업 계획서 (Next Work Plan) — PATCH_010

## 0. 시작 전 필수 확인사항
- 이번 세션을 시작하기 전, **업로드된 zip 파일을 직접 열어 아래 파일들이
  실제로 존재하는지 먼저 확인**하세요. 대화 로그의 서술과 실제 파일 상태가
  다를 수 있습니다 (`00_PROJECT/NEXT_AI_HANDOFF_GUIDE_PATCH_009.md` §4 참고).
  - `lib/api_config.dart`, `lib/api_config_io.dart`, `lib/api_config_web.dart`
  - `web/index.html`, `web/manifest.json`
  - `deploy/Dockerfile.web`, `deploy/nginx.conf`, `deploy/docker-compose.web.yml`
  - `lib/diet_screen.dart`, `lib/workout_screen.dart`의 `ApiDataProvider` 사용 여부
- 위 항목이 확인되지 않으면, 먼저 `PATCH_009_EXECUTION_REPORT.md`를 읽고
  실제 코드 상태부터 재파악한 뒤 작업을 시작하세요.

## 1. 작업 목표
- 고아 상태인 `DietScreen`/`WorkoutScreen`의 네비게이션 경로 문제 해결.
- 웹 아이콘 실제 파일 채우기 및 Flutter 실행 가능 환경에서의 실제 빌드 검증.
- FastAPI 통합 테스트 3건 및 가짜 테스트 6건 복구.
- 실서버 배포 1회 시도 및 HTTPS 적용.

## 2. 우선순위

### 1순위 — DietScreen/WorkoutScreen 고아 화면 문제 해결 (신규, 최우선)
- 문제: `main_navigation_screen.dart`의 하단 탭(홈/퀘스트/상점) 어디에서도
  `DietScreen`/`WorkoutScreen`으로 진입하는 경로가 없다. API 연동은
  PATCH_009에서 완료됐지만 사용자가 도달할 방법이 없다.
- 확인할 것: `home_screen.dart`의 "빠른 기록하기" 버튼이 이미 같은 기능을
  더 간단하게 제공하고 있어(칼로리/운동/수분 즉시 기록) 두 화면이 원래
  의도적으로 배제된 것인지, 아니면 "상세 입력 폼"(식사 종류/탄단지 개별
  입력, 운동 종목/강도 선택 등)이 필요한 시나리오를 위해 별도로 만들어졌는데
  네비게이션 연결만 누락된 것인지 코드/문서(`06_QA`, `07_PRODUCT` 등 참고
  문서 폴더)를 먼저 확인할 것.
- 누락으로 판단되면: `home_screen.dart` 상단에 "상세 기록" 버튼을 추가하거나
  `main_navigation_screen.dart`에 4번째 탭으로 추가하는 등, 기존 UI 패턴과
  일관된 방식으로 진입 경로를 연결.
- 의도된 배제로 판단되면: 화면 코드 자체를 삭제할지, 향후 재사용을 위해
  남겨둘지 결정하고 그 판단 근거를 실행보고서에 기록.

### 2순위 — 웹 아이콘 및 Flutter 환경 실제 검증
- `web/icons/README.md` 안내에 따라 실제 PNG 아이콘 4종 + `web/favicon.png` 채우기.
- `flutter pub get`
- `flutter analyze`
- `flutter build web --release`
- `flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000`
  (백엔드를 `uvicorn backend.main:app --reload`로 함께 띄운 상태에서)
- 위 4개 명령의 **실제 출력 로그를 원문 그대로** 실행보고서에 남길 것
  (경고/오류가 있다면 축약하지 말고 전부 포함).

### 3순위 — 가짜 테스트 6건 실테스트화
- Mock/Fake 의존성 정리
- 실패 재현 후 실제 assertions로 교체

### 4순위 — FastAPI 통합 테스트 3건 복구
- `pip install -r requirements.txt` (네트워크 가능한 환경에서)
- `pytest -q` 기준 실패 케이스 재현
- 라우터/의존성 주입/Mock 수정
- `activity_logs` 기반 오늘자 집계 로직에 대한 통합 테스트 케이스 추가 검토
  (PATCH_008/009 지시서에서 계속 이월되고 있는 항목 — 이번에는 반드시 착수)

### 5순위 — 실서버 배포 1회 시도
- 클라우드 VM 또는 유사 환경 확보 (사용자 확인 필요 — 이 작업은 AI 세션
  단독으로 진행 불가능할 수 있음).
- `deploy/docker-compose.web.yml`로 실제 빌드/기동 확인.
- HTTPS 적용 (Let's Encrypt 또는 Cloudflare 프록시 등, `WEB_DEPLOYMENT_GUIDE.md`
  참고).
- 실제 모바일 브라우저(크롬/사파리)에서 "홈 화면에 추가" 동작 확인.

### 6순위 — DB 타임존 전략 검토
- Postgres 실환경 기준 tz-aware 마이그레이션 초안 작성
- `created_at`, `updated_at`, `logged_at`(`activity_logs`) 비교 로직 영향도 분석

## 3. 실행 시 주의사항
- 화면/기능 수정은 하나씩 완료하고 즉시 정적 검증(가능하면 실제
  `flutter analyze`/`pytest`) 후 다음 항목으로 넘어가세요. 여러 개를 한
  번에 고치고 마지막에 몰아서 검증하면 오류 원인 추적이 어렵습니다.
- `MockDataProvider`와 관련 화면을 삭제하지 마세요. 오프라인/개발용으로
  계속 유지합니다.
- 이번 세션(PATCH_009)에서 `dart:html`을 쓰지 않고 `package:web`으로
  웹 코드를 작성했습니다. 앞으로 웹 관련 Dart 코드를 추가/수정할 때도
  `dart:html`을 다시 쓰지 마세요 (deprecated, Wasm 미지원).
- Flutter/FastAPI/Docker는 반드시 실행 가능한 환경에서만 최종 검증하세요.
  이 환경(컨테이너)에서 실행이 불가능하면 정적 검증까지만 수행하고, 그
  사실을 실행보고서에 명확히 남기세요 ("확인함"이라고 서술하면서 실제로는
  실행하지 않는 것이 이 프로젝트에서 반복되어 온 가장 큰 문제입니다).
- 부분 수정 후에는 전체 회귀 테스트와 문서 동기화를 함께 수행하세요.
- 작업 완료 후 실행보고서에는 반드시 "실제 실행 검증 로그"를 원문 그대로
  남겨, 다음 세션이 서술만 보고 오판하지 않도록 하세요.
