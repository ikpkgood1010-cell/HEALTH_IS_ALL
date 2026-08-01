import 'package:flutter/material.dart';

/// HEALTH IS ALL - Wearable Heart Rate & Spirit Aura Widget
/// Filename: heartrate_spirit_widget.dart
/// Path: HEALTH IS ALL/lib/heartrate_spirit_widget.dart
/// Purpose: 실시간 심박수, HR Zone, EPOC 칼로리 및 정령 아우라 이펙트 표시 UI
class HeartRateSpiritWidget extends StatelessWidget {
  final double currentBpm;
  final int userAge;
  final double caloriesBurned;
  final double epocBonus;
  final String auraState;
  final bool isSensorConnected;

  const HeartRateSpiritWidget({
    Key? key,
    this.currentBpm = 148.0,
    this.userAge = 30,
    this.caloriesBurned = 345.2,
    this.epocBonus = 28.5,
    this.auraState = 'AEROBIC_AURA',
    this.isSensorConnected = true,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    double maxHr = 208.0 - (0.7 * userAge);
    double hrPercentage = (currentBpm / maxHr * 100).clamp(0.0, 100.0);
    Color zoneColor = _getZoneColor(auraState);

    return Card(
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      color: Colors.grey[900],
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Top: 연결 상태 & 헤더
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Icon(Icons.favorite, color: zoneColor, size: 22),
                    const SizedBox(width: 8),
                    Text(
                      '실시간 심박 & 정령 아우라',
                      style: TextStyle(color: Colors.grey[300], fontSize: 15, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: isSensorConnected ? Colors.green.withOpacity(0.2) : Colors.red.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: isSensorConnected ? Colors.greenAccent : Colors.redAccent),
                  ),
                  child: Text(
                    isSensorConnected ? '웨어러블 연결됨' : '센서 미연결 (Fallback)',
                    style: TextStyle(
                      color: isSensorConnected ? Colors.greenAccent : Colors.redAccent,
                      fontSize: 11,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Middle: 심박수 및 아우라 시각화
            Row(
              children: [
                // 심박수 큰 글씨 및 파동 이펙트
                Container(
                  width: 90,
                  height: 90,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: zoneColor.withOpacity(0.15),
                    border: Border.all(color: zoneColor, width: 3),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        '${currentBpm.toInt()}',
                        style: TextStyle(color: zoneColor, fontSize: 28, fontWeight: FontWeight.bold),
                      ),
                      Text('BPM', style: TextStyle(color: Colors.grey[400], fontSize: 10)),
                    ],
                  ),
                ),
                const SizedBox(width: 16),
                // 정령 상태 및 심박 비율
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'HR Zone: ${_getZoneTitle(auraState)} (${hrPercentage.toStringAsFixed(1)}%)',
                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
                      ),
                      const SizedBox(height: 6),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(6),
                        child: LinearProgressIndicator(
                          value: hrPercentage / 100.0,
                          minHeight: 8,
                          backgroundColor: Colors.grey[800],
                          valueColor: AlwaysStoppedAnimation<Color>(zoneColor),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: Colors.grey[850],
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          _getAuraDescription(auraState),
                          style: TextStyle(color: Colors.grey[300], fontSize: 11),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const Divider(color: Colors.grey),

            // Bottom: 동적 소모 칼로리 및 EPOC 보너스 (건강 본위 수치)
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildCalorieMetric('동적 소모 칼로리', '${caloriesBurned.toStringAsFixed(1)} kcal', Colors.orangeAccent),
                _buildCalorieMetric('EPOC 애프터번', '+${epocBonus.toStringAsFixed(1)} kcal', Colors.cyanAccent),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCalorieMetric(String label, String value, Color color) {
    return Column(
      children: [
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 11)),
        const SizedBox(height: 2),
        Text(value, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 14)),
      ],
    );
  }

  Color _getZoneColor(String aura) {
    switch (aura) {
      case 'OVERHEAT': return Colors.purpleAccent;
      case 'ANAEROBIC_AURA': return Colors.redAccent;
      case 'AEROBIC_AURA': return Colors.orangeAccent;
      case 'FAT_BURN_AURA': return Colors.greenAccent;
      case 'WARMUP_AURA': return Colors.lightBlueAccent;
      default: return Colors.grey;
    }
  }

  String _getZoneTitle(String aura) {
    switch (aura) {
      case 'OVERHEAT': return 'Zone 5 (과부하 경고)';
      case 'ANAEROBIC_AURA': return 'Zone 4 (무산소)';
      case 'AEROBIC_AURA': return 'Zone 3 (유산소)';
      case 'FAT_BURN_AURA': return 'Zone 2 (지방 연소)';
      case 'WARMUP_AURA': return 'Zone 1 (웜업)';
      default: return 'Zone 0 (휴식)';
    }
  }

  String _getAuraDescription(String aura) {
    switch (aura) {
      case 'OVERHEAT': return '⚠️ 심박수가 높습니다! 안전을 위해 강도를 낮추세요.';
      case 'ANAEROBIC_AURA': return '🔥 정령이 붉은 무산소 아우라로 폭발적 힘을 발휘합니다!';
      case 'AEROBIC_AURA': return '⚡ 심폐 지구력이 강화되며 정령이 황금빛으로 빛납니다.';
      case 'FAT_BURN_AURA': return '🌱 효율적인 지방 연소 구간입니다. 정령이 활기를 얻습니다.';
      default: return '🍃 몸을 풀며 준비 운동을 진행 중입니다.';
    }
  }
}