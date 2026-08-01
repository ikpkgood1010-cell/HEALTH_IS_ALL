/// HEALTH IS ALL - Interactive Spirit Widget V2
/// 건강 UI 가시성을 해치지 않으며 정령 애니메이션 및 공감 메시지를 표시하는 Flutter 위젯

import 'package:flutter/material.dart';

class InteractiveSpiritWidgetV2 extends StatelessWidget {
  final String spiritName;
  final String dialogueLine1;
  final String dialogueLine2;
  final String dialogueLine3;
  final double affinityProgress; // 0.0 ~ 1.0

  const InteractiveSpiritWidgetV2({
    Key? key,
    required this.spiritName,
    required this.dialogueLine1,
    required this.dialogueLine2,
    required this.dialogueLine3,
    required this.affinityProgress,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 12.0, horizontal: 16.0),
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: Colors.lightGreen.shade50,
        borderRadius: BorderRadius.circular(16.0),
        border: Border.all(color: Colors.green.shade200, width: 1.5),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.eco, color: Colors.green.shade700, size: 28),
              const SizedBox(width: 8),
              Text(
                spiritName,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.green.shade900,
                ),
              ),
              const Spacer(),
              Text(
                "친밀도 ${(affinityProgress * 100).toInt()}%",
                style: TextStyle(fontSize: 14, color: Colors.green.shade800),
              ),
            ],
          ),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: LinearProgressIndicator(
              value: affinityProgress,
              backgroundColor: Colors.green.shade100,
              valueColor: AlwaysStoppedAnimation<Color>(Colors.green.shade600),
              minHeight: 8,
            ),
          ),
          const SizedBox(height: 12),
          // 모바일 자동 줄바꿈 및 잘림 방지 3줄 대화 카드
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12.0),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  dialogueLine1,
                  style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: Colors.black80),
                  softWrap: true,
                ),
                const SizedBox(height: 4),
                Text(
                  dialogueLine2,
                  style: const TextStyle(fontSize: 13, color: Colors.black70),
                  softWrap: true,
                ),
                const SizedBox(height: 4),
                Text(
                  dialogueLine3,
                  style: const TextStyle(fontSize: 13, color: Colors.black70),
                  softWrap: true,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}