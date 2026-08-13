import 'dart:convert';

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
        if (request.url.path == '/api/v1/game/state/initialize') {
          return http.Response(
            '{"initialized":true,"phase":"ONBOARDING",'
            '"user_id":"anon_test","revision":0,"run_number":1,'
            '"tower_floor":1,"highest_floor":1,"room_position":1,'
            '"rooms_per_floor":6,"gold":0,"health_essence":0,'
            '"star_shards":0,"transcendence_points":0,'
            '"initial_hero_selected":false,'
            '"large_node_slots_by_layer":{"0":5,"1":6,"2":6,"3":6,"4":6,"5":6,"6":6},'
            '"heroes":['
            '{"hero_code":"TANKER","role_name":"탱커","recruited":false,"advancement_tier":0,"appearance_code":"BASE","active_skill_slots":0},'
            '{"hero_code":"WARRIOR","role_name":"전사","recruited":false,"advancement_tier":0,"appearance_code":"BASE","active_skill_slots":0},'
            '{"hero_code":"MAGE","role_name":"마법사","recruited":false,"advancement_tier":0,"appearance_code":"BASE","active_skill_slots":0},'
            '{"hero_code":"ARCHER","role_name":"궁수","recruited":false,"advancement_tier":0,"appearance_code":"BASE","active_skill_slots":0},'
            '{"hero_code":"ROGUE","role_name":"도적","recruited":false,"advancement_tier":0,"appearance_code":"BASE","active_skill_slots":0},'
            '{"hero_code":"HEALER","role_name":"치유사","recruited":false,"advancement_tier":0,"appearance_code":"BASE","active_skill_slots":0}],'
            '"node_counts":{"SMALL":0,"MEDIUM":0,"LARGE":0}}',
            200,
            headers: {'content-type': 'application/json; charset=utf-8'},
          );
        }
        if (request.url.path == '/api/v1/game/heroes/select-initial') {
          return http.Response(
            jsonEncode(_selectedGameState()),
            200,
            headers: {'content-type': 'application/json; charset=utf-8'},
          );
        }
        if (request.url.path == '/api/v1/game/battle/settle') {
          final state = _selectedGameState()
            ..['tower_floor'] = 2
            ..['room_position'] = 3
            ..['gold'] = 128
            ..['revision'] = 2;
          return http.Response(
            jsonEncode({
              'settlement_id': 'cccccccc-cccc-4ccc-8ccc-cccccccccccc',
              'already_settled': false,
              'elapsed_seconds': 600,
              'credited_seconds': 600,
              'capped': false,
              'rooms_cleared': 8,
              'bosses_cleared': 1,
              'gold_earned': 128,
              'state': state,
            }),
            200,
            headers: {'content-type': 'application/json; charset=utf-8'},
          );
        }
        if (request.url.path.contains('/api/v1/game/rebirth/preview/')) {
          return http.Response(
            '{"user_id":"anon_test","revision":0,"can_rebirth":false,'
            '"next_run_number":2,"reset":{"tower_floor":1,'
            '"room_position":1,"gold":0,"small_nodes":0,"medium_nodes":0},'
            '"retain":{"heroes":6,"recruited_heroes":0,"large_nodes":0,'
            '"health_essence":0,"star_shards":0,"transcendence_points":0}}',
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
    expect(find.text('첫 용사 영입을 기다리고 있어요'), findsOneWidget);
    expect(find.byKey(const Key('initial-hero-selector')), findsOneWidget);
    await tester.drag(
      find.byKey(const Key('game-hub')),
      const Offset(0, -500),
    );
    await tester.pumpAndSettle();
    expect(find.text('나의 6인 파티'), findsOneWidget);
    expect(find.text('탱커'), findsWidgets);
    expect(find.text('치유사'), findsWidgets);
    await tester.drag(
      find.byKey(const Key('game-hub')),
      const Offset(0, -1000),
    );
    await tester.pumpAndSettle();
    expect(find.text('마을·길드'), findsOneWidget);
    await tester.tap(find.text('환생').first);
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('rebirth-rules')), findsOneWidget);
    expect(find.text('회차마다 초기화'), findsOneWidget);
    await tester.drag(
      find.byKey(const Key('rebirth-rules')),
      const Offset(0, -700),
    );
    await tester.pumpAndSettle();
    expect(find.textContaining('소형 노드 0개'), findsOneWidget);
    expect(find.text('영구 보존'), findsOneWidget);
    expect(find.textContaining('최고 전직 차수·전직 외형'), findsOneWidget);
  });

  testWidgets('첫 용사 1명을 확인 후 무료 영입한다', (tester) async {
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pumpAndSettle();
    await tester.tap(find.text('게임으로 입장'));
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const Key('initial-hero-MAGE')));
    await tester.pumpAndSettle();
    expect(find.text('마법사를 첫 용사로 선택할까요?'), findsOneWidget);
    await tester.tap(find.byKey(const Key('confirm-initial-hero')));
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('initial-hero-selector')), findsNothing);
    expect(find.text('1명의 용사가 다음 적을 향해 이동합니다.'), findsOneWidget);
  });

  testWidgets('승인 배경 위에 0계층 5개와 전직 계층 6개를 표시한다', (tester) async {
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pumpAndSettle();
    await tester.tap(find.text('게임으로 입장'));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('initial-hero-MAGE')));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('confirm-initial-hero')));
    await tester.pumpAndSettle();

    await tester.ensureVisible(find.text('별자리').first);
    await tester.pumpAndSettle();
    await tester.tap(find.text('별자리').first);
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('constellation-board')), findsOneWidget);
    expect(find.byKey(const Key('constellation-node-0-MAGE')), findsNothing);
    for (final code in ['TANKER', 'WARRIOR', 'ARCHER', 'ROGUE', 'HEALER']) {
      expect(find.byKey(Key('constellation-node-0-$code')), findsOneWidget);
    }

    await tester.tap(find.byKey(const Key('constellation-layer-1')));
    await tester.pumpAndSettle();
    for (final code in [
      'TANKER',
      'WARRIOR',
      'MAGE',
      'ARCHER',
      'ROGUE',
      'HEALER'
    ]) {
      expect(find.byKey(Key('constellation-node-1-$code')), findsOneWidget);
    }
    expect(find.text('무료 첫 용사 · 마법사'), findsOneWidget);
  });

  testWidgets('자동 전투 진입 시 서버 정산 결과와 현재 방을 표시한다', (tester) async {
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pumpAndSettle();
    await tester.tap(find.text('게임으로 입장'));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('initial-hero-MAGE')));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('confirm-initial-hero')));
    await tester.pumpAndSettle();

    await tester.tap(find.text('전투 화면 보기'));
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('idle-battle-runtime')), findsOneWidget);
    expect(find.text('2층 · 3번 방'), findsOneWidget);
    expect(find.byKey(const Key('battle-settlement-summary')), findsOneWidget);
    expect(find.textContaining('방 8개'), findsOneWidget);
    expect(find.textContaining('골드 +128'), findsOneWidget);
  });
}

