import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'api_client.dart';
import 'api_data_provider.dart';

class DailyHealthReviewScreen extends StatefulWidget {
  const DailyHealthReviewScreen({super.key});

  @override
  State<DailyHealthReviewScreen> createState() =>
      _DailyHealthReviewScreenState();
}

class _DailyHealthReviewScreenState extends State<DailyHealthReviewScreen> {
  late Future<DailyHealthReview?> _future;

  @override
  void initState() {
    super.initState();
    _future = context.read<ApiDataProvider>().fetchDailyHealthReview();
  }

  void _reload() => setState(() {
        _future = context.read<ApiDataProvider>().fetchDailyHealthReview();
      });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('오늘 건강 상세 리뷰'),
        actions: [
          IconButton(onPressed: _reload, icon: const Icon(Icons.refresh))
        ],
      ),
      body: FutureBuilder<DailyHealthReview?>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final review = snapshot.data;
          if (review == null) {
            return Center(
              child: FilledButton.icon(
                onPressed: _reload,
                icon: const Icon(Icons.refresh),
                label: const Text('다시 불러오기'),
              ),
            );
          }
          return _ReviewBody(review: review);
        },
      ),
    );
  }
}

class _ReviewBody extends StatelessWidget {
  final DailyHealthReview review;
  const _ReviewBody({required this.review});

  String _n(Object? value) => value is num
      ? value.toStringAsFixed(value.toDouble() % 1 == 0 ? 0 : 1)
      : '-';

  @override
  Widget build(BuildContext context) {
    final d = review.data;
    final n = review.nutrition;
    final low = review.nutritionLow;
    final high = review.nutritionHigh;
    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 36),
      children: [
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: [
            _summary('식사', '${d['meal_count']}회'),
            _summary('운동', '${d['workout_count']}회'),
            _summary('획득 Exp', '${d['exp_earned']}'),
            _summary('건강 정수', '${d['health_essence_earned']}'),
          ],
        ),
        const SizedBox(height: 18),
        Text('오늘의 추정 영양소', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 8),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                _nutrient('열량', 'kcal', 'kcal', n, low, high),
                _nutrient('탄수화물', 'carbs_g', 'g', n, low, high),
                _nutrient('단백질', 'protein_g', 'g', n, low, high),
                _nutrient('지방', 'fat_g', 'g', n, low, high),
                _nutrient('식이섬유', 'fiber_g', 'g', n, low, high),
                const Divider(),
                _row('평균 식단점수', '${_n(d['meal_score'])}점'),
                _row('총 운동시간', '${_n(d['workout_minutes'])}분'),
              ],
            ),
          ),
        ),
        const SizedBox(height: 18),
        Text('식사별 상세', style: Theme.of(context).textTheme.titleLarge),
        if (review.meals.isEmpty)
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 16),
            child: Text('오늘 저장한 상세 식단이 아직 없어요.'),
          ),
        ...review.meals.map(_mealTile),
        const SizedBox(height: 18),
        Text('운동별 상세', style: Theme.of(context).textTheme.titleLarge),
        if (review.workouts.isEmpty)
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 16),
            child: Text('오늘 저장한 상세 운동이 아직 없어요.'),
          ),
        ...review.workouts.map(_workoutTile),
        const SizedBox(height: 20),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('ⓘ 계산 산출 기준',
                    style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(height: 6),
                const Text(
                    '식품은 국가표준식품성분표와 USDA 평균값, 운동은 사용자가 확정한 시간·횟수·RPE를 우선합니다.'),
                const SizedBox(height: 6),
                Text('${d['disclaimer'] ?? '추정값은 의료 진단이나 치료 기준이 아닙니다.'}'),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _summary(String label, String value) => Container(
        width: 150,
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Colors.blueGrey.shade50,
          borderRadius: BorderRadius.circular(14),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label),
            Text(value,
                style:
                    const TextStyle(fontSize: 20, fontWeight: FontWeight.bold))
          ],
        ),
      );

  Widget _nutrient(
          String label,
          String key,
          String unit,
          Map<String, dynamic> value,
          Map<String, dynamic> low,
          Map<String, dynamic> high) =>
      _row(
          label, '${_n(value[key])} $unit  (${_n(low[key])}~${_n(high[key])})');

  Widget _row(String left, String right) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 5),
        child: Row(
          children: [
            Expanded(child: Text(left)),
            Text(right, style: const TextStyle(fontWeight: FontWeight.w600))
          ],
        ),
      );

  Widget _mealTile(Map<String, dynamic> meal) {
    final totals =
        Map<String, dynamic>.from(meal['totals'] as Map? ?? const {});
    final items = (meal['items'] as List? ?? const []).whereType<Map>();
    final intervals = meal['interval_minutes'] as List? ?? const [];
    final methods = meal['preparation_methods'] as List? ?? const [];
    final sources = meal['sources'] as List? ?? const [];
    return Card(
      child: ExpansionTile(
        title: Text('${meal['meal_type']} · ${_n(totals['kcal'])} kcal'),
        subtitle: Text(
            '식단점수 ${_n(meal['score'])} · Exp ${meal['exp']} · 건강 정수 ${meal['health_essence']}'),
        childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
        expandedCrossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('${meal['text'] ?? ''}'),
          const SizedBox(height: 8),
          Text(items
              .map((item) => '${item['name']} ${_n(item['grams'])}g')
              .join(' · ')),
          const SizedBox(height: 8),
          Text(
              '식품 ${meal['food_variety_count'] ?? items.length}종 · 섭취 간격 ${intervals.isEmpty ? '기록 없음' : '${intervals.join(', ')}분'} · 조리 ${methods.isEmpty ? '기록 없음' : methods.join(', ')}'),
          const SizedBox(height: 8),
          Text(
              '탄수화물 ${_n(totals['carbs_g'])}g · 단백질 ${_n(totals['protein_g'])}g · 지방 ${_n(totals['fat_g'])}g · 식이섬유 ${_n(totals['fiber_g'])}g'),
          if (sources.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text('계산 출처: ${sources.join(' · ')}'),
          ],
        ],
      ),
    );
  }

  Widget _workoutTile(Map<String, dynamic> workout) {
    final blocks = (workout['blocks'] as List? ?? const []).whereType<Map>();
    return Card(
      child: ExpansionTile(
        title:
            Text('${_n(workout['duration_min'])}분 · RPE ${_n(workout['rpe'])}'),
        subtitle: Text(
            '활동점수 ${_n(workout['activity_score'])} · Exp ${workout['exp']} · 건강 정수 ${workout['health_essence']}'),
        childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
        expandedCrossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('${workout['text'] ?? ''}'),
          const SizedBox(height: 8),
          Text(blocks
              .map((block) => '${block['label'] ?? block['type']}')
              .join(' · ')),
        ],
      ),
    );
  }
}
