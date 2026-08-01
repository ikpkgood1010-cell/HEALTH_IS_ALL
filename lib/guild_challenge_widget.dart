import 'package:flutter/material.dart';

/// HEALTH IS ALL - Social Guild Challenge & Co-op Spirit Widget
/// Filename: guild_challenge_widget.dart
/// Path: HEALTH IS ALL/lib/guild_challenge_widget.dart
/// Purpose: 길드 수호 정령 거대진화 현황 및 길드원 함께 걷기 챌린지 UI
class GuildChallengeWidget extends StatelessWidget {
  final String guardianStage;
  final int totalGuildSteps;
  final int targetGuildSteps;
  final String friendlyMessage;

  const GuildChallengeWidget({
    Key? key,
    this.guardianStage = 'SKY_WARDEN',
    this.totalGuildSteps = 18700,
    this.targetGuildSteps = 30000,
    this.friendlyMessage = '오늘 길드원들과 함께 모은 발걸음이 수호 정령에게 따스한 온기를 전했습니다 🌿',
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    double progress = (totalGuildSteps / targetGuildSteps).clamp(0.0, 1.0);

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
                    Icon(Icons.shield_outlined, color: Colors.amberAccent, size: 22),
                    SizedBox(width: 8),
                    Text(
                      '길드 수호 정령 챌린지',
                      style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.amberAccent.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.amberAccent),
                  ),
                  child: Text(
                    guardianStage,
                    style: const TextStyle(color: Colors.amberAccent, fontSize: 11, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            // Guardian Avatar Visual
            Center(
              child: Column(
                children: [
                  Container(
                    width: 90,
                    height: 90,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: Colors.amberAccent.withOpacity(0.1),
                      border: Border.all(color: Colors.amberAccent, width: 2),
                    ),
                    child: const Center(
                      child: Text('🐉', style: TextStyle(fontSize: 48)),
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    friendlyMessage,
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.grey[400], fontSize: 12, height: 1.3),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Co-op Progress Bar
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('길드 공동 걸음 목표', style: TextStyle(color: Colors.white70, fontSize: 12)),
                    Text(
                      '$totalGuildSteps / $targetGuildSteps 보',
                      style: const TextStyle(color: Colors.amberAccent, fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: LinearProgressIndicator(
                    value: progress,
                    minHeight: 10,
                    backgroundColor: Colors.grey[800],
                    valueColor: const AlwaysStoppedAnimation<Color>(Colors.amberAccent),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            // Cheer Action Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () => _showCheerDialog(context),
                icon: const Icon(Icons.favorite_rounded, size: 18),
                label: const Text('길드원들에게 따뜻한 응원 보내기'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF2C3142),
                  foregroundColor: Colors.amberAccent,
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

  void _showCheerDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF222634),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Row(
          children: [
            Text('💌', style: TextStyle(fontSize: 24)),
            SizedBox(width: 8),
            Text('따뜻한 길드 응원', style: TextStyle(color: Colors.white, fontSize: 16)),
          ],
        ),
        content: const Text(
          '오늘도 함께 걸어주시는 길드원분들께 다정한 응원 하트를 전달했습니다! 정령의 온기가 더해집니다 ✨',
          style: TextStyle(color: Colors.white70, fontSize: 13, height: 1.4),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('확인', style: TextStyle(color: Colors.amberAccent, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}