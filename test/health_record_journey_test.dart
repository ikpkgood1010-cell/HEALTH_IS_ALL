import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:health_is_all/api_client.dart';
import 'package:health_is_all/api_data_provider.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

void main() {
  test('실패한 건강 기록 재시도는 같은 UUID를 사용한다', () async {
    var attempts = 0;
    final keys = <String>[];
    final client = MockClient((request) async {
      if (request.method == 'POST' &&
          request.url.path == '/api/v1/health/record') {
        final body = jsonDecode(request.body) as Map<String, dynamic>;
        keys.add(body['idempotency_key'] as String);
        attempts += 1;
        if (attempts == 1) {
          throw http.ClientException('response lost after send');
        }
        return http.Response(
          '{"success":true,"record_id":"${keys.last}",'
          '"exp_gained":30,"current_daily_exp":30,'
          '"message":"30 Exp가 반영되었습니다.","duplicate":false}',
          200,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }
      if (request.method == 'GET' &&
          request.url.path.contains('/health-i/status/')) {
        return http.Response(
          '{"name":"건강이","level":1,"current_exp":30,'
          '"daily_exp_cap":300,"emotion_state":"평온함",'
          '"dialogue":"기록을 잘 챙겼어요.",'
          '"equipped_skin":"default_skin",'
          '"last_updated":"2026-08-11T00:00:00",'
          '"today_consumed_calories":550,'
          '"today_workout_minutes":0,"today_water_liters":0,'
          '"streak_days":1}',
          200,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }
      return http.Response('{}', 404);
    });
    final provider = ApiDataProvider(
      userId: 'journey_test',
      apiClient:
          HealthIApiClient(baseUrl: 'https://example.test', client: client),
    );

    expect(await provider.logMeal(550, '점심'), isNull);
    final retried = await provider.logMeal(550, '점심');

    expect(retried, isNotNull);
    expect(keys, hasLength(2));
    expect(keys[1], keys[0]);
    expect(
      keys.first,
      matches(RegExp(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
      )),
    );
    expect(provider.consumedCalories, 550);
    provider.dispose();
  });
}
