// 파일 저장 경로: HEALTH IS ALL/lib/dynamic_health_calculator_v3.dart
// SSOT: HEALTH IS ALL/lib/dynamic_health_calculator_v3.dart
// Related Documents: HEALTH IS ALL/01_ARCHITECTURE/DYNAMIC_FORMULA_REGISTRY_V6.md
// Change History: V2 -> V3 (Dart 모바일 클라이언트 dynamic 계산 및 예외 폴백 로직 적용)

import 'dart:math';

class DynamicHealthCalculatorV3 {
  final String version = "6.0.0";

  /// 동적 건강 수치 산출 함수 (오류 발생 시 안전한 기본값 반환)
  Map<String, dynamic> calculateDynamicHealth({
    required double weight,
    required double height,
    required int age,
    required String gender,
    double hrvNorm = 0.5,
    double sleepHours = 7.0,
  }) {
    try {
      if (weight <= 0 || height <= 0 || age <= 0) {
        return _getFallbackResult("유효하지 않은 신체 데이터");
      }

      // 기본 BMR 계산
      double genderOffset = (gender.toUpperCase() == 'M') ? 5.0 : -161.0;
      double bmrBase = (10.0 * weight) + (6.25 * height) - (5.0 * age) + genderOffset;

      // V6 다변수 동적 보정
      double sleepFactor = (sleepHours / 8.0).clamp(0.85, 1.15);
      double hrvFactor = 0.95 + 0.1 * sin(hrvNorm * pi);

      double dynamicBmr = bmrBase * sleepFactor * hrvFactor;
      double dynamicTdee = dynamicBmr * 1.2; // 기본 활동량 기준

      return {
        "status": "SUCCESS",
        "bmr": dynamicBmr.roundToDouble(),
        "tdee": dynamicTdee.roundToDouble(),
        "isFallback": false,
        "message": "오늘의 생체 리듬이 정밀 반영된 수치입니다.",
      };
    } catch (e) {
      return _getFallbackResult(e.toString());
    }
  }

  Map<String, dynamic> _getFallbackResult(String reason) {
    return {
      "status": "FALLBACK",
      "bmr": 1500.0,
      "tdee": 1800.0,
      "isFallback": true,
      "message": "기본 건강 수치가 적용되었습니다.",
      "reason": reason
    };
  }
}