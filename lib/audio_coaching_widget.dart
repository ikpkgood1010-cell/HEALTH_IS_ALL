import 'package:flutter/material.dart';

/// HEALTH IS ALL - AI Audio Coaching & Spirit Voice Widget
/// Filename: audio_coaching_widget.dart
/// Path: HEALTH IS ALL/lib/audio_coaching_widget.dart
/// Purpose: 운동 중 실시간 음성 가이드 상태 시각화 및 정령 보이스 인터랙션 UI
class AudioCoachingWidget extends StatefulWidget {
  final int currentHr;
  final String voiceScript;
  final bool shouldSlowDown;

  const AudioCoachingWidget({
    Key? key,
    this.currentHr = 138,
    this.voiceScript = '완벽한 페이스예요! 현재 최적 유산소 구간에 있습니다. 정령이 발걸음을 응원해요 ✨',
    this.shouldSlowDown = false,
  }) : super(key: key);

  @override
  State<AudioCoachingWidget> createState() => _AudioCoachingWidgetState();
}

class _AudioCoachingWidgetState extends State<AudioCoachingWidget> {
  bool isAudioPlaying = true;

  @override
  Widget build(BuildContext context) {
    Color statusColor = widget.shouldSlowDown ? Colors.orangeAccent : Colors.tealAccent;

    return Card(
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      color: const Color(0xFF1A1D26),
      child: Padding(
        padding: const EdgeInsets.all(18.0),
        child: Column(
          children: [
            // Header Row
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(
                  children: [
                    Icon(Icons.record_voice_over_rounded, color: Colors.cyanAccent, size: 20),
                    SizedBox(width: 8),
                    Text(
                      'AI 정령 음성 코칭',
                      style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                IconButton(
                  icon: Icon(
                    isAudioPlaying ? Icons.volume_up_rounded : Icons.volume_off_rounded,
                    color: isAudioPlaying ? Colors.cyanAccent : Colors.grey,
                  ),
                  onPressed: () {
                    setState(() {
                      isAudioPlaying = !isAudioPlaying;
                    });
                  },
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Live Heart Rate & Voice Bubble
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFF242836),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: statusColor.withOpacity(0.4)),
              ),
              child: Row(
                children: [
                  CircleAvatar(
                    backgroundColor: statusColor.withOpacity(0.2),
                    radius: 24,
                    child: Icon(
                      widget.shouldSlowDown ? Icons.warning_amber_rounded : Icons.favorite_rounded,
                      color: statusColor,
                      size: 26,
                    ),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '현재 심박수: ${widget.currentHr} BPM',
                          style: TextStyle(color: statusColor, fontSize: 12, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          widget.voiceScript,
                          style: const TextStyle(color: Colors.white70, fontSize: 12, height: 1.3),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // Action Button
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () => _showVoiceSettingsModal(context),
                icon: const Icon(Icons.graphic_eq_rounded, size: 18),
                label: const Text('음성 가이드 스타일 변경'),
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.tealAccent,
                  side: const BorderSide(color: Colors.tealAccent),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showVoiceSettingsModal(BuildContext context) {
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
              '정령 음성 톤앤매너 설정',
              style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            const Text(
              '유저님의 취향에 맞는 다정하고 따뜻한 목소리 스타일을 선택하실 수 있습니다.',
              style: TextStyle(color: Colors.white60, fontSize: 12),
            ),
            const SizedBox(height: 16),
            ListTile(
              leading: const Text('✨', style: TextStyle(fontSize: 24)),
              title: const Text('다정한 자상함 모드', style: TextStyle(color: Colors.white, fontSize: 13)),
              onTap: () => Navigator.pop(ctx),
            ),
            ListTile(
              leading: const Text('🔥', style: TextStyle(fontSize: 24)),
              title: const Text('열정적인 응원 모드', style: TextStyle(color: Colors.white, fontSize: 13)),
              onTap: () => Navigator.pop(ctx),
            ),
          ],
        ),
      ),
    );
  }
}