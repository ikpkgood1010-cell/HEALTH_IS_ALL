# SPIRIT_ALBUM_SPEC.md

## Purpose
본 문서는 유저가 달성한 건강 습관과 함께 진화해온 수호 정령들의 모습을 기록하고, 추억의 순간을 앨범 형태로 수집 및 감상할 수 있는 정령 도감 & 힐링 앨범 시스템 명세를 정의한다.

## Scope
1. 정령 진화 단계별 앨범 카탈로그 자동 해금 알고리즘
2. 유저의 특정 건강 달성 기록(예: 클린 식단 10회, 1만보 7일 연속)과 연동된 '힐링 메모리 스냅샷' 생성
3. 정령과의 친밀도 레벨($Affinity Level$) 산출
4. 도감 수집률에 따른 건강 보너스 혜택 부여

## SSOT
본 문서는 정령 앨범 백엔드 엔진(`backend/spirit_album_engine.py`) 및 프론트엔드 위젯(`lib/monthly_report_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Spirit Affinity Level ($SAL$)**: 정령과의 교감 및 누적 건강 활동으로 결정되는 친밀도 지수.
- **Healing Snapshot**: 건강 목표 달성 시 정령과 함께 찍은 듯한 일러스트 기반 메모리 카드.

## Runtime
- 프론트엔드(Flutter): Grid 형태의 정령 앨범 도감, 스냅샷 확대 보기 모달, 친밀도 게이지.
- 백엔드(FastAPI/Python): 해금 조건 검증, 앨범 스냅샷 데이터 생성 및 친밀도 수식 계산.

## Rules
1. **정서적 유대감 형성**: 단순 아이템 수집이 아닌, 유저가 자신의 몸을 보살핀 일시와 노력이 정령과의 추억으로 저장되도록 연출한다.
2. **과도한 가챠 요소 배제**: 앨범 해금은 오직 유저의 건강 행동(걸음, 영양, 수분)을 통해서만 이루어진다.
3. **오류 방지 Fallback**: 네트워크 오프라인 시 로컬 저장소의 앨범 데이터를 캐싱하여 즉시 표시한다.

## State
- `unlocked_spirits_list`, `unlocked_snapshots_count`
- `spirit_affinity_level`, `collection_rate_pct`

## Event
- `ON_SPIRIT_EVOLVED`: 정령 진화 시 신규 도감 카드 해금
- `ON_SNAPSHOT_UNLOCKED`: 주요 건강 업적 달성 시 힐링 스냅샷 저장

## Example
$$SAL = \text{BaseLevel} + \left( \frac{\text{TotalCleanMeals} \times 12 + \text{TotalSteps}}{5000} \right) \times 0.1$$

## Exception
- 이미지 자원이 유실되거나 해금 데이터가 일치하지 않을 경우 기본 숲 속성 정령 스냅샷을 대체하여 앱 안정성을 유지한다.

## Related Documents
- `01_ARCHITECTURE/MONTHLY_REPORT_SPEC.md`
- `01_ARCHITECTURE/GUILD_CHALLENGE_SPEC.md`

## Change History
- 2026-07-31 (PATCH_016): 정령 도감 & 힐링 앨범 시스템 명세서 신규 작성 (SSOT 규격 준수).