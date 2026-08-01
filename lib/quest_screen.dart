import 'package:flutter/material.dart';

/// HEALTH IS ALL - Daily Health Quests Screen
/// Dual-Excellence: 건강 목표 달성과 Exp 보상 연동
class QuestScreen extends StatefulWidget {
  const QuestScreen({Key? key}) : super(key: key);

  @override
  State<QuestScreen> createState() => _QuestScreenState();
}

class _QuestScreenState extends State<QuestScreen> {
  final List<Map<String, dynamic>> _quests = [
    {
      'id': 'q1',
      'title': '건강 식단 2회 기록하기',
      'progress': 1,
      'target': 2,
      'reward': 40,
      'isClaimed': false,
      'icon': Icons.restaurant,
    },
    {
      'id': 'q2',
      'title': '30분 이상 운동 완수',
      'progress': 30,
      'target': 30,
      'reward': 60,
      'isClaimed': false,
      'icon': Icons.fitness_center,
    },
    {
      'id': 'q3',
      'title': '수분 섭취 1.5L 달성',
      'progress': 1.0,
      'target': 1.5,
      'reward': 30,
      'isClaimed': false,
      'icon': Icons.water_drop,
    },
  ];

  void _claimReward(int index) {
    setState(() {
      _quests[index]['isClaimed'] = true;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text("${_quests[index]['reward']} Exp 보상을 수령했습니다! '건강이'가 기뻐합니다."),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('일일 건강 퀘스트', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 1,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: _quests.length,
        itemBuilder: (context, index) {
          final q = _quests[index];
          final double progress = (q['progress'] as num).toDouble();
          final double target = (q['target'] as num).toDouble();
          final bool isDone = progress >= target;
          final bool isClaimed = q['isClaimed'] as bool;

          return Container(
            margin: const EdgeInsets.only(bottom: 12.0),
            padding: const EdgeInsets.all(16.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.04),
                  blurRadius: 6,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(q['icon'] as IconData, color: Colors.blueAccent),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        q['title'] as String,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                      ),
                    ),
                    Chip(
                      label: Text(
                        "+${q['reward']} Exp",
                        style: const TextStyle(color: Colors.purple, fontWeight: FontWeight.bold),
                      ),
                      backgroundColor: Colors.purple.shade50,
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                LinearProgressIndicator(
                  value: (progress / target).clamp(0.0, 1.0),
                  backgroundColor: Colors.grey.shade200,
                  color: isDone ? Colors.green : Colors.blue,
                  minHeight: 8,
                ),
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      '진행도: ${q['progress']} / ${q['target']}',
                      style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                    ),
                    ElevatedButton(
                      onPressed: (isDone && !isClaimed) ? () => _claimReward(index) : null,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: isClaimed ? Colors.grey : Colors.green,
                      ),
                      child: Text(isClaimed ? '수령 완료' : (isDone ? '보상 수령' : '진행 중')),
                    ),
                  ],
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
