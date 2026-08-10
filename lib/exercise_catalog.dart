enum ExerciseCategoryGroup { cardio, strength, flexibility, sports }

enum IntensityLevel { high, medium, low }

class ExerciseDefinition {
  final ExerciseCategoryGroup group;
  final String label;
  final String code;
  final IntensityLevel recommendedIntensity;
  final double met;

  const ExerciseDefinition({
    required this.group,
    required this.label,
    required this.code,
    required this.recommendedIntensity,
    required this.met,
  });
}

const exerciseCatalog = <ExerciseDefinition>[
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '계단 오르기 (빠르게)',
      code: 'STAIR_CLIMBING_FAST',
      recommendedIntensity: IntensityLevel.high,
      met: 8.8),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.sports,
      label: '등산 (고강도)',
      code: 'HIKING_HARD',
      recommendedIntensity: IntensityLevel.high,
      met: 8.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.strength,
      label: '크로스핏',
      code: 'CROSSFIT',
      recommendedIntensity: IntensityLevel.high,
      met: 8.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.strength,
      label: '하이록스',
      code: 'HYROX',
      recommendedIntensity: IntensityLevel.high,
      met: 8.5),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '점핑 (트램펄린)',
      code: 'TRAMPOLINE_JUMPING',
      recommendedIntensity: IntensityLevel.high,
      met: 7.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '인터벌 트레이닝 (HIIT)',
      code: 'HIIT',
      recommendedIntensity: IntensityLevel.high,
      met: 9.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '줄넘기',
      code: 'JUMP_ROPE',
      recommendedIntensity: IntensityLevel.high,
      met: 10.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.strength,
      label: '케틀벨 플로우 / 스윙',
      code: 'KETTLEBELL_SWING',
      recommendedIntensity: IntensityLevel.high,
      met: 8.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '로잉 (전력 질주)',
      code: 'ROWING_FAST',
      recommendedIntensity: IntensityLevel.high,
      met: 8.5),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '어설트 바이크',
      code: 'ASSAULT_BIKE',
      recommendedIntensity: IntensityLevel.high,
      met: 9.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '달리기 (러닝)',
      code: 'RUNNING',
      recommendedIntensity: IntensityLevel.high,
      met: 8.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '스피닝',
      code: 'SPINNING',
      recommendedIntensity: IntensityLevel.high,
      met: 8.5),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.strength,
      label: '버피 및 플라이오메트릭',
      code: 'BURPEE_PLYOMETRICS',
      recommendedIntensity: IntensityLevel.high,
      met: 8.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '계단 오르기 (천천히)',
      code: 'STAIR_CLIMBING_SLOW',
      recommendedIntensity: IntensityLevel.medium,
      met: 5.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.sports,
      label: '등산 (낮은산)',
      code: 'HIKING_EASY',
      recommendedIntensity: IntensityLevel.medium,
      met: 6.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '줌바',
      code: 'ZUMBA',
      recommendedIntensity: IntensityLevel.medium,
      met: 6.5),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '빨리 걷기 (경보)',
      code: 'POWER_WALKING',
      recommendedIntensity: IntensityLevel.medium,
      met: 5.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.flexibility,
      label: '필라테스',
      code: 'PILATES',
      recommendedIntensity: IntensityLevel.medium,
      met: 3.5),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '조깅 (가벼운 달리기)',
      code: 'JOGGING',
      recommendedIntensity: IntensityLevel.medium,
      met: 6.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '수영 (중강도)',
      code: 'SWIMMING',
      recommendedIntensity: IntensityLevel.medium,
      met: 7.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '자전거 (평지, 적당히)',
      code: 'CYCLING',
      recommendedIntensity: IntensityLevel.medium,
      met: 6.8),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.strength,
      label: '웨이트 트레이닝',
      code: 'WEIGHT_TRAINING',
      recommendedIntensity: IntensityLevel.medium,
      met: 5.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.flexibility,
      label: '요가',
      code: 'YOGA',
      recommendedIntensity: IntensityLevel.low,
      met: 2.5),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.flexibility,
      label: '스트레칭 및 폼롤러',
      code: 'STRETCHING_FOAM_ROLLER',
      recommendedIntensity: IntensityLevel.low,
      met: 2.3),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '산책 (천천히 걷기)',
      code: 'WALKING',
      recommendedIntensity: IntensityLevel.low,
      met: 3.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.flexibility,
      label: '태극권 및 기공체조',
      code: 'TAI_CHI',
      recommendedIntensity: IntensityLevel.low,
      met: 3.0),
  ExerciseDefinition(
      group: ExerciseCategoryGroup.cardio,
      label: '가벼운 수영 (물놀이)',
      code: 'SWIMMING_LIGHT',
      recommendedIntensity: IntensityLevel.low,
      met: 4.0),
];

String groupLabel(ExerciseCategoryGroup group) => switch (group) {
      ExerciseCategoryGroup.cardio => '유산소',
      ExerciseCategoryGroup.strength => '근력',
      ExerciseCategoryGroup.flexibility => '유연성',
      ExerciseCategoryGroup.sports => '스포츠',
    };

String intensityLabel(IntensityLevel intensity) => switch (intensity) {
      IntensityLevel.high => '고강도',
      IntensityLevel.medium => '중강도',
      IntensityLevel.low => '저강도',
    };

String intensityCode(IntensityLevel intensity) => intensity.name.toUpperCase();
