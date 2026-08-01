import 'dart:math';
import 'package:flutter/material.dart';

/// HEALTH IS ALL - Spirit Diet Interactive UI Component
/// Filename: spirit_diet_interactive_widget.dart
/// Path: HEALTH IS ALL/lib/spirit_diet_interactive_widget.dart
/// Purpose: 식단 분석 결과에 따른 정령의 대사, 감정 표현, 촉진제 획득 연출 위젯
class SpiritDietInteractiveWidget extends StatelessWidget {
  final double calories;
  final double proteinG;
  final double carbsG;
  final double fatG;
  final double? fiberG;
  final double? addedSugarG;
  final int cleanStreak;
  final int spiritAffinity;

  const SpiritDietInteractiveWidget({
    Key? key,
    required this.calories,
    required this.proteinG,
    required this.carbsG,
    required this.fatG,
    this.fiberG,
    this.addedSugarG,
    this.cleanStreak = 0,
    this.spiritAffinity = 1,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final result = _calculateDietResult();

    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      color: Colors.grey[900],
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header: 건강 지표 표시 (게임에 가려지지 않음)
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '식단 영양 밸런스 (NBS)',
                  style: TextStyle(color: Colors.grey[400], fontSize: 14, fontWeight: FontWeight.bold),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: _getScoreColor(result.score).withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: _getScoreColor(result.score)),
                  ),
                  child: Text(
                    '${result.score.toStringAsFixed(1)} 점',
                    style: TextStyle(color: _getScoreColor(result.score), fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Middle: 정령 상태 및 반응 연출
            Row(
              children: [
                // 정령 아바타 및 감정 표현
                Container(
                  width: 70,
                  height: 70,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: _getScoreColor(result.score).withOpacity(0.15),
                    border: Border.all(color: _getScoreColor(result.score), width: 2),
                  ),
                  child: Center(
                    child: Text(
                      _getMoodEmoji(result.mood),
                      style: const TextStyle(fontSize: 36),
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                // 정령 상호작용 대사
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.grey[850],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      '"${result.dialogue}"',
                      style: const TextStyle(color: Colors.white, fontSize: 13, height: 1.4),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const Divider(color: Colors.grey),

            // Bottom: 게임 보상 (정령 성장 촉진제 & EXP)
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildRewardBadge(Icons.auto_awesome, '촉진제 에센스', '+${result.catalystGained} 개', Colors.amber),
                _buildRewardBadge(Icons.bolt, '정령 EXP', '+${result.expGained} EXP', Colors.cyanAccent),
                if (result.isFallback)
                  Text('(간이 계산 적용됨)', style: TextStyle(color: Colors.grey[500], fontSize: 10)),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRewardBadge(IconData icon, String label, String value, Color color) {
    return Row(
      children: [
        Icon(icon, color: color, size: 18),
        const SizedBox(width: 6),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(color: Colors.grey, fontSize: 11)),
            Text(value, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 13)),
          ],
        ),
      ],
    );
  }

  _DietCalculationResult _calculateDietResult() {
    bool isFallback = (fiberG == null || addedSugarG == null);
    double totalCal = max(calories, 1.0);
    double nbs = 50.0;

    if (!isFallback) {
      double pScore = min(40.0, ((proteinG * 4.0) / totalCal) * 150.0);
      double fScore = min(30.0, (fiberG! / 12.0) * 30.0);
      double sugarPenalty = max(0.0, ((addedSugarG! * 4.0) / totalCal) - 0.10) * 120.0;
      nbs = (pScore + fScore + 30.0 - sugarPenalty).clamp(10.0, 100.0);
    } else {
      nbs = (50.0 + (((proteinG * 4.0) / totalCal) * 100.0)).clamp(30.0, 90.0);
    }

    String mood = nbs >= 85 ? 'JOYFUL' : (nbs >= 65 ? 'SATISFIED' : (nbs >= 40 ? 'SLUGGISH' : 'DISTRESSED'));
    String dialogue = nbs >= 85
        ? '신선하고 클린한 식단이에요! 정령 촉진제가 가득 생겨납니다!'
        : (nbs >= 65
            ? '균형 잡힌 영양 공급이네요. 쑥쑥 성장하는 느낌입니다.'
            : (nbs >= 40
                ? '단백질과 식이섬유를 조금 더 챙겨주시면 좋겠어요!'
                : '정제당이 많아 정령 에센스 생성이 지체되고 있어요...'));

    double streakFactor = 1.0 + log(1.0 + max(0, cleanStreak)) * 0.08;
    double affinityFactor = 1.0 + (spiritAffinity * 0.005);
    double fluctuator = 0.95 + (Random().nextDouble() * 0.10);

    int catalyst = ((nbs * 1.8) * streakFactor * affinityFactor * fluctuator).floor();
    int exp = ((nbs * 1.2) * streakFactor * fluctuator).floor();

    return _DietCalculationResult(
      score: nbs,
      mood: mood,
      dialogue: dialogue,
      catalystGained: max(5, catalyst),
      expGained: max(10, exp),
      isFallback: isFallback,
    );
  }

  Color _getScoreColor(double score) {
    if (score >= 85) return Colors.greenAccent;
    if (score >= 65) return Colors.lightBlueAccent;
    if (score >= 40) return Colors.orangeAccent;
    return Colors.redAccent;
  }

  String _getMoodEmoji(String mood) {
    switch (mood) {
      case 'JOYFUL': return '🌟';
      case 'SATISFIED': return '🌱';
      case 'SLUGGISH': return '🍃';
      default: return '🌫️';
    }
  }
}

class _DietCalculationResult {
  final double score;
  final String mood;
  final String dialogue;
  final int catalystGained;
  final int expGained;
  final bool isFallback;

  _DietCalculationResult({
    required this.score,
    required this.mood,
    required this.dialogue,
    required this.catalystGained,
    required this.expGained,
    required this.isFallback,
  });
}