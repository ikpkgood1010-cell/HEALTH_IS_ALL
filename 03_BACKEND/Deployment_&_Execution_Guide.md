Deployment & Execution Guide (시스템 실행 및 배포 가이드)

1. 개요
본 문서는 HEALTH IS ALL 프로젝트의 데이터베이스 마이그레이션, 백엔드 API 서버, AI 에이전트 서비스 및 Flutter 클라이언트 실행 절차를 규정합니다.

───

2. 환경 변수 설정 (.env)

백엔드 실행 루트 디렉토리에 .env 파일을 생성하고 아래 항목을 설정합니다.

env
# Database Credentials
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=health_is_all
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# LLM API Keys
OPENAI_API_KEY=sk-proj-your-openai-key

# Server Configuration
PORT=8000
DEBUG=True