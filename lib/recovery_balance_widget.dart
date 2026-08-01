import 'package:flutter/material.dart';

/// HEALTH IS ALL - AI Recovery Balance & Rest Skill Widget
/// Filename: recovery_balance_widget.dart
/// Path: HEALTH IS ALL/lib/recovery_balance_widget.dart
/// Purpose: 일일 회복 지수(RS), AI 운동 강도 권장 및 정령 휴식 스킬 표시 UI
class RecoveryBalanceWidget extends StatelessWidget {
  final double recoveryScore;
  final String recommendedIntensity;
  final String aiRecommendation;
  final String restSkillName;
  final double staminaBuffPct;
  final bool isFallbackUsed;

  const RecoveryBalanceWidget({
    Key? key,
    this.recoveryScore = 84.5,
    this.recommendedIntensity = 'HIGH',
    this.aiRecommendation = '신체 회복 상태가 최상입니다! 고강도 웨이트/인터벌 운동을 추천합니다.',
    this.restSkillName = '정령의 신성한 활력 (Vitality Aura)',
    this.staminaBuffPct = 20.0,
    this.isFallbackUsed = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Color scoreColor = _getScoreColor(recoveryScore);

    return Card(
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      color: Colors.grey[900],
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Top: Header & Fallback status
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Icon(Icons.nightlight_round, color: Colors.indigoAccent, size: 22),
                    const SizedBox(width: 8),
                    Text(
                      'AI 수면 & 회복 밸런스',
                      style: TextStyle(color: Colors.grey[300], fontSize: 15, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                if (isFallbackUsed)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.orange.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.orangeAccent),
                    ),
                    child: const Text(
                      '자가 평가 반영',
                      style: TextStyle(color: Colors.orangeAccent, fontSize: 11, fontWeight: FontWeight.bold),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 16),

            // Middle: Recovery Gauge & Intensity Badge
            Row(
              children: [
                // Recovery Score Circular Display
                Container(
                  width: 85,
                  height: 85,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: scoreColor.withOpacity(0.15),
                    border: Border.all(color: scoreColor, width: 3),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        '${recoveryScore.toInt()}',
                        style: TextStyle(color: scoreColor, fontSize: 26, fontWeight: FontWeight.bold),
                      ),
                      Text('회복 점수', style: TextStyle(color: Colors.grey[400], fontSize: 10)),
                    ],
                  ),
                ),
                const SizedBox(width: 16),
                // AI Recommendation Text
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Text('오늘의 권장 강도: ', style: TextStyle(color: Colors.grey, fontSize: 12)),
                          _buildIntensityBadge(recommendedIntensity),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text(
                        aiRecommendation,
                        style: const TextStyle(color: Colors.white, fontSize: 12, height: 1.3),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const Divider(color: Colors.grey),

            // Bottom: Spirit Rest Skill Banner
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.indigo.withOpacity(0.25),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.indigoAccent.withOpacity(0.6)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.auto_awesome, color: Colors.amberAccent, size: 24),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '정령의 휴식 스킬 패시브',
                          style: TextStyle(color: Colors.grey[400], fontSize: 11),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          restSkillName,
                          style: const TextStyle(color: Colors.amberAccent, fontWeight: FontWeight.bold, fontSize: 13),
                        ),
                      ],
                    ),
                  ),
                  Text(
                    '+${staminaBuffPct.toInt()}% 버프',
                    style: const TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold, fontSize: 14),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Color _getScoreColor(double score) {
    if (score >= 80) return Colors.greenAccent;
    if (score >= 60) return Colors.lightBlueAccent;
    if (score >= 40) return Colors.orangeAccent;
    return Colors.redAccent;
  }

  Widget _buildIntensityBadge(String intensity) {
    Color bg;
    String label;
    switch (intensity) {
      case 'HIGH':
        bg = Colors.redAccent;
        label = '고강도 가능';
        break;
      case 'MODERATE':
        bg = Colors.green;
        label = '중강도 권장';
        break;
      case 'LIGHT':
        bg = Colors.orange;
        label = '저강도 추천';
        break;
      default:
        bg = Colors.purple;
        label = '휴식 권장';
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: bg.withOpacity(0.3),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: bg),
      ),
      child: Text(
        label,
        style: TextStyle(color: bg, fontSize: 11, fontWeight: FontWeight.bold),
      ),
    );
  }
}