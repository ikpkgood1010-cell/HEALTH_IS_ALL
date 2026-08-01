import 'package:flutter/material.dart';

/// HEALTH IS ALL - AI Nutrition Analytics & Clean Recipe Card Widget
/// Filename: nutrition_analytics_widget.dart
/// Path: HEALTH IS ALL/lib/nutrition_analytics_widget.dart
/// Purpose: 영양 결핍 심화 분석 시각화 및 맞춤 클린 추천 레시피 카드 UI
class NutritionAnalyticsWidget extends StatelessWidget {
  final double deficiencyIndex;
  final String recommendedRecipe;
  final String recipeDescription;
  final String spiritAdvice;

  const NutritionAnalyticsWidget({
    Key? key,
    this.deficiencyIndex = 0.15,
    this.recommendedRecipe = '🥩 담백한 돼지목살 양파 찜',
    this.recipeDescription = '기름기를 줄이고 원재료의 수분과 단백질을 정갈하게 채우는 스팀 요리입니다.',
    this.spiritAdvice = '싱그러운 야채와 수분을 조금 더 채워주시면 정령이 더욱 예쁜 싹을 틔울 거예요 🌿',
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
            const Row(
              children: [
                Icon(Icons.analytics_outlined, color: Colors.lightGreenAccent, size: 22),
                SizedBox(width: 8),
                Text(
                  'AI 식단 영양 진단',
                  style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Spirit Advice Bubble
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFF242836),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: Colors.lightGreenAccent.withOpacity(0.3)),
              ),
              child: Row(
                children: [
                  const Text('🌿', style: TextStyle(fontSize: 26)),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      spiritAdvice,
                      style: const TextStyle(color: Colors.white70, fontSize: 12, height: 1.3),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Recipe Card
            const Text(
              '오늘의 다정한 맞춤 추천 식단',
              style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFF2C3142),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    recommendedRecipe,
                    style: const TextStyle(color: Colors.lightGreenAccent, fontSize: 14, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    recipeDescription,
                    style: TextStyle(color: Colors.grey[300], fontSize: 12, height: 1.3),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // Recipe Modal Button
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () => _showRecipeDetailModal(context),
                icon: const Icon(Icons.restaurant_menu_rounded, size: 18),
                label: const Text('레시피 조리법 자세히 보기'),
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.lightGreenAccent,
                  side: const BorderSide(color: Colors.lightGreenAccent),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showRecipeDetailModal(BuildContext context) {
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
            Text(
              recommendedRecipe,
              style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            const Text(
              '1. 찜기에 얇게 썬 양파를 깔아줍니다.\n2. 신선한 목살을 올리고 부드럽게 스팀으로 익혀 기름기를 뺍니다.\n3. 설탕이나 밀가루 대신 천연 감미료와 자극적이지 않은 양념으로 마무리합니다.',
              style: TextStyle(color: Colors.white70, fontSize: 13, height: 1.5),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => Navigator.pop(ctx),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.lightGreenAccent,
                  foregroundColor: Colors.black,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('확인', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}