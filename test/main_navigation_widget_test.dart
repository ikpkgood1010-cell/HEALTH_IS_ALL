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
        if (request.url.path == '/api/v1/game/adventures/settle') {
          return http.Response(
            '{"adventure_id":"adv-test","user_id":"anon_test",'
            '"window_start":"2026-08-10T00:00:00",'
            '"window_end":"2026-08-10T12:00:00","vitality":40,'
            '"gross_guild_coins":28,"offline_efficiency":0.7,'
            '"hbi_score":52.5,"tower_floor":4,"rooms":['
            '{"position":1,"room_type":"COMBAT","title":"안개 길목",'
            '"outcome":"활력으로 길을 열었어요."},'
            '{"position":2,"room_type":"EVENT","title":"반짝이는 샘",'
            '"outcome":"작은 발견을 했어요."},'
            '{"position":3,"room_type":"ELITE","title":"수호자의 문",'
            '"outcome":"관문을 넘었어요."},'
            '{"position":4,"room_type":"REST","title":"회복의 모닥불",'
            '"outcome":"숨을 골랐어요."},'
            '{"position":5,"room_type":"BOSS","title":"층의 수호자",'
            '"outcome":"모험을 마쳤어요."}],"claimed":false}',
            200,
            headers: {'content-type': 'application/json; charset=utf-8'},
          );
        }
        if (request.url.path.contains('/facilities/training-grounds/')) {
          return http.Response(
            '{"code":"TRAINING_GROUNDS","name":"훈련장","level":2,'
            '"total_invested":120,"current_level_progress":20,'
            '"next_level_cost":150,"progress_ratio":0.1333,'
            '"guild_coin_balance":80,"description":"기초 시설"}',
            200,
            headers: {'content-type': 'application/json; charset=utf-8'},
          );
        }
        if (request.url.path.endsWith('/claim')) {
          return http.Response(
            '{"adventure_id":"adv-test","claim_id":"claim-test",'
            '"already_claimed":false,"gross_guild_coins":28,'
            '"facility_invested":5,"guild_coins_received":23}',
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

  testWidgets('길드 탭에서 자동 모험과 훈련장을 표시하고 보상을 받는다', (tester) async {
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pump();

    await tester.tap(find.text('길드'));
    await tester.pumpAndSettle();

    expect(find.text('자동 모험'), findsOneWidget);
    expect(find.text('모험대가 돌아왔어요'), findsOneWidget);
    expect(find.text('탑 4층 탐험 경로'), findsOneWidget);
    expect(find.text('1. 안개 길목'), findsOneWidget);
    expect(find.text('5. 층의 수호자'), findsOneWidget);

    await tester.ensureVisible(find.text('안전하게 보상 받기'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('안전하게 보상 받기'));
    await tester.pumpAndSettle();
    expect(find.text('보상을 받았어요'), findsOneWidget);

    await tester.ensureVisible(find.text('길드 시설'));
    await tester.pumpAndSettle();
    expect(find.text('길드 시설'), findsOneWidget);
    expect(find.text('훈련장'), findsOneWidget);
  });
}
