Screen Specification Master (화면 단위 UI 상태 및 인터랙션 명세)

1. 개요
본 문서는 HEALTH IS ALL Flutter 프론트엔드 개발을 위한 마스터 화면 명세서입니다. 단순 디자인 레이아웃을 넘어, 화면별 6대 핵심 상태 Lifecycle(Ready, Loading, Syncing, Offline, Error, Empty)과 이벤트 바인딩 규격을 정의합니다.

───

2. 표준 화면 상태 파이프라인 (UI State Lifecycle)

모든 Flutter 화면 위젯은 아래의 6개 공통 UI State를 일관되게 처리해야 합니다.

text
┌───────────┐
       │   Initial │
       └─────┬─────┘
             │ (Data Fetching)
             ▼
       ┌───────────┐
       │  Loading  ├──────────────────────┐
       └─────┬─────┘                      │
             │ (Success)                  │ (Failure)
             ▼                            ▼
┌─────────────────────────┐     ┌───────────────────┐
│          Ready          │     │       Error       │
└┬───────────┬───────────┬┘     └───────────────────┘
 │           │           │
 │ (No Data) │ (Offline) │ (Background Sync)
 ▼           ▼           ▼
┌───────┐ ┌─────────┐ ┌─────────┐
│ Empty │ │ Offline │ │ Syncing │
└───────┘ └─────────┘ └─────────┘