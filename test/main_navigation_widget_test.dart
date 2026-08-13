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
        return http.Response('{}', 404);
      }),
    );

    return riverpod.ProviderScope(
      child: ChangeNotifierProvider(
        create: (_) => ApiDataProvider(
          userId: 'anon_test',
          apiClient: apiClient,
        ),
        child: const MaterialApp(home: MainNavigationScreen()),
      ),
    );
  }

  testWidgets('건강 앱 하단 탭 4개를 순서대로 표시한다', (tester) async {
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pumpAndSettle();

    for (final label in ['홈', '운동', '식단', '마이']) {
      expect(
        find.descendant(
          of: find.byType(NavigationBar),
          matching: find.text(label),
        ),
        findsOneWidget,
      );
    }
    expect(find.text('길드'), findsNothing);
    expect(find.byType(NavigationDestination), findsNWidgets(4));
  });

  testWidgets('홈 상단에서 게임에 입장하고 환생 보존 규칙을 확인한다', (tester) async {
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('home-game-entry')), findsOneWidget);
    await tester.tap(find.text('게임으로 입장'));
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('game-hub')), findsOneWidget);
    expect(find.text('나의 6인 파티'), findsOneWidget);
    expect(find.text('탱커'), findsOneWidget);
    expect(find.text('치유사'), findsOneWidget);
    expect(find.text('마을·길드'), findsOneWidget);

    await tester.drag(
      find.byKey(const Key('game-hub')),
      const Offset(0, -1000),
    );
    await tester.pumpAndSettle();
    await tester.tap(find.text('환생').first);
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('rebirth-rules')), findsOneWidget);
    expect(find.text('회차마다 초기화'), findsOneWidget);
    await tester.drag(
      find.byKey(const Key('rebirth-rules')),
      const Offset(0, -400),
    );
    await tester.pumpAndSettle();
    expect(find.textContaining('소형·중형 노드'), findsOneWidget);
    expect(find.text('영구 보존'), findsOneWidget);
    expect(find.textContaining('최고 전직 차수와 전직 외형'), findsOneWidget);
  });
}
