import 'package:flutter/material.dart';

/// HEALTH IS ALL - Wearable Real-time Heart Rate & Spirit Pulse Sync Widget
/// Filename: wearable_sync_widget.dart
/// Path: HEALTH IS ALL/lib/wearable_sync_widget.dart
/// Purpose: 스마트 워치 연결 상태, 실시간 심박수 펄스 및 속성 에너지 UI 카드
class WearableSyncWidget extends StatelessWidget {
  final String deviceName;
  final int heartRate;
  final double activeKcal;
  final String primaryElement;
  final String syncMessage;

  const WearableSyncWidget({
    Key? key,
    this.deviceName = 'Galaxy Watch 6',
    this.heartRate = 128,
    this.activeKcal = 245.8,
    this.primaryElement = 'WIND',
    this.syncMessage = '스마트 워치와 정령이 같은 박자로 호흡 중입니다 ✨',
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      color: const Color(0xFF1A1D26),
      child: Padding(
        padding: const EdgeInsets.all(18.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header Row
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Icon(Icons.watch_rounded, color: Colors.pinkAccent, size: 22),
                    const SizedBox(width: 8),
                    Text(
                      deviceName,
                      style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.pinkAccent.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.pinkAccent),
                  ),
                  child: const Row(
                    children: [
                      CircleAvatar(radius: 3, backgroundColor: Colors.greenAccent),
                      SizedBox(width: 6),
                      Text('실시간 동기화', style: TextStyle(color: Colors.pinkAccent, fontSize: 11, fontWeight: FontWeight.bold)),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Heart Rate & Pulse Visual
            Row(
              children: [
                // Pulse Circle
                Container(
                  width: 70,
                  height: 70,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.pinkAccent.withOpacity(0.1),
                    border: Border.all(color: Colors.pinkAccent, width: 2),
                  ),
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.favorite, color: Colors.pinkAccent, size: 22),
                        const SizedBox(height: 2),
                        Text(
                          '$heartRate',
                          style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                // Stats
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('동적 소모 열량', style: TextStyle(color: Colors.white70, fontSize: 12)),
                          Text(
                            '$activeKcal kcal',
                            style: const TextStyle(color: Colors.amberAccent, fontSize: 13, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('주요 축적 속성', style: TextStyle(color: Colors.white70, fontSize: 12)),
                          Text(
                            '🍃 $primaryElement',
                            style: const TextStyle(color: Colors.lightGreenAccent, fontSize: 12, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            // Message Banner
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFF242836),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Text(
                syncMessage,
                style: TextStyle(color: Colors.grey[300], fontSize: 12, height: 1.3),
              ),
            ),
          ],
        ),
      ),
    );
  }
}