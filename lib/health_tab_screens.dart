import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'api_data_provider.dart';
import 'app_theme.dart';
import 'diet_screen.dart';
import 'workout_screen.dart';

class ExerciseTabScreen extends StatelessWidget {
  const ExerciseTabScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final data = context.watch<ApiDataProvider>();
    return _RecordTab(
      title: '운동',
      headline: '${data.workoutMinutes}분',
      target: data.targetWorkoutMinutes,
      current: data.workoutMinutes,
      accent: AppColors.secondary500,
      icon: Icons.directions_run,
      message: '운동 종류·강도·시간을 기록하면 길드의 훈련장이 자라요.',
      buttonLabel: '운동 기록하기',
      onPressed: () => Navigator.of(context)
          .push(MaterialPageRoute(builder: (_) => const WorkoutScreen())),
    );
  }
}

class DietTabScreen extends StatelessWidget {
  const DietTabScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final data = context.watch<ApiDataProvider>();
    return _RecordTab(
      title: '식단',
      headline: '${data.consumedCalories} kcal',
      target: data.targetCalories,
      current: data.consumedCalories,
      accent: AppColors.primary500,
      icon: Icons.restaurant,
      message: '식사를 기록하면 영양 균형과 길드 식당의 성장을 함께 확인해요.',
      buttonLabel: '식단 기록하기',
      onPressed: () => Navigator.of(context)
          .push(MaterialPageRoute(builder: (_) => const DietScreen())),
    );
  }
}

class _RecordTab extends StatelessWidget {
  final String title;
  final String headline;
  final num target;
  final num current;
  final Color accent;
  final IconData icon;
  final String message;
  final String buttonLabel;
  final VoidCallback onPressed;

  const _RecordTab(
      {required this.title,
      required this.headline,
      required this.target,
      required this.current,
      required this.accent,
      required this.icon,
      required this.message,
      required this.buttonLabel,
      required this.onPressed});

  @override
  Widget build(BuildContext context) {
    final progress = (current / target).clamp(0, 1).toDouble();
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(icon, color: accent, size: 32),
                    const SizedBox(height: 18),
                    Text(headline, style: AppTypography.displayLg),
                    const SizedBox(height: 8),
                    LinearProgressIndicator(
                        value: progress,
                        minHeight: 8,
                        borderRadius: BorderRadius.circular(99),
                        color: accent,
                        backgroundColor: AppColors.neutral200),
                    const SizedBox(height: 10),
                    Text('오늘 목표 ${target.toString()}',
                        style: AppTypography.captionSm),
                  ]),
            ),
          ),
          const SizedBox(height: 16),
          Card(
              child: Padding(
                  padding: const EdgeInsets.all(18),
                  child: Text(message, style: AppTypography.bodyMd))),
          const SizedBox(height: 24),
          ElevatedButton.icon(
              onPressed: onPressed,
              icon: const Icon(Icons.add),
              label: Text(buttonLabel)),
        ],
      ),
    );
  }
}
