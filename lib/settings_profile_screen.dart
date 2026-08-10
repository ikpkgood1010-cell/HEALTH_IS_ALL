import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app_theme.dart';

class UserPreferences {
  final int targetCalories;
  final int targetWaterMl;
  final int targetExerciseMinutes;
  final bool notificationsEnabled;
  final bool largeTextEnabled;
  final bool reducedMotionEnabled;

  const UserPreferences({
    this.targetCalories = 2000,
    this.targetWaterMl = 2000,
    this.targetExerciseMinutes = 45,
    this.notificationsEnabled = true,
    this.largeTextEnabled = false,
    this.reducedMotionEnabled = false,
  });

  UserPreferences copyWith({
    int? targetCalories,
    int? targetWaterMl,
    int? targetExerciseMinutes,
    bool? notificationsEnabled,
    bool? largeTextEnabled,
    bool? reducedMotionEnabled,
  }) {
    return UserPreferences(
      targetCalories: targetCalories ?? this.targetCalories,
      targetWaterMl: targetWaterMl ?? this.targetWaterMl,
      targetExerciseMinutes:
          targetExerciseMinutes ?? this.targetExerciseMinutes,
      notificationsEnabled: notificationsEnabled ?? this.notificationsEnabled,
      largeTextEnabled: largeTextEnabled ?? this.largeTextEnabled,
      reducedMotionEnabled: reducedMotionEnabled ?? this.reducedMotionEnabled,
    );
  }
}

class UserPreferencesNotifier extends StateNotifier<UserPreferences> {
  UserPreferencesNotifier() : super(const UserPreferences());

  void updateTargets({int? calories, int? water, int? exercise}) {
    state = state.copyWith(
      targetCalories: calories,
      targetWaterMl: water,
      targetExerciseMinutes: exercise,
    );
  }

  void setNotifications(bool value) =>
      state = state.copyWith(notificationsEnabled: value);
  void setLargeText(bool value) =>
      state = state.copyWith(largeTextEnabled: value);
  void setReducedMotion(bool value) =>
      state = state.copyWith(reducedMotionEnabled: value);
}

final userPreferencesProvider =
    StateNotifierProvider<UserPreferencesNotifier, UserPreferences>(
  (_) => UserPreferencesNotifier(),
);

class SettingsProfileScreen extends ConsumerWidget {
  const SettingsProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final preferences = ref.watch(userPreferencesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('마이')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
        children: [
          Card(
            color: AppColors.primary100,
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  const CircleAvatar(
                    radius: 28,
                    backgroundColor: AppColors.primary500,
                    child: Icon(Icons.person_rounded,
                        color: Colors.white, size: 30),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('익명 모험가', style: AppTypography.titleMd),
                        const SizedBox(height: 4),
                        Text(
                          '로그인 없이 이 기기의 익명 ID로 기록 중',
                          style: AppTypography.captionSm,
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          Text('건강 목표', style: AppTypography.titleMd),
          const SizedBox(height: 8),
          _TargetTile(
            icon: Icons.restaurant_rounded,
            title: '하루 섭취 목표',
            value: '${preferences.targetCalories} kcal',
            onTap: () => _editTarget(
              context,
              title: '하루 섭취 목표',
              value: preferences.targetCalories,
              unit: 'kcal',
              onSave: (value) => ref
                  .read(userPreferencesProvider.notifier)
                  .updateTargets(calories: value),
            ),
          ),
          _TargetTile(
            icon: Icons.water_drop_rounded,
            title: '하루 수분 목표',
            value: '${preferences.targetWaterMl} ml',
            onTap: () => _editTarget(
              context,
              title: '하루 수분 목표',
              value: preferences.targetWaterMl,
              unit: 'ml',
              onSave: (value) => ref
                  .read(userPreferencesProvider.notifier)
                  .updateTargets(water: value),
            ),
          ),
          _TargetTile(
            icon: Icons.directions_run_rounded,
            title: '하루 운동 목표',
            value: '${preferences.targetExerciseMinutes}분',
            onTap: () => _editTarget(
              context,
              title: '하루 운동 목표',
              value: preferences.targetExerciseMinutes,
              unit: '분',
              onSave: (value) => ref
                  .read(userPreferencesProvider.notifier)
                  .updateTargets(exercise: value),
            ),
          ),
          const SizedBox(height: 24),
          Text('알림 및 접근성', style: AppTypography.titleMd),
          const SizedBox(height: 8),
          Card(
            child: Column(
              children: [
                SwitchListTile(
                  title: const Text('건강 루틴 알림'),
                  subtitle: const Text('설정한 기록 시간을 부드럽게 알려드려요.'),
                  value: preferences.notificationsEnabled,
                  onChanged: ref
                      .read(userPreferencesProvider.notifier)
                      .setNotifications,
                ),
                const Divider(height: 1),
                SwitchListTile(
                  title: const Text('큰 글자 우선'),
                  subtitle: const Text('중요한 수치와 안내 문구를 더 크게 표시해요.'),
                  value: preferences.largeTextEnabled,
                  onChanged:
                      ref.read(userPreferencesProvider.notifier).setLargeText,
                ),
                const Divider(height: 1),
                SwitchListTile(
                  title: const Text('움직임 줄이기'),
                  subtitle: const Text('게임 화면의 장식 애니메이션을 최소화해요.'),
                  value: preferences.reducedMotionEnabled,
                  onChanged: ref
                      .read(userPreferencesProvider.notifier)
                      .setReducedMotion,
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(
                '익명 MVP에서는 계정 연결과 로그아웃을 제공하지 않습니다. '
                '소셜 로그인은 데이터 이전·복구 정책이 준비된 뒤 추가합니다.',
                style: AppTypography.captionSm,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _TargetTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;
  final VoidCallback onTap;

  const _TargetTile({
    required this.icon,
    required this.title,
    required this.value,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon, color: AppColors.primary500),
        title: Text(title),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(value,
                style:
                    AppTypography.bodyMd.copyWith(fontWeight: FontWeight.w700)),
            const SizedBox(width: 4),
            const Icon(Icons.chevron_right_rounded),
          ],
        ),
        onTap: onTap,
      ),
    );
  }
}

Future<void> _editTarget(
  BuildContext context, {
  required String title,
  required int value,
  required String unit,
  required ValueChanged<int> onSave,
}) async {
  final controller = TextEditingController(text: value.toString());
  final result = await showDialog<int>(
    context: context,
    builder: (context) => AlertDialog(
      title: Text(title),
      content: TextField(
        controller: controller,
        keyboardType: TextInputType.number,
        decoration: InputDecoration(suffixText: unit),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('취소'),
        ),
        FilledButton(
          onPressed: () {
            final parsed = int.tryParse(controller.text.trim());
            if (parsed != null && parsed > 0) Navigator.pop(context, parsed);
          },
          child: const Text('저장'),
        ),
      ],
    ),
  );
  controller.dispose();
  if (result != null) onSave(result);
}
