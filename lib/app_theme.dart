import 'package:flutter/material.dart';

/// ============================================================================
/// HEALTH IS ALL - Design Tokens & Theme Specification (v1.0)
/// Based on: Component_Catalog.md
/// ============================================================================

abstract class AppColors {
// Primary & Brand Colors
static const Color primary500 = Color(0xFF2ECC71); // 주 액션 버튼, 달성 상태
static const Color primary100 = Color(0xFFE8F8F5); // 버튼 배경, 카드 틴트
static const Color secondary500 = Color(0xFF3498DB); // 운동/수분/신체 지표
static const Color accentEnergy = Color(0xFFF1C40F); // Spirit Energy, XP 게이지

// Neutrals
static const Color neutral900 = Color(0xFF2C3E50); // 메인 텍스트, 타이틀
static const Color neutral500 = Color(0xFF7F8C8D); // 서브 텍스트, 비활성 아이콘
static const Color neutral100 = Color(0xFFF8F9FA); // 전체 화면 배경, 카드 배경

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
backgroundColor: AppColors.neutral100,
elevation: 0,
centerTitle: true,
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
),
),
);
}
}