# PATCH_004_SUMMARY

## 개요
PATCH-004는 기획 문서 추가가 아니라, 실제 개발 단계에서 구현 방식의 편차를 줄이기 위한 Implementation Governance 패치다.

## 이번 패치에서 반영한 산출물
### 00_PROJECT
- IMPLEMENTATION_GUIDELINES.md
- CONFIG_AND_CONSTANT_POLICY.md
- CODE_REVIEW_CHECKLIST.md
- TECH_DEBT_REGISTER.md
- TEST_COVERAGE_STANDARD.md
- CANONICAL_CONSTANTS.md
- CANONICAL_NAMING.md (v2 갱신)
- NEXT_AI_HANDOFF_GUIDE_PATCH_004.md
- NEXT_AI_EXECUTION_PLAN_PATCH_004.md
- PATCH_004_SUMMARY.md

### 03_BACKEND
- API_CONTRACT_STANDARD.md
- ENGINE_INTEGRATION_GUIDE.md
- ORPHAN_MODULE_POLICY.md

### 04_FRONTEND
- STATE_MANAGEMENT_STANDARD.md

### 03_GAME_SYSTEM
- BALANCE_CHANGE_PROCESS.md
- EXP_RULE.md (PATCH-004 기준 재작성)

### scripts
- check_canonical_constants.py

## 핵심 결정사항
- Exp 표기 통일
- 정령 = 역할명 유지
- 건강이 = 기본 이름
- Daily Exp Soft Cap = 300
- Weekly Soft Cap = 2100
- anti-farming interval = 10분
- 신규 상태관리 표준 = Riverpod
- 기존 Provider = 레거시 허용 후 단계적 migration

## 검증 결과
- 핵심 상수 검증 스크립트 통과
- 신규 문서 생성 및 재작성 반영 완료

## 다음 담당자 시작점
1. 00_PROJECT/CANONICAL_CONSTANTS.md
2. 00_PROJECT/IMPLEMENTATION_GUIDELINES.md
3. 00_PROJECT/NEXT_AI_HANDOFF_GUIDE_PATCH_004.md
4. 00_PROJECT/NEXT_AI_EXECUTION_PLAN_PATCH_004.md
