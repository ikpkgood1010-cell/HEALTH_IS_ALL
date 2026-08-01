# RELEASE_READINESS_CHECKLIST

## Purpose
본 문서는 '헬스 이스 올' 앱의 신규 버전 배포 시 각 단계(MVP, Beta, Production)별 필수 승인 조건을 검증하고, 스토어 출시 및 서비스 안정성을 확보하기 위한 단일 진실 출처(SSOT) 체크리스트이다.

## Scope
iOS App Store 및 Google Play Store 배포 전 과정, Backend API, AI Prompt, Formula 엔지니어링 및 인프라 검증에 적용된다.

## SSOT
배포 가능 여부(Go / No-Go) 판정을 위한 품질 게이트 기준의 단일 진실 출처이다.

## Gate 1: MVP Release Criteria (최소 기능 제품)
- [ ] 핵심 건강 기록 기능(운동, 식단, 습관) 정상 작동 및 Hive/RDB 동기화 검증
- [ ] 건강이(Companion) 캐릭터 기본 렌더링 및 상태(기쁨/피로/배고픔) 피드백 작동
- [ ] Formula 계산 엔진 유닛 테스트 커버리지 $> 85\%$ 달성
- [ ] API 핵심 엔드포인트 응답 속도 $p_{95} < 500\text{ms}$ 충족
- [ ] App Crash Free User Rate $> 98.0\%$ 확보

## Gate 2: Beta Release Criteria (오픈/클로즈드 베타)
- [ ] AI 비전 식단 분석 및 텍스트 프롬프트 응답 시 환각(Hallucination)률 $< 3\%$ 검증
- [ ] Transactional Outbox 및 이벤트 프로젝션 지연 시간 $< 1.0\text{sec}$ 유지
- [ ] Analytics 이벤트 발송 무결성 및 PII 필터링 검증 완료
- [ ] iOS/Android 백그라운드 퍼미션(건강 데이터 API, 푸시 알림) 동의 흐름 정상화
- [ ] App Crash Free User Rate $> 99.0\%$ 확보

## Gate 3: Production Release Criteria (상용 상용화)
- [ ] **Security & Privacy**: 개인정보보호 영향평가 완료 및 PII 암호화/익명화 검증 (`PRIVACY_DATA_POLICY.md` 준수)
- [ ] **Performance Budget**: 앱 Cold Start $< 1.5\text{sec}$, 화면 전환 60 FPS 유지 (`PERFORMANCE_BUDGET.md` 충족)
- [ ] **Observability**: Trace ID 기반 로깅 및 P0/P1 Alert 모니터링 시스템 작동 확인
- [ ] **DR & Backup**: DB 및 S3 백업 자동화 및 RTO/RPO 모의 복구 훈련 통과
- [ ] **Accessibility & i18n**: 스크린 리더(TalkBack/VoiceOver) 기본 지원 및 다국어 리소스 검증
- [ ] App Crash Free User Rate $> 99.8\%$ 확보

## Store Submission Verification Table

| Check Category | Item | Verification Method | Responsible Role | Pass Threshold |
| :--- | :--- | :--- | :--- | :--- |
| **App Store** | Human Interface Guidelines | UI/UX Audit | FE Lead | Checklist Pass |
| **Play Store** | Target SDK & Privacy Policy | Google Play Console | DevOps | Compliance 100% |
| **AI Safety** | Prompt Injection Defense | Automated QA Test | AI Engineer | Block Rate 100% |
| **Database** | Zero-Downtime Migration | Flyway Dry-Run Test | BE Lead | Zero Data Loss |

## Runtime Impact
- 미검증 배포로 인한 앱 튕김, 데이터 유실, 개인정보 유출 및 스토어 거절(Rejection) 리스크가 원천 차단된다.

## Related Documents
- `06_QA/QA_TEST_STRATEGY.md`
- `03_BACKEND/SECURITY_POLICY.md`
- `03_BACKEND/PRIVACY_DATA_POLICY.md`

## Change History
- v1.0.0 (2026-07-31): Initial Release Readiness Checklist established.