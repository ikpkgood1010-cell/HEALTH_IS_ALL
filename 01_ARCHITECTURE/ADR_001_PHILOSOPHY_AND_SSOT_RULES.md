ADR 001: Health-First Principle & SSOT Governance

Status
Accepted

Context
본 프로젝트는 63개 이상의 Markdown 문서를 기반으로 설계되고 있으며, 다수의 엔진(Habit, Health, Progression, Quest 등)이 존재합니다.
이 과정에서 게임성(XP, Level, Item)이 건강 습관 형성이라는 본래 목적을 압도하거나, 문서 간 용어 불일치가 발생하는 문제가 제기되었습니다.

Decision
1. Health-First 법칙: 
◦ 모든 기능 구현 및 이벤트 발생 시 "건강 습관 형성"에 이로운지를 먼저 판단한다.
◦ 과도한 경쟁, 무한 파밍 유도, 불필요한 보상 인플레이션은 즉시 제거한다.
2. SSOT(Single Source of Truth) 규칙: 
◦ 동일한 도메인 용어 및 공식은 단 하나의 지정된 문서에만 작성한다.
◦ 용어: 07_PRODUCT/Master Canonical Glossary.md
◦ DB Schema: 02_DATABASE/Database Schema Master.md
◦ API: 03_BACKEND/API_SPECIFICATION.md
3. 쉬운 표현 준수: 
◦ BMR, TDEE, Macronutrient 등의 전문 용어는 백엔드 엔진 내부에서만 계산하며, 사용자 UI에는 "오늘 걸음 수", "추천 식단" 형태의 행동 중심 문장으로 변환하여 노출한다.

Consequences
• 개발 중 용어 충돌 발생 시 Master Canonical Glossary.md의 정의를 최우선으로 적용합니다.
• 복잡한 DDD 설계 문서 중 실사용성이 떨어지는 중복 문서는 축소 및 통합 대상이 됩니다.