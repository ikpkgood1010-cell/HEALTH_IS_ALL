POINT_RULE

Purpose
본 문서는 Point(꾸미기 재화)의 수급, 사용, 소멸, 상점 연동 규칙을 정의한다.

Scope
• Point 획득 수식 및 품질 보정 계수
• 상점(Shop) 구매 및 꾸미기 요소 소모 규칙
• 시즌 이월 및 소멸(Expiration) 정책

SSOT
본 문서는 Point 경제 시스템에 대한 단일 진실 출처(SSOT)이다.

Definitions
• Point: 외형 꾸미기, 프로필 테마, 건강이 코스튬 등을 구매하기 위한 상점 전용 재화.

Rules
1. Point 산출 공식:

◦ : 기본 10 ~ 30 Point

◦ : 연속 출석 및 습관 달성 시 최대 

◦ 

◦ : AI 영양/운동 품질 평가 지수 (

◦ )

1. Point 소모 및 상점 규칙: 
◦ 코스튬 구매, 방 꾸미기 오브젝트 구매, 프로필 테마 해금에만 사용.
◦ Point는 타 사용자에게 양도할 수 없으며 환불이 불가능하다.

1. 시즌 소멸 및 이월 정책: 
◦ Point는 획득일로부터 365일간 유효하며, 미사용 Point는 순차 소멸한다.
◦ 시즌 변경 시 기존 Point는 유지되나, 시즌 한정 코스튬은 해당 시즌 Point로만 구매 가능하도록 제한할 수 있다.

Runtime
• Point 차감은 구매 시 트랜잭션으로 원자적(Atomic) 처리되며, 잔액 부족 시 INSUFFICIENT_POINTS 에러를 반환한다.

Examples
• 7일 연속 기록 유저가 품질 평가 1.1을 받고 기본 20 Point 미션을 수행한 경우:

• 

Forbidden
• Point를 사용해 Exp를 올리거나 퀘스트를 즉시 완료(Skip)하는 기능.
• Point의 현금 환금 기능.

Related Documents
• 03_GAME_SYSTEM/ECONOMY_MASTER.md
• 03_GAME_SYSTEM/CANONICAL_NAMING.md

Change History
• 2026-07-31: PATCH-001 최초 작성 (Gemini)