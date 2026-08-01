AI Agent Integration Spec (AI 에이전트 연동 및 프롬프트 파이프라인 명세)

1. 개요
본 문서는 HEALTH IS ALL 프로젝트 내 AI 에이전트(LLM Engine)의 컨텍스트 동기화, 동적 시스템 프롬프트(Dynamic System Prompt) 주입, 가드레일(Guardrails), 및 응답 파이프라인을 정의합니다. 유저의 건강 데이터 및 정령 상태를 바탕으로 긍정 심리학(Product_Language_Guide)을 준수하는 자연스러운 AI 피드백을 생성하는 것을 목적으로 합니다.

───

2. AI Context Building Pipeline (컨텍스트 조합 구조)

LLM에 전달할 컨텍스트는 유저의 실시간 상태 데이터와 정령의 감정 상태를 조합하여 생성됩니다.

text
[ Trigger Event ] ────────> [ Context Collector ] ────────> [ System Prompt Assembler ] ────────> [ LLM Engine ]
(예: 식단/운동 기록)      (User Health + Spirit State)      (Product Language + Safety)          (JSON Output)