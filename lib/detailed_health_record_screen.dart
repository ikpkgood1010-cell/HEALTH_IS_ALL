import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'api_client.dart';
import 'api_data_provider.dart';
import 'daily_health_review_screen.dart';

class DetailedHealthRecordScreen extends StatefulWidget {
  final bool isMeal;
  const DetailedHealthRecordScreen({super.key, required this.isMeal});

  @override
  State<DetailedHealthRecordScreen> createState() =>
      _DetailedHealthRecordScreenState();
}

class _DetailedHealthRecordScreenState
    extends State<DetailedHealthRecordScreen> {
  final _text = TextEditingController();
  String _mealType = '점심';
  bool _loading = false;
  HealthTextAnalysis? _analysis;
  final Map<String, double> _answers = {};

  String get _recordType => widget.isMeal ? 'meal_log' : 'workout_log';

  @override
  void dispose() {
    _text.dispose();
    super.dispose();
  }

  Future<void> _analyze() async {
    if (_text.text.trim().isEmpty) {
      _message('먹은 음식이나 수행한 운동을 문장으로 적어 주세요.');
      return;
    }
    setState(() => _loading = true);
    final provider = context.read<ApiDataProvider>();
    final result = await provider.analyzeDetailedText(
      recordType: _recordType,
      text: _text.text.trim(),
      mealType: widget.isMeal ? _mealType : null,
      answers: _answers,
    );
    if (!mounted) return;
    setState(() {
      _loading = false;
      _analysis = result;
    });
    if (result == null) _message(provider.lastError ?? '분석하지 못했습니다.');
  }

  Future<void> _choose(String id, num value) async {
    _answers[id] = value.toDouble();
    await _analyze();
  }

  Future<void> _acceptRecommendations() async {
    for (final card in _analysis?.confirmationCards ?? const []) {
      final value = card['recommended_value'];
      if (value is num) _answers['${card['id']}'] = value.toDouble();
    }
    await _analyze();
  }

  Future<void> _save() async {
    final analysis = _analysis;
    if (analysis == null || analysis.confirmationCards.isNotEmpty) return;
    setState(() => _loading = true);
    final provider = context.read<ApiDataProvider>();
    final result = await provider.logAnalyzedRecord(analysis);
    if (!mounted) return;
    setState(() => _loading = false);
    if (result == null) {
      _message(provider.lastError ?? '저장하지 못했습니다.');
      return;
    }
    await showDialog<void>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text('기록을 저장했어요'),
        content: Text(
          '실제 지급: Exp ${result.expGained} · 건강 정수 ${result.healthEssenceEarned}\n'
          '오늘 전체 기록과 영양·운동 분석도 확인할 수 있어요.',
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(dialogContext);
              Navigator.pop(context);
            },
            child: const Text('닫기'),
          ),
          FilledButton(
            onPressed: () {
              Navigator.pop(dialogContext);
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (_) => const DailyHealthReviewScreen(),
                ),
              );
            },
            child: const Text('오늘 상세 리뷰'),
          ),
        ],
      ),
    );
  }

  void _message(String text) =>
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(text)));

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.isMeal ? '상세 식단 기록' : '상세 운동 기록')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
        children: [
          Text(
            widget.isMeal
                ? '먹은 순서·제품명·수량·조리법을 평소 말하듯 적어 주세요.'
                : '운동 종류·시간·횟수·세트·휴식·강도를 평소 말하듯 적어 주세요.',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          const Text('평균값으로 먼저 계산하고, 결과에 영향이 큰 애매한 내용만 선택 카드로 확인합니다.'),
          if (widget.isMeal) ...[
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              initialValue: _mealType,
              decoration: const InputDecoration(
                labelText: '식사 종류',
                border: OutlineInputBorder(),
              ),
              items: const ['아침', '점심', '저녁', '간식']
                  .map((value) =>
                      DropdownMenuItem(value: value, child: Text(value)))
                  .toList(),
              onChanged: (value) {
                if (value != null) setState(() => _mealType = value);
              },
            ),
          ],
          const SizedBox(height: 16),
          TextField(
            controller: _text,
            minLines: 5,
            maxLines: 10,
            decoration: InputDecoration(
              labelText: widget.isMeal ? '오늘 먹은 식사' : '오늘 수행한 운동',
              hintText: widget.isMeal
                  ? '예: 양배추 한 줌을 먹고 10분 후 삶은 계란 3개를 먹었어.'
                  : '예: 20분간 크로스핏 CINDY 18라운드 후 계단을 3번 올랐어.',
              alignLabelWithHint: true,
              border: const OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 14),
          FilledButton.icon(
            onPressed: _loading ? null : _analyze,
            icon: _loading
                ? const SizedBox.square(
                    dimension: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.auto_awesome),
            label: Text(_loading ? '계산 중...' : '상세 값 계산하기'),
          ),
          if (_analysis != null) ...[
            const SizedBox(height: 20),
            _AnalysisResult(analysis: _analysis!, isMeal: widget.isMeal),
            if (_analysis!.confirmationCards.isNotEmpty) ...[
              const SizedBox(height: 16),
              Text('정확도를 높이기 위한 확인',
                  style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 8),
              ..._analysis!.confirmationCards.map(
                (card) => _ConfirmationCard(
                  card: card,
                  selected: _answers['${card['id']}'],
                  onSelected: (value) => _choose('${card['id']}', value),
                ),
              ),
              if (_analysis!.confirmationCards.every(
                (card) => (card['options'] as List? ?? const []).isNotEmpty,
              ))
                OutlinedButton(
                  onPressed: _loading ? null : _acceptRecommendations,
                  child: const Text('추천 평균값으로 모두 확인'),
                ),
            ],
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: !_loading && _analysis!.confirmationCards.isEmpty
                  ? _save
                  : null,
              icon: const Icon(Icons.check_rounded),
              label: Text(_analysis!.confirmationCards.isEmpty
                  ? '확정 결과 저장하기'
                  : '위 항목을 확인하면 저장할 수 있어요'),
            ),
          ],
        ],
      ),
    );
  }
}

