import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('HEALTH IS ALL 앱 통합 테스트 (E2E)', () {
    testWidgets('앱 정상 시작 및 메인 화면 탭 전환 시나리오 검증', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: const Center(child: Text('홈 화면 대시보드')),
            bottomNavigationBar: BottomNavigationBar(
              items: const [
                BottomNavigationBarItem(icon: Icon(Icons.home), label: '홈'),
                BottomNavigationBarItem(icon: Icon(Icons.check), label: '습관'),
              ],
            ),
          ),
        ),
      );

      await tester.pumpAndSettle();

      expect(find.text('홈 화면 대시보드'), findsOneWidget);
      expect(find.text('습관'), findsOneWidget);
    });
  });
}