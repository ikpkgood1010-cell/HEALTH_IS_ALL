# CANONICAL_CONSTANTS

- Document Name: CANONICAL_CONSTANTS.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 프로젝트 전역의 변경 빈도가 낮지만 영향도가 높은 핵심 상수의 기준표를 정의한다.
- Implementation Status: Implemented
- Source of Truth: Documentation + Config
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: `scripts/check_canonical_constants.py`

## Canonical Constants Table
| Item | Value | Description |
|---|---:|---|
| Exp Daily Soft Cap | 300 | 일일 성장 반영 최대치 |
| Exp Weekly Soft Cap | 2100 | 300 x 7 기준 주간 관리치 |
| Anti-Farming Interval Minutes | 10 | 동일 계열 연속 입력 제한 |
| Default Spirit Role Label | 정령 | 사용자 노출 역할 명칭 |
| Default Spirit Name | 건강이 | 기본 이름, 사용자 변경 가능 |
| Health Score Range Min | 0 | AI 및 UI 공통 최솟값 |
| Health Score Range Max | 100 | AI 및 UI 공통 최댓값 |
| Default Time Zone Policy | Local Time | 사용자 기준 날짜/리셋 해석 |
| Default Locale Policy | ko-KR fallback en-US | UI/메시지 기본 로케일 정책 |

## Operating Notes
1. 역할명은 `정령`, 기본 이름은 `건강이`로 분리한다.
2. Daily Cap은 건강 행동을 막는 hard stop이 아니라 성장 반영 기준의 soft cap으로 운영한다.
3. 300 초과 행동은 기록/통계/배지에는 반영될 수 있지만 성장 경제는 점진 감쇄를 우선 검토한다.
4. 상수 변경은 밸런스 문서, config, API 모델, 테스트를 같은 패치에서 갱신한다.

## Related Source Files
- `backend/config.py`
- `.env.example`
- `backend/models.py`
- `lib/mock_data_provider.dart`
- `03_GAME_SYSTEM/BALANCE_CHANGE_PROCESS.md`

## Validation Method
- Static Scan
- Compile Check
- Runtime Verification
