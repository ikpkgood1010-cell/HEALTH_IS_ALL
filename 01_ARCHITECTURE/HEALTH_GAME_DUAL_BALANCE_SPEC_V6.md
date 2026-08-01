# HEALTH IS ALL - 건강 & 게임 듀얼 밸런스 사양서 V6
**File Path**: `HEALTH IS ALL/01_ARCHITECTURE/HEALTH_GAME_DUAL_BALANCE_SPEC_V6.md`  
**Status**: APPROVED  
**Version**: 6.0.0  

---

## 1. Purpose
본 문서는 'HEALTH IS ALL' 플랫폼 내에서 **건강 기능(운동, 식단, 수면, HRV)**과 **게임 요소(정령 성장, 퀘스트, 아이템 획득)**가 어느 한쪽으로 치우치지 않고 동등한 최고 품질(Dual-Peak Quality)을 유지하도록 규정한다. 사용자가 매번 동일한 결과값에 지루함을 느끼지 않도록 다변수 동적 계산 공식을 제공하고, 계산 오류 시 시스템 안정성을 보장하는 Fallback 연산 체계를 구축하는 것을 목적으로 한다.

---

## 2. Scope
1. 동적 칼로리-경험치(EXP) 및 정령 친밀도 연산 엔진
2. 다변수 작용 계산식 및 2단계 간결 공식 Fallback 매커니즘
3. 실시간 1~3줄 건강/식단 꿀팁 피더 및 사용자 친화적 알림/팝업 UX 흐름
4. 프론트엔드/백엔드/AI 엔진 간 듀얼 밸런스 동기화 인터페이스

---

## 3. SSOT (Single Source of Truth)
* **건강 데이터 연산 규칙**: `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v12.py`
* **영양 및 정령 촉매 연산**: `HEALTH IS ALL/03_BACKEND/diet_spirit_engine_v10.py`
* **동적 수식 등록소**: `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md`
* **AI 팁 피더 명세**: `HEALTH IS ALL/05_AI/HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V2.md`

---

## 4. Definitions
* **Dual-Peak Balance**: 게임성(재미, 보상)과 건강성(정확한 웰니스 케어)이 1:1 비중으로 결합되어, 사용자가 건강 케어를 게임 플레이 자체로 인식하게 만드는 밸런스 상태.
* **Dynamic Multi-Variable Formula**: 시간대(Circadian Index), 수면 품질(Recovery Factor), 누적 피로도, 식단 영양 시너지 등 5개 이상의 변수가 결합되어 매번 다른 보상 수치를 산출하는 계산 방식.
* **Fallback Calculation Mode**: 다변수 연산 과정에서 데이터 누락이나 연산 에러 감지 시, 앱 중단 없이 1단계 간결 수식으로 즉시 전환하여 연산을 완수하는 안정성 보호 모드.
* **Micro Tip Feeder**: 식단/운동 기록 완료 시 즉시 팝업되는 1~3줄 분량의 호감형 웰니스 팁 및 게임 재화 동시 지급 시스템.

---

## 5. Runtime
* **Execution Trigger**: 
  1. 센서 데이터 동기화 완료 시 (애플 헬스케어 / 구글 핏 / 웨어러블)
  2. 사용자의 식단 기록 및 운동 일지 제출 완료 시
  3. AI 건강 코치 대화 및 꿀팁 요청 이벤트 발생 시
* **Performance Budget**: 동적 다변수 연산 및 Fallback 판정 포함 50ms 이내 처리 완료.

---

## 6. Rules

### 규칙 1: 게임성과 건강성의 동등한 품질 유지 (Dual-Peak Rule)
* 앱 화면 및 팝업 구성 시 직관적인 게임 그래픽 연출을 제공하되, 사용자의 실제 건강 수치(걸음 수, 칼로리, 영양성분)가 시각적으로 흐려지거나 경시되지 않아야 한다.
* 보상 팝업에는 "운동 성과"와 "정령의 반응/성장"이 동시에 명확히 표현되어야 한다.

### 규칙 2: 다변수 동적 계산식 적용
* **경험치(EXP) 및 정령 스탯 증가 연산 공식**:
  $$EXP_{final} = EXP_{base} \times \left(1 + \frac{HeartRate_{avg}}{HeartRate_{max}}\right) \times Factor_{circadian} \times Synergy_{nutritive}$$
  * $Factor_{circadian}$: 생체시계 매칭 지수 ($0.9 \sim 1.25$)
  * $Synergy_{nutritive}$: 영양 섭취 균형도 시너지 ($0.85 \sim 1.30$)

