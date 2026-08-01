# CONFIG_AND_CONSTANT_POLICY

- Document Name: CONFIG_AND_CONSTANT_POLICY.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 문서와 코드의 상수 불일치를 빌드 전에 탐지하고, 중앙 상수 관리 절차를 정의한다.
- Implementation Status: Implemented
- Source of Truth: Documentation + Config + Code
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: `scripts/check_canonical_constants.py`

## Policy Statement
Exp Daily Cap 300 vs 1000 같은 충돌은 “문서 오류”나 “코드 오류”로 즉시 단정하지 않는다. 먼저 **어느 쪽이 SSOT인지 결정**한 뒤, 문서·코드·테스트를 한 패치에서 같이 동기화한다.

## Config 위치
1. 런타임 설정 기본값: `backend/config.py`
2. 환경별 override: `.env`, `.env.example`
3. API schema 기본값: `backend/models.py`
4. 프론트 임시/목업 상수: `lib/mock_data_provider.dart` 등

## 상수 위치
1. 프로젝트 전역 핵심 상수의 기준표는 `00_PROJECT/CANONICAL_CONSTANTS.md`
2. 도메인별 파생 상수는 각 도메인 문서에 두되, 중앙 상수와 충돌하면 안 된다.
3. 하드코딩 숫자는 허용하더라도 중앙 상수와 같은 의미인지 주석 또는 이름으로 식별 가능해야 한다.

## SSOT 우선순위
1. `00_PROJECT/CANONICAL_CONSTANTS.md`
2. `backend/config.py`
3. `.env.example` 및 환경설정
4. API 모델 기본값
5. UI 표기 및 목업 데이터
6. 설명 문서/예시 문구

## 문서 변경 절차
1. 변경 요청 등록
2. SSOT 후보와 영향 파일 식별
3. 제품/밸런스 결정
4. `CANONICAL_CONSTANTS.md` 갱신
5. 하위 문서 갱신
6. 검증 스크립트 및 테스트 통과 확인

## 코드 변경 절차
1. `backend/config.py` 또는 해당 중앙 상수 파일 수정
2. 환경 변수 예시 수정
3. API 모델/프론트 기본값 수정
4. 테스트 fixture 수정
5. 리뷰에서 drift 여부 확인

## 동기화 체크
- `backend/config.py`의 `DAILY_EXP_CAP`
- `.env.example`의 `DAILY_EXP_CAP`
- `backend/models.py`의 `daily_exp_cap`
- `lib/mock_data_provider.dart`의 `_dailyExpCap`
- `03_GAME_SYSTEM/EXP_RULE.md` 및 밸런스 문서

## Build Before Detect Rule
모든 PR은 병합 전에 `scripts/check_canonical_constants.py`를 실행해야 한다. 핵심 상수 불일치가 있으면 빌드 전 단계에서 실패로 간주한다.

## Canonical Decision for PATCH-004
- Exp Daily Soft Cap: `300`
- Exp Weekly Soft Cap: `2100`
- Role Label: `정령`
- Default Name: `건강이`
- Health Score Range: `0~100`
- Anti-Farming Interval: `10분`

## Drift 처리 4단계
1. 발견
2. 분류(설계 변경 예정 / 코드 버그 / 문서 미반영)
3. 결정(SSOT 채택)
4. 동기화(문서·코드·테스트 동시 수정)

## Related Source Files
- `00_PROJECT/CANONICAL_CONSTANTS.md`
- `backend/config.py`
- `backend/models.py`
- `.env.example`
- `lib/mock_data_provider.dart`
- `scripts/check_canonical_constants.py`

## Validation Method
- Static Scan
- Compile Check
- PR Gate
- Runtime Verification
