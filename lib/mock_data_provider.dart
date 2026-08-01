import 'package:flutter/material.dart';

/// HEALTH IS ALL - Global State Management Provider
/// Dual-Excellence: 건강 정보 관리 + 게임 Progression 및 '건강이' 상태 실시간 반영
class MockDataProvider extends ChangeNotifier {
  String _healthIName = '건강이';
  int _level = 1;
  int _currentExp = 120;
  final int _dailyExpCap = 300;
  int _todayExpGained = 120;
  String _emotionState = '활기참';
  String _dialogue = '오늘 운동과 영양 균형이 정말 유익해요! 이대로 계속 가봐요!';

  int _consumedCalories = 1450;
  int _targetCalories = 2000;
  int _workoutMinutes = 40;
  int _targetWorkoutMinutes = 45;
  double _waterLiters = 1.6;
  double _targetWaterLiters = 2.0;
  int _streakDays = 4;

  String get healthIName => _healthIName;
  int get level => _level;
  int get currentExp => _currentExp;
  int get dailyExpCap => _dailyExpCap;
  int get todayExpGained => _todayExpGained;
  String get emotionState => _emotionState;
  String get dialogue => _dialogue;

  int get consumedCalories => _consumedCalories;
  int get targetCalories => _targetCalories;
  int get workoutMinutes => _workoutMinutes;
  int get targetWorkoutMinutes => _targetWorkoutMinutes;
  double get waterLiters => _waterLiters;
  double get targetWaterLiters => _targetWaterLiters;
  int get streakDays => _streakDays;

  void logMeal(int calories, String mealType) {
    _consumedCalories += calories;
    _addExp(30);
    _updateHealthIStatus('기특함', "'${mealType}' 식단을 영양가 있게 챙겨드셨군요! 30 Exp를 받아가세요!");
  }

  void logWorkout(int minutes, int burnedCalories) {
    _workoutMinutes += minutes;
    _addExp(50);
    _updateHealthIStatus('최고의 행복', '${minutes}분 동안 멋지게 땀 흘리셨네요! 50 Exp 획득!');
  }

  void addWater(double amount) {
    _waterLiters += amount;
    _addExp(10);
    _updateHealthIStatus('시원함', '수분 보충으로 활력이 수직 상승했습니다! 10 Exp 획득!');
  }

  void _addExp(int amount) {
    if (_todayExpGained >= _dailyExpCap) return;

    int actualGain = amount;
    if (_todayExpGained + amount > _dailyExpCap) {
      actualGain = _dailyExpCap - _todayExpGained;
    }

    _todayExpGained += actualGain;
    _currentExp += actualGain;

    final int calculatedLevel = (_currentExp ~/ 300) + 1;
    if (calculatedLevel > _level) {
      _level = calculatedLevel;
      _dialogue = "축하합니다! '건강이'가 Lv. $_level 로 레벨업했습니다!";
    }

    notifyListeners();
  }

  void _updateHealthIStatus(String emotion, String newDialogue) {
    _emotionState = emotion;
    _dialogue = newDialogue;
    notifyListeners();
  }
}
