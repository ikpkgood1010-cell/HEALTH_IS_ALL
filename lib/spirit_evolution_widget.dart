import 'package:flutter/material.dart';

/// HEALTH IS ALL - Spirit Evolution & Interactive Dialogue Widget
/// Filename: spirit_evolution_widget.dart
/// Path: HEALTH IS ALL/lib/spirit_evolution_widget.dart
/// Purpose: 정령 4대 속성 시각화, 진화 단계 표시 및 터치 반응 호감형 대화 팝업 UI
class SpiritEvolutionWidget extends StatelessWidget {
  final String dominantElement;
  final String evolutionStage;
  final double fireScore;
  final double waterScore;
  final double earthScore;
  final double lightScore;
  final String friendlyDialogue;

  const SpiritEvolutionWidget({
    Key? key,
    this.dominantElement = 'LIGHT',
    this.evolutionStage = 'JUNIOR',
    this.fireScore = 120.0,
    this.waterScore = 140.0,
    this.earthScore = 110.0,
    this.lightScore = 210.0,
    this.friendlyDialogue = '✨ 완벽한 영양 균형에 정령이 눈부신 빛의 아우라를 감싸 안았습니다!',
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Color elementColor = _getElementColor(dominantElement);

    return Card(
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      color: const Color(0xFF1A1D26),
      child: Padding(
        padding: const EdgeInsets.all(18.0),
        child: Column(
          children: [
            // Top Stage Badge
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'AI 속성 정령',
                  style: TextStyle(color: Colors.grey[400], fontSize: 13, fontWeight: FontWeight.bold),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: elementColor.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: elementColor),
                  ),
                  child: Text(
                    '$evolutionStage 단계 · $dominantElement',
                    style: TextStyle(color: elementColor, fontSize: 11, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Spirit Avatar Touch Target
            GestureDetector(
              onTap: () => _showSpiritDialogueModal(context, elementColor),
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 300),
                width: 110,
                height: 110,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: elementColor.withOpacity(0.15),
                  border: Border.all(color: elementColor, width: 3),
                  boxShadow: [
                    BoxShadow(color: elementColor.withOpacity(0.3), blurRadius: 15, spreadRadius: 2),
                  ],
                ),
                child: Center(
                  child: Text(
                    _getSpiritEmoji(dominantElement),
                    style: const TextStyle(fontSize: 52),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 12),
            Text(
              '탭하여 정령과 교감하기 👆',
              style: TextStyle(color: Colors.grey[500], fontSize: 11),
            ),
            const SizedBox(height: 16),

            // 4-Elemental Score Progress Bars
            Column(
              children: [
                _buildElementRow('🔥 불 (단백질/근력)', fireScore, Colors.orangeAccent),
                _buildElementRow('💧 물 (유산소/수분)', waterScore, Colors.cyanAccent),
                _buildElementRow('🌿 풀 (식이섬유/휴식)', earthScore, Colors.lightGreenAccent),
                _buildElementRow('✨ 빛 (영양 균형)', lightScore, Colors.amberAccent),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildElementRow(String label, double score, Color color) {
    double ratio = (score / 300.0).clamp(0.0, 1.0);
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3.0),
      child: Row(
        children: [
          SizedBox(
            width: 130,
            child: Text(label, style: const TextStyle(color: Colors.white70, fontSize: 11)),
          ),
          Expanded(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(6),
              child: LinearProgressIndicator(
                value: ratio,
                minHeight: 8,
                backgroundColor: Colors.grey[800],
                valueColor: AlwaysStoppedAnimation<Color>(color),
              ),
            ),
          ),
          const SizedBox(width: 8),
          SizedBox(
            width: 35,
            child: Text('${score.toInt()}', style: TextStyle(color: color, fontSize: 11, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  Color _getElementColor(String element) {
    switch (element) {
      case 'FIRE': return Colors.orangeAccent;
      case 'WATER': return Colors.cyanAccent;
      case 'EARTH': return Colors.lightGreenAccent;
      default: return Colors.amberAccent;
    }
  }

  String _getSpiritEmoji(String element) {
    switch (element) {
      case 'FIRE': return '🦊';
      case 'WATER': return '🐬';
      case 'EARTH': return '🦌';
      default: return '🦄';
    }
  }

  void _showSpiritDialogueModal(BuildContext context, Color themeColor) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF222634),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            Text(_getSpiritEmoji(dominantElement), style: const TextStyle(fontSize: 28)),
            const SizedBox(width: 10),
            const Text('정령의 따뜻한 한마디', style: TextStyle(color: Colors.white, fontSize: 16)),
          ],
        ),
        content: Text(
          friendlyDialogue,
          style: const TextStyle(color: Colors.white70, fontSize: 13, height: 1.4),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: Text('기분 좋게 마음 나누기', style: TextStyle(color: themeColor, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}