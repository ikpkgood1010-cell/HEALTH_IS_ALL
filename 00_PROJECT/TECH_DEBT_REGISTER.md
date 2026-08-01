# TECH_DEBT_REGISTER

- Document Name: TECH_DEBT_REGISTER.md
- Version: 1.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 기술 부채를 추적 가능한 형태로 관리하고, 운영 리스크를 우선순위에 따라 해소한다.
- Implementation Status: Implemented
- Source of Truth: Documentation
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: manual audit baseline

## Register
| ID | Priority | Owner | Status | Risk | Due | Impact | Resolution |
|---|---|---|---|---|---|---|---|
| TD-001 | Critical | Product + Backend | Open | High | Next patch | `EXP_RULE.md` 1000 vs `backend/config.py` 300 불일치로 밸런스/표기/테스트 기준이 분열됨 | `CANONICAL_CONSTANTS.md`를 기준으로 문서·코드·테스트 동시 동기화 |
| TD-002 | High | Architecture | Open | Medium | Next patch | `spirit_*`, `guild_*`, `heartrate_spirit_widget.dart` 등 orphan 후보 모듈이 활성 코드처럼 혼재 | `ORPHAN_MODULE_POLICY.md` 기준으로 archive 또는 복귀 결정 |
| TD-003 | High | Frontend | Open | Medium | Next patch | `Meal`, `Exercise`, `Profile`, `Settings` 화면 구현 대비 `main_navigation_screen.dart` 미연결 | 라우트 연결 또는 숨김 정책 문서화 |
| TD-004 | High | Frontend | Open | Medium | Next patch | Provider와 Riverpod가 혼재하여 상태관리 표준이 분열 | 신규는 Riverpod, 기존 Provider는 단계적 migration |
| TD-005 | Medium | Product + UX | Open | Medium | Later | 사용자 표기 `Exp.`와 목표 표준 `Exp`가 혼재 | UI/문서/번역 문자열 점진 교체 |
| TD-006 | Medium | Docs | Open | Medium | Later | `03_GAME_SYSTEM/EXP_RULE.md`와 일부 밸런스 문서가 손상/구식 표현 포함 | 재작성 및 검증 기준 추가 |
| TD-007 | Medium | Frontend | Open | Low | Later | `home_screen.dart`, `shop_screen.dart` 등에 템플릿 손상 문자열 존재 | 화면별 정리 및 실제 빌드 검증 |
| TD-008 | Medium | Backend | Open | Medium | Later | `profile.level = (profile.current_exp // 300) + 1`가 데일리 캡과 같은 숫자를 공유해 의미 혼동 가능 | 레벨업 기준 상수 분리 |

## Operating Rules
1. 기술 부채는 발견 즉시 등록한다.
2. 제품 결정이 필요한 항목과 단순 버그를 분리한다.
3. 해결 시 관련 테스트와 문서를 함께 갱신한다.
4. Close 처리 전 재검증 근거를 남긴다.

## Related Source Files
- `backend/config.py`
- `backend/main.py`
- `lib/main_navigation_screen.dart`
- `04_FRONTEND/STATE_MANAGEMENT_GUIDE.md`
- `03_GAME_SYSTEM/EXP_RULE.md`

## Validation Method
- Manual Audit
- Runtime Verification
- Backlog Review