class _ConfirmationCard extends StatelessWidget {
  final Map<String, dynamic> card;
  final double? selected;
  final ValueChanged<num> onSelected;
  const _ConfirmationCard({
    required this.card,
    required this.selected,
    required this.onSelected,
  });

  @override
  Widget build(BuildContext context) {
    final options = (card['options'] as List? ?? const []).whereType<Map>();
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('${card['question']}',
                style: Theme.of(context).textTheme.titleSmall),
            const SizedBox(height: 4),
            Text('${card['help']}',
                style: Theme.of(context).textTheme.bodySmall),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: options.map((option) {
                final value = option['value'] as num;
                return ChoiceChip(
                  label: Text('${option['label']}'),
                  selected: selected == value.toDouble(),
                  onSelected: (_) => onSelected(value),
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}

class _AnalysisResult extends StatelessWidget {
  final HealthTextAnalysis analysis;
  final bool isMeal;
  const _AnalysisResult({required this.analysis, required this.isMeal});

  String _number(Object? value) =>
      value is num ? value.toStringAsFixed(value % 1 == 0 ? 0 : 1) : '-';

  @override
  Widget build(BuildContext context) {
    final totals = Map<String, dynamic>.from(
      analysis.estimated['totals'] as Map? ?? const {},
    );
    final estimated = analysis.estimated;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(analysis.summary,
                style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 12),
            if (isMeal)
              Wrap(
                spacing: 16,
                runSpacing: 10,
                children: [
                  _metric('열량', '${_number(totals['kcal'])} kcal'),
                  _metric('탄수화물', '${_number(totals['carbs_g'])} g'),
                  _metric('단백질', '${_number(totals['protein_g'])} g'),
                  _metric('지방', '${_number(totals['fat_g'])} g'),
                  _metric('식이섬유', '${_number(totals['fiber_g'])} g'),
                  _metric('식단점수', '${_number(estimated['meal_score'])}점'),
                  _metric(
                      '식품 다양성', '${_number(estimated['food_variety_count'])}종'),
                  _metric(
                    '섭취 간격',
                    (estimated['interval_minutes'] as List? ?? const []).isEmpty
                        ? '기록 없음'
                        : '${(estimated['interval_minutes'] as List).join(', ')}분',
                  ),
                ],
              )
            else
              Wrap(
                spacing: 16,
                runSpacing: 10,
                children: [
                  _metric('전체 시간', '${_number(estimated['duration_min'])}분'),
                  _metric('체감강도', 'RPE ${_number(estimated['rpe'])}'),
                  _metric('활동점수', '${_number(estimated['activity_score'])}점'),
                  _metric('운동 블록', '${_number(estimated['block_count'])}개'),
                  _metric(
                    '세트간 휴식',
                    (estimated['rest_seconds'] as List? ?? const []).isEmpty
                        ? '기록 없음'
                        : '${(estimated['rest_seconds'] as List).join(', ')}초',
                  ),
                ],
              ),
            const Divider(height: 28),
            if (analysis.sources.isNotEmpty) ...[
              Text('계산 출처: ${analysis.sources.join(' · ')}'),
              const SizedBox(height: 8),
            ],
            Text(
              '예상 보상: Exp ${analysis.rewardPreview['base_exp']} · 건강 정수 ${analysis.rewardPreview['health_essence']}',
            ),
            const SizedBox(height: 4),
            const Text('※ 저장 시 서버의 일일 한도와 중복 방지 규칙을 적용한 실제 보상이 확정됩니다.'),
          ],
        ),
      ),
    );
  }

  Widget _metric(String label, String value) => SizedBox(
        width: 105,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label),
            Text(value, style: const TextStyle(fontWeight: FontWeight.bold))
          ],
        ),
      );
}
