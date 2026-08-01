Flutter Architecture Setup (클라이언트 아키텍처 및 상태 관리 명세)

1. 개요
본 문서는 HEALTH IS ALL Flutter 애플리케이션의 클라이언트 아키텍처, 디렉토리 구조, 상태 관리(Riverpod/Bloc) 표준, 오프라인 퍼스트(Offline-First) 캐싱 전략을 정의합니다. 본 명세는 유지보수성과 확장성을 극대화하기 위해 Feature-First + Clean Architecture 레이어링 원칙을 준수합니다.

───

2. 디렉토리 구조 (Feature-First Directory Structure)

모든 코드 모듈은 도메인 기능(Feature) 단위로 격리되며, 공통 재사용 요소는 core 모듈에 위치합니다.

text
lib/
├── app/                        # 앱 진입점, 라우팅, 테마 설정
│   ├── app.dart
│   ├── router/                 # GoRouter 설정 및 Auth Guard
│   └── theme/                  # Component Catalog 기반 디자인 토큰
├── core/                       # 공통 모빌리티 및 모듈
│   ├── constants/              # Master Canonical Glossary 기반 상수
│   ├── network/                # Dio Client, Interceptors, Idempotency Header
│   ├── storage/                # Hive Local DB Storage & Cache
│   ├── utils/                  # DateFormatter, CalorieCalculator
│   └── widgets/                # Component Catalog 기반 공통 UI
└── features/                   # 기능 단위 모듈 (Feature-First)
    ├── home/
    │   ├── data/               # Repositories & ReadModel Data Sources
    │   ├── domain/             # Entities, UseCases
    │   └── presentation/       # Screens, Widgets, State Notifiers
    ├── exercise/
    ├── meal/
    ├── spirit/
    └── progression/