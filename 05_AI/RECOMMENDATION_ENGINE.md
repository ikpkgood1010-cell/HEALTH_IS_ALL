RECOMMENDATION_ENGINE

Purpose
본 문서는 AI 건강이가 플레이어에게 제시하는 건강 제안 및 코칭 추천 알고리즘 규칙을 정의한다.

Recommendation Priority Hierarchy
1. Priority 1 (Risk Avoidance) : 48시간 이상 특정 필수 행동 누락 시 안부 및 안전 가이드.
2. Priority 2 (Recent Lack) : 최근 3일간 가장 점수가 낮은 도메인(예: 수면 부족) 보완 추천.
3. Priority 3 (Habit Maintenance) : 연속 진행 중인 습관 잇기 격려.
4. Priority 4 (Goal & Quest) : 현재 일일 퀘스트 연계 제안.

Anti-Repetition Rules (3-Day Lock)
• 동일한 추천 템플릿 코드(REC_CODE)는 3일(72시간) 연속으로 사용자에게 노출될 수 없다.
• RecommendationEngine은 추천 파이프라인 가동 시 최근 3일간 노출된 REC_CODE 리스트를 Exclude Filter로 설정한 후 차순위 추천안을 반환한다.

Related Documents
• 05_AI/HEALTH_FEEDBACK_POLICY.md
• 05_AI/DIALOGUE_POLICY.md