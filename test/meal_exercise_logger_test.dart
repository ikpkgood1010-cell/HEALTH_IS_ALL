import 'package:flutter_test/flutter_test.dart';

enum MealTimeType { breakfast, lunch, dinner, snack }

class MealRecord {
  final String id;
  final MealTimeType timeType;
  final String foodName;
  final int calories;

  MealRecord({
    required this.id,
    required this.timeType,
    required this.foodName,
    required this.calories,
  });
}

class MealTracker {
  final List<MealRecord> _meals = [];

  List<MealRecord> get meals => List.unmodifiable(_meals);

  void addMeal(MealRecord meal) {
    _meals.add(meal);
  }

  int get totalCalories => _meals.fold(0, (sum, item) => sum + item.calories);
}

void main() {
  group('MealTracker 단위 테스트', () {
    late MealTracker tracker;

    setUp(() {
      tracker = MealTracker();
    });

    test('식단 추가 시 총 섭취 칼로리가 정확히 합산된다', () {
      tracker.addMeal(MealRecord(
        id: 'm1',
        timeType: MealTimeType.breakfast,
        foodName: '오트밀 & 사과',
        calories: 350,
      ));

      tracker.addMeal(MealRecord(
        id: 'm2',
        timeType: MealTimeType.lunch,
        foodName: '닭가슴살 샐러드',
        calories: 450,
      ));

      expect(tracker.meals.length, equals(2));
      expect(tracker.totalCalories, equals(800));
    });
  });
}