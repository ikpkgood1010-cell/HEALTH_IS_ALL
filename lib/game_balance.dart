import 'dart:math' as math;

double _score(double value) => value.clamp(0, 100).toDouble();

double calculateHbi(List<double> scores) {
  if (scores.isEmpty) return 0;
  final normalized = scores.map(_score).toList();
  final minimum = normalized.reduce(math.min);
  final average = normalized.reduce((a, b) => a + b) / normalized.length;
  return double.parse((minimum * 0.6 + average * 0.4).toStringAsFixed(1));
}

class GuildProjection {
  final double hbi;
  final Map<String, double> breakdown;
  final int level;
  final String stageName;
  final int towerFloor;
  final int vitality;
  final int guildCoins;
  final int memoryShards;
  final String environmentName;
  final String environmentMessage;
  final double rewardMultiplier;

  const GuildProjection({
    required this.hbi,
    required this.breakdown,
    required this.level,
    required this.stageName,
    required this.towerFloor,
    required this.vitality,
    required this.guildCoins,
    required this.memoryShards,
    required this.environmentName,
    required this.environmentMessage,
    required this.rewardMultiplier,
  });

  factory GuildProjection.fromHealth({
    required int level,
    required int calories,
    required int targetCalories,
    required int workoutMinutes,
    required int targetWorkoutMinutes,
    required double waterLiters,
    required double targetWaterLiters,
    required int streakDays,
  }) {
    final activity =
        _score(workoutMinutes / math.max(targetWorkoutMinutes, 1) * 100);
    final nutrition = _score(100 -
        (calories - targetCalories).abs() / math.max(targetCalories, 1) * 100);
    final hydration =
        _score(waterLiters / math.max(targetWaterLiters, 0.1) * 100);
    final consistency = _score(streakDays / 7 * 100);
    final hbi = calculateHbi([activity, nutrition, hydration, consistency]);
    final vitality = math.min(
        200,
        (activity * .8 +
                nutrition * .35 +
                hydration * .25 +
                math.min(streakDays, 7) * 5)
            .floor());
    final towerFloor = math.max(1, level * 3 + (hbi / 20).floor());

    String stageName;
    if (level >= 100) {
      stageName = '전설 길드';
    } else if (level >= 50) {
      stageName = '유명 길드';
    } else if (level >= 30) {
      stageName = '모험가 길드';
    } else if (level >= 10) {
      stageName = '견습 길드';
    } else {
      stageName = '작은 캠프';
    }

    String environmentName;
    String environmentMessage;
    double multiplier;
    if (hbi >= 80) {
      environmentName = '별빛 정원';
      environmentMessage = '희귀 정령의 흔적이 나타났어요.';
      multiplier = 1.15;
    } else if (hbi >= 60) {
      environmentName = '햇살길';
      environmentMessage = '균형 잡힌 하루가 길드를 밝힙니다.';
      multiplier = 1.08;
    } else if (hbi >= 40) {
      environmentName = '고요한 숲';
      environmentMessage = '천천히 다음 모험을 준비하고 있어요.';
      multiplier = 1.03;
    } else {
      environmentName = '회복의 안개';
      environmentMessage = '쉬어도 성장은 사라지지 않아요.';
      multiplier = 1.0;
    }

    return GuildProjection(
      hbi: hbi,
      breakdown: {
        '운동': activity,
        '식단': nutrition,
        '수분(대체)': hydration,
        '꾸준함(대체)': consistency
      },
      level: math.max(1, level),
      stageName: stageName,
      towerFloor: towerFloor,
      vitality: vitality,
      guildCoins: (vitality * (1 + hbi / 500)).floor(),
      memoryShards: towerFloor < 30
          ? 0
          : (math.sqrt(towerFloor) * 10 * (.8 + hbi / 500)).floor(),
      environmentName: environmentName,
      environmentMessage: environmentMessage,
      rewardMultiplier: multiplier,
    );
  }
}
