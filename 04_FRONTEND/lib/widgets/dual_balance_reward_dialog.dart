import 'package:flutter/material.dart';
import '../services/health_game_sync_service.dart';

class DualBalanceRewardDialog extends StatelessWidget {
  final DualBalanceRewardModel reward;

  const DualBalanceRewardDialog({Key? key, required this.reward}) : super(key: key);

  static void show(BuildContext context, DualBalanceRewardModel reward) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) => DualBalanceRewardDialog(reward: reward),
    );
  }

  @override
  Widget build(BuildContext context) {
    final bool isFallback = reward.mode == CalculationMode.FALLBACK_SIMPLE;

    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      title: Row(
        children: [
          const Icon(Icons.eco, color: Colors.green),
          const SizedBox(width: 8),
          Text(
            isFallback ? '기본 건강 보상 획득!' : '정령과의 건강 시너지 완료!',
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ],
      ),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 보상 수치 카드 (게임 요소)
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.green.shade50,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildStatItem('EXP', '+${reward.expGained}', Icons.bolt, Colors.orange),
                _buildStatItem('친밀도', '+${reward.spiritAffinityDelta}', Icons.favorite, Colors.pink),
                _buildStatItem('스낵', '+${reward.snackRewardCount}', Icons.cookie, Colors.brown),
              ],
            ),
          ),
          const SizedBox(height: 16),
          // 1~3줄 건강 팁 박스 (건강 요소)
          const Text(
            '💡 오늘의 웰니스 팁',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
          ),
          const SizedBox(height: 6),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.grey.shade100,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: Colors.grey.shade300),
            ),
            child: Text(
              reward.healthTipMessage,
              style: const TextStyle(fontSize: 13, height: 1.4, color: Colors.black80),
            ),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('확인', style: TextStyle(fontWeight: FontWeight.bold)),
        ),
      ],
    );
  }

  Widget _buildStatItem(String label, String value, IconData icon, Color color) {
    return Column(
      children: [
        Icon(icon, color: color, size: 24),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
        Text(value, style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: color)),
      ],
    );
  }
}