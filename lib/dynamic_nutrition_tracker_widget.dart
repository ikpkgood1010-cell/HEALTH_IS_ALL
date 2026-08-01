import 'package:flutter/material.dart';

/// HEALTH IS ALL - Dynamic Nutrition & Metabolism Tracker Widget
/// Filename: dynamic_nutrition_tracker_widget.dart
/// Path: HEALTH IS ALL/lib/dynamic_nutrition_tracker_widget.dart
/// Purpose: 다변수 영양 대사량(BMR, TEF, EPOC) 시각화 및 따뜻한 영양 가이드 팝업 UI
class DynamicNutritionTrackerWidget extends StatelessWidget {
  final double intakeKcal;
  final double dynamicTdeeKcal;
  final double tefKcal;
  final double epocKcal;
  final String friendlyFeedback;

  const DynamicNutritionTrackerWidget({
    Key? key,
    this.intakeKcal = 1850.0,
    this.dynamicTdeeKcal = 2120.0,
    this.tefKcal = 142.5,
    this.epocKcal = 38.0,
    this.friendlyFeedback = '🌿 훌륭한 활동량입니다! 따뜻한 물과 건강한 단백질 간식으로 에너지를 채워주셔도 좋아요.',
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 5,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      color: const Color(0xFF1E222D),
      child: Padding(
        padding: const EdgeInsets.all(18.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Title
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(
                  children: [
                    Icon(Icons.restaurant_menu, color: Colors.orangeAccent, size: 22),
                    SizedBox(width: 8),
                    Text(
                      'AI 정밀 영양 대사 트래커',
                      style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                IconButton(
                  icon: const Icon(Icons.info_outline, color: Colors.grey, size: 20),
                  onPressed: () => _showNutritionDetailModal(context),
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Intake vs TDEE Comparison
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildCalorieColumn('오늘 섭취 열량', '${intakeKcal.toInt()} kcal', Colors.orangeAccent),
                Container(width: 1, height: 35, color: Colors.grey[700]),
                _buildCalorieColumn('동적 소비 대사량(TDEE)', '${dynamicTdeeKcal.toInt()} kcal', Colors.cyanAccent),
              ],
            ),
            const SizedBox(height: 16),

            // Multi-variable breakdown chips (TEF & EPOC)
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildMetaChip('소화 대사열(TEF)', '+${tefKcal.toInt()} kcal', Colors.amber),
                const SizedBox(width: 10),
                _buildMetaChip('후속 소모량(EPOC)', '+${epocKcal.toInt()} kcal', Colors.lightGreenAccent),
              ],
            ),
            const SizedBox(height: 16),

            // Friendly Feedback Banner
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.orange.withOpacity(0.12),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.orangeAccent.withOpacity(0.4)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.eco, color: Colors.lightGreenAccent, size: 20),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      friendlyFeedback,
                      style: const TextStyle(color: Colors.white70, fontSize: 12, height: 1.3),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCalorieColumn(String label, String value, Color color) {
    return Column(
      children: [
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 11)),
        const SizedBox(height: 4),
        Text(value, style: TextStyle(color: color, fontSize: 18, fontWeight: FontWeight.bold)),
      ],
    );
  }

  Widget _buildMetaChip(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color.withOpacity(0.5)),
      ),
      child: Text(
        '$label: $value',
        style: TextStyle(color: color, fontSize: 11, fontWeight: FontWeight.bold),
      ),
    );
  }

  void _showNutritionDetailModal(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF2A2E3D),
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
              '💡 정밀 대사 계산 방식 안내',
              style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            Text(
              '단순 고정 칼로리가 아니라, 드신 음식을 소화시키는 데 사용되는 열량(TEF)과 운동 후 계속 소모되는 열량(EPOC), 그리고 정령 친밀도 보너스가 결합되어 매일 가장 정밀한 신체 대사량을 계산해 드립니다.',
              style: TextStyle(color: Colors.grey[300], fontSize: 13, height: 1.4),
            ),
            const SizedBox(height: 16),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: () => Navigator.of(ctx).pop(),
                child: const Text('잘 알겠어요!', style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}