/// HEALTH IS ALL - Dynamic Health Calculator V4
/// Flutter 모바일 단 다변수 정밀 건강 계산 및 안전 폴백(Fallback) 구현 모듈

import 'dart:math';

class CalculationResult {
  final double calories;
  final String formulaType;
  final double hrFactorApplied;
  final String status;

  CalculationResult({
    required this.calories,
    required this.formulaType,
    required this.hrFactorApplied,
    required this.status,
  });
}

class DynamicHealthCalculatorV4 {
  static const String version = "4.0.0";

  /// 다변수 정밀 소모 칼로리 계산 (심박수 연동 및 안전 폴백 적용)
  CalculationResult calculateCalories({
    required double weightKg,
    required double durationHours,
    required double metValue,
    double? heartRateAvg,
    double heartRateRest = 60.0,
    double heartRateMax = 190.0,
  }) {
    // 입력값 기본 보정
    final double safeWeight = weightKg > 0 ? weightKg : 60.0;
    final double safeDuration = durationHours > 0 ? durationHours : 0.1;
    final double safeMet = metValue > 0 ? metValue : 1.0;

    // 다변수 정밀 연산 시도
    try {
      if (heartRateAvg != null && heartRateAvg > heartRateRest) {
        if (heartRateMax <= heartRateRest) {
          throw Exception("최대 심박수 오류");
        }

        double hrFactor = (heartRateAvg - heartRateRest) / (heartRateMax - heartRateRest);
        hrFactor = min(max(hrFactor, 0.0), 1.5); // 안전 범위 제한

        final double precisionCalories = safeMet * safeWeight * safeDuration * (1.0 + hrFactor);

        return CalculationResult(
          calories: double.parse(precisionCalories.toStringAsFixed(2)),
          formulaType: "PRECISION_V8",
          hrFactorApplied: double.parse(hrFactor.toStringAsFixed(3)),
          status: "SUCCESS",
        );
      }
    } catch (e) {
      // 연산 예외 발생 시 안전 폴백으로 자동 전환
    }

    // 간결 안전 수식 (Fallback)
    final double fallbackCalories = safeMet * safeWeight * safeDuration;
    return CalculationResult(
      calories: double.parse(fallbackCalories.toStringAsFixed(2)),
      formulaType: "FALLBACK_V1",
      hrFactorApplied: 0.0,
      status: "FALLBACK_APPLIED",
    );
  }
}