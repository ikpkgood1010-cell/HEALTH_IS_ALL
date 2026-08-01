# CANONICAL_NAMING

- Document Name: CANONICAL_NAMING.md
- Version: 2.0
- Status: Active
- Owner: PATCH-004 Implementation Governance
- Last Updated: 2026-08-01
- Purpose: 프로젝트 전반의 용어 표준과 금지 용어를 정의하는 SSOT다.
- Implementation Status: Implemented
- Source of Truth: Documentation
- Verification:
  - Last Verified Date: 2026-08-01
  - Verified By: PATCH-004 governance pass
  - Test Reference: naming scan, manual review

## Scope
- 코드
- 문서
- UI/UX
- DB 스키마
- AI 프롬프트

## Canonical Terms
| Canonical | Meaning | Allowed Form |
|---|---|---|
| Exp | 사용자 성장 경험치 | Exp |
| 정령 | 동반자 역할명 | 정령 |
| 건강이 | 기본 정령 이름 | 건강이 |
| Point | 상점/꾸미기 전용 재화 | Point, Pt |
| Habit | 반복 습관 | Habit |
| Goal | 중기 목표 | Goal |
| Quest | 시스템 제공 미션 | Quest |
| Achievement | 업적 | Achievement |
| Memory | 기록/추억 앨범 | Memory |
| Season | 시즌 단위 운영 | Season |

## Naming Notes
1. 역할명과 기본 이름을 분리한다.
2. 사용자에게는 “정령의 이름을 정해 주세요.”라고 안내하고, 기본 이름은 `건강이`를 제공한다.
3. 코드 변수는 `exp`, `currentExp`, `totalExp`처럼 소문자 카멜 케이스를 사용한다.

## Forbidden Terms
| Forbidden | Reason | Replacement |
|---|---|---|
| XP | 표기 혼선 | Exp |
| EXP | 표기 혼선 | Exp |
| Experience Point | 장문/비일관 | Exp |
| Experience | 의미 확장 과다 | Exp |
| Spirit | 역할명 표준 불일치 | 정령 또는 건강이(문맥에 따라) |
| Pet | 동반자 개념 축소 | 정령 또는 건강이 |
| Energy | 가챠/모바일 F2P 오해 가능 | 문맥별 재정의 |
| Coin / Gold | 범용 게임 재화 뉘앙스 | Point |
| Mission | Quest와 혼용 | Quest |

## Review Rule
- 신규 코드/문서/UI에서 금지 용어가 발견되면 리뷰에서 반려한다.
- 레거시 문서/코드는 기술 부채 또는 archive 예외로 관리한다.

## Related Source Files
- `backend/config.py`
- `backend/ai_agent_service.py`
- `backend/progression_engine.py`
- `lib/shop_screen.dart`
- `03_GAME_SYSTEM/EXP_RULE.md`

## Validation Method
- Naming Scan
- Code Review
- Manual Review
