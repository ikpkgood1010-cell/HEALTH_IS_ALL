App Architecture & Data Integration Guide

1. 데이터 연동 구조 (End-to-End Data Flow)

• UI 레이어 (Flutter) : HomeScreen에서 식단/운동/습관 입력
• API 백엔드 (FastAPI) : HealthRecordRequest 수신 후 ProgressionEngine 처리
• 엔진 처리: 일일 최대 300 Exp. 제한 및 10분 이내 연달아 입력 방지 로직 연산
• DB 레이어 (PostgreSQL) : meal_logs / workout_logs 저장 및 health_i_profiles 상태 업데이트
• 인터랙션 연동: '건강이' 반응 애니메이션 출력 및 Exp. 바 업데이트

───

2. Dual-Excellence UI 검수 가이드라인
1. 건강 지표 가독성: 홈 화면 최상단 건강 카드는 게임 요소에 침범당하지 않아야 한다.
2. '건강이' 모션 완성도: 캐릭터 터치 반응 및 바운스 애니메이션은 60fps 이상의 부드러운 프레임으로 출력되어야 한다.
3. 용어 표준: UI 내 경험치는 오직 Exp., 정령 캐릭터는 오직 **건강이**로 표기한다.