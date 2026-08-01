# NEXT_AI_HANDOFF_GUIDE_PATCH_004

## 목적
다음 AI가 PATCH-004 이후 작업을 바로 이어받을 수 있도록 현재 결정사항과 금지사항, 다음 액션을 압축 정리한다.

## 이번 패치에서 완료한 것
1. Implementation Governance 문서군 10종 작성
2. `CANONICAL_CONSTANTS.md` 신규 작성
3. `EXP_RULE.md`를 300 soft cap 기준으로 재작성
4. 다음 AI용 실행 계획 문서 추가

## 이번 패치의 핵심 결정
- 표기 표준: `Exp`
- 역할명: `정령`
- 기본 이름: `건강이`
- Daily Exp Soft Cap: `300`
- Weekly Soft Cap: `2100`
- anti-farming interval: `10분`
- 신규 상태관리 표준: Riverpod
- 기존 Provider는 레거시 허용 후 단계적 migration

## 다음 AI가 먼저 할 일
1. `scripts/check_canonical_constants.py` 실행 또는 같은 로직으로 상수 drift 재검증
2. `CANONICAL_NAMING.md` 전체 정비 여부 확인
3. `backend/config.py`, `backend/progression_engine.py`, 사용자 노출 문자열에서 `Exp.` -> `Exp` 정리 범위 결정
4. `main_navigation_screen.dart`에 미연결 화면 연결 여부 제품 결정
5. orphan 후보 모듈을 archive/roadmap 중 하나로 분류

## 건드릴 때 주의할 것
- 문서와 코드가 다르면 임의 hotfix 금지
- SSOT 결정 없는 숫자 교체 금지
- orphan 모듈을 활성 코드처럼 설명하지 말 것
- Provider/Riverpod 혼용 화면 확대 금지

## 권장 읽기 순서
1. `00_PROJECT/CANONICAL_CONSTANTS.md`
2. `00_PROJECT/IMPLEMENTATION_GUIDELINES.md`
3. `03_BACKEND/API_CONTRACT_STANDARD.md`
4. `04_FRONTEND/STATE_MANAGEMENT_STANDARD.md`
5. `03_BACKEND/ENGINE_INTEGRATION_GUIDE.md`
6. `00_PROJECT/TECH_DEBT_REGISTER.md`

## 산출물 확인 포인트
- 새 문서 10종 존재 여부
- `EXP_RULE.md` 재작성 여부
- zip 내부 handoff/plan 문서 포함 여부
