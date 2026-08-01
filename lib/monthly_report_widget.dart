import 'package:flutter/material.dart';

/// HEALTH IS ALL - Monthly Healing Report & Spirit Album Card Widget
/// Filename: monthly_report_widget.dart
/// Path: HEALTH IS ALL/lib/monthly_report_widget.dart
/// Purpose: 월간 건강 개선 지수(MHII) 및 정령 도감 앨범 요약 프론트엔드 UI
class MonthlyReportWidget extends StatelessWidget {
  final double mhiiScore;
  final String badgeName;
  final String spiritComment;
  final int unlockedSnapshots;

  const MonthlyReportWidget({
    Key? key,
    this.mhiiScore = 88.5,
    this.badgeName = '🌟 푸른 정원의 수호자',
    this.spiritComment = '이번 달은 정말 눈부신 한 달이었어요! 평균 8,500보를 걸으시며 정령의 정원을 푸르게 피워내셨습니다 ✨',
    this.unlockedSnapshots = 3,
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
                const Row(
                  children: [
                    Icon(Icons.calendar_month_rounded, color: Colors.cyanAccent, size: 22),
                    SizedBox(width: 8),
                    Text(
                      '월간 힐링 리포트',
                      style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.cyanAccent.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.cyanAccent),
                  ),
                  child: Text(
                    'MHII $mhiiScore점',
                    style: const TextStyle(color: Colors.cyanAccent, fontSize: 12, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            // Badge & Comment Box
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFF242836),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    badgeName,
                    style: const TextStyle(color: Colors.amberAccent, fontSize: 13, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    spiritComment,
                    style: TextStyle(color: Colors.grey[300], fontSize: 12, height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Spirit Album Quick Access Row
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Text('📸', style: TextStyle(fontSize: 18)),
                    const SizedBox(width: 6),
                    Text(
                      '수집한 힐링 스냅샷 ($unlockedSnapshots개)',
                      style: const TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ],
                ),
                TextButton(
                  onPressed: () => _showAlbumModal(context),
                  child: const Text('앨범 보기', style: TextStyle(color: Colors.cyanAccent, fontSize: 12)),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  void _showAlbumModal(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF222634),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '🖼️ 수호 정령 힐링 앨범',
              style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 14),
            ListTile(
              leading: const Text('🍃', style: TextStyle(fontSize: 28)),
              title: const Text('바람의 언덕에서 보낸 첫 걸음', style: TextStyle(color: Colors.white, fontSize: 13)),
              subtitle: const Text('누적 5만 보 달성 기공 메모리', style: TextStyle(color: Colors.grey, fontSize: 11)),
            ),
            ListTile(
              leading: const Text('🥩', style: TextStyle(fontSize: 28)),
              title: const Text('담백한 스팀 오프닝', style: TextStyle(color: Colors.white, fontSize: 13)),
              subtitle: const Text('클린 식단 20회 달성 메모리', style: TextStyle(color: Colors.grey, fontSize: 11)),
            ),
            const SizedBox(height: 10),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => Navigator.pop(ctx),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.cyanAccent,
                  foregroundColor: Colors.black,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('닫기', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}