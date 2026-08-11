import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'api_data_provider.dart';
import 'app_theme.dart';
import 'exercise_catalog.dart';

class WorkoutScreen extends StatefulWidget {
  const WorkoutScreen({super.key});

  @override
  State<WorkoutScreen> createState() => _WorkoutScreenState();
}

class _WorkoutScreenState extends State<WorkoutScreen> {
  ExerciseCategoryGroup _group = ExerciseCategoryGroup.cardio;
  late ExerciseDefinition _exercise;
  IntensityLevel _intensity = IntensityLevel.high;
  int _durationMinutes = 30;
  int _rpe = 6;
  String _condition = 'NORMAL';
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    _exercise = _exercisesFor(_group).first;
    _intensity = _exercise.recommendedIntensity;
  }

  List<ExerciseDefinition> _exercisesFor(ExerciseCategoryGroup group) =>
      exerciseCatalog.where((item) => item.group == group).toList();

  double get _estimatedCalories {
    final factor = switch (_intensity) {
      IntensityLevel.low => .85,
      IntensityLevel.medium => 1.0,
      IntensityLevel.high => 1.25,
    };
    return _exercise.met * 70 * (_durationMinutes / 60) * factor;
  }

  Future<void> _save() async {
    setState(() => _saving = true);
    final provider = context.read<ApiDataProvider>();
    final result = await provider.logWorkout(
      _durationMinutes,
      _estimatedCalories.round(),
      exerciseCategoryGroup: _group.name.toUpperCase(),
      exerciseCategory: _exercise.code,
      intensityLevel: intensityCode(_intensity),
      rpe: _rpe,
      conditionScore: _condition,
    );
    if (!mounted) return;
    setState(() => _saving = false);

    if (provider.lastError != null || result == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(provider.lastError!)),
      );
      return;
    }
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          result.duplicate ? result.message : '운동 기록을 저장했어요. 모험 활력에 반영됩니다.',
        ),
      ),
    );
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final groupExercises = _exercisesFor(_group);
    return Scaffold(
      appBar: AppBar(title: const Text('운동 기록하기')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
        children: [
          Card(
            color: AppColors.primary100,
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  Text('예상 소모 칼로리', style: AppTypography.captionSm),
                  const SizedBox(height: 6),
                  Text(
                    '${_estimatedCalories.toStringAsFixed(0)} kcal',
                    style: AppTypography.displayLg
                        .copyWith(color: AppColors.primary700),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${_exercise.label} · ${intensityLabel(_intensity)} · METs 기준',
                    textAlign: TextAlign.center,
                    style: AppTypography.captionSm,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          DropdownButtonFormField<ExerciseCategoryGroup>(
            initialValue: _group,
            decoration: const InputDecoration(
              labelText: '1. 운동 대분류',
              border: OutlineInputBorder(),
            ),
            items: ExerciseCategoryGroup.values
                .map((group) => DropdownMenuItem(
                      value: group,
                      child: Text(groupLabel(group)),
                    ))
                .toList(),
            onChanged: (value) {
              if (value == null) return;
              setState(() {
                _group = value;
                _exercise = _exercisesFor(value).first;
                _intensity = _exercise.recommendedIntensity;
              });
            },
          ),
          const SizedBox(height: 14),
          DropdownButtonFormField<ExerciseDefinition>(
            key: ValueKey(_group),
            initialValue: _exercise,
            decoration: const InputDecoration(
              labelText: '2. 운동 종목',
              border: OutlineInputBorder(),
            ),
            items: groupExercises
                .map((exercise) => DropdownMenuItem(
                      value: exercise,
                      child: Text(exercise.label),
                    ))
                .toList(),
            onChanged: (value) {
              if (value == null) return;
              setState(() {
                _exercise = value;
                _intensity = value.recommendedIntensity;
              });
            },
          ),
          const SizedBox(height: 22),
          Text('3. 수행 강도', style: AppTypography.titleMd),
          const SizedBox(height: 8),
          SegmentedButton<IntensityLevel>(
            segments: IntensityLevel.values
                .map((level) => ButtonSegment(
                      value: level,
                      label: Text(intensityLabel(level)),
                    ))
                .toList(),
            selected: {_intensity},
            onSelectionChanged: (selection) =>
                setState(() => _intensity = selection.first),
          ),
          const SizedBox(height: 22),
          Text('운동 시간: $_durationMinutes분', style: AppTypography.titleMd),
          Slider(
            value: _durationMinutes.toDouble(),
            min: 10,
            max: 120,
            divisions: 22,
            label: '$_durationMinutes분',
            onChanged: (value) =>
                setState(() => _durationMinutes = value.round()),
          ),
          const SizedBox(height: 14),
          Text('체감 강도(RPE): $_rpe / 10', style: AppTypography.titleMd),
          Slider(
            value: _rpe.toDouble(),
            min: 1,
            max: 10,
            divisions: 9,
            label: '$_rpe',
            onChanged: (value) => setState(() => _rpe = value.round()),
          ),
          Text(_rpeGuide(_rpe), style: AppTypography.captionSm),
          const SizedBox(height: 22),
          Text('오늘의 컨디션', style: AppTypography.titleMd),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: const {
              'EXCELLENT': '⚡ 최상',
              'GOOD': '😊 좋음',
              'NORMAL': '😐 보통',
              'POOR': '😴 피곤',
              'CRITICAL': '⚠️ 경고',
            }
                .entries
                .map((entry) => ChoiceChip(
                      label: Text(entry.value),
                      selected: _condition == entry.key,
                      onSelected: (_) => setState(() => _condition = entry.key),
                    ))
                .toList(),
          ),
          const SizedBox(height: 28),
          ElevatedButton.icon(
            onPressed: _saving ? null : _save,
            icon: _saving
                ? const SizedBox.square(
                    dimension: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.check_rounded),
            label: Text(_saving ? '저장 중...' : '운동 기록 저장'),
          ),
        ],
      ),
    );
  }
}

String _rpeGuide(int rpe) {
  if (rpe <= 4) return '가벼움 · 편안하게 대화할 수 있어요.';
  if (rpe <= 7) return '적당함 · 숨은 차지만 짧은 대화가 가능해요.';
  if (rpe <= 9) return '힘듦 · 1~2회 정도만 더 할 수 있어요.';
  return '한계 · 무리하지 말고 회복 시간을 충분히 확보하세요.';
}
