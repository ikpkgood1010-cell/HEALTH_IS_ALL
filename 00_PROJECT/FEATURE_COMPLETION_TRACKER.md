# FEATURE_COMPLETION_TRACKER

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: 기능 단위 구현률과 병목 구간을 추적한다.

| Feature | UI | Backend | AI | Test | Done | Notes |
|---|---|---|---|---|---|---|
| 건강 기록 입력 | Yes | Yes | N/A | Yes | Yes | API + 단위/통합 테스트 확인 |
| Exp 지급 / cap / anti-farming | Partial | Yes | N/A | Yes | Yes | active code는 정리 완료, legacy 문서 드리프트 잔존 |
| 건강이 상태 조회 | Yes | Yes | Yes | Yes | Yes | `/api/v1/health-i/status/{user_id}` 검증 완료 |
| 일일 퀘스트 | Yes | Yes | N/A | Partial | Partial | UI 자동 테스트 없음 |
| 상점 / 스킨 | Yes | Partial | N/A | No | Partial | 메모리성 UI, 영속화 미구현 |
| 식단 기록 화면 | Yes | Partial | N/A | No | Partial | 메인 진입점 미연결 |
| 운동 기록 화면 | Yes | Partial | N/A | No | Partial | 메인 진입점 미연결 |
| 감정/대사 피드백 | Yes | Partial | Yes | Partial | Partial | 별도 emotion engine 없이 서비스 로직 내장 |
| 오프라인 동기화 | No | Partial | N/A | No | No | 엔진 파일만 확인 |
| 웨어러블 연동 | No | Partial | N/A | No | No | 엔진/위젯 후보만 존재 |
| 월간 리포트 | Partial | Partial | Partial | No | No | 컴포넌트와 엔진은 있으나 미연결 |
| 메모리/앨범 | Partial | Partial | Partial | No | No | F-004와 구현 연결 필요 |
| 소셜 길드/레이드 | Partial | Partial | N/A | No | No | 범위 재평가 필요 |

## Bottlenecks
1. UI 연결되지 않은 화면이 많다.
2. 이벤트/스케줄러 계층의 명시적 구현 부족.
3. 영속화/상점/포인트 경제는 화면 대비 백엔드 계약이 부족하다.
