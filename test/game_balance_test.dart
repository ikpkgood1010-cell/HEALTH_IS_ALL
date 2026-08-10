import 'package:flutter_test/flutter_test.dart';
import 'package:health_is_all/game_balance.dart';

void main() {
  group('건강 우선 게임 밸런스', () {
    test('HBI는 최저 영역 60%와 평균 40%로 계산한다', () {
      expect(calculateHbi([20, 80, 80, 80]), 38.0);
    });

    test('활동이 없는 날에도 불이익 배율을 적용하지 않는다', () {
      final projection = GuildProjection.fromHealth(
        level: 1,
        calories: 0,
        targetCalories: 2000,
        workoutMinutes: 0,
        targetWorkoutMinutes: 45,
        waterLiters: 0,
        targetWaterLiters: 2,
        streakDays: 0,
      );

      expect(projection.rewardMultiplier, 1.0);
      expect(projection.environmentName, '회복의 안개');
      expect(projection.memoryShards, 0);
    });

    test('기억 조각은 탑 30층 전에는 지급하지 않는다', () {
      final projection = GuildProjection.fromHealth(
        level: 5,
        calories: 2000,
        targetCalories: 2000,
        workoutMinutes: 45,
        targetWorkoutMinutes: 45,
        waterLiters: 2,
        targetWaterLiters: 2,
        streakDays: 7,
      );

      expect(projection.towerFloor, lessThan(30));
      expect(projection.memoryShards, 0);
    });
  });
}