### 규칙 3: 계산 충돌 및 예외 발생 시 2단계 Fallback 전환
* 다변수 파라미터 중 `None` 값 또는 산술 연산 오류(Division by Zero 등) 감지 시, 0.001초 이내에 1단계 간결 공식으로 자동 전환한다.
* **1단계 간결 공식 (Fallback)**:
  $$EXP_{fallback} = EXP_{base} \times 1.0$$

### 규칙 4: 1~3줄 맞춤형 건강 꿀팁 및 호감형 인터페이스 제공
* 건강 데이터 기록 완료 직후 사용자에게 호감형 문구로 구성된 1~3줄 건강 팁과 함께 micro-reward(정령 스낵, 영혼 조각)를 제공한다.

---

## 7. State
| State Name | Type | Description |
| :--- | :--- | :--- |
| `CALCULATION_MODE` | `Enum` | `DYNAMIC_MULTI` (다변수 모드) \| `FALLBACK_SIMPLE` (간결 모드) |
| `SPIRIT_HARMONY_RATIO` | `Float` | 건강 성과 대비 정령 친밀도 밸런스 비율 ($0.0 \sim 1.0$) |
| `MICRO_TIP_QUEUE` | `List<String>` | 사용자 상태에 따라 대기 중인 1~3줄 꿀팁 리스트 |
| `HEALTH_GAME_SYNC_STATUS`| `Enum` | `SYNCED` \| `PENDING` \| `ERROR_RECOVERED` |

---

## 8. Event
```json
{
  "event_id": "EVT_DUAL_BALANCE_CALCULATED_V6",
  "timestamp": "2026-07-31T20:40:28Z",
  "user_id": "USR_994812",
  "payload": {
    "calculation_mode": "DYNAMIC_MULTI",
    "health_input": {
      "steps": 8500,
      "burned_kcal": 420.5,
      "avg_hr": 135
    },
    "game_output": {
      "exp_gained": 630,
      "spirit_affinity_delta": +12,
      "snack_reward_count": 2
    },
    "health_tip": {
      "lines_count": 2,
      "message": "단백질 섭취 후 30분 내 가벼운 산책은 근육 합성률을 15% 높여줘요! 정령도 함께 기운을 얻었습니다."
    }
  }
}
```

---

## 9. Example

### 정상 실행 예시 (다변수 연산 모드)
1. **사용자 행동**: 저녁 7시 산책 완료 (8,500보, 평균 심박수 135bpm, 단백질 식단 기록 완료).
2. **시스템 연산**: 
   * 생체시계 지수 $1.15$ + 영양 시너지 $1.20$ 적용.
   * 최종 보상: $EXP = 400 \times 1.15 \times 1.20 = 552\,EXP$.
3. **UI/UX 반응**: 호감형 팝업 렌더링.
   > 🌿 **정령의 메시지**:  
   > "우와! 저녁 산책 덕분에 저도 기운이 쑥쑥 나요!  
   > **꿀팁**: 식사 후 30분 뒤 산책은 혈당 피크를 막는 최고의 비밀무기랍니다!"  
   > **보상**: +552 EXP / 정령 친밀도 +12 상승!

---

## 10. Exception
```json
{
  "exception_code": "EX_CALC_PARAM_MISSING",
  "severity": "WARNING",
  "message": "생체시계 지수 연산 중 수면 데이터 누락 감지. Fallback 모드로 즉시 전환합니다.",
  "fallback_action": {
    "mode_switched_to": "FALLBACK_SIMPLE",
    "applied_formula": "EXP_base * 1.0",
    "user_notification": "기본 건강 보상이 안전하게 지급되었습니다!"
  }
}
```

---

## 11. Related Documents
* `HEALTH IS ALL/00_PROJECT_START/DEVELOPMENT_ROADMAP_V9.md`
* `HEALTH IS ALL/01_ARCHITECTURE/UNIFIED_ENGINE_V11_SPEC.md`
* `HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V8.md`
* `HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v12.py`
* `HEALTH IS ALL/05_AI/HEALTH_DYNAMIC_TIP_FEEDER_SPEC_V2.md`
* `HEALTH IS ALL/10_ARCHIVE/HEALTH_GAME_DUAL_BALANCE_SPEC_V5.md`

---

## 12. Change History
| Version | Date | Author | Description |
| :--- | :--- | :--- | :--- |
| 1.0.0 | 2026-01-10 | Dev Team | 최초 듀얼 밸런스 기초 사양 제정 |
| 5.0.0 | 2026-03-15 | Dev Team | V5 엔진 연동 및 퀘스트 밸런스 개선 |
| **6.0.0** | **2026-07-31** | **Gemini** | **다변수 동적 연산 공식 도입, 2단계 Fallback 모드 구축, 1~3줄 꿀팁 피더 실시간 연동 명세 반영 (V6 업그레이드)** |
```

여기까지 복사