import 'package:flutter/material.dart';

/// HEALTH IS ALL - Sleep Recovery Report & Healing Widget
/// Filename: recovery_sleep_widget.dart
/// Path: HEALTH IS ALL/lib/recovery_sleep_widget.dart
/// Purpose: 수면 회복 지수 시각화 및 정령 힐링 케어 대화 UI
class RecoverySleepWidget extends StatelessWidget {
  final double recoveryScore;
  final String statusTitle;
  final String spiritMessage;
  final double sleepEfficiencyPct;

  const RecoverySleepWidget({
    Key? key,
    this.recoveryScore = 88.5,
    this.statusTitle = '최상의 생체 에너지 ✨',
    this.spiritMessage = '깊은 수면 덕분에 정령과 유저님 모두 100% 충전되었어요! 멋진 하루를 시작해볼까요?',
    this.sleepEfficiencyPct = 92.0,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Color scoreColor = recoveryScore >= 70 ? Colors.amberAccent : Colors.lightBlueAccent;

    return Card(
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      color: const Color(0xFF1A1D26),
      child: Padding(
        padding: const EdgeInsets.all(18.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(
                  children: [
                    Icon(Icons.nights_stay_rounded, color: Colors.indigoAccent, size: 20),
                    SizedBox(width: 8),
                    Text(
                      '수면·회복 리포트',
                      style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                Text(
                  '수면 효율 $sleepEfficiencyPct%',
                  style: const TextStyle(color: Colors.white54, fontSize: 11),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Recovery Score Display
            Row(
              children: [
                Container(
                  width: 70,
                  height: 70,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: scoreColor.withOpacity(0.15),
                    border: Border.all(color: scoreColor, width: 2.5),
                  ),
                  child: Center(
                    child: Text(
                      '${recoveryScore.toInt()}',
                      style: TextStyle(color: scoreColor, fontSize: 24, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        statusTitle,
                        style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        spiritMessage,
                        style: TextStyle(color: Colors.grey[400], fontSize: 11, height: 1.3),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Healing Night Care Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () => _showNightCareDialog(context),
                icon: const Icon(Icons.bedtime_rounded, size: 18),
                label: const Text('정령과 함께하는 밤 힐링케어'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF2C3142),
                  foregroundColor: Colors.indigoAccent,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  padding: const EdgeInsets.symmetric(vertical: 10),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showNightCareDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF222634),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Row(
          children: [
            Text('🌙', style: TextStyle(fontSize: 26)),
            SizedBox(width: 8),
            Text('정령의 편안한 밤 케어', style: TextStyle(color: Colors.white, fontSize: 16)),
          ],
        ),
        content: const Text(
          '오늘 하루도 정말 고생 많으셨어요. 정령이 따뜻한 숲의 조용한 빗소리와 힐링 사운드로 유저님의 편안한 수면을 도와드릴게요 🌿',
          style: TextStyle(color: Colors.white70, fontSize: 13, height: 1.4),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('음악 듣고 편히 쉬기', style: TextStyle(color: Colors.indigoAccent, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}