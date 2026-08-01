# HEALTH IS ALL (헬스 이즈 올)

AI 기반 정령과 함께하는 건강 관리 및 습관 형성 플랫폼입니다.

## 📁 주요 폴더 구조
- `backend/`: FastAPI 기반 백엔드 API 서버 및 DB 연동
- `test/`: Flutter 클라이언트 단위/위젯 테스트
- `scripts/`: 개발 환경 구축 및 실행 자동화 스크립트
- `.github/workflows/`: GitHub Actions CI/CD 자동화 설정

## 🚀 빠른 시작 방법
1. `.env.example` 파일을 복사하여 `.env` 파일로 이름을 바꿉니다.
2. `.env` 파일 안의 비밀번호와 API 키를 본인 정보로 수정합니다.
3. `scripts/run_all.sh` 스크립트를 실행하여 전체 서버를 켭니다.

## ⚠️ 현재 상태 (PATCH-007 재검증 기준, 2026-08-01)
- 백엔드(FastAPI)와 Flutter 앱은 **아직 서로 연결되어 있지 않습니다**. 앱은 로컬 목업 데이터(`MockDataProvider`)만 사용합니다.
- 코드 실행 위치는 루트 `backend/`, 루트 `lib/`뿐입니다. `03_BACKEND/`, `04_FRONTEND/`, `10_ARCHIVE/`의 소스는 참고용이며 실행되지 않습니다.
- 자세한 내용은 `00_PROJECT/PATCH_007_EXECUTION_REPORT.md`와 `00_PROJECT/IMPLEMENTATION_STATUS_MATRIX.md`를 참고하세요.