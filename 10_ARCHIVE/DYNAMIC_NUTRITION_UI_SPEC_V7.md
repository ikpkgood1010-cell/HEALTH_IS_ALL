# DYNAMIC\_NUTRITION\_UI\_SPEC\_V7.md

## Purpose

프론트엔드 모바일 UI에서 건강 수치와 게임 보상이 텍스트 잘림 현상 없이 유저 친화적으로 표현되도록 하는 V7 UX/UI 명세입니다.

## Scope

* 모바일 반응형 영양/운동 메인 화면 카드 레이아웃
* 텍스트 자동 줄바꿈(Soft-Wrap) 및 코드/텍스트 복사 영역 가이드

## SSOT

* UI/UX 레이아웃 규격 및 스타일 가이드의 단일 진실 공급원.

## Definitions

* **Soft-Wrap Container**: 글자 수가 길어져도 모바일 레이아웃 밖으로 자르지 않고 자연스럽게 다음 줄로 넘기는 UI 컨테이너.

## Runtime

* Flutter 3.x UI Rendering Framework.

## Rules

1. 모든 텍스트 영역에는 `TextOverflow.visible` 및 `softWrap: true` 속성을 필수로 부여한다.
2. 건강 기록 완료 시 나타나는 팝업은 긍정적이고 호감을 주는 응원 문구를 최상단에 배치한다.
3. 게임 요소(스피릿 캐릭터)가 건강 수치 그래프를 가리지 않도록 상단 좌측 50%는 건강 수치, 우측 50%는 스피릿 카드로 명확히 분할한다.

## State

* UI States: CARD\_EXPANDED, POPUP\_SHOWING, ANIMATION\_ACTIVE

## Event

* `EVENT\_UI\_NUTRITION\_CARD\_TAPPED`: 영양 카드 터치 시 정밀 분석 팝업 출력.

## Example

```dart
// Flutter 자동 줄바꿈 및 응답형 UI 적용 예시
Widget buildFriendlyHealthCard(String title, String message) {
  return Container(
    padding: const EdgeInsets.all(16.0),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: \[
        Text(
          title,
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        Text(
          message,
          softWrap: true, // 자동 줄바꿈 적용
          style: const TextStyle(fontSize: 14, color: Colors.black87),
        ),
      ],
    ),
  );
}



Exception

화면 해상도 Width < 320dp 극소형 기기인 경우 폰트 크기를 동적으로 12sp로 축소하여 레이아웃 보존.



Related Documents

HEALTH IS ALL/lib/dynamic\_nutrition\_tracker\_widget.dart

HEALTH IS ALL/05\_AI/HEALTH\_FEEDBACK\_INTELLIGENCE\_SPEC\_V7.md



Change History

날짜 2026-07-31

버전 V7.0.0

작성자 UI/UX Team

변경 내용 V7 반응형 줄바꿈 및 유저 친화 팝업 스타일 지정





