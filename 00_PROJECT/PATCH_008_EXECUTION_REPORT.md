# 작업 완료 및 검증 보고서 (Execution Report) — PATCH_008

> ⚠️ **중요 인수인계 사항**: 이전 세션(패치007 이후 진행되던 세션)의 대화 로그에는
> "앱-백엔드 연동을 구현했다"는 서술이 다수 존재하지만, 실제로 업로드된 3개 zip
> 파일을 열어 확인한 결과 **해당 작업은 파일에 전혀 반영되어 있지 않았다**
> (`backend/database.py`에 `ActivityLogModel` 없음, `lib/`에 `api_client.dart`/
> `api_data_provider.dart` 없음, `pubspec.yaml`에 `http` 패키지 없음, `main.dart`는
> `MockDataProvider`만 등록, `home_screen.dart`는 하드코딩된 로컬 필드만 사용).
> 즉 이전 세션은 계획을 서술하는 도중 실제 파일 저장 없이 중단된 것으로 판단된다.
> 이번 패치는 그 서술된 계획을 **원본 파일 레벨에서 처음부터 실제로 구현**한 것이다.

## 1. 성공 (Success)

### 백엔드 확장
- `backend/database.py`: 범용 `ActivityLogModel` 테이블 신규 추가. 식사/운동/수분/습관
  등 모든 `record_type`을 하나의 테이블에 통합 기록하도록 설계해, 향후 새 활동 타입
  추가 시 스키마 변경이 필요 없도록 했다.
- `backend/progression_engine.py`: `base_exp_map`에 `water_log: 10` 추가
  (Flutter mock의 `addWater` +10 Exp와 값 일치).
- `backend/models.py`: `HealthIStateResponse`에 `today_consumed_calories`,
  `today_workout_minutes`, `today_water_liters`, `streak_days` 필드 추가.
- `backend/main.py`:
  - 활동 기록 시 `activity_logs`에도 저장 (Exp 획득 여부와 무관하게 항상 저장).
  - 상태 조회 시 `activity_logs`에서 **오늘자 실제 집계값**을 계산해 응답에 반영.
  - `func.date()` 방언 이슈를 피하기 위해 Python 레벨에서 오늘 00:00~내일 00:00
    범위를 계산하는 `_today_range()`로 단순화 (SQLite/Postgres 모두 동일하게 동작).
  - 연속 기록 일수(`streak_days`)를 `activity_logs`의 날짜 집합에서 계산하는
    `_calc_streak_days()` 추가, EXP 계산의 streak 보너스에도 실제 값을 반영.

### Flutter 연동
- `pubspec.yaml`: `http: ^1.2.2` 패키지 추가.
- `lib/api_client.dart` (신규): 백엔드 REST API를 감싸는 얇은 클라이언트.
  `backend/main.py`의 실제 엔드포인트/스키마와 정확히 일치시켰다.
- `lib/api_data_provider.dart` (신규): `MockDataProvider`와 **동일한 getter/메서드
  시그니처**를 가진 실서버 연동 Provider. 기존 `MockDataProvider`는 오프라인/개발용
  으로 그대로 유지했다 (삭제하지 않음).
- `lib/main.dart`: `ApiDataProvider`를 `MultiProvider`에 함께 등록. 화면 코드는
  건드리지 않았으며, 어떤 Provider를 쓸지는 화면 단위에서 선택 가능하다.
- `lib/home_screen.dart`: **레퍼런스 구현**으로 `ApiDataProvider` 연동 버전으로
  전면 재작성. 로딩 인디케이터, 에러 배너, pull-to-refresh, 빠른 기록 버튼(식단/
  운동/수분)이 실제로 서버에 저장되고 서버 값으로 재동기화되도록 구현했다.
  다음 작업자가 `diet_screen.dart`/`workout_screen.dart`에도 그대로 따라 적용할
  수 있는 예시로 남겨두었다.
- `API_REFERENCE.md` (신규, 루트): 실제 실행되는 백엔드 API 문서. `03_BACKEND/`
  등 구버전 참고 문서와 헷갈리지 않도록 별도 파일로 분리했다.

## 2. 실패 (Failure)
- 없음.

## 3. 확인 불가 — 환경 제약 (Unverifiable)
- **Flutter (`pub get`/`analyze`/`test`)**: 이 컨테이너에 Flutter SDK가 설치되어
  있지 않고 네트워크가 차단되어 있어 실제 컴파일 검증은 불가능하다. 대신 아래
  §4의 정적 검증(괄호 균형, import 경로 실존, 파라미터 시그니처 대조)을 수행했다.
