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
            Text('나의 원정대', style: AppTypography.titleMd),
            const SizedBox(height: 8),
            _HeroRosterCard(heroes: data.heroRoster),
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
            const SizedBox(height: 20),
            Text('지난 모험 회상', style: AppTypography.titleMd),
            const SizedBox(height: 8),
            _AdventureHistoryCard(items: data.adventureHistory),
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
      height: 260,
      clipBehavior: Clip.antiAlias,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(28),
        gradient: const LinearGradient(
          colors: [Color(0xFF8EDCCA), Color(0xFF77B9E8), Color(0xFFFFD790)],
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
        ),
      ),
      child: Stack(
        children: [
          Positioned(
            right: -36,
            top: -48,
            child: Container(
              width: 170,
              height: 170,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white.withValues(alpha: .24),
              ),
            ),
          ),
          Positioned(
            right: 24,
            bottom: 35,
            child: Icon(
              Icons.castle_rounded,
              color: const Color(0xFF315C68).withValues(alpha: .78),
              size: 110,
            ),
          ),
          Positioned(
            left: -24,
            right: -24,
            bottom: -52,
            child: Container(
              height: 108,
              decoration: BoxDecoration(
                color: const Color(0xFF4E9A65),
                borderRadius: BorderRadius.circular(100),
                boxShadow: const [
                  BoxShadow(color: Color(0x33406455), blurRadius: 12),
                ],
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(22),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                  decoration: BoxDecoration(
                    color: const Color(0xFF244D55).withValues(alpha: .78),
                    borderRadius: BorderRadius.circular(99),
                  ),
                  child: const Text(
                    '생명의 탑 원정대',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
                const Spacer(),
                Text(
                  guild.stageName,
                  style: AppTypography.displayLg.copyWith(
                    color: const Color(0xFF173D45),
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '${guild.environmentName} · 탑 ${guild.towerFloor}층 탐험 중',
                  style: AppTypography.bodyMd.copyWith(
                    color: const Color(0xFF244D55),
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 8),
                SizedBox(
                  width: 230,
                  child: Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 9, vertical: 6),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: .58),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      guild.environmentMessage,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: AppTypography.captionSm.copyWith(
                        color: const Color(0xFF315C68),
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _HeroRosterCard extends StatelessWidget {
  final List<HeroCompanion> heroes;

  const _HeroRosterCard({required this.heroes});

  @override
  Widget build(BuildContext context) {
    final hero = heroes.isEmpty ? null : heroes.first;
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(22),
        gradient: const LinearGradient(
          colors: [Color(0xFFFFF1C7), Color(0xFFE8F7D8)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        border: Border.all(color: const Color(0xFFB5D89D)),
        boxShadow: const [
          BoxShadow(
            color: Color(0x18305A42),
            blurRadius: 16,
            offset: Offset(0, 6),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            width: 86,
            height: 100,
            decoration: BoxDecoration(
              color: const Color(0xFF8DCB78),
              borderRadius: BorderRadius.circular(22),
            ),
            child: Icon(
              hero == null
                  ? Icons.person_add_alt_1_rounded
                  : Icons.hiking_rounded,
              size: 52,
              color: Colors.white,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  hero == null
                      ? '첫 용사를 기다리는 중'
                      : '${hero.title} · ${hero.name}',
                  style: AppTypography.titleMd.copyWith(
                    color: const Color(0xFF315538),
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  hero == null
                      ? '건강 기록으로 활력이 생긴 첫 모험을 마치면 이야기 속 용사가 확정 합류해요.'
                      : hero.joinMessage,
                  style: AppTypography.bodyMd.copyWith(
                    color: const Color(0xFF4C6550),
                  ),
                ),
                const SizedBox(height: 9),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: .72),
                    borderRadius: BorderRadius.circular(99),
                  ),
                  child: Text(
                    hero == null ? '확률형 뽑기 없음' : '${hero.role} · 숲 속성',
                    style: AppTypography.captionSm.copyWith(
                      color: const Color(0xFF3E6A46),
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
              ],
            ),
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
            if (adventure.rooms.isNotEmpty) ...[
              const Divider(height: 32),
              Text(
                '탑 ${adventure.towerFloor}층 탐험 경로',
                style: AppTypography.titleMd,
              ),
              const SizedBox(height: 10),
              ...adventure.rooms.map(
                (room) => _AdventureRoomRow(room: room),
              ),
            ],
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
                              result.joinedHero == null
                                  ? '주화 ${result.guildCoinsReceived}개 수령 · '
                                      '훈련장 ${result.facilityInvested}개 투자'
                                  : '${result.joinedHero!.title} '
                                      '${result.joinedHero!.name} 합류! · '
                                      '주화 ${result.guildCoinsReceived}개 수령',
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

class _AdventureRoomRow extends StatelessWidget {
  final AdventureRoom room;

  const _AdventureRoomRow({required this.room});

  @override
  Widget build(BuildContext context) {
    final icon = switch (room.roomType) {
      'EVENT' => Icons.auto_awesome_rounded,
      'REST' => Icons.local_fire_department_rounded,
      'SHOP' => Icons.storefront_rounded,
      'ELITE' => Icons.shield_rounded,
      'BOSS' => Icons.workspace_premium_rounded,
      _ => Icons.sports_martial_arts_rounded,
    };
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CircleAvatar(
            radius: 17,
            backgroundColor: AppColors.primary100,
            child: Icon(icon, size: 18, color: AppColors.primary700),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('${room.position}. ${room.title}',
                    style: AppTypography.bodyMd.copyWith(
                      fontWeight: FontWeight.w700,
                    )),
                const SizedBox(height: 2),
                Text(
                  room.resultTitle,
                  style: AppTypography.captionSm.copyWith(
                    color: AppColors.primary700,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 2),
                Text(room.outcome, style: AppTypography.captionSm),
              ],
            ),
          ),
        ],
      ),
    );
  }
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
                      Text(value?.stageName ?? '훈련장',
                          style: AppTypography.titleMd),
                      Text(
                        value == null ? '서버 연결 대기 중' : '훈련장 Lv. ${value.level}',
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
            if (value != null) ...[
              const SizedBox(height: 12),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.primary100,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(value.stageMessage, style: AppTypography.bodyMd),
              ),
              if (value.nextMilestoneLevel != null) ...[
                const SizedBox(height: 8),
                Text(
                  '다음 모습은 훈련장 Lv. ${value.nextMilestoneLevel}에서 열려요.',
                  style: AppTypography.captionSm,
                ),
              ],
            ],
          ],
        ),
      ),
    );
  }
}

class _AdventureHistoryCard extends StatelessWidget {
  final List<AdventureState> items;

  const _AdventureHistoryCard({required this.items});

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(18),
          child: Text('완료한 모험이 생기면 건강 기록의 여정이 이곳에 남아요.'),
        ),
      );
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          children: [
            for (var index = 0; index < items.length; index++) ...[
              _AdventureMemoryRow(adventure: items[index]),
              if (index != items.length - 1) const Divider(height: 24),
            ],
          ],
        ),
      ),
    );
  }
}

