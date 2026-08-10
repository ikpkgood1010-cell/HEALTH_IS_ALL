import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'api_data_provider.dart';
import 'app_theme.dart';
import 'game_balance.dart';

/// Read-only Living Guild preview derived from health records.
class GuildScreen extends StatelessWidget {
  const GuildScreen({super.key});

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
      appBar: AppBar(title: const Text('길드')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
        children: [
          Container(
            padding: const EdgeInsets.all(22),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(24),
              gradient: const LinearGradient(
                colors: [Color(0xFF00B89C), Color(0xFF2D8CFF)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.castle_rounded, color: Colors.white, size: 38),
                const SizedBox(height: 28),
                Text(
                  guild.stageName,
                  style: AppTypography.displayLg.copyWith(color: Colors.white),
                ),
                const SizedBox(height: 4),
                Text(
                  '${guild.environmentName} · ${guild.towerFloor}층 탐험 중',
                  style: AppTypography.bodyMd
                      .copyWith(color: Colors.white.withOpacity(.9)),
                ),
                const SizedBox(height: 16),
                Text(
                  guild.environmentMessage,
                  style: AppTypography.bodyMd.copyWith(color: Colors.white),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: _ResourceCard(
                  icon: Icons.bolt_rounded,
                  label: '활력',
                  value: '${guild.vitality}',
                  color: AppColors.accentEnergy,
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: _ResourceCard(
                  icon: Icons.monetization_on_rounded,
                  label: '길드 주화',
                  value: '${guild.guildCoins}',
                  color: const Color(0xFFE2A400),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: _ResourceCard(
                  icon: Icons.auto_awesome_rounded,
                  label: '기억 조각',
                  value: '${guild.memoryShards}',
                  color: const Color(0xFF8B5CF6),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Text('오늘의 건강이 만든 변화', style: AppTypography.titleMd),
          const SizedBox(height: 8),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(18),
              child: Column(
                children: [
                  _BalanceRow(
                    label: '건강 균형 지수',
                    value: guild.hbi,
                    description: '최저 영역을 먼저 보완하는 균형 지표',
                  ),
                  const Divider(height: 28),
                  ...guild.breakdown.entries.map(
                    (entry) => Padding(
                      padding: const EdgeInsets.only(bottom: 10),
                      child: Row(
                        children: [
                          Expanded(
                            child:
                                Text(entry.key, style: AppTypography.captionSm),
                          ),
                          Text(entry.value.toStringAsFixed(0),
                              style: AppTypography.bodyMd
                                  .copyWith(fontWeight: FontWeight.w700)),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(18),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('자동 모험 규칙', style: AppTypography.titleMd),
                  const SizedBox(height: 12),
                  const _RuleLine(text: '앱을 반복해서 열어도 추가 보상 없음'),
                  const _RuleLine(text: '오프라인 진행 최대 12시간 · 효율 70%'),
                  const _RuleLine(text: '낮은 활동량에도 보상 배율은 1.0 아래로 내려가지 않음'),
                  _RuleLine(
                    text: guild.towerFloor >= 30
                        ? '30층 달성: 기억의 순환(환생) 검토 가능'
                        : '기억의 순환은 30층부터 열림',
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Text(
            '현재 화면은 건강 기록으로 계산한 MVP 미리보기입니다. '
            '전투·보상 수령·결제 기능은 아직 활성화하지 않았습니다.',
            style: AppTypography.captionSm,
          ),
        ],
      ),
    );
  }
}

class _ResourceCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color color;

  const _ResourceCard({
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 14),
        child: Column(
          children: [
            Icon(icon, color: color),
            const SizedBox(height: 7),
            Text(value, style: AppTypography.titleMd.copyWith(fontSize: 18)),
            Text(label,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: AppTypography.captionSm),
          ],
        ),
      ),
    );
  }
}

class _BalanceRow extends StatelessWidget {
  final String label;
  final double value;
  final String description;

  const _BalanceRow({
    required this.label,
    required this.value,
    required this.description,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label, style: AppTypography.bodyMd),
              Text(description, style: AppTypography.captionSm),
            ],
          ),
        ),
        Text(
          value.toStringAsFixed(1),
          style: AppTypography.displayLg.copyWith(color: AppColors.primary700),
        ),
      ],
    );
  }
}

class _RuleLine extends StatelessWidget {
  final String text;

  const _RuleLine({required this.text});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 9),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.check_circle_rounded,
              size: 18, color: AppColors.primary500),
          const SizedBox(width: 8),
          Expanded(child: Text(text, style: AppTypography.bodyMd)),
        ],
      ),
    );
  }
}
