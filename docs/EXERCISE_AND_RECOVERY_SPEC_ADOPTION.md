# 운동 분류 및 회복 계산 명세 반영 기록

## 입력 자료

- `exercise_category_enum_spec.pdf`
- `HEALTH_IS_ALL_Recovery_Specification.pdf`

두 PDF의 전체 6페이지를 텍스트 추출과 페이지 렌더링으로 확인했다.

## 운동 분류

운동은 한 개의 결합 코드가 아니라 다음 세 필드를 분리한다.

```text
exerciseCategoryGroup: CARDIO | STRENGTH | FLEXIBILITY | SPORTS
exerciseCategory: 27개 표준 운동 코드
intensityLevel: HIGH | MEDIUM | LOW
```

백엔드 표준 Enum과 27개 카탈로그는 `backend/exercise_catalog.py`, Flutter 선택
카탈로그는 `lib/exercise_catalog.dart`에 반영했다. 운동 기록 화면은 대분류 → 종목 →
강도 → 시간 → RPE → 컨디션 순서로 입력하며 종목별 권장 강도를 기본 선택한다.

현재 `/api/v1/health/record`의 `detail_data`에 위 코드를 함께 저장한다. PDF가 제안한
별도 `/api/v1/exercise-logs`는 전용 DB 모델과 migration이 없으므로 이번 범위에서는
추가하지 않았다. 동일 데이터를 두 경로에 중복 저장하는 것을 피하기 위한 결정이다.

## 회복 계산

```text
권장 회복시간 = 기본 회복시간
              × 강도 계수
              × 컨디션 계수
              × 빈도 계수
              × 연령 계수

회복률 = 경과시간 ÷ 권장 회복시간 × 100
```

### 기본 시간

| 근육 | 시간 |
|---|---:|
| ABS, CORE | 24 |
| BICEPS, TRICEPS, FOREARMS | 36 |
| CHEST, SHOULDERS | 48 |
| BACK, GLUTES, THIGHS | 72 |

### 계수

- RPE 1~4: 0.8 / 5~7: 1.0 / 8~9: 1.2 / 10: 1.4
- 컨디션 EXCELLENT 0.85 / GOOD 0.95 / NORMAL 1.0 / POOR 1.25 /
  CRITICAL 1.4
- 초보·오랜만 1.25 / 주 1~2회 1.0 / 주 3회 이상 0.85
- 20대 이하 0.95 / 30대 1.0 / 40대 1.1 / 50대 이상 1.2

회복률은 0~100으로 제한하고 `90~100 READY`, `50~89 RECOVERING`,
`0~49 REST`로 분류한다.

## API 반영

`POST /api/v1/recovery/calculate`는 DB를 변경하지 않는 계산 API로 추가했다. PDF 요청
스키마에는 연령 계수 공식이 있으나 `age` 필드가 누락되어 있어, 호환성을 유지하면서
선택 필드 `age`를 추가하고 미입력 기본값을 30으로 정했다. 초보·오랜만 조건도 기존
`frequencyPerWeek`만으로 구분할 수 없어 선택 필드 `isBeginner`를 추가했다.

이 API는 근육별 기본 시간, 권장 시간, 경과시간, 회복률, 상태, 예상 완충 시각을
반환한다. 계산 결과를 저장하거나 푸시를 발송하지 않는다.

## 아직 하지 않은 것

- 회복 결과 DB 저장과 15~30분 백그라운드 갱신
- 22:00~08:00 푸시 지연 및 딥링크 알림
- 스마트워치 자동 입력
- 연령·초보 여부를 익명 프로필에 영구 저장

이 기능들은 기기 권한·개인정보·백그라운드 실행 정책 결정이 필요한 단계에서 묶어서
구현한다.
