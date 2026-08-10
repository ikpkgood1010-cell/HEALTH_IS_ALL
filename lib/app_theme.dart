import 'package:flutter/material.dart';

/// ============================================================================
/// HEALTH IS ALL - Design Tokens & Theme Specification (v1.0)
/// Based on: Component_Catalog.md
/// ============================================================================

abstract class AppColors {
// Primary & Brand Colors
  static const Color primary500 = Color(0xFF00B89C); // Toss-style mint action
  static const Color primary700 = Color(0xFF008F7A);
  static const Color primary100 = Color(0xFFE6F8F5);
  static const Color secondary500 = Color(0xFF2D8CFF);
  static const Color accentEnergy = Color(0xFFFFB020);

// Neutrals
  static const Color neutral900 = Color(0xFF191F28);
  static const Color neutral700 = Color(0xFF4E5968);
  static const Color neutral500 = Color(0xFF8B95A1);
  static const Color neutral200 = Color(0xFFE5E8EB);
  static const Color neutral100 = Color(0xFFF5F6F8);

// Status Colors
  static const Color statusError = Color(0xFFE74C3C); // 경고/재시도
}

abstract class AppSpacing {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double xl = 32.0;
}

abstract class AppRadius {
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double full = 999.0;

  static BorderRadius get borderRadiusSm => BorderRadius.circular(sm);
  static BorderRadius get borderRadiusMd => BorderRadius.circular(md);
  static BorderRadius get borderRadiusFull => BorderRadius.circular(full);
}

abstract class AppTypography {
  static const String fontFamily = 'Pretendard';

  static const TextStyle displayLg = TextStyle(
    fontFamily: fontFamily,
    fontSize: 28.0,
    fontWeight: FontWeight.w700,
    height: 1.3,
    color: AppColors.neutral900,
  );

  static const TextStyle titleMd = TextStyle(
    fontFamily: fontFamily,
    fontSize: 20.0,
    fontWeight: FontWeight.w600,
    height: 1.4,
    color: AppColors.neutral900,
  );

  static const TextStyle bodyMd = TextStyle(
    fontFamily: fontFamily,
    fontSize: 16.0,
    fontWeight: FontWeight.w400,
    height: 1.5,
    color: AppColors.neutral900,
  );

  static const TextStyle captionSm = TextStyle(
    fontFamily: fontFamily,
    fontSize: 12.0,
    fontWeight: FontWeight.w500,
    height: 1.4,
    color: AppColors.neutral500,
  );
}

abstract class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      fontFamily: AppTypography.fontFamily,
      scaffoldBackgroundColor: AppColors.neutral100,
      colorScheme: const ColorScheme.light(
        primary: AppColors.primary500,
        secondary: AppColors.secondary500,
        surface: AppColors.neutral100,
        error: AppColors.statusError,
        onPrimary: Colors.white,
        onSecondary: Colors.white,
        onSurface: AppColors.neutral900,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: AppTypography.titleMd,
        iconTheme: IconThemeData(color: AppColors.neutral900),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary500,
          foregroundColor: Colors.white,
          minimumSize: const Size.fromHeight(52.0),
          shape: RoundedRectangleBorder(
            borderRadius: AppRadius.borderRadiusMd,
          ),
          elevation: 2,
          textStyle: AppTypography.bodyMd.copyWith(
            fontWeight: FontWeight.w600,
            color: Colors.white,
          ),
        ),
      ),
      cardTheme: CardThemeData(
        color: Colors.white,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: AppRadius.borderRadiusMd,
          side: const BorderSide(color: AppColors.neutral200, width: 0.7),
        ),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: Colors.white,
        indicatorColor: AppColors.primary100,
        labelTextStyle: WidgetStateProperty.resolveWith((states) => TextStyle(
              color: states.contains(WidgetState.selected)
                  ? AppColors.primary700
                  : AppColors.neutral500,
              fontSize: 11,
              fontWeight: states.contains(WidgetState.selected)
                  ? FontWeight.w700
                  : FontWeight.w500,
            )),
      ),
    );
  }
}
