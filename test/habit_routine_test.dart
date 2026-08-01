import 'package:flutter_test/flutter_test.dart';

/// 습관 루틴 데이터 모델
class HabitRoutineModel {
  final String id;
  final String title;
  final String category;
  bool isCompleted;
  int streakCount;

  HabitRoutineModel({
    required this.id,
    required this.title,
    required this.category,
    this.isCompleted = false,
    this.streakCount = 0,
  });

  void toggleComplete() {
    if (isCompleted) {
      isCompleted = false;
      if (streakCount > 0) streakCount--;
    } else {
      isCompleted = true;
      streakCount++;
    }
  }
}

void main() {
  group('HabitRoutineModel 단위 테스트', () {
    test('습관 완료 처리 시 연속 달성(streak) 수가 1 증가한다', () {
      final habit = HabitRoutineModel(
        id: 'h1',
        title: '물 500ml 마시기',
        category: 'morning',
        isCompleted: false,
        streakCount: 5,
      );

      habit.toggleComplete();

      expect(habit.isCompleted, isTrue);
      expect(habit.streakCount, equals(6));
    });

    test('완료된 습관 취소 시 연속 달성 수가 1 감소한다', () {
      final habit = HabitRoutineModel(
        id: 'h2',
        title: '아침 스트레칭',
        category: 'morning',
        isCompleted: true,
        streakCount: 10,
      );

      habit.toggleComplete();

      expect(habit.isCompleted, isFalse);
      expect(habit.streakCount, equals(9));
    });
  });
}