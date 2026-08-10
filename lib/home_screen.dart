import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'api_data_provider.dart';
import 'app_theme.dart';
import 'game_balance.dart';

/// Health-first dashboard for the anonymous MVP.
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) context.read<ApiDataProvider>().refreshStatus();
    });
  }

  @override
  Widget build(BuildContext context) {
    final data = context.watch<ApiDataProvider>();
    final guild = GuildProjection.fromHealth(
      level: data.level,
      calories: data.consumedCalories,
      targetCalories: data.targetCalories,
      workoutMinutes: data.workoutMinutes,
      targetWorkoutMinutes: data.targetWorkoutMinutes,
      waterLiters: data.waterLiters,
      targetWaterLiters: data.targetWaterLiters,
      streakDays: data.streakDays,
    );

    return Scaffold(
      appBar: AppBar(
        title: const Text('HEALTH IS ALL'),
        actions: [
          if (data.isLoading)
            const Padding(
              padding: EdgeInsets.only(right: 20),
              child: Center(
                child: SizedBox.square(
                  dimension: 20,
                  child: CircularProgressIndicator(strokeWidth: 2),
                ),
              ),
            )
          else
            IconButton(
              tooltip: '새로고침',
              onPressed: data.refreshStatus,
              icon: const Icon(Icons.refresh_rounded),
            ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: data.refreshStatus,
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
          children: [
            Text('오늘도 내 몸부터 살펴볼까요?', style: AppTypography.displayLg),
            const SizedBox(height: 8),
            Text(
              '건강 기록이 먼저이고, 게임 성장은 그 기록을 따라옵니다.',
              style: AppTypography.bodyMd.copyWith(color: AppColors.neutral700),
            ),
            if (data.lastError != null) ...[
              const SizedBox(height: 16),
              _NoticeCard(
                icon: Icons.cloud_off_outlined,
                title: '서버와 연결되지 않았어요',
                message: '기록은 추가하지 않고 마지막으로 확인한 화면을 보여드려요.',
                color: AppColors.statusError,
              ),
            ],
            const SizedBox(height: 20),
            _BalanceCard(projection: guild),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _MetricCard(
                    icon: Icons.directions_run_rounded,
                    label: '운동',
                    value: '${data.workoutMinutes}분',
                    target: '목표 ${data.targetWorkoutMinutes}분',
                    color: AppColors.secondary500,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _MetricCard(
                    icon: Icons.restaurant_rounded,
                    label: '식단',
                    value: '${data.consumedCalories} kcal',
                    target: '목표 ${data.targetCalories}',
                    color: AppColors.primary500,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _MetricCard(
                    icon: Icons.water_drop_rounded,
                    label: '수분',
                    value: '${data.waterLiters.toStringAsFixed(1)} L',
                    target: '목표 ${data.targetWaterLiters.toStringAsFixed(1)} L',
                    color: const Color(0xFF36A3FF),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _MetricCard(
                    icon: Icons.local_fire_department_rounded,
                    label: '꾸준함',
                    value: '${data.streakDays}일',
                    target: '최근 7일 기준',
                    color: AppColors.accentEnergy,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const _NoticeCard(
              icon: Icons.self_improvement_rounded,
              title: '쉬는 날도 건강 관리예요',
              message: '활동이 적은 날에는 불이익을 주지 않아요. 회복 후 다시 이어가면 됩니다.',
              color: AppColors.primary700,
            ),
          ],
        ),
      ),
    );
  }
}

class _BalanceCard extends StatelessWidget {
  final GuildProjection projection;

  const _BalanceCard({required this.projection});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.primary100,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.health_and_safety_rounded,
                    color: AppColors.primary700),
                const SizedBox(width: 8),
                Text('건강 균형 지수', style: AppTypography.titleMd),
                const Spacer(),
                Text(
                  projection.hbi.toStringAsFixed(1),
                  style: AppTypography.displayLg.copyWith(
                    color: AppColors.primary700,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            ClipRRect(
              borderRadius: BorderRadius.circular(99),
              child: LinearProgressIndicator(
                value: projection.hbi / 100,
                minHeight: 10,
                color: AppColors.primary500,
                backgroundColor: Colors.white,
              ),
            ),
            const SizedBox(height: 12),
            Text(projection.environmentMessage, style: AppTypography.bodyMd),
            const SizedBox(height: 4),
            Text(
              '최저 영역 60% + 전체 평균 40%',
              style: AppTypography.captionSm,
            ),
          ],
        ),
      ),
    );
  }
}

class _MetricCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final String target;
  final Color color;

  const _MetricCard({
    required this.icon,
    required this.label,
    required this.value,
    required this.target,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color),
            const SizedBox(height: 14),
            Text(label, style: AppTypography.captionSm),
            const SizedBox(height: 3),
            Text(value, style: AppTypography.titleMd.copyWith(fontSize: 18)),
            const SizedBox(height: 3),
            Text(target, style: AppTypography.captionSm),
          ],
        ),
      ),
    );
  }
}

class _NoticeCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String message;
  final Color color;

  const _NoticeCard({
    required this.icon,
    required this.title,
    required this.message,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title,
                      style: AppTypography.bodyMd
                          .copyWith(fontWeight: FontWeight.w700)),
                  const SizedBox(height: 4),
                  Text(message, style: AppTypography.captionSm),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
