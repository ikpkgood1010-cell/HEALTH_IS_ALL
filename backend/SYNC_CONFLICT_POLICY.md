SYNC_CONFLICT_POLICY

Purpose
본 문서는 오프라인 상태에서 누적된 데이터와 서버 데이터가 동기화될 때 발생하는 충돌 해결(Conflict Resolution) 규칙을 정의한다.

General Principle
• 단순한 Last Write Wins (LWW) 정책을 지양하고, 도메인의 특성에 따른 병합(Merge) 정책을 우선 적용한다.

Domain-Specific Conflict Resolution Matrix


Domain Category
Conflict Resolution Strategy
Details

식단 / 운동 기록
Union & Append Merge
로컬 및 서버 데이터를 중복 아이디(UUID) 검증 후 합집합으로 병합 (데이터 손실 방지).

유저 프로필 / 설정
Last Write Wins (LWW)
가장 최근 타임스탬프를 가진 수정본으로 덮어씀.

Exp / Point 재화
Cumulative Audit
클라이언트의 재화 수치를 그대로 믿지 않고, 누적된 트랜잭션 로그를 서버가 재검증 후 최종 합산.

습관 Streak
Max Value Preservation
로컬과 서버 중 더 높은 연속 달성 기록을 보존.



Related Documents
• 03_BACKEND/OFFLINE_FIRST_POLICY.md