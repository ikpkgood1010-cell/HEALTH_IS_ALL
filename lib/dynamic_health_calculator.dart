import 'dart:math';

/// HEALTH IS ALL - Frontend Dynamic Health & RPG Calculator
/// Filename: dynamic_health_calculator.dart
/// Path: HEALTH IS ALL/lib/dynamic_health_calculator.dart
/// Purpose: SSOT 수식 문서 규격에 맞춘 Flutter 오프라인 동적 계산 엔진
class DynamicHealthCalculator {
  /// BMR 계산 (Mifflin-St Jeor)
  static double calculateBmr({
    required double weightKg,
    required double heightCm,
    required int age,
    required String gender,
  }) {
    // 안전망 처리 (Fallback Defaults)
    double safeWeight = (weightKg <= 30 || weightKg >= 250) ? (gender.toUpperCase() == 'M' ? 70.0 : 55.0) : weightKg;
    double safeHeight = (heightCm <= 100 || heightCm >= 230) ? (gender.toUpperCase() == 'M' ? 175.0 : 162.0) : heightCm;
    int safeAge = (age <= 5 || age >= 120) ? 30 : age;

    double baseBmr = (10.0 * safeWeight) + (6.25 * safeHeight) - (5.0 * safeAge);
    return gender.toUpperCase() == 'M' ? baseBmr + 5.0 : baseBmr - 161.0;
  }

  /// 운동 결과 및 동적 RPG EXP 산출
  static ExerciseRewardResult calculateExerciseReward({
    required double durationMin,
    required double metValue,
    required double weightKg,
    int? rpe,
    double? avgHr,
    double? maxHr,
    int streakDays = 0,
    int spiritAffinityLevel = 1,
  }) {
    // 1. 기본 소모 칼로리 산출
    double baseCalories = durationMin * (metValue * 3.5 * weightKg) / 200.0;

    // 2. 강도 보정 인자 산출
    double intensityRatio = 1.0;
    bool isFallback = false;

    if (avgHr != null && maxHr != null && maxHr > 0) {
      double hrRatio = avgHr / maxHr;
      intensityRatio = (hrRatio * 1.4).clamp(0.8, 1.5);
    } else if (rpe != null) {
      intensityRatio = 0.7 + (rpe / 10.0) * 0.6;
    } else {
      intensityRatio = 1.0;
      isFallback = true;
    }

    double caloriesBurned = double.parse((baseCalories * intensityRatio).toStringAsFixed(1));

    // 3. EXP 및 변동성 적용
    double baseExp = durationMin * metValue * 1.5;
    double streakBonus = 1.0 + log(1.0 + max(0, streakDays)) * 0.05;
    double affinityMultiplier = 0.9 + min(0.4, (spiritAffinityLevel * 0.008));

    // 미세 변동 난수 인자 (0.95 ~ 1.05)
    double fluctuator = 0.95 + (Random().nextDouble() * 0.10);

    int finalExp = (baseExp * intensityRatio * streakBonus * affinityMultiplier * fluctuator).floor();

    return ExerciseRewardResult(
      caloriesBurned: caloriesBurned,
      expGained: max(10, finalExp),
      intensityRatio: double.parse(intensityRatio.toStringAsFixed(2)),
      streakBonusPct: double.parse(((streakBonus - 1.0) * 100).toStringAsFixed(1)),
      isFallbackUsed: isFallback,
    );
  }
}

/// 운동 결과 데이터 모델
class ExerciseRewardResult {
  final double caloriesBurned;
  final int expGained;
  final double intensityRatio;
  final double streakBonusPct;
  final bool isFallbackUsed;

  ExerciseRewardResult({
    required this.caloriesBurned,
    required this.expGained,
    required this.intensityRatio,
    required this.streakBonusPct,
    required this.isFallbackUsed,
  });

  @override
  String toString() {
    return 'ExerciseRewardResult(calories: $caloriesBurned, exp: $expGained, intensityRatio: $intensityRatio, streakBonus: $streakBonusPct%, fallback: $isFallbackUsed)';
  }
}