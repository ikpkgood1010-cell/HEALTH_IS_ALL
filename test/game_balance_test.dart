import 'package:flutter_test/flutter_test.dart';
import 'package:health_is_all/game_balance.dart';

void main() {
  group('건강 균형 계산', () {
    test('HBI는 최저 영역 60%와 평균 40%로 계산한다', () {
      expect(calculateHbi([20, 80, 80, 80]), 38.0);
    });

    test('활동이 없는 날에도 휴식을 처벌하지 않는다', () {
      final projection = HealthBalanceProjection.fromHealth(
        calories: 0,
        targetCalories: 2000,
        workoutMinutes: 0,
        targetWorkoutMinutes: 45,
        waterLiters: 0,
        targetWaterLiters: 2,
        streakDays: 0,
      );

      expect(projection.hbi, 0);
      expect(projection.environmentMessage, contains('쉬어도 괜찮아요'));
    });

    test('목표 초과 활동은 100점에서 상한 처리한다', () {
      final projection = HealthBalanceProjection.fromHealth(
        calories: 2000,
        targetCalories: 2000,
        workoutMinutes: 180,
        targetWorkoutMinutes: 45,
        waterLiters: 4,
        targetWaterLiters: 2,
        streakDays: 30,
      );

      expect(
          projection.breakdown.values.every((score) => score <= 100), isTrue);
      expect(projection.hbi, 100);
    });
  });
}
