HEALTH_SCORE_ENGINE

Purpose
본 문서는 앱 전체의 건강 평가 핵심인 '건강 점수(Health Score)' 연산 엔진 SSOT이다. 단순 절대 100점 만점보다 **'최근의 성취 및 성장률'**에 가중치를 부여하여 지속적 동기부여를 유도한다.

Overall Formula

Components & Weights (

)

•  (식단 점수): 

• 

•  (운동 점수): 

• 
•  (수면 점수): 

• 

•  (습관/회복 점수): 

• 

Growth Rate Weight (

)

• : 성장 가중 계수 (

• ).
• 점수가 다소 낮더라도 최근 3일간 긍정적 변화를 보이면 점수가 대폭 상승 보정되어 사용자가 지루함을 느끼지 않도록 설계함.

Related Documents
• 01_ARCHITECTURE/FORMULA_REGISTRY.md