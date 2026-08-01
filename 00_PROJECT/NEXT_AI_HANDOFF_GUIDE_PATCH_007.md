# AI 인수인계서 (Handoff Guide)

## 1. 현재 진행 상태 및 작업 요약
- `datetime.utcnow()` deprecation 대응을 실제 코드에 반영 완료했습니다.
- `backend/config.py`에 `utc_now()` 헬퍼를 추가하고, 순수 Python 범위의 직접 호출부를 공용 헬퍼 기반으로 통일했습니다.
- Flutter/FastAPI의 환경 의존 검증 대상은 원본 구조를 유지한 채 차기 작업으로 이관했습니다.

## 2. 이번 패치에서 실제 수정한 파일
- `backend/config.py`
- `backend/main.py`
- `backend/health_calculator.py`
- `backend/progression_engine.py`
- `backend/diet_calculator.py`
- `backend/ai_agent_service.py`
- `test/progression_engine_test.py`

## 3. 미완료 및 이관된 작업
- **Flutter 6개 가짜 테스트 재작성**: Flutter 실행 환경 부재로 검증 불가
- **FastAPI 테스트 3건 복구**: 통합 실행 환경 부재로 검증 불가
- **DB tz-aware 전환**: 실제 DB 통합 검증 전까지 보류

## 4. 다음 작업자를 위한 주의사항
- 현재 UTC 시간이 필요하면 반드시 `from backend.config import utc_now`를 사용하세요.
- naive UTC 저장 구조를 전제로 동작하므로, tz-aware 전환은 마이그레이션·쿼리·테스트를 함께 설계해야 합니다.
- 문서상 완료 처리와 실제 코드 상태가 어긋나지 않도록, 다음 패치에서도 grep/테스트 결과를 함께 남기세요.
