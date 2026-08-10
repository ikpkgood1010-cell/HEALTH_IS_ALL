import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'api_client.dart';
import 'api_data_provider.dart';
import 'app_theme.dart';
import 'game_balance.dart';

/// Health-derived Living Guild with an idempotent automatic-adventure claim.
class GuildScreen extends StatefulWidget {
  const GuildScreen({super.key});

  @override
  State<GuildScreen> createState() => _GuildScreenState();
}

class _GuildScreenState extends State<GuildScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) context.read<ApiDataProvider>().refreshGuild();
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
    final facility = data.trainingGrounds;

    return Scaffold(
      appBar: AppBar(title: const Text('길드')),
      body: RefreshIndicator(
        onRefresh: data.refreshGuild,
        child: ListView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
          children: [
            _GuildHero(guild: guild),
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
                    label: '보유 주화',
                    value: '${facility?.guildCoinBalance ?? guild.guildCoins}',
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
            Text('자동 모험', style: AppTypography.titleMd),
            const SizedBox(height: 8),
            _AdventureCard(data: data),
            const SizedBox(height: 16),
            Text('길드 시설', style: AppTypography.titleMd),
            const SizedBox(height: 8),
            _TrainingGroundsCard(facility: facility),
            if (data.guildError != null) ...[
              const SizedBox(height: 12),
              _InfoBanner(message: data.guildError!),
            ],
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
                      description: '가장 낮은 영역을 먼저 보완하는 균형 지수',
                    ),
                    const Divider(height: 28),
                    ...guild.breakdown.entries.map(
                      (entry) => Padding(
                        padding: const EdgeInsets.only(bottom: 10),
                        child: Row(
                          children: [
                            Expanded(
                              child: Text(entry.key,
                                  style: AppTypography.captionSm),
                            ),
                            Text(
                              entry.value.toStringAsFixed(0),
                              style: AppTypography.bodyMd.copyWith(
                                fontWeight: FontWeight.w700,
                              ),
                            ),
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
                    Text('안전한 성장 규칙', style: AppTypography.titleMd),
                    const SizedBox(height: 12),
                    const _RuleLine(text: '같은 12시간 모험은 여러 번 열어도 보상이 늘지 않아요.'),
                    const _RuleLine(text: '자동 모험 효율은 70%, 최대 누적 시간은 12시간이에요.'),
                    const _RuleLine(text: '보상의 20%는 훈련장에 자동 투자돼요.'),
                    const _RuleLine(
                        text: '건강 상태가 낮아도 보상 배율이 1.0 아래로 내려가지 않아요.'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _GuildHero extends StatelessWidget {
  final GuildProjection guild;

  const _GuildHero({required this.guild});

  @override
  Widget build(BuildContext context) {
    return Container(
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
            '${guild.environmentName} · 탑 ${guild.towerFloor}층 탐험 중',
            style: AppTypography.bodyMd.copyWith(
              color: Colors.white.withValues(alpha: .9),
            ),
          ),
          const SizedBox(height: 16),
          Text(
            guild.environmentMessage,
            style: AppTypography.bodyMd.copyWith(color: Colors.white),
          ),
        ],
      ),
    );
  }
}

class _AdventureCard extends StatelessWidget {
  final ApiDataProvider data;

  const _AdventureCard({required this.data});

  @override
  Widget build(BuildContext context) {
    final adventure = data.adventure;
    if (data.isGuildLoading && adventure == null) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(28),
          child: Center(child: CircularProgressIndicator()),
        ),
      );
    }
    if (adventure == null) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(18),
          child: Text('서버 연결 후 현재 모험 결과가 이곳에 표시돼요.'),
        ),
      );
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.explore_rounded, color: AppColors.primary500),
                const SizedBox(width: 8),
                Expanded(
                  child: Text('모험대가 돌아왔어요', style: AppTypography.titleMd),
                ),
                if (adventure.claimed)
                  const Chip(
                    avatar: Icon(Icons.check_rounded, size: 16),
                    label: Text('수령 완료'),
                  ),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              '${_clock(adventure.windowStart)}–${_clock(adventure.windowEnd)} 정산 · '
              '효율 ${(adventure.offlineEfficiency * 100).round()}%',
              style: AppTypography.captionSm,
            ),
            const SizedBox(height: 14),
            Row(
              children: [
                Expanded(
                    child: _Metric(
                        label: '모험 활력', value: '${adventure.vitality}')),
                Expanded(
                    child: _Metric(
                        label: '획득 주화', value: '${adventure.grossGuildCoins}')),
                Expanded(
                    child: _Metric(
                        label: '건강 균형',
                        value: adventure.hbiScore.toStringAsFixed(1))),
              ],
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                onPressed: adventure.claimed || data.isGuildLoading
                    ? null
                    : () async {
                        final result = await data.claimAdventure();
                        if (!context.mounted || result == null) return;
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text(
                              '주화 ${result.guildCoinsReceived}개 수령 · '
                              '훈련장 ${result.facilityInvested}개 투자',
                            ),
                          ),
                        );
                      },
                icon: data.isGuildLoading
                    ? const SizedBox.square(
                        dimension: 16,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.redeem_rounded),
                label: Text(adventure.claimed ? '보상을 받았어요' : '안전하게 보상 받기'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _clock(DateTime value) =>
      '${value.hour.toString().padLeft(2, '0')}:${value.minute.toString().padLeft(2, '0')}';
}

class _TrainingGroundsCard extends StatelessWidget {
  final TrainingGroundsStatus? facility;

  const _TrainingGroundsCard({required this.facility});

  @override
  Widget build(BuildContext context) {
    final value = facility;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: AppColors.primary100,
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: const Icon(Icons.fitness_center_rounded,
                      color: AppColors.primary700),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('훈련장', style: AppTypography.titleMd),
                      Text(
                        value == null ? '서버 연결 대기 중' : 'Lv. ${value.level}',
                        style: AppTypography.captionSm,
                      ),
                    ],
                  ),
                ),
                Text(
                  '${value?.totalInvested ?? 0} 투자',
                  style: AppTypography.bodyMd
                      .copyWith(fontWeight: FontWeight.w700),
                ),
              ],
            ),
            const SizedBox(height: 16),
            LinearProgressIndicator(
              value: (value?.progressRatio ?? 0).clamp(0.0, 1.0).toDouble(),
              minHeight: 8,
              borderRadius: BorderRadius.circular(99),
            ),
            const SizedBox(height: 8),
            Text(
              value == null
                  ? '모험 보상 수령 시 성장도가 표시돼요.'
                  : '다음 레벨까지 ${value.nextLevelCost - value.currentLevelProgress} 주화',
              style: AppTypography.captionSm,
            ),
          ],
        ),
      ),
    );
  }
}

class _Metric extends StatelessWidget {
  final String label;
  final String value;

  const _Metric({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(value, style: AppTypography.titleMd),
        const SizedBox(height: 2),
        Text(label, style: AppTypography.captionSm),
      ],
    );
  }
}

class _InfoBanner extends StatelessWidget {
  final String message;

  const _InfoBanner({required this.message});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFFFFF6D8),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Row(
        children: [
          const Icon(Icons.info_outline_rounded, color: Color(0xFF9A6A00)),
          const SizedBox(width: 10),
          Expanded(child: Text(message, style: AppTypography.captionSm)),
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
            Text(
              label,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: AppTypography.captionSm,
            ),
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