- **FastAPI 통합 테스트**: 네트워크 차단으로 `pip install -r requirements.txt`
  불가. 순수 Python 로직 시뮬레이션(§4)으로 대체 검증했다.
- **실제 DB 인스턴스 기반 마이그레이션/쿼리 실행**: 실제 DB가 없어 실행 불가.
  대신 in-memory 시뮬레이션으로 집계 로직을 검증했다.

## 4. 실제 실행 검증 로그

### 백엔드 컴파일
```
python3 -m py_compile backend/*.py test/*.py tests/*.py scripts/*.py → 오류 0건
grep -rn "datetime.utcnow()" backend/ test/ tests/ scripts/ → 0건 (패치007 유지 확인)
```

### 순수 Python 로직 시뮬레이션 (신규 기능)
```
PASS - water_log base exp == 10
PASS - unknown type fallback == 15 (신규 활동 타입 추가 시 안전성 확인)
PASS - 3-day consecutive streak == 3
PASS - broken streak == 1
PASS - ai_agent zero-activity feedback 정상 생성
PASS - ActivityLogModel 집계 시뮬레이션: calories=1250.0, minutes=30.0, water=1.0
       (meal_log 2건, workout_log 1건, water_log 2건, habit_complete 1건 혼합 입력 기준
        habit_complete는 DAILY_AGGREGATE_MAP에 없어 집계에서 정상적으로 제외됨을 확인)
ALL PASS
```

### Flutter 정적 검증
```
괄호 균형 검사 (api_client.dart, api_data_provider.dart, home_screen.dart, main.dart):
  curly=0 paren=0 square=0 (전 파일 균형 정상)

import 경로 실존 확인:
  home_screen.dart → widgets/health_i_widget.dart (존재), api_data_provider.dart (존재)
  api_data_provider.dart → api_client.dart (존재)
  main.dart → mock_data_provider.dart, api_data_provider.dart, main_navigation_screen.dart (모두 존재)

HealthIWidget 생성자 파라미터 대조:
  정의: currentExp, level, emotionState, dialogue, onTapHealthI
  호출: currentExp, level, emotionState, dialogue, onTapHealthI (정확히 일치)

ApiDataProvider 메서드/getter 대조 (home_screen.dart 사용부 전체):
  refreshStatus(), logMeal(), logWorkout(), addWater() 시그니처 일치
  consumedCalories, currentExp, dailyExpCap, dialogue, emotionState, isLoading,
  lastError, level, streakDays, targetCalories, targetWaterLiters, todayExpGained,
  waterLiters, workoutMinutes — 전부 ApiDataProvider에 정의됨 확인

SDK 호환성: sdk: '>=3.3.0 <4.0.0', State.mounted 사용(3.0+ 지원) → 문제없음
```

## 5. 개선 및 변경사항 (Improvements & Changes)
- **확장 용이성 우선 설계**: `ActivityLogModel`을 활동 타입별 개별 테이블이 아닌
  범용 테이블로 설계해, 새 활동 타입 추가 시 DB 마이그레이션 없이 문자열 값
  추가만으로 동작하도록 했다 (`API_REFERENCE.md`의 "새 활동 타입을 추가하려면"
  섹션에 절차 문서화).
- **안전한 점진적 전환 (Mock/Real 스위치 방식)**: 기존 `MockDataProvider`를
  삭제하거나 변경하지 않고 `ApiDataProvider`를 나란히 추가했다. `main.dart`에는
  두 Provider가 모두 등록되어 있어, 화면별로 어느 쪽을 쓸지 선택 가능하며 앱
  전체가 한 번에 깨질 위험이 없다.
- **레퍼런스 구현 우선**: 모든 화면을 한 번에 전환하지 않고 `home_screen.dart`
  하나를 완성도 있게 전환해, 다음 작업자가 동일 패턴을 나머지 화면에 복제할 수
  있는 실증 예제로 남겼다.
- **오늘자 실측 데이터 반영**: 상태 조회 API가 더 이상 하드코딩된 값
  (`consumed_calories=1600` 등)이 아닌, `activity_logs`의 실제 오늘자 합산값과
  실제 연속 기록 일수를 반환하도록 개선했다.
