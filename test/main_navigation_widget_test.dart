import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:health_is_all/main_navigation_screen.dart';

/// NOTE(PATCH-006 검증): 기존 테스트는 MainNavigationScreen을 import하지 않고
/// 하드코딩된 mock BottomNavigationBar를 자체적으로 그려서 검증했습니다.
/// 그 결과 실제 lib/main_navigation_screen.dart의 라벨('건강 홈', '퀘스트', '건강이 상점')이
/// 바뀌거나 깨져도 이 테스트는 항상 통과하는 상태였습니다.
/// 아래는 실제 위젯을 pumpWidget하여 진짜 회귀를 감지하도록 재작성한 버전입니다.
void main() {
  Widget createWidgetUnderTest() {
    return const MaterialApp(
      home: MainNavigationScreen(),
    );
  }

  group('MainNavigation 위젯 테스트 (실제 화면 기준)', () {
    testWidgets('하단 내비게이션 바 항목 3개가 실제 라벨로 렌더링된다', (WidgetTester tester) async {
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      expect(find.text('건강 홈'), findsOneWidget);
      expect(find.text('퀘스트'), findsOneWidget);
      expect(find.text('건강이 상점'), findsOneWidget);
    });

    testWidgets('탭을 누르면 currentIndex가 바뀌고 다른 화면으로 전환된다', (WidgetTester tester) async {
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      await tester.tap(find.text('퀘스트'));
      await tester.pumpAndSettle();

      final navBar = tester.widget<BottomNavigationBar>(find.byType(BottomNavigationBar));
      expect(navBar.currentIndex, 1);
    });
  });
}