# 다음 작업 계획서 (Next Work Plan)

## 1. 작업 목표
- Flutter 실행 가능 환경에서 정적 분석 및 테스트 체계를 복구합니다.
- FastAPI 통합 테스트 3건의 실패 원인을 재현하고 수정합니다.
- `utc_now()` 헬퍼 적용 이후, 장기적으로 tz-aware 전환이 가능한지 검토합니다.

## 2. 우선순위
1. **Flutter 환경 복구**
   - `flutter pub get`
   - `flutter analyze`
   - `flutter test`
2. **가짜 테스트 6건 실테스트화**
   - Mock/Fake 의존성 정리
   - 실패 재현 후 실제 assertions로 교체
3. **FastAPI 통합 테스트 3건 복구**
   - `pytest -q` 기준 실패 케이스 재현
   - 라우터/의존성 주입/Mock 수정
4. **DB 타임존 전략 검토**
   - Postgres 실환경 기준 tz-aware 마이그레이션 초안 작성
   - `created_at`, `updated_at` 비교 로직 영향도 분석

## 3. 실행 시 주의사항
- 이번 패치로 해결된 범위는 **순수 Python의 naive UTC 경고 정리**까지입니다.
- Flutter/FastAPI는 반드시 실행 가능한 환경에서만 수정하세요.
- 부분 수정 후에는 전체 회귀 테스트와 문서 동기화를 함께 수행하세요.
