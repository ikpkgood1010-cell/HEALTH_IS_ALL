# CODE_REVIEW_CHECKLIST

- Document Name: CODE_REVIEW_CHECKLIST.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 리뷰어가 무엇을 확인해야 하는지 프로젝트 표준으로 고정한다.
- Implementation Status: Implemented
- Source of Truth: Documentation
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: PR review process

## Reviewer Checklist
### 1. SSOT 확인
- [ ] 관련 상위 문서가 식별되었는가
- [ ] `CANONICAL_CONSTANTS.md`와 값이 일치하는가
- [ ] 문서 변경이 필요한 경우 같은 PR에 포함되었는가

### 2. Naming 확인
- [ ] 신규 사용자 표기에서 `Exp`, `정령`, `건강이` 규칙을 따르는가
- [ ] 신규 금지 용어(`XP`, `EXP`, `Spirit` 등)를 추가하지 않았는가
- [ ] 레거시 유지가 필요하면 기술 부채로 등록했는가

### 3. Formula 확인
- [ ] Exp/Point/Quest/Reward 계산 변경이 문서화되었는가
- [ ] hard-coded cap, multiplier, threshold가 중앙 상수와 일치하는가
- [ ] fallback 공식과 normal 공식이 구분되는가

### 4. Event 확인
- [ ] 이벤트 이름과 발생 조건이 명확한가
- [ ] 중복 이벤트 지급, anti-farming 우회, sync 중복이 없는가

### 5. Runtime 확인
- [ ] 실행 코드는 `backend/`, `lib/` 기준으로 반영되었는가
- [ ] orphan 모듈이나 미연결 화면에 변경이 들어가면 의도가 기록되었는가
- [ ] 로그/예외/오프라인 정책이 유지되는가

### 6. AI Prompt 확인
- [ ] 프롬프트/대사/코칭 문구가 canonical naming과 일치하는가
- [ ] 사용자 노출 문구에 레거시 용어가 없는가
- [ ] fallback 메시지가 과장되거나 오해를 주지 않는가

### 7. Test 확인
- [ ] 단위 테스트 또는 통합 테스트가 추가/수정되었는가
- [ ] 기존 테스트를 깨는 변경이면 이유가 기록되었는가
- [ ] 실행 검증과 정적 검증을 구분해 보고했는가

### 8. Migration 확인
- [ ] Provider -> Riverpod 등 점진 전환 항목이면 호환 전략이 있는가
- [ ] route 추가/삭제, schema 변경, env 변경 시 migration 메모가 있는가

## Merge Stop Conditions
- 중앙 상수 mismatch
- 문서와 코드의 계약 불일치
- 테스트 없이 핵심 계산 로직 변경
- orphan/legacy 코드를 활성 코드처럼 병합

## Related Source Files
- `00_PROJECT/CANONICAL_CONSTANTS.md`
- `00_PROJECT/IMPLEMENTATION_GUIDELINES.md`
- `03_BACKEND/API_CONTRACT_STANDARD.md`
- `04_FRONTEND/STATE_MANAGEMENT_STANDARD.md`

## Validation Method
- Manual Review
- PR Checklist
- Static Scan
