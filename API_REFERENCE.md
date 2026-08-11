# API_REFERENCE.md — 실제 실행되는 백엔드 API 문서

> ⚠️ 이 문서는 **실제로 실행되는 코드**(`backend/`, `lib/`)만을 대상으로 한다.
> `03_BACKEND/`, `04_FRONTEND/lib/`, `10_ARCHIVE/`는 실행되지 않는 참고/구버전
> 문서 폴더이므로 이 문서와 내용이 다르더라도 무시할 것. 실제 진입점은
> 루트 `backend/main.py`와 루트 `lib/main.dart`뿐이다.

## 개요
- 서버: FastAPI (`backend/main.py`)
- DB: SQLite(기본) 또는 Postgres (`backend/config.py`의 `database_url` 참고)
- 실행: `uvicorn backend.main:app --reload` (프로젝트 루트에서)
- Base URL: 플랫폼별로 `lib/api_config.dart`가 자동 결정한다 (하드코딩 없음).
  - **웹**: 접속 중인 브라우저 주소(origin)를 그대로 사용. 배포 시 `deploy/nginx.conf`가
    같은 오리진에서 `/api`를 백엔드로 프록시하므로 코드 수정이 필요 없다.
  - **Android 에뮬레이터**: `http://10.0.2.2:8000` (호스트 PC의 localhost를 가리킴)
  - **iOS 시뮬레이터 / 데스크톱**: `http://localhost:8000`
  - **오버라이드**: 위 자동 감지가 맞지 않는 모든 경우
    `--dart-define=API_BASE_URL=http://...` 로 실행 시점에 강제 지정 가능
    (예: 실기기 테스트 시 PC의 실제 네트워크 IP로 지정).

## 엔드포인트

### `GET /`
헬스체크용 루트. `{"message": ..., "version": ...}` 반환.

### `GET /healthz`
`{"status": "ok", "service": "HEALTH IS ALL API"}` 반환.

### `POST /api/v1/health/record`
활동(식사/운동/수분/습관 등)을 기록하고 Exp를 계산한다.

**요청 바디** (`HealthRecordRequest`, `backend/models.py`)
```json
{
  "user_id": "user_test_001",
  "record_type": "meal_log",
  "value": 550.0,
  "detail_data": { "meal_type": "점심" }
}
```

- `record_type`: 현재 EXP가 명시적으로 매핑된 값은 `meal_log`(30), `workout_log`(50),
  `habit_complete`(20), `water_log`(10)이다. 그 외 임의의 문자열도 허용되며,
  매핑되지 않은 타입은 안전하게 fallback exp(15)로 처리된다
  (`backend/progression_engine.py`의 `base_exp_map`).
- `value`의 의미는 `record_type`에 따라 다르다:
  - `meal_log` → 칼로리(kcal)
  - `workout_log` → 운동 시간(분)
  - `water_log` → 수분 섭취량(L)
  - 그 외 타입은 자유롭게 정의해서 사용 가능 (오늘자 집계에는 반영되지 않을 뿐,
    `activity_logs` 테이블에는 항상 저장된다)

**응답** (`HealthRecordResponse`)
```json
{
  "success": true,
  "record_id": "rec_xxxxxxxxxxxx",
  "exp_gained": 30,
  "current_daily_exp": 30,
  "message": "30 Exp가 반영되었습니다."
}
```

**비즈니스 규칙**
- 안티파밍: 같은 유저의 마지막 활동으로부터 10분(`ANTI_FARMING_INTERVAL_MINUTES`)
  이내 재요청 시 `exp_gained=0`, 남은 시간이 `message`에 표시됨.
- 일일 Exp 캡: 하루 300(`DAILY_EXP_CAP`) 초과분은 잘려서 지급됨.
- Streak 보너스: 연속 기록 일수(2일째부터)에 따라 최대 20%까지 가산.
- Exp 획득 여부와 무관하게 활동 자체는 항상 `activity_logs`에 저장됨
  (안티파밍으로 0 Exp여도 오늘자 칼로리/운동/수분 집계에는 정상 반영).

### `GET /api/v1/health-i/status/{user_id}`
'건강이' 캐릭터의 현재 상태와 오늘자 실측 집계값을 반환한다.

