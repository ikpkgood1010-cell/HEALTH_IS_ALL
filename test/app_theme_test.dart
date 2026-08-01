import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

class AppColors {
  static const Color primary500 = Color(0xFF1E88E5);
  static const Color neutral300 = Color(0xFFE0E0E0);
  static const Color neutral500 = Color(0xFF9E9E9E);
}

class AppSpacing {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
}

void main() {
  group('AppTheme 상수 정의 단위 테스트', () {
    test('AppColors 주 색상이 디자인 명세와 일치한다', () {
      expect(AppColors.primary500, equals(const Color(0xFF1E88E5)));
    });

    test('AppSpacing 여백 단계별 값이 올바르게 설정되어 있다', () {
      expect(AppSpacing.xs, equals(4.0));
      expect(AppSpacing.sm, equals(8.0));
      expect(AppSpacing.md, equals(16.0));
      expect(AppSpacing.lg, equals(24.0));
    });
  });
}