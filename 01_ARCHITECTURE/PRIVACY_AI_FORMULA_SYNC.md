# PRIVACY_AI_FORMULA_SYNC.md

## Purpose
개인정보 보호 정책(Privacy Policy)과 AI 엔진 프롬프트 처리, 건강 수치 계산식(Formula) 간의 데이터 흐름 일관성을 검증하고 PII 유출을 차단한다.

## Scope
* AI Agent Interaction Layer
* Health Formula Calculation Engine
* Privacy Data Anonymization Pipeline

## Rules
1. **AI 전송 데이터 제한**: AI 프롬프트 생성 시 사용자의 실명, 계정 ID, 구체적 주소는 절대로 포함하지 않는다.
2. **동적 BMR/TDEE 계산식**:
   $$BMR = 10 \times W_{kg} + 6.25 \times H_{cm} - 5 \times A_{years} + s$$
3. **AI 피드백 검증**: AI가 생성한 응답 내 의료 진단/약물 처방 유동 표현 발견 시 Rule Engine에서 자동 차단한다.

## Change History
* **v1.0.0 (2026-07-31)**: PATCH-005 최초 작성.