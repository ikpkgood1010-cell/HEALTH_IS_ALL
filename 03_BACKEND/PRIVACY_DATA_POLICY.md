# PRIVACY_DATA_POLICY

## Purpose
본 문서는 사용자 건강, 식단, 생체 정보 등 고도의 민감 개인정보(PII) 수집, 저장, 파기, 익명화, AI 모델 입력 통제 및 데이터 최소 수집 원칙을 규정하는 SSOT이다.

## Scope
앱 및 백엔드에 저장되는 모든 사용자 데이터 및 AI 연산 파이프라인 데이터 흐름에 적용된다.

## SSOT
개인정보 처리 방침 및 민감 데이터 프라이버시 보호 기준의 단일 진실 출처이다.

## Data Classification & Retention Table

| Data Category | Specific Elements | Encryption Level | Retention Period | Anonymization Rule |
| :--- | :--- | :--- | :--- | :--- |
| **Account Data** | 이메일, OAuth ID, 연령대 | AES-256 | 회원 탈퇴 시 즉시 삭제 | N/A |
| **Health & Bio** | 신장, 체중, 골격근량, 질환 이력 | AES-256 (Strict) | 회원 탈퇴 시 즉시 삭제 | 통계 분석 시 비식별 조치 |
| **Meal Photos** | 식단 촬영 이미지 원본 | S3 Private Encrypted | 30일 후 자동 파기 | AI 분석 후 즉시 메타데이터만 추출 |
| **AI Log & Prompt**| 프롬프트 대화 기록 | Salt-Hashed Log | 14일 후 자동 삭제 | PII 정규식 자동 마스킹 (`[REDACTED]`) |

## Privacy Rules for AI Engine Integration
1. **Zero PII Leakage**: 외부 AI API(LLM/Vision) 호출 시 **이메일, 이름, 상세 위치, 사용자 ID를 절대로 포함하지 않는다.** 오직 비식별 처리된 건강 수치(예: Age Group, Calorie Delta)만 전달한다.
2. **Right to be Forgotten (파기 요청)**: 회원 탈퇴 요청 시, RDB, Hive, Redis 캐시 및 S3 이미지는 단일 트랜잭션 내에서 **3초 이내 완전 삭제**되어야 한다.
3. **Data Export**: 유저는 본인의 전체 건강/게이밍 데이터를 표준 JSON 형태로 내보내기(Export)할 수 있는 권리를 가진다.

## Runtime Impact
- 개인정보보호법 및 글로벌 프라이버시 규정을 100% 준수하여 법적/윤리적 리스크를 완벽 제거한다.

## Related Documents
- `03_BACKEND/SECURITY_POLICY.md`
- `06_ANALYTICS/ANALYTICS_EVENT_SPEC.md`

## Change History
- v1.0.0 (2026-07-31): Privacy Data Policy established.