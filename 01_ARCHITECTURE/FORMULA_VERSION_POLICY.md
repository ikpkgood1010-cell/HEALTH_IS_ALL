FORMULA_VERSION_POLICY

Purpose
본 문서는 밸런싱, 기능 개선 등에 따른 수식 변경 시 버전 관리 규칙(SemVer 적용) 및 기존 사용자 데이터 마이그레이션/롤백 가이드라인을 정의한다.

Version Structure
• Major.Minor.Patch (예: 1.2.0) 
◦ Major: 수식의 대규모 개편으로 기존 결과 수치의 범위가 근본적으로 바뀌는 경우. (마이그레이션 필수)
◦ Minor: 계수 조정, 변수 추가 등으로 결과값 밸런싱이 변경되는 경우.
◦ Patch: 단순 오타 수정, 경계값 엣지 케이스 오류 수정.

User Data Migration & Rollback Rules
1. Backward Compatibility: Formula의 Major 변경 시, 이전 수식으로 계산된 과거 이력 데이터(예: 일일 건강 점수 이력)는 재계산하여 소급 적용하지 않고, 산출 당시의 스냅샷 값을 보존한다.
2. Migration Script Requirement: Major 변경 시 이전 데이터와의 단절을 막기 위해 델타 보정 계수를 적용하는 DB Migration 스크립트를 반드시 동시 배포해야 한다.
3. Rollback Policy: 수식 오류 발견 시 1시간 이내 이전 Stable 버전을 롤백 적용하며, 오지급된 인게임 재화/경험치는 차감하지 않고 보정 퀘스트로 밸런싱을 완화한다.

Related Documents
• 01_ARCHITECTURE/FORMULA_REGISTRY.md