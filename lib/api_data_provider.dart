import 'package:flutter/material.dart';
import 'api_client.dart';

/// HEALTH IS ALL - Server-backed State Management Provider
///
/// MockDataProvider와 동일한 getter/메서드 시그니처를 제공하는 것이 핵심
/// 설계 원칙이다. 화면(diet_screen, workout_screen, home_screen 등)은
/// `Provider.of<MockDataProvider>` 대신 `Provider.of<ApiDataProvider>`를
/// 쓰기만 하면 되고, 내부 로직 변경은 필요 없다.
///
/// MockDataProvider는 오프라인/개발용으로 그대로 유지되며, main.dart에서
/// 두 Provider를 동시에 등록해 두었다. 실제로 어떤 Provider를 쓸지는
/// 화면단에서 선택한다 (점진적 마이그레이션을 위한 안전한 전환 방식).
class ApiDataProvider extends ChangeNotifier {
  final HealthIApiClient _api;
  final String userId;

  ApiDataProvider({HealthIApiClient? apiClient, this.userId = 'user_test_001'})
      : _api = apiClient ?? HealthIApiClient();

  // ---- MockDataProvider와 동일한 필드/게터 (화면 호환성 유지) ----
  String _healthIName = '건강이';
  int _level = 1;
  int _currentExp = 0;
  int _dailyExpCap = 300;
  int _todayExpGained = 0;
  String _emotionState = '평온함';
  String _dialogue = '오늘 하루도 차근차근 시작해볼까요?';

  double _consumedCalories = 0;
  int _targetCalories = 2000;
  double _workoutMinutes = 0;
  int _targetWorkoutMinutes = 45;
  double _waterLiters = 0;
  double _targetWaterLiters = 2.0;
  int _streakDays = 0;

  bool _isLoading = false;
  String? _lastError;

  String get healthIName => _healthIName;
  int get level => _level;
  int get currentExp => _currentExp;
  int get dailyExpCap => _dailyExpCap;
  int get todayExpGained => _todayExpGained;
  String get emotionState => _emotionState;
  String get dialogue => _dialogue;

  int get consumedCalories => _consumedCalories.toInt();
  int get targetCalories => _targetCalories;
  int get workoutMinutes => _workoutMinutes.toInt();
  int get targetWorkoutMinutes => _targetWorkoutMinutes;
  double get waterLiters => _waterLiters;
  double get targetWaterLiters => _targetWaterLiters;
  int get streakDays => _streakDays;

  bool get isLoading => _isLoading;
  String? get lastError => _lastError;

  /// 서버에서 현재 상태를 불러와 화면에 반영한다.
  /// 화면 진입 시(initState) 호출하도록 설계되었다.
  Future<void> refreshStatus() async {
    _isLoading = true;
    _lastError = null;
    notifyListeners();
    try {
      final status = await _api.fetchHealthIStatus(userId);
      _healthIName = status.name;
      _level = status.level;
      _currentExp = status.currentExp;
      _dailyExpCap = status.dailyExpCap;
      _todayExpGained = status.currentExp % status.dailyExpCap;
      _emotionState = status.emotionState;
      _dialogue = status.dialogue;
      _consumedCalories = status.todayConsumedCalories;
      _workoutMinutes = status.todayWorkoutMinutes;
      _waterLiters = status.todayWaterLiters;
      _streakDays = status.streakDays;
    } catch (e) {
      _lastError = '서버 연결에 실패했습니다. 네트워크 상태를 확인해주세요.';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> logMeal(int calories, String mealType) async {
    await _recordActivity(
      recordType: 'meal_log',
      value: calories.toDouble(),
      detailData: {'meal_type': mealType},
      localApply: () => _consumedCalories += calories,
    );
  }

  Future<void> logWorkout(int minutes, int burnedCalories) async {
    await _recordActivity(
      recordType: 'workout_log',
      value: minutes.toDouble(),
      detailData: {'burned_calories': burnedCalories},
      localApply: () => _workoutMinutes += minutes,
    );
  }

  Future<void> addWater(double amount) async {
    await _recordActivity(
      recordType: 'water_log',
      value: amount,
      localApply: () => _waterLiters += amount,
    );
  }

  /// 공통 기록 처리: 서버에 저장 → 성공 시 로컬 상태에도 즉시 반영(낙관적 갱신)
  /// → 최신 서버 상태로 재동기화. 서버 실패 시 로컬 상태는 건드리지 않고
  /// 에러만 노출한다 (화면 표시값과 서버 값이 어긋나는 것을 방지).
  Future<void> _recordActivity({
    required String recordType,
    required double value,
    Map<String, dynamic>? detailData,
    required VoidCallback localApply,
  }) async {
    _lastError = null;
    try {
      final result = await _api.logHealthActivity(
        userId: userId,
        recordType: recordType,
        value: value,
        detailData: detailData,
      );

      localApply();
      _currentExp += result.expGained;
      _todayExpGained = result.currentDailyExp;

      final int calculatedLevel = (_currentExp ~/ 300) + 1;
      if (calculatedLevel > _level) {
        _level = calculatedLevel;
        _dialogue = "축하합니다! '건강이'가 Lv. $_level 로 레벨업했습니다!";
      } else if (result.message.isNotEmpty) {
        _dialogue = result.message;
      }

      notifyListeners();
      // 서버 기준 최신 집계(오늘자 칼로리/운동/수분/streak/감정상태)로 동기화
      await refreshStatus();
    } catch (e) {
      _lastError = '기록 저장에 실패했습니다. 네트워크 상태를 확인해주세요.';
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _api.dispose();
    super.dispose();
  }
}
