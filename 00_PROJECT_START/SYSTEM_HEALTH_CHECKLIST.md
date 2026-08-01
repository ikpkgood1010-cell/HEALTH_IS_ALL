HEALTH IS ALL - System Health & SSOT Audit Checklist

1. 정밀 검사 종합 점검표


점검 영역
항목
상태
비고 및 조치사항

용어 표준화
Exp. 명칭 표기
완료
모든 코드, DB 명세, MD 문서에서 XP/EXP 제거 및 Exp. 통일

용어 표준화
'건강이' 캐릭터 명칭
완료
Spirit/Pet/NPC 용어 퇴출 및 '건강이' 완전 통합

Dual-Excellence
건강 수치 전달력
완료
UI 상에서 운동/식단 수치가 게임 요소에 가려지지 않도록 독립 영역 보장

Dual-Excellence
게임성 완성도
완료
'건강이' 인터랙션 및 Exp. 획득 모션의 고품질 그래픽 디자인 레이어 분리

백엔드 로직
Exp. 일일 상한선
완료
 및 10분 어뷰징 방지 로직 적용

파일 구조
표준 파일명 준수
완료
UPPER_SNAKE_CASE 적용 및 루트 SQL 파일 02_DATABASE/ 정리 완료



───

2. 다음 단계 이행 예정 항목 (Next Steps)
1. Database Table DDL 검수: 02_DATABASE/DATABASE_SCHEMA_MASTER.md 내 컬럼명을 exp_points 및 health_i_id로 최종 업데이트.
2. Flutter Screen Integration: lib/home_screen.dart에 새로 작성된 HealthIWidget 결합.