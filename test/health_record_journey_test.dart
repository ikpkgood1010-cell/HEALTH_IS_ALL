import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:health_is_all/api_client.dart';
import 'package:health_is_all/api_data_provider.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

void main() {
  test('상세 문장 분석과 오늘 리뷰 응답을 앱 모델로 읽는다', () async {
    final client = MockClient((request) async {
      if (request.url.path == '/api/v1/health/text/analyze') {
        final body = jsonDecode(request.body) as Map<String, dynamic>;
        expect(body['text'], contains('삶은 계란'));
        return http.Response(
          jsonEncode({
            'record_type': 'meal_log',
            'status': 'NEEDS_CONFIRMATION',
            'summary': '2개 식품 · 식단점수 75점',
            'estimated': {
              'totals': {'kcal': 482.5, 'protein_g': 21.2},
              'totals_low': {'kcal': 430.0},
              'totals_high': {'kcal': 530.0},
              'meal_score': 75,
            },
            'confirmation_cards': [
              {
                'id': 'grams_boiled_egg',
                'question': '삶은 계란 양을 확인할까요?',
                'recommended_value': 150,
                'options': [
                  {'label': '150g', 'value': 150}
                ],
              }
            ],
            'reward_preview': {'base_exp': 30, 'health_essence': 1},
            'storage_detail': {'analysis_version': 'meal_text_v1'},
            'value': 482.5,
            'items': [],
            'blocks': [],
            'sources': ['국가표준식품성분표'],
          }),
          200,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }
      if (request.url.path == '/api/v1/health/review/daily/journey_test') {
        return http.Response(
          jsonEncode({
            'meal_count': 1,
            'workout_count': 0,
            'nutrition': {'kcal': 482.5},
            'nutrition_low': {'kcal': 430.0},
            'nutrition_high': {'kcal': 530.0},
            'meal_score': 75,
            'workout_minutes': 0,
            'exp_earned': 30,
            'health_essence_earned': 1,
            'meals': [],
            'workouts': [],
            'disclaimer': '추정값',
          }),
          200,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }
      return http.Response('{}', 404);
    });
    final api =
        HealthIApiClient(baseUrl: 'https://example.test', client: client);
    final analysis = await api.analyzeHealthText(
      userId: 'journey_test',
      recordType: 'meal_log',
      text: '삶은 계란 3개를 먹었어',
      mealType: '아침',
    );
    final review = await api.fetchDailyHealthReview('journey_test');

    expect(analysis.value, 482.5);
    expect(analysis.confirmationCards.single['recommended_value'], 150);
    expect(review.nutrition['kcal'], 482.5);
    expect(review.nutritionLow['kcal'], 430.0);
    api.dispose();
  });

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