**응답** (`HealthIStateResponse`)
```json
{
  "name": "건강이",
  "level": 3,
  "current_exp": 620,
  "daily_exp_cap": 300,
  "emotion_state": "활기참",
  "dialogue": "좋아요. 수분과 가벼운 활동을 조금만 더 챙기면 더 안정적이에요.",
  "equipped_skin": "default_skin",
  "last_updated": "2026-08-01T09:00:00",
  "today_consumed_calories": 1250.0,
  "today_workout_minutes": 30.0,
  "today_water_liters": 1.0,
  "streak_days": 3
}
```

- `today_*` 필드와 `streak_days`는 `activity_logs` 테이블의 **오늘자 실측값**을
  Python 레벨에서 집계한 결과다 (SQLite/Postgres 방언 차이를 피하기 위해
  `func.date()` 대신 날짜 범위 필터링 방식을 사용, `backend/main.py`의
  `_today_range()`/`_calc_streak_days()` 참고).
- 유저가 아직 없으면(첫 요청) 기본값(레벨 1, Exp 0, 오늘자 값 전부 0)으로 응답한다.

### 길드 제작소·인벤토리·파티

- `GET /api/v1/game/workshop/{user_id}`: 제작법, 보유 주화, 제작 인벤토리 조회
- `POST /api/v1/game/workshop/{recipe_code}/craft`: 사용자당 한 번만 제작하고 비용 차감
- `GET /api/v1/game/party/{user_id}`: 현재 원정대 슬롯 조회
- `POST /api/v1/game/party/vanguard/assign`: 합류한 용사를 선봉 슬롯에 배치

제작과 배치는 `activity_logs`의 append-only 게임 이벤트로 저장한다. 제작품과 파티
배치는 MVP에서 Exp, 건강 기록, 전투력, 보상 배율을 변경하지 않는다.

## 데이터 모델 (`backend/database.py`)

| 테이블 | 용도 |
|---|---|
| `health_i_profiles` | 유저별 캐릭터 레벨/Exp/감정 상태 |
| `user_exp_logs` | Exp 획득 이력(안티파밍/일일캡 계산용) |
| `meal_logs` | (레거시) 식사 상세 기록 — 현재 신규 기능은 `activity_logs` 사용 |
| `activity_logs` | **신규.** 식사/운동/수분/습관 등 모든 활동을 통합 기록하는 범용 테이블 |

### 새 활동 타입을 추가하려면
1. (선택) `backend/progression_engine.py`의 `base_exp_map`에 `"새타입": exp값` 한 줄 추가
   — 추가하지 않아도 fallback 15 Exp로 안전하게 동작함.
2. (선택) 오늘자 상태 응답에 합산값을 반영하고 싶다면 `backend/main.py`의
   `DAILY_AGGREGATE_MAP`에 `"새타입": "필드명"` 추가 후 `HealthIStateResponse`,
   `models.py`에 해당 필드 추가.
3. 앱 쪽에서는 `record_type`에 새 문자열을 넣어 `POST /api/v1/health/record`를
   호출하기만 하면 됨. `activity_logs` 테이블 스키마 변경은 필요 없음.

## Flutter 클라이언트 (`lib/api_client.dart`, `lib/api_data_provider.dart`)

- `HealthIApiClient`: 위 두 엔드포인트를 감싸는 얇은 HTTP 클라이언트.
  `baseUrl`을 명시적으로 넘기지 않으면 `lib/api_config.dart`가 플랫폼별로
  자동 결정한다 (개요 섹션 참고). 필요하면 생성 시
  `HealthIApiClient(baseUrl: '...')`로 직접 지정해 오버라이드할 수 있다.
- `ApiDataProvider`: `MockDataProvider`와 **동일한 getter/메서드 시그니처**를
  제공하는 `ChangeNotifier`. 화면은 두 Provider 중 어느 쪽을 써도 코드 구조가
  같다. `main.dart`에 두 Provider가 모두 등록되어 있으므로, 화면 단위로
  `Provider.of<ApiDataProvider>` 또는 `Provider.of<MockDataProvider>`를
  선택해서 점진적으로 전환하면 된다.
- `lib/home_screen.dart`가 `ApiDataProvider` 연동의 레퍼런스 구현이다.
  나머지 화면(`diet_screen.dart`, `workout_screen.dart` 등)에도 동일한
  패턴(initState에서 refreshStatus, build에서 watch, 기록 시 async 메서드
  호출 후 lastError 체크)을 적용하면 된다.

## 로컬 실행 방법 (참고)
```bash
# 백엔드
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000

# Flutter (에뮬레이터/기기 연결 후)
flutter pub get
flutter run
```
