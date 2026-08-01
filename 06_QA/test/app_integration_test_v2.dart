/// HEALTH IS ALL - App Integration Test V2
/// 건강 계산식, 예외 안전 폴백, 정령 반응 연동 E2E 종합 검증 코드

import 'package:flutter_test/flutter_test.dart';
import '../lib/services/dynamic_health_calculator_v4.dart';

void main() {
  group('HEALTH IS ALL V8/V9 E2E 통합 테스트', () {
    late DynamicHealthCalculatorV4 calculator;

    setUp(() {
      calculator = DynamicHealthCalculatorV4();
    });

    test('고강도 운동 세차 시 다변수 정밀 칼로리 계산 검증', () {
      final result = calculator.calculateCalories(
        weightKg: 72.0,
        durationHours: 2.0,
        metValue: 4.5,
        heartRateAvg: 135.0,
      );

      expect(result.status, equals('SUCCESS'));
      expect(result.formulaType, equals('PRECISION_V8'));
      expect(result.calories, greaterThan(600.0));
    });

    test('심박수 누락 시 안전 폴백(Fallback) 모드 정상 작동 검증', () {
      final result = calculator.calculateCalories(
        weightKg: 72.0,
        durationHours: 2.0,
        metValue: 4.5,
        heartRateAvg: null, // 심박수 누락
      );

      expect(result.status, equals('FALLBACK_APPLIED'));
      expect(result.formulaType, equals('FALLBACK_V1'));
      expect(result.calories, equals(648.0)); // 4.5 * 72 * 2 = 648
    });
  });
}