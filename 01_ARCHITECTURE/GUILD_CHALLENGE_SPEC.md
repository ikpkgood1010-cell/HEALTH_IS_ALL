# GUILD_CHALLENGE_SPEC.md

## Purpose
본 문서는 개인의 건강 습관 형성을 넘어 길드원 간의 유기적 협동을 통해 함께 목표를 달성하고, 길드 수호 정령을 거대 진화시키는 소셜 길드 챌린지 엔진의 기술 요구사항 및 보상 공식을 정의한다.

## Scope
1. 길드원 일일 누적 걸음 수 및 영양 균형 점수 합산 알고리즘
2. 개인별 길드 기여도($Contribution Score$) 및 연속 달성 가중치 산출
3. 길드 수호 정령의 4단계 거대 진화(Baby Guard, Sky Warden, Cosmic Aegis, Immortal Spirit) 트리를 연동
4. 경쟁 유발 억제 및 상호 응원을 유도하는 호감형 길드 메시지 인터페이스
5. 네트워크 단절 시 개인 기여 데이터를 로컬에 보존하고 복구 시 합산하는 Fallback 로직

## SSOT
본 문서는 길드 챌린지 백엔드 엔진(`backend/guild_challenge_engine.py`) 및 프론트엔드 길드 위젯(`lib/guild_challenge_widget.dart`)의 최상위 **SSOT(Single Source of Truth)**로 기능한다.

## Definitions
- **Guild Contribution Score ($GCS$)**: 개인의 걸음 수, 영양 기록, 정령 친밀도가 결합되어 길드 전체 목표에 기여하는 종합 점수.
- **Guardian Spirit Stage**: 길드원 전체의 누적 경험치에 따라 진화하는 공동 정령 단계.

## Runtime
- 프론트엔드(Flutter): 길드 목표 달성 프로그레스 바, 거대 정령 진화 애니메이션, 응원 팝업 출력.
- 백엔드(FastAPI/Python): 길드원 활동 데이터 실시간 집계, 기여도 계산, 일일 획득 골드 및 칭호 부여.

## Rules
1. **건강 중심 본위 원칙**: 과도한 무리나 경쟁을 방지하기 위해 일일 개인 기여 걸음 수 상한선(15,000보)을 설정하여 유저의 근골격계 안전을 보호한다.
2. **따뜻한 협동 문구**: 목표 미달 시 질책 대신 "오늘 길드원들과 함께 모은 발걸음이 정령에게 따스한 온기를 전했습니다 🌿"와 같은 격려 중심 대화를 사용한다.
3. **세분화 동적 수식**: 개인 걸음 수, 영양 밸런스 지수, 연속 참여일(Streak) 및 $0.96 \sim 1.04$ 범위의 미세 난수 지터를 조합하여 보상을 다변화한다.

## State
- `guild_total_exp`, `guild_guardian_stage`
- `member_count`, `daily_guild_target_steps`
- `personal_contribution_score`, `member_streak`

## Event
- `ON_MEMBER_ACTIVITY_LOGGED`: 길드원의 걸음 수/영양 기록 추가 시 길드 경험치 반영
- `ON_GUILD_STAGE_UPGRADED`: 길드 수호 정령의 다음 단계 진화 이벤트 트리거
- `ON_CHEER_POPUP_SEND`: 길드원 간 칭찬 및 응원 메시지 전송

## Example
$$GCS = \left( \frac{\text{UserSteps}}{1000} \times 15 + \text{NutriBalanceScore} \times 0.8 \right) \times (1.0 + \text{Streak} \times 0.02) \times \text{Jitter}$$

## Exception
- 길드원이 1명인 solo 길드의 경우, 자동 AI 서포터 정령이 가상의 기여도를 보조 제공하여 혼자서도 챌린지를 즐길 수 있도록 지원한다.

## Related Documents
- `01_ARCHITECTURE/SPIRIT_EVOLUTION_SPEC.md`
- `01_ARCHITECTURE/NUTRITION_QUEST_SPEC.md`

## Change History
- 2026-07-31 (PATCH_015): 소셜 길드 챌린지 & 정령 거대진화 시스템 명세 신규 작성 (SSOT 규격 준수).