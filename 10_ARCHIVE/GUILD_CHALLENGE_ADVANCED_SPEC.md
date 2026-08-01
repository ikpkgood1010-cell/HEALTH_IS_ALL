# [중복문서-덮어쓰기, 교체] Guild Challenge Advanced Specification

## Purpose
개인의 건강 관리를 넘어서 커뮤니티(하이킹 클럽 'VMTC' 등 소그룹 및 길드) 단위로 건강 목표를 공유하고 협력하는 챌린지 시스템을 정의합니다.

## Scope
- 길드 레이드, 공동 식단/운동 미션, 기여도 산출 규칙

## SSOT
- 길드 및 커뮤니티 연계 기능의 단일 진실 공급원.

## Definitions
- **VMTC Synergy**: 클럽 멤버들의 누적 운동 시간 및 클린 식단 실천율에 비례하여 길드 전체에 버프를 부여하는 시스템.

## Runtime
- 백엔드 서버와 실시간 WebSocket 연동을 통해 길드 현황판 업데이트.

## Rules
1. 경쟁보다는 상호 격려와 협력을 우선시하는 디자인 철학을 유지합니다.
2. 데이터 동기화 오류 방지를 위해 오프라인 상태에서의 기록은 로컬에 임시 저장 후 일괄 동기화합니다.

## State
- 길드원들의 실시간 기여도 상태 (`GuildContributionState`).

## Event
- `GUILD_EVENT_MISSION_ACCOMPLISHED`: 공동 미션 달성 시 트리거.

## Example
- 길드원 5명이 주간 클린 식단 달성 시 'VMTC 산행 버프' 활성화.

## Exception
- 통신 불량 시 로컬 캐시 데이터를 우선 표시하고 상단에 '오프라인 동기화 대기 중' 배너 표시.

## Related Documents
- `HEALTH IS ALL/03_BACKEND/guild_challenge_engine.py`

## Change History
- v3.0 (2026-07-31): 하이킹 클럽 'VMTC' 연계 협력 미션 스펙 고도화