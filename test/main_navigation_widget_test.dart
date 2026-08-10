import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart' as riverpod;
import 'package:flutter_test/flutter_test.dart';
import 'package:health_is_all/api_client.dart';
import 'package:health_is_all/api_data_provider.dart';
import 'package:health_is_all/main_navigation_screen.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:provider/provider.dart';

void main() {
  Widget createWidgetUnderTest() {
    final apiClient = HealthIApiClient(
      client: MockClient((request) async {
        if (request.url.path.contains('/health-i/status/')) {
          return http.Response(
            '{"name":"건강이","level":1,"current_exp":0,'
            '"daily_exp_cap":300,"emotion_state":"평온함",'
            '"dialogue":"오늘도 천천히 시작해요.",'
            '"equipped_skin":"default_skin",'
            '"last_updated":"2026-08-10T00:00:00",'
            '"today_consumed_calories":0,'
            '"today_workout_minutes":0,"today_water_liters":0,'
            '"streak_days":0}',
            200,
            headers: {'content-type': 'application/json; charset=utf-8'},
          );
        }
        return http.Response('{}', 200);
      }),
    );

    return riverpod.ProviderScope(
      child: ChangeNotifierProvider(
        create: (_) =>
            ApiDataProvider(userId: 'anon_test', apiClient: apiClient),
        child: const MaterialApp(home: MainNavigationScreen()),
      ),
    );
  }

  testWidgets('확정된 하단 탭 5개를 순서대로 표시한다', (tester) async {
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pump();

    for (final label in ['홈', '운동', '식단', '길드', '마이']) {
      expect(
        find.descendant(
          of: find.byType(NavigationBar),
          matching: find.text(label),
        ),
        findsOneWidget,
      );
    }
    expect(find.byType(NavigationDestination), findsNWidgets(5));
  });

  testWidgets('길드 탭에서 건강 기반 길드 화면을 표시한다', (tester) async {
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pump();

    await tester.tap(find.text('길드'));
    await tester.pumpAndSettle();

    expect(find.text('오늘의 건강이 만든 변화'), findsOneWidget);
    await tester.scrollUntilVisible(
      find.text('자동 모험 규칙'),
      300,
      scrollable: find.byType(Scrollable).first,
    );
    expect(find.text('자동 모험 규칙'), findsOneWidget);
  });
}
