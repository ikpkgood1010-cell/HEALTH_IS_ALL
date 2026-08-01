# WEARABLE_SYNC_SPEC.md

## Purpose
본 문서는 Wear OS, Apple Watch 등 외부 스마트 워치 및 웨어러블 기기와의 실시간 생체 데이터(심박수, 실시간 걸음 수, 활동 강도) 연동 표준 및 동기화 수신 체계 규격을 정의한다.

## Scope
1. 웨어러블 기기와의 Bluetooth Low Energy(BLE) 및 OS 헬스 키트(HealthConnect/HealthKit) 실시간 파이프라인 수신
2. 실시간 심박수($HeartRate, HR$) 데이터 유효성 검증 및 이상치 필터링
3. 연결 단절 시 로컬 버퍼링 및 재연동 자동 복구(Fallback) 메커니즘
4. 정령과의 생체 동기화(Heartbeat Pulse Sync) 모션 및 다정한 연결 안내 UI 규격

## SSOT
본 문서는 웨어러블 동기화 백엔드 엔진(`backend/wearable_sync_engine.py`) 및 프론트엔드 워치 위젯(`lib/wearable_sync_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Heartbeat Pulse Sync**: 유저의 실제 심박수에 맞춰 수호 정령의 호흡 및 아우라 박동 속도를 실시간 인터랙션하는 UI 기술.
- **Biometric Health Packet**: 기기에서 10초 간격으로 백엔드/클라이언트에 전달되는 생체 신호 데이터 묶음.

## Runtime
- 프론트엔드(Flutter): 실시간 심박 애니메이션, 워치 연결 상태 뱃지, 다정한 연결 축하 팝업.
- 백엔드(FastAPI/Python): 센서 데이터 무결성 검증, 데이터 노이즈 제거, 동적 운동 강도 레이블링.

## Rules
1. **건강 본위 및 생체 안전 우선**: 기기 측정 심박수가 유저의 연령별 최고 심박수($220 - \text{Age}$)의 85%를 초과할 경우 과도한 운동 방지 주의 팝업을 우선 출력한다.
2. **다정한 안내 문구**: 연결 이상 발생 시 "연결 실패"라는 차가운 문구 대신 "스마트 워치가 잠시 쉬고 있어요 🌿 손목을 가볍게 토닥여 다시 연결해 볼까요?"라는 문구를 사용한다.
3. **세분화 동적 수식**: 기본 심박수($HR_{rest}$), 활동 심박수($HR_{act}$), 센서 신뢰도 지수 및 $0.98 \sim 1.02$ 난수를 종합 적용한다.

## State
- `device_connected_status`, `realtime_hr`
- `hr_confidence_score`, `buffered_packet_count`

## Event
- `ON_WEARABLE_CONNECTED`: 워치 기기 연결 성공 이벤트
- `ON_HEART_RATE_UPDATED`: 실시간 심박수 수신 및 UI 펄스 업데이트
- `ON_HR_WARNING_TRIGGERED`: 과도한 안정/고심박수 탐지 시 안전 알림

## Example
$$HR_{valid} = \begin{cases} HR_{raw}, & \text{if } 40 \le HR_{raw} \le 210 \\ \text{Fallback Value}, & \text{otherwise} \end{cases}$$

## Exception
- 워치 연결이 해제되거나 센서 미착용으로 측정값이 유실된 경우, 직전 5분간의 평균 심박수를 안전 대체치로 사용한다.

## Related Documents
- `01_ARCHITECTURE/HEART_RATE_CALORIE_SPEC.md`
- `01_ARCHITECTURE/GUILD_CHALLENGE_SPEC.md`

## Change History
- 2026-07-31 (PATCH_017): 웨어러블 디바이스 실시간 연동 명세서 신규 작성 (SSOT 규격 준수).