class _AdventureMemoryRow extends StatelessWidget {
  final AdventureState adventure;

  const _AdventureMemoryRow({required this.adventure});

  @override
  Widget build(BuildContext context) {
    final bossName =
        adventure.rooms.isEmpty ? '모험 경로' : adventure.rooms.last.title;
    final date = adventure.windowEnd.toLocal();
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        CircleAvatar(
          backgroundColor: adventure.claimed
              ? AppColors.primary100
              : const Color(0xFFFFF6D8),
          child: Icon(
            adventure.claimed
                ? Icons.auto_stories_rounded
                : Icons.pending_actions_rounded,
            color: adventure.claimed
                ? AppColors.primary700
                : const Color(0xFF9A6A00),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('탑 ${adventure.towerFloor}층 · $bossName',
                  style: AppTypography.bodyMd
                      .copyWith(fontWeight: FontWeight.w700)),
              const SizedBox(height: 3),
              Text(
                '${date.month}월 ${date.day}일 · 방 ${adventure.rooms.length}개 · '
                '주화 ${adventure.grossGuildCoins}',
                style: AppTypography.captionSm,
              ),
              const SizedBox(height: 3),
              Text(
                adventure.claimed ? '보상 수령 완료' : '아직 받을 보상이 있어요',
                style: AppTypography.captionSm.copyWith(
                  color: adventure.claimed
                      ? AppColors.primary700
                      : const Color(0xFF9A6A00),
                ),
              ),
            ],
          ),
        ),
      ],
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
