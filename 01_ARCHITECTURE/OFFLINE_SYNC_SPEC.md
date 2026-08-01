# OFFLINE_SYNC_SPEC.md

## Purpose
본 문서는 산행, 지하철, 음영 지역 등 오프라인 상태에서 수집된 유저의 건강 데이터(걸음 수, 스팀 식단 기록, 수분 섭취)를 로컬 DB에 안전하게 보관하고, 네트워크 재연동 시 백엔드로 충돌 없이 동기화하는 모듈 규격을 정의한다.

## Scope
1. 오프라인 네트워크 감지 및 SQLite/Hive 기반 로컬 동기화 큐(Queue) 관리
2. 재연동 시 일괄 패킷(Batch Sync) 전송 체계 구축
3. 네트워크 불안정 시 정령이 유저의 기록을 소중히 보관하는 UI 연출
4. 서버와 클라이언트 간 타임스탬프 충돌 해결(Resolution) 정책

## SSOT
본 문서는 오프라인 동기화 백엔드 엔진(`backend/offline_sync_engine.py`) 및 프론트엔드 위젯(`lib/offline_sync_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Local Sync Queue**: 오프라인 중 생성된 식단, 운동, 수분 데이터 트랜잭션 패킷이 순차 보관되는 로컬 저장소.
- **Timestamp Priority Merge**: 동일 시각에 발생한 데이터 충돌 시, 클라이언트의 유효 생체 신호가 포함된 최신 기록을 우선 반영하는 정책.

## Runtime
- 프론트엔드(Flutter): 오프라인 상태 감지 뱃지, 로컬 저장 건수 표시, 다정한 안심 팝업.
- 백엔드(FastAPI/Python): 재연동 패킷 순차 파싱, 데이터 중복 검증, 정령 성장 경험치 지연 합산.

## Rules
1. **건강 데이터 유실 제로화**: 오프라인 상태에서 입력된 식단이나 걸음 수 기록은 어떠한 경우에도 유실되지 않고 정령의 소중한 배낭에 보관된다.
2. **다정한 안내 어조**: "오프라인 오류"라는 단어 대신 "정령이 비밀 노트에 소중히 기록해두고 있어요 📝 network가 연결되면 한 번에 전해줄게요!"라는 문구를 표출한다.
3. **세분화 동적 수식**: 동기화 지연 시간($Delay_{sec}$), 패킷 밀도 및 $0.98 \sim 1.02$ 난수 가중치를 적용하여 지연 보상 정령 에너지를 계산한다.

## State
- `is_offline_mode`, `pending_queue_count`
- `last_synced_timestamp`, `sync_status_enum`

## Event
- `ON_NETWORK_DISCONNECTED`: 오프라인 모드 전환 및 로컬 큐 활성화
- `ON_NETWORK_RECONNECTED`: 백엔드 재연동 및 큐 일괄 수신/합산

## Example
$$Energy_{delay\_bonus} = \text{BaseEnergy} \times \left( 1 + \min\left(0.1, \frac{\text{DelaySec}}{3600} \times 0.02\right) \right) \times \text{Jitter}$$

## Exception
- 재연동 시 클라이언트 시간과 서버 시간의 차이가 24시간 이상 벌어질 경우, 서버 시각 기준으로 정렬하여 데이터 왜곡을 방지한다.

## Related Documents
- `01_ARCHITECTURE/DATA_IDEMPOTENCY_SPEC.md`
- `01_ARCHITECTURE/WEARABLE_SYNC_SPEC.md`

## Change History
- 2026-07-31 (PATCH_018): 오프라인 로컬 데이터 동기화 명세서 신규 작성 (SSOT 규격 준수).