Map<String, dynamic> _selectedGameState() {
  const roles = [
    ('TANKER', '탱커'),
    ('WARRIOR', '전사'),
    ('MAGE', '마법사'),
    ('ARCHER', '궁수'),
    ('ROGUE', '도적'),
    ('HEALER', '치유사'),
  ];
  Map<String, dynamic> node((String, String) role, int layer) => {
        'node_code': layer == 0
            ? 'L0_RECRUIT_${role.$1}'
            : 'L${layer}_ADVANCE_${role.$1}',
        'layer': layer,
        'hero_code': role.$1,
        'role_name': role.$2,
        'node_kind': layer == 0 ? 'RECRUIT' : 'ADVANCEMENT',
        'state': layer == 1 && role.$1 == 'MAGE' ? 'NEXT' : 'LOCKED',
        'advancement_tier': 0,
      };
  return {
    'initialized': true,
    'phase': 'IDLE_BATTLE',
    'user_id': 'anon_test',
    'revision': 1,
    'run_number': 1,
    'tower_floor': 1,
    'highest_floor': 1,
    'room_position': 1,
    'rooms_per_floor': 6,
    'gold': 0,
    'battle': {
      'status': 'RUNNING',
      'server_anchor_at': '2026-08-14T00:10:00Z',
      'offline_cap_seconds': 43200,
      'party_power': 100,
      'current_room_kind': 'NORMAL',
      'room_progress_seconds': 15,
      'room_required_seconds': 45,
    },
    'health_essence': 0,
    'star_shards': 0,
    'transcendence_points': 0,
    'initial_hero_selected': true,
    'starter_hero_code': 'MAGE',
    'large_node_slots_by_layer': {
      '0': 5,
      for (var layer = 1; layer <= 6; layer++) '$layer': 6,
    },
    'constellation_layers': [
      {
        'layer': 0,
        'title': '용사 영입',
        'node_count': 5,
        'nodes': [
          for (final role in roles.where((role) => role.$1 != 'MAGE'))
            node(role, 0)
        ],
      },
      for (var layer = 1; layer <= 6; layer++)
        {
          'layer': layer,
          'title': '$layer차 전직',
          'node_count': 6,
          'nodes': [for (final role in roles) node(role, layer)],
        },
    ],
    'heroes': [
      for (final role in roles)
        {
          'hero_code': role.$1,
          'role_name': role.$2,
          'recruited': role.$1 == 'MAGE',
          'advancement_tier': 0,
          'appearance_code': 'BASE',
          'active_skill_slots': 0,
        },
    ],
    'node_counts': {'SMALL': 0, 'MEDIUM': 0, 'LARGE': 0},
  };
}
