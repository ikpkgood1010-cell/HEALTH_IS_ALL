# PERFORMANCE_BUDGET

## Purpose
본 문서는 '헬스 이스 올' 앱의 프론트엔드(Flutter) 및 API 통신 시 쾌적한 UX와 게이밍 애니메이션을 보장하기 위한 성능 예산(Performance Budget)과 허용 한계선을 규정하는 SSOT이다.

## Scope
Flutter 앱 렌더링 Engine, 네트워크 통신, 메모리, 배터리 및 AI 응답 지연 시간 제어에 적용된다.

## SSOT
모바일 클라이언트 성능 측정 항목 및 한계 초과 시 대응 방안의 단일 진실 출처이다.

## Performance Budget Specifications

| Metric Category | Target Value | Hard Limit (Alert) | Mitigation Strategy on Breach |
| :--- | :--- | :--- | :--- |
| **App Cold Start** | $< 1.2\text{sec}$ | $> 2.0\text{sec}$ | 스플래시 화면 초기화 비동기 지연 로딩 |
| **Screen Transition**| 60 FPS ($16.6\text{ms}$) | $< 45\text{FPS}$ | UI 위젯 Tree Rebuild 범위 축소 |
| **API Response (p95)**| $< 300\text{ms}$ | $> 800\text{ms}$ | Read Model Redis 캐시 우선 전환 |
| **AI Vision Response**| $< 2.0\text{sec}$ | $> 4.0\text{sec}$ | UI 쾌속 Skelaton Animation 적용 |
| **App RAM Usage** | $< 180\text{MB}$ | $> 300\text{MB}$ | 이미지 메모리 캐시 및 Rive 애니메이션 Unload |
| **Asset Image Size** | WebP / $< 200\text{KB}$ | $> 500\text{KB}$ | 압축 파이프라인 자동 적용 |

## Performance Throttling Formula
화면 프레임 드랍 발생 시 Companion 애니메이션 품질 자동 조정 수식:
$$\text{TargetFPS} = \begin{cases} 60 & \text{if } \text{AvailableRAM} > 100\text{MB} \text{ and } \text{Battery} > 20\% \\ 30 & \text{otherwise (Quality Reduced)} \end{cases}$$

## Runtime Impact
- 저사양 기기에서도 앱 튕김(OOM)이나 버벅임 없이 유려한 60 FPS 건강이(Companion) 게이밍 경험을 제공한다.

## Related Documents
- `00_PROJECT/RELEASE_READINESS_CHECKLIST.md`
- `06_QA/QA_TEST_STRATEGY.md`

## Change History
- v1.0.0 (2026-07-31): Performance Budget established.