Component Catalog (공통 UI 컴포넌트 및 디자인 토큰 명세)

1. 개요
본 문서는 HEALTH IS ALL 애플리케이션의 일관된 UI/UX 제공을 위한 단일 디자인 시스템 및 컴포넌트 카탈로그(Single Source of Truth) 입니다. 모든 Flutter UI 화면은 본 명세서에 정의된 디자인 토큰 및 재사용 컴포넌트를 사용해야 하며, 화면별로 중복된 스타일 정의를 금지합니다.

───

2. 디자인 토큰 (Design Tokens)

2.1. 컬러 팔레트 (Color Palette)
• Health First & Positive Psychology를 바탕으로 눈의 피로도를 낮추고 긍정적 에너지를 주는 컬러 스키마를 채택합니다.


토큰명 (Token)
Hex Code
용도 / 사용처

primary-500
#2ECC71
주 액션 버튼, 달성 상태, 정령 성장 메인 컬러

primary-100
#E8F8F5
주 액션 버튼 배경, 하이라이트 카드의 기본 틴트

secondary-500
#3498DB
운동 기록, 수분 섭취, 신체 상태 지표

accent-energy
#F1C40F
Spirit Energy, XP 게이지, 보상 획득 연출

neutral-900
#2C3E50
메인 텍스트, 타이틀, 중요 다이얼로그 텍스트

neutral-500
#7F8C8D
서브 텍스트, 비활성 아이콘, 캡션

neutral-100
#F8F9FA
전체 화면 배경, 일반 카드 배경

status-error
#E74C3C
네트워크 재시도, 필수 입력 누락 (경고성 메시지 지양)



2.2. 타이포그래피 (Typography)
• 기본 폰트: Pretendard (Flutter pubspec.yaml 기본 적용)


토큰명
Font Size
Weight
Line Height
사용처

display-lg
28px
Bold (700)
1.3
홈 화면 대형 정령 대사, 레벨업 팝업

title-md
20px
SemiBold (600)
1.4
섹션 타이틀, 카드 헤더, 다이얼로그 제목

body-md
16px
Regular (400)
1.5
본문, 습관 리스트 텍스트, 설명글

caption-sm
12px
Medium (500)
1.4
타임스탬프, 단위 지표(kcal, kg, min)



2.3. 레이아웃 & 스페이싱 (Spacing & Radius)
• 기본 격자 단위: 8pt Grid System
• space-xs: 4px | space-sm: 8px | space-md: 16px | space-lg: 24px | space-xl: 32px
• radius-sm: 8px (버튼, 태그) | radius-md: 16px (일반 카드, 다이얼로그) | radius-full: 999px (아바타, 칩)

───

3. 핵심 공통 컴포넌트 명세 (Core Component Specs)

3.1. 기본 버튼 (PrimaryActionButton)
• 역할: 화면 내 가장 중요한 단일 액션(저장, 기록 완료, 퀘스트 수령) 수행

text
┌───────────────────────────────────────────────┐
│              기록 완료하기 (+50 XP)            │  <- Height: 52px, Radius: 16px
└───────────────────────────────────────────────┘     Bg: primary-500, Text: white