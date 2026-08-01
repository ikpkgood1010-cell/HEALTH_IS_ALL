# AUDIO_COACHING_SPEC.md

## Purpose
본 문서는 유저가 운동 수행 중 시각 화면 확인 없이도 안전하고 효율적으로 운동할 수 있도록, 실시간 심박수, 페이스, 정령 친밀도 데이터에 기반하여 정령의 목소리로 피드백을 전달하는 AI 오디오 코칭 엔진의 기술 요구사항을 정의한다.

## Scope
1. 실시간 심박수 구간(안전, 유산소, 피크) 모니터링 및 억제/독려 음성 멘트 동적 생성
2. 정령 속성(불, 물, 풀, 빛)별 커스텀 톤앤매너 및 호감형 페르소나 음성 스크립트 매핑
3. 운동 페이스 유지를 위한 템포 가이드 큐(Cue) 및 간격 타이머 로직 산출
4. 심박수 과부하 시 유저 보호를 위한 즉각 휴식 권고 음성 오버라이드
5. 오디오 스트리밍 지연 시 텍스트 팝업으로 우선 대체하는 안전 Fallback 연동

## SSOT
본 문서는 오디오 코칭 백엔드 엔진(`backend/audio_coaching_engine.py`) 및 프론트엔드 오디오 위젯(`lib/audio_coaching_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Target HR Zone**: 유저 연령 및 기초체력 기반 최적 유산소 심박수 범위.
- **Audio Cue Interval**: 오디오 코칭이 실행되는 피드백 주기(예: 3분, 5분 또는 심박수 위험 탐지 시).

## Runtime
- 프론트엔드(Flutter): TTS(Text-to-Speech) 엔진 제어, 오디오 재생 인터페이스 및 정령 대화 팝업 표시.
- 백엔드(FastAPI/Python): 실시간 바이오 파라미터 파싱, 피드백 멘트 최적화, 속성별 맞춤 문장 조합.

## Rules
1. **건강 중심 본위 원칙**: 게임적 목표 달성보다 유저의 심혈관 안전이 최우선이다. 목표 심박수의 $85\%$를 초과할 경우 정령은 "지금 정말 멋지게 달리고 계세요! 하지만 정령의 안전을 위해 1분만 천천히 걸으며 호흡을 가다듬어봐요 🌿"와 같이 즉각 속도 조절을 권고한다.
2. **따뜻하고 호감 가는 문구**: 칭찬과 응원을 기본으로 하며, 지친 유저에게 비난이나 조급함을 유발하는 표현을 엄격히 금지한다.
3. **다변수 미세 수식**: 현재 심박수, 평균 페이스, 정령 친밀도 레벨 및 $0.97 \sim 1.03$ 난수 지터를 조합하여 매번 다채로운 멘트를 구성한다.

## State
- `current_heart_rate`, `target_hr_min`, `target_hr_max`
- `spirit_element`, `spirit_affinity_lvl`
- `coaching_state` (IDLE, ACTIVE, REST_ADVISED, COMPLETED)

## Event
- `ON_HEART_RATE_UPDATED`: 실시간 심박수 입력 및 구간 판정
- `ON_COACHING_INTERVAL_REACHED`: 지정된 정기 코칭 시점 도달
- `ON_SAFETY_OVERLOAD_DETECTED`: 과부하 심박수 탐지 시 긴급 음성 트리거

## Example
$$\text{VoicePace} = \text{BasePace} \times \left(1.0 + \frac{\text{HeartRate} - \text{TargetHR}}{200}\right) \times \text{Jitter}$$

## Exception
- 센서 신호 유실 시 "유저님의 페이스를 차분히 기다리고 있어요. 천천히 호흡을 유지해주세요!" 메시지와 함께 안전 모드로 전환한다.

## Related Documents
- `01_ARCHITECTURE/SPIRIT_EVOLUTION_SPEC.md`
- `01_ARCHITECTURE/RECOVERY_SLEEP_SPEC.md`

## Change History
- 2026-07-31 (PATCH_014): AI 오디오 코칭 & 정령 음성 가이드 시스템 명세 신규 작성 (SSOT 규격 준수).