import 'package:flutter/material.dart';

/// HEALTH IS ALL - Friendly Daily Nutrition & Workout Quest Widget
/// Filename: nutrition_quest_widget.dart
/// Path: HEALTH IS ALL/lib/nutrition_quest_widget.dart
/// Purpose: 유저 맞춤형 일일 건강 퀘스트 카드 및 따뜻한 축하 보상 팝업 UI
class NutritionQuestWidget extends StatelessWidget {
  final List<Map<String, dynamic>> quests;
  final String friendlyGreeting;

  const NutritionQuestWidget({
    Key? key,
    this.quests = const [
      {
        "title": "🏃‍♂️ 활력 넘치는 7,000보 달성하기",
        "category": "WORKOUT",
        "current": 5200,
        "target": 7000,
        "unit": "걸음",
        "reward_gold": 300
      },
      {
        "title": "🥩 목표 단백질 밸런스 채우기",
        "category": "NUTRITION",
        "current": 1,
        "target": 1,
        "unit": "달성",
        "reward_gold": 250
      },
    ],
    this.friendlyGreeting = '오늘 몸 상태에 딱 맞춘 건강 미션이 도착했어요! 무리하지 말고 정령과 차근차근 함께해요 🌿',
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 5,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      color: const Color(0xFF1A1D26),
      child: Padding(
        padding: const EdgeInsets.all(18.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Title Header
            const Row(
              children: [
                Icon(Icons.assignment_turned_in_outlined, color: Colors.tealAccent, size: 22),
                SizedBox(width: 8),
                Text(
                  '일일 맞춤 건강 퀘스트',
                  style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 10),

            // Friendly Greeting
            Text(
              friendlyGreeting,
              style: TextStyle(color: Colors.grey[400], fontSize: 12, height: 1.3),
            ),
            const SizedBox(height: 16),

            // Quest Item Cards
            Column(
              children: quests.map((quest) => _buildQuestCard(context, quest)).toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuestCard(BuildContext context, Map<String, dynamic> quest) {
    int current = quest["current"] ?? 0;
    int target = quest["target"] ?? 1;
    bool isDone = current >= target;
    double progress = (current / target).clamp(0.0, 1.0);

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFF242836),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: isDone ? Colors.tealAccent.withOpacity(0.5) : Colors.transparent,
        ),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  quest["title"] ?? "",
                  style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 6),
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: progress,
                    minHeight: 6,
                    backgroundColor: Colors.grey[800],
                    valueColor: AlwaysStoppedAnimation<Color>(
                      isDone ? Colors.tealAccent : Colors.cyanAccent,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 14),
          ElevatedButton(
            onPressed: isDone ? () => _showRewardPopup(context, quest) : null,
            style: ElevatedButton.styleFrom(
              backgroundColor: isDone ? Colors.tealAccent : Colors.grey[700],
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            ),
            child: Text(
              isDone ? '보상 받기' : '$current/$target',
              style: TextStyle(
                color: isDone ? Colors.black : Colors.white60,
                fontWeight: FontWeight.bold,
                fontSize: 11,
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showRewardPopup(BuildContext context, Map<String, dynamic> quest) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF222634),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Row(
          children: [
            Icon(Icons.stars, color: Colors.amberAccent, size: 26),
            SizedBox(width: 8),
            Text('퀘스트 달성 축하!', style: TextStyle(color: Colors.white, fontSize: 16)),
          ],
        ),
        content: Text(
          '멋지게 해내셨어요! 정령이 고마운 마음을 담아 골드 +${quest["reward_gold"]} 및 친밀도 경험치를 전달했습니다 ✨',
          style: const TextStyle(color: Colors.white70, fontSize: 13, height: 1.4),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('기분 좋게 받기', style: TextStyle(color: Colors.tealAccent, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}