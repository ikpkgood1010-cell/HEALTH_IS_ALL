import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:health_is_all/app_theme.dart';

void main() {
  group('앱 테마', () {
    test('토스형 민트 주 색상과 기본 여백을 사용한다', () {
      expect(AppColors.primary500, const Color(0xFF00B89C));
      expect(AppSpacing.xs, 4.0);
      expect(AppSpacing.sm, 8.0);
      expect(AppSpacing.md, 16.0);
      expect(AppSpacing.lg, 24.0);
    });

    test('Material 3와 흰색 내비게이션 배경을 사용한다', () {
      final theme = AppTheme.lightTheme;
      expect(theme.useMaterial3, isTrue);
      expect(theme.navigationBarTheme.backgroundColor, Colors.white);
    });
  });
}
