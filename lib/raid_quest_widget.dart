import 'package:flutter/material.dart';

/// HEALTH IS ALL - Dynamic Raid Quest Dashboard Widget
/// Filename: raid_quest_widget.dart
/// Path: HEALTH IS ALL/lib/raid_quest_widget.dart
/// Purpose: 주간 레이드 보스 체력, 건강 달성도 타격 딜량 및 미션 진행률 대시보드 UI
class RaidQuestWidget extends StatelessWidget {
  final String bossName;
  final int bossMaxHp;
  final int bossCurrentHp;
  final double weeklyWorkoutMinutes;
  final double avgNbsScore;
  final int cleanStreakDays;
  final int lastDamageDealt;
  final bool isCriticalHit;

  const RaidQuestWidget({
    Key? key,
    this.bossName = '타락한 태만 골렘',
    this.bossMaxHp = 12000,
    this.bossCurrentHp = 4200,
    this.weeklyWorkoutMinutes = 210.0,
    this.avgNbsScore = 82.5,
    this.cleanStreakDays = 5,
    this.lastDamageDealt = 1850,
    this.isCriticalHit = true,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    double hpRatio = (bossCurrentHp / bossMaxHp).clamp(0.0, 1.0);

    return Card(
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      color: Colors.grey[900],
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header: 건강 우선 지표 & 보스 이름
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Icon(Icons.fitness_center, color: Colors.greenAccent, size: 20),
                    const SizedBox(width: 8),
                    Text(
                      '주간 건강 레이드',
                      style: TextStyle(color: Colors.grey[300], fontSize: 15, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.purple.withOpacity(0.3),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.purpleAccent),
                  ),
                  child: Text(
                    bossName,
                    style: const TextStyle(color: Colors.purpleAccent, fontSize: 12, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Middle 1: 보스 체력바 (HP)
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('보스 체력 (Boss HP)', style: TextStyle(color: Colors.grey[400], fontSize: 12)),
                    Text(
                      '$bossCurrentHp / $bossMaxHp (${(hpRatio * 100).toStringAsFixed(1)}%)',
                      style: const TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold, fontSize: 13),
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: LinearProgressIndicator(
                    value: hpRatio,
                    minHeight: 12,
                    backgroundColor: Colors.grey[800],
                    valueColor: AlwaysStoppedAnimation<Color>(
                      hpRatio > 0.3 ? Colors.redAccent : Colors.orangeAccent,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Middle 2: 최근 건강 행동에 따른 타격 연출
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.grey[850],
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: isCriticalHit ? Colors.amber : Colors.grey[700]!),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Icon(
                        isCriticalHit ? Icons.bolt : Icons.sports_mma,
                        color: isCriticalHit ? Colors.amber : Colors.cyanAccent,
                        size: 24,
                      ),
                      const SizedBox(width: 10),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            isCriticalHit ? '크리티컬 건강 타격!' : '일일 건강 타격',
                            style: TextStyle(
                              color: isCriticalHit ? Colors.amber : Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 13,
                            ),
                          ),
                          Text(
                            '운동 ${weeklyWorkoutMinutes.toInt()}분 / 식단 $avgNbsScore점 반영',
                            style: TextStyle(color: Colors.grey[400], fontSize: 11),
                          ),
                        ],
                      ),
                    ],
                  ),
                  Text(
                    '-$lastDamageDealt DMG',
                    style: TextStyle(
                      color: isCriticalHit ? Colors.amber : Colors.redAccent,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // Bottom: 주간 건강 지표 기여도 (건강 본위 원칙)
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildHealthMetric('주간 운동', '${weeklyWorkoutMinutes.toInt()} 분', Colors.greenAccent),
                _buildHealthMetric('평균 식단', '$avgNbsScore 점', Colors.lightBlueAccent),
                _buildHealthMetric('클린 유지', '$cleanStreakDays 일', Colors.orangeAccent),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHealthMetric(String label, String value, Color color) {
    return Column(
      children: [
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 11)),
        const SizedBox(height: 2),
        Text(value, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 13)),
      ],
    );
  }
}