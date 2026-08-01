import 'dart:math';

/// HEALTH IS ALL - Dynamic Health Calculator v2
/// Client-side local offline precision calculation & fallback handling engine.
class DynamicHealthCalculatorV2 {
  /// Mifflin-St Jeor 기본 BMR 계산
  static double calculateBmr({
    required double weightKg,
    required double heightCm,
    required int age,
    required String gender,
  }) {
    final bool isMale = gender.toLowerCase() == 'male' ||
        gender.toLowerCase() == 'm' ||
        gender == '남성';
    final double genderOffset = isMale ? 5.0 : -161.0;
    return (10.0 * weightKg) + (6.25 * heightCm) - (5.0 * age) + genderOffset;
  }

  /// 다변수 TDEE 및 건강 점수 계산 (오프라인 모드 대응)
  static Map<String, dynamic> calculatePrecisionTdee({
    required double weightKg,
    required double heightCm,
    required int age,
    required String gender,
    required int dailySteps,
    required int workoutMinutes,
    double? hrvMs,
    double? baselineHrvMs,
    double? sleepQualityScore,
  }) {
    try {
      final double bmr = calculateBmr(
        weightKg: weightKg,
        heightCm: heightCm,
        age: age,
        gender: gender,
      );

      // 활동 계수 산출
      final double stepFactor = min(dailySteps / 10000.0, 1.5) * 0.35;
      final double workoutFactor = (workoutMinutes / 60.0) * 0.25;
      final double activityMultiplier = 1.2 + stepFactor + workoutFactor;

      bool isFallback = false;
      double recoveryFactor = 1.0;

      // HRV 변수 적용
      if (hrvMs != null && baselineHrvMs != null && baselineHrvMs > 0) {
        final double hrvRatio = hrvMs / baselineHrvMs;
        recoveryFactor *= hrvRatio.clamp(0.85, 1.15);
      } else {
        isFallback = true;
      }

      // 수면 점수 적용
      if (sleepQualityScore != null) {
        final double sleepFactor = 0.9 + (sleepQualityScore.clamp(0.0, 100.0) / 100.0) * 0.2;
        recoveryFactor *= sleepFactor;
      }

      final double finalTdee = bmr * activityMultiplier * recoveryFactor;

      return {
        'status': 'SUCCESS',
        'isFallback': isFallback,
        'bmr': bmr.roundToDouble(),
        'tdee': finalTdee.roundToDouble(),
        'activityMultiplier': double.parse(activityMultiplier.toStringAsFixed(3)),
        'recoveryFactor': double.parse(recoveryFactor.toStringAsFixed(3)),
        'healthScoreBonus': ((recoveryFactor - 1.0) * 100).roundToDouble(),
      };
    } catch (e) {
      // Fallback Level 1 적용
      final double fallbackBmr = calculateBmr(
        weightKg: weightKg,
        heightCm: heightCm,
        age: age,
        gender: gender,
      );
      return {
        'status': 'FALLBACK_SUCCESS',
        'isFallback': true,
        'bmr': fallbackBmr.roundToDouble(),
        'tdee': (fallbackBmr * 1.375).roundToDouble(),
        'activityMultiplier': 1.375,
        'recoveryFactor': 1.0,
        'healthScoreBonus': 0.0,
      };
    }
  }
}