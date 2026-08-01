# SSOT_VERIFICATION_CHECKLIST

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: SSOT와 코드/테스트/운영 구성이 일치하는지 검증하는 PATCH-005 표준 체크리스트.

## Verification Order
1. Config
2. Formula
3. Reward / Exp
4. Event
5. Runtime
6. API Contract
7. Test Coverage
8. Naming / UI Exposure
9. Orphan Classification

## Checklist
| Area | Required Check | Current Result |
|---|---|---|
| Formula | Registry ID가 코드와 테스트에 연결되는가 | Partial |
| Config | 핵심 상수(Exp cap, anti-farming, 기본 이름)가 코드/문서에 일치하는가 | PASS |
| Event | Event ID가 실제 producer/consumer 코드에 매핑되는가 | FAIL |
| Runtime | 상태 전이/timeout/recovery가 코드 수준에서 확인되는가 | Partial |
| Reward | 보상 계산과 UI 노출 표기가 일치하는가 | PASS |
| Exp | `Exp` 표준 표기를 유지하는가 | PASS |
| Point | Point 정책과 상점 재화 명칭이 분리되는가 | Partial |
| AI Prompt | Prompt/AI 규칙이 코드와 문서에 연결되는가 | Partial |
| Memory | Memory 관련 구현과 문서가 연결되는가 | Partial |
| Emotion | 감정 상태 규칙이 AI 피드백과 UI에 반영되는가 | Partial |
| API Contract | 주요 엔드포인트가 테스트로 확인되는가 | PASS |
| Test | 핵심 런타임 변경이 회귀 테스트를 갖는가 | PASS (현재 9개) |
| Naming | 금지 용어(XP/EXP/Spirit) 신규 노출이 제거되었는가 | PASS for active code, legacy docs remain |
| Orphan | 미연결 모듈이 active/roadmap/archive로 분류되었는가 | Partial |

## Mandatory Evidence For PASS
- `scripts/check_canonical_constants.py`
- `scripts/check_patch005_integrity.py`
- `pytest -q`
- naming scan (`Exp.` / backtick / malformed interpolation)

## Exit Criteria
- P0 항목(Config, Formula, Reward, API Contract)에서 FAIL이 없어야 한다.
- Event/Runtime는 최소 Partial 이상이되, 운영 배포 전 explicit gap log가 있어야 한다.
