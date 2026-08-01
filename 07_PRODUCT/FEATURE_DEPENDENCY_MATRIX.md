Feature Dependency Matrix (기능 연쇄 영향도 추적표)

1. 개요
본 문서는 HEALTH IS ALL 프로젝트 내 단일 기능 변경이 시스템 전체(도메인, DB, UI, AI, Analytics)에 미치는 파급 효과를 정의합니다. 개발자 및 AI 에이전트는 코드 및 공식 수정 전 본 매트릭스를 반드시 참조하여 연쇄 부작용을 방지해야 합니다.

───

2. 도메인 간 연쇄 영향도 매트릭스 (Cascade Matrix)


원천 기능 (Trigger Event)
1차 영향 (Primary)
2차 영향 (Secondary)
3차 영향 (Tertiary)
최종 출력 (Output Layer)

운동 기록 완료
ExerciseCompleted
• Exercise DB 저장
• Health Engine 계산
• XP / Spirit Energy 지급
• Quest 진행도 갱신
• Spirit 감정/성장 업데이트
• 랭킹 / 연속 달성(Streak)
• Home ReadModel 갱신
• 축하 Notification
• Analytics Event 전송

식단 기록 등록
MealRecorded
• Health DB 저장
• 영양소/칼로리 분석
• 일일 권장량 대비 비율 계산
• AI Recommendation Engine
• Spirit 대사/반응 변경
• Habit 달성도 반영
• Meal Screen UI 갱신
• 피드백 피드 생성

습관 달성 완료
HabitAchieved
• Habit DB 갱신
• Streak 카운트 증가
• Quest (습관 연계) 완료
• Spirit Energy 보상
• Spirit 친밀도(Relationship) 증가
• 습관 난이도 자동 조절
• Habit UI Check 애니메이션
• 보상 Pop-up

XP / 난이도 공식 변경
FormulaUpdated
• Progression Engine 계산식 변경
• 레벨업 필요 XP 재산정
• Spirit 성장 속도 변동
• 퀘스트 보상 밸런스 재조정
• LiveOps 시즌 밸런스
• 전체 사용자 XP 게이지 UI
• 밸런싱 검증 로그

정령 상태 변경
SpiritStateChanged
• Spirit DB 상태 업데이트
• AI 대사 생성 프롬프트 변경
• Spirit 애니메이션/표정 전환
• 사용자 맞춤 멘트 발송 스케줄
• Home 화면 정령 Widget
• Push Notification



───

3. 세부 기능별 연쇄 영향 흐름 (Detail Impact Flows)

Flow A: 운동 기록 완료 시 파급 경로
text
[운동 기록 입력] 
   │
   ├──> 1. Health Engine: MET 기반 칼로리 및 운동 강도 계산
   ├──> 2. Exercise DB: 운동 세션 및 상세 세트 기록 저장
   ├──> 3. Progression Engine: 운동 강도 비례 XP 및 Spirit Energy 산정
   ├──> 4. Quest Engine: '일일 운동 N분' 퀘스트 조건 검증 및 자동 완료
   ├──> 5. Spirit Engine: 정령 피로도 소모 및 에너제틱 감정 상태 전환
   ├──> 6. Analytics Engine: `exercise_session_completed` 이벤트 로깅
   └──> 7. UI ReadModel: Home 화면 및 Profile 운동 캘린더 즉시 Invalidate