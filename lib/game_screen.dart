import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'api_client.dart';
import 'api_data_provider.dart';
import 'app_theme.dart';

const gameOfficialName = 'HEALTH IS ALL : 건강이 전부다 !!';

enum _GameSection {
  hub,
  battle,
  village,
  heroes,
  constellation,
  spirits,
  workshop,
  rebirth,
  hallOfFame,
}

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  _GameSection _section = _GameSection.hub;

  static const _heroes = [
    ('TANKER', '탱커', Icons.shield_rounded),
    ('WARRIOR', '전사', Icons.sports_martial_arts_rounded),
    ('MAGE', '마법사', Icons.auto_fix_high_rounded),
    ('ARCHER', '궁수', Icons.gps_fixed_rounded),
    ('ROGUE', '도적', Icons.bolt_rounded),
    ('HEALER', '치유사', Icons.healing_rounded),
  ];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) context.read<ApiDataProvider>().refreshGame();
    });
  }

  @override
  Widget build(BuildContext context) {
    final data = context.watch<ApiDataProvider>();
    final isHub = _section == _GameSection.hub;
    return Scaffold(
      backgroundColor: const Color(0xFFF4F0E8),
      appBar: AppBar(
        backgroundColor: const Color(0xFFFFFBF2),
        leading: isHub
            ? const BackButton()
            : IconButton(
                tooltip: '게임 허브로 돌아가기',
                onPressed: () => setState(() => _section = _GameSection.hub),
                icon: const Icon(Icons.arrow_back_rounded),
              ),
        title: Text(isHub ? gameOfficialName : _sectionTitle(_section)),
      ),
      body: SafeArea(child: isHub ? _buildHub(data) : _buildSection(data)),
    );
  }

  Widget _buildHub(ApiDataProvider data) {
    final state = data.canonicalGame;
    final onboarding = state == null || state.phase == 'ONBOARDING';
    final recruitedCount =
        state?.heroes.where((hero) => hero.recruited).length ?? 0;
    return ListView(
      key: const Key('game-hub'),
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 32),
      children: [
        _BattleBanner(
          onTap: () => _open(_GameSection.battle),
          statusLabel: data.isGameLoading
              ? 'LOADING'
              : onboarding
                  ? '준비 단계'
                  : 'AUTO ON',
          title: onboarding
              ? '첫 용사 영입을 기다리고 있어요'
              : '탑 ${state.towerFloor}층 · ${state.roomPosition}번 방',
          message: onboarding
              ? '6직업 중 첫 용사 1명을 무료로 선택하면 자동 전투가 시작됩니다.'
              : '$recruitedCount명의 용사가 다음 적을 향해 이동합니다.',
        ),
        if (data.gameError != null) ...[
          const SizedBox(height: 10),
          _GameNotice(message: data.gameError!),
        ],
        if (state != null) ...[
          const SizedBox(height: 10),
          _RunStatusCard(state: state),
        ],
        if (state != null && !state.initialHeroSelected) ...[
          const SizedBox(height: 14),
          _InitialHeroSelector(
            heroes: _heroes,
            disabled: data.isGameLoading,
            onSelected: data.selectInitialHero,
          ),
        ],
        const SizedBox(height: 18),
        Text('나의 6인 파티', style: AppTypography.titleMd),
        const SizedBox(height: 4),
        Text(
          onboarding
              ? '첫 용사 1명은 무료 선택, 나머지 5명은 0계층 대형 노드에서 확정 영입합니다.'
              : '남은 용사는 0계층 대형 노드 5개에서 확정 영입합니다.',
          style: AppTypography.captionSm,
        ),
        const SizedBox(height: 10),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Wrap(
              alignment: WrapAlignment.spaceBetween,
              runSpacing: 12,
              children:
                  _heroes.map((hero) => _buildHeroSlot(hero, state)).toList(),
            ),
          ),
        ),
        const SizedBox(height: 20),
        Text('게임 메뉴', style: AppTypography.titleMd),
        const SizedBox(height: 10),
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          childAspectRatio: 1.5,
          mainAxisSpacing: 10,
          crossAxisSpacing: 10,
          children: [
            _MenuCard(
              icon: Icons.fort_rounded,
              title: '자동 전투',
              subtitle: '5개 일반방 + 보스',
              onTap: () => _open(_GameSection.battle),
            ),
            _MenuCard(
              icon: Icons.holiday_village_rounded,
              title: '마을·길드',
              subtitle: '게임 안의 생활 거점',
              onTap: () => _open(_GameSection.village),
            ),
            _MenuCard(
              icon: Icons.groups_rounded,
              title: '용사',
              subtitle: '6인 영입·전직',
              onTap: () => _open(_GameSection.heroes),
            ),
            _MenuCard(
              icon: Icons.hub_rounded,
              title: '별자리',
              subtitle: '7개 층 · 대형 노드',
              onTap: () => _open(_GameSection.constellation),
            ),
            _MenuCard(
              icon: Icons.egg_alt_rounded,
              title: '정령',
              subtitle: '확정 부화 · 중복 없음',
              onTap: () => _open(_GameSection.spirits),
            ),
            _MenuCard(
              icon: Icons.handyman_rounded,
              title: '제작',
              subtitle: '스킬·아바타 확정 제작',
              onTap: () => _open(_GameSection.workshop),
            ),
            _MenuCard(
              icon: Icons.replay_circle_filled_rounded,
              title: '환생',
              subtitle: '전직 영구 보존',
              onTap: () => _open(_GameSection.rebirth),
            ),
            _MenuCard(
              icon: Icons.emoji_events_rounded,
              title: '명예의 전당',
              subtitle: '개인 성장 기록',
              onTap: () => _open(_GameSection.hallOfFame),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildHeroSlot(
    (String, String, IconData) hero,
    CanonicalGameState? state,
  ) {
    CanonicalGameHero? saved;
    for (final item in state?.heroes ?? const <CanonicalGameHero>[]) {
      if (item.heroCode == hero.$1) {
        saved = item;
        break;
      }
    }
    final recruited = saved?.recruited ?? false;
    return SizedBox(
      width: 74,
      child: Column(
        children: [
          CircleAvatar(
            backgroundColor:
                recruited ? const Color(0xFFFFE5A5) : AppColors.neutral200,
            foregroundColor:
                recruited ? const Color(0xFF6A451F) : AppColors.neutral500,
            child: Icon(recruited ? hero.$3 : Icons.lock_outline_rounded),
          ),
          const SizedBox(height: 6),
          Text(hero.$2, style: AppTypography.captionSm),
          if ((saved?.advancementTier ?? 0) > 0)
            Text('전직 ${saved!.advancementTier}',
                style: AppTypography.captionSm),
        ],
      ),
    );
  }

  Widget _buildSection(ApiDataProvider data) {
    switch (_section) {
      case _GameSection.battle:
        return _BattleDetail(data: data);
      case _GameSection.village:
        return const _DetailList(
          title: '마을과 길드',
          description: '길드는 건강 앱의 하단 탭이 아니라 게임 세계 안의 거점입니다.',
          items: ['시설·NPC·교류 기능은 경제 검증 뒤 순차 개방', '현재 단계에서는 위치와 진입 구조만 확정'],
        );
      case _GameSection.heroes:
        return _HeroDetail(heroes: _heroes);
      case _GameSection.constellation:
        return _ConstellationDetail(state: data.canonicalGame);
      case _GameSection.spirits:
        return const _DetailList(
          title: '정령 확정 부화',
          description: '랜덤 뽑기와 중복 정령은 없습니다. 노드에서 알을 열고 건강 에너지로 부화기를 채웁니다.',
          items: ['부화 결과 100% 확정', '기본 표시 이름: 정령', '사용자가 정령 이름 변경 가능'],
        );
      case _GameSection.workshop:
        return const _DetailList(
          title: '스킬·아바타 제작',
          description: '별도 장비 인벤토리 없이 스킬과 아바타만 확정 제작합니다.',
          items: [
            '확률형 제작 없음',
            '전직 시 무기·방어구 외형과 기본 능력치 일괄 전환',
            '패시브 스킬은 전직마다 자동 추가'
          ],
        );
      case _GameSection.rebirth:
        return _RebirthDetail(preview: data.rebirthPreview);
      case _GameSection.hallOfFame:
        return const _DetailList(
          title: '명예의 전당',
          description: '타인과의 과도한 경쟁보다 자신의 누적 성장과 최고 기록을 남기는 공간입니다.',
          items: [
            '최고 도달 층',
            '완료한 전직',
            '수집한 정령·아바타',
            '건강 원본 기록은 게임 화면에 표시하지 않음'
          ],
        );
      case _GameSection.hub:
        return const SizedBox.shrink();
    }
  }

  void _open(_GameSection section) {
    setState(() => _section = section);
    if (section == _GameSection.battle) {
      context.read<ApiDataProvider>().settleBattle();
    }
  }

  String _sectionTitle(_GameSection section) => switch (section) {
        _GameSection.battle => '자동 전투',
        _GameSection.village => '마을·길드',
        _GameSection.heroes => '용사',
        _GameSection.constellation => '별자리',
        _GameSection.spirits => '정령',
        _GameSection.workshop => '제작',
        _GameSection.rebirth => '환생',
        _GameSection.hallOfFame => '명예의 전당',
        _GameSection.hub => gameOfficialName,
      };
}

class _BattleBanner extends StatelessWidget {
  final VoidCallback onTap;
  final String statusLabel;
  final String title;
  final String message;

  const _BattleBanner({
    required this.onTap,
    required this.statusLabel,
    required this.title,
    required this.message,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF263659),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.auto_awesome_rounded,
                      color: Color(0xFFFFD36E)),
                  const SizedBox(width: 8),
                  const Text('자동 전투',
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.w700)),
                  const Spacer(),
                  _StatusPill(label: statusLabel),
                ],
              ),
              const SizedBox(height: 24),
              Text(title,
                  style: const TextStyle(
                      color: Colors.white,
                      fontSize: 26,
                      fontWeight: FontWeight.w800)),
              const SizedBox(height: 6),
              Text(message, style: const TextStyle(color: Color(0xFFD8DEEF))),
              const SizedBox(height: 18),
              FilledButton.tonalIcon(
                onPressed: onTap,
                icon: const Icon(Icons.play_arrow_rounded),
                label: const Text('전투 화면 보기'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _InitialHeroSelector extends StatelessWidget {
  final List<(String, String, IconData)> heroes;
  final bool disabled;
  final Future<void> Function(String heroCode) onSelected;

  const _InitialHeroSelector({
    required this.heroes,
    required this.disabled,
    required this.onSelected,
  });

  @override
  Widget build(BuildContext context) => Card(
        key: const Key('initial-hero-selector'),
        color: const Color(0xFFFFF3D6),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('첫 용사 무료 선택', style: AppTypography.titleMd),
              const SizedBox(height: 5),
              Text(
                '원하는 직업 1명을 무료로 영입합니다. 선택하지 않은 5명은 0계층 대형 노드에서 확정 영입할 수 있어요.',
                style: AppTypography.captionSm,
              ),
              const SizedBox(height: 12),
              GridView.count(
                crossAxisCount: 3,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                childAspectRatio: 1.08,
                mainAxisSpacing: 8,
                crossAxisSpacing: 8,
                children: [
                  for (final hero in heroes)
                    OutlinedButton(
                      key: Key('initial-hero-${hero.$1}'),
                      onPressed: disabled
                          ? null
                          : () => _confirmSelection(context, hero),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(hero.$3),
                          const SizedBox(height: 5),
                          Text(hero.$2),
                        ],
                      ),
                    ),
                ],
              ),
            ],
          ),
        ),
      );

  Future<void> _confirmSelection(
    BuildContext context,
    (String, String, IconData) hero,
  ) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text('${hero.$2}를 첫 용사로 선택할까요?'),
        content: const Text(
          '첫 용사 선택은 영구 보존됩니다. 나머지 5명은 0계층 대형 노드에서 차례로 영입합니다.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext, false),
            child: const Text('다시 고르기'),
          ),
          FilledButton(
            key: const Key('confirm-initial-hero'),
            onPressed: () => Navigator.pop(dialogContext, true),
            child: const Text('무료 영입'),
          ),
        ],
      ),
    );
    if (confirmed == true) await onSelected(hero.$1);
  }
}

class _StatusPill extends StatelessWidget {
  final String label;

  const _StatusPill({required this.label});

  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
        decoration: BoxDecoration(
            color: const Color(0xFF4B996F),
            borderRadius: BorderRadius.circular(99)),
        child: Text(label,
            style: const TextStyle(
                color: Colors.white,
                fontSize: 11,
                fontWeight: FontWeight.w800)),
      );
}

class _GameNotice extends StatelessWidget {
  final String message;

  const _GameNotice({required this.message});

  @override
  Widget build(BuildContext context) => Card(
        color: const Color(0xFFFFF3D6),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              const Icon(Icons.info_outline_rounded, color: Color(0xFF8B5E34)),
              const SizedBox(width: 8),
              Expanded(child: Text(message, style: AppTypography.captionSm)),
            ],
          ),
        ),
      );
}

class _BattleDetail extends StatelessWidget {
  final ApiDataProvider data;

  const _BattleDetail({required this.data});

  @override
  Widget build(BuildContext context) {
    final state = data.canonicalGame;
    if (state == null) {
      return const Center(child: CircularProgressIndicator());
    }
    if (!state.initialHeroSelected) {
      return const _DetailList(
        title: '자동 전투 준비 중',
        description: '게임 허브에서 첫 용사 1명을 무료로 선택하면 서버 시간 기준 자동 전투가 시작됩니다.',
        items: ['1~5번 방: 일반 전투', '6번 방: 층 보스', '첫 영입 전에는 시간과 보상이 쌓이지 않음'],
      );
    }

    final battle = state.battle;
    final progress = battle.roomRequiredSeconds <= 0
        ? 0.0
        : (battle.roomProgressSeconds / battle.roomRequiredSeconds)
            .clamp(0.0, 1.0);
    final last = data.lastBattleSettlement;
    return ListView(
      key: const Key('idle-battle-runtime'),
      padding: const EdgeInsets.all(20),
      children: [
        Text('완전 자동 탑 전투', style: AppTypography.displayLg),
        const SizedBox(height: 8),
        Text(
          '앱을 닫아도 서버 시간을 기준으로 진행하며, 다시 열 때 한 번만 안전하게 정산합니다.',
          style: AppTypography.bodyMd.copyWith(color: AppColors.neutral700),
        ),
        const SizedBox(height: 18),
        Card(
          color: const Color(0xFF263659),
          child: Padding(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${state.towerFloor}층 · ${state.roomPosition}번 방',
                  key: const Key('battle-current-room'),
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 28,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  battle.currentRoomKind == 'BOSS' ? '층 보스 전투' : '일반 전투',
                  style: const TextStyle(color: Color(0xFFFFD36E)),
                ),
                const SizedBox(height: 16),
                LinearProgressIndicator(
                  value: progress,
                  minHeight: 10,
                  borderRadius: BorderRadius.circular(99),
                ),
                const SizedBox(height: 8),
                Text(
                  '${battle.roomProgressSeconds}초 / ${battle.roomRequiredSeconds}초 · 파티 전투력 ${battle.partyPower}',
                  style: const TextStyle(color: Color(0xFFD8DEEF)),
                ),
              ],
            ),
          ),
        ),
        if (last != null) ...[
          const SizedBox(height: 12),
          Card(
            key: const Key('battle-settlement-summary'),
            color: const Color(0xFFE9F7EF),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Text(
                '이번 정산 · 방 ${last.roomsCleared}개 · 보스 ${last.bossesCleared}회 · 골드 +${last.goldEarned}'
                '${last.capped ? ' · 오프라인 상한 적용' : ''}',
                style: AppTypography.bodyMd.copyWith(
                  color: const Color(0xFF245C3F),
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
          ),
        ],
        if (data.gameError != null) ...[
          const SizedBox(height: 12),
          _GameNotice(message: data.gameError!),
        ],
        const SizedBox(height: 14),
        FilledButton.icon(
          key: const Key('battle-settle-button'),
          onPressed: data.isGameLoading ? null : data.settleBattle,
          icon: data.isGameLoading
              ? const SizedBox.square(
                  dimension: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Icon(Icons.sync_rounded),
          label: Text(data.isGameLoading ? '정산 중' : '현재 진행 새로고침'),
        ),
        const SizedBox(height: 14),
        Text(
          '현재 조정 후보: 오프라인 최대 ${battle.offlineCapSeconds ~/ 3600}시간 · 1~5번 일반방 · 6번 보스방. '
          '골드와 전투 속도는 30회차 시뮬레이션 후 확정합니다.',
          style: AppTypography.captionSm,
        ),
      ],
    );
  }
}

class _RunStatusCard extends StatelessWidget {
  final CanonicalGameState state;

  const _RunStatusCard({required this.state});

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          child: Wrap(
            spacing: 18,
            runSpacing: 8,
            children: [
              Text('회차 ${state.runNumber}', style: AppTypography.captionSm),
              Text('최고 ${state.highestFloor}층', style: AppTypography.captionSm),
              Text('골드 ${state.gold}', style: AppTypography.captionSm),
              Text('별 조각 ${state.starShards}', style: AppTypography.captionSm),
            ],
          ),
        ),
      );
}

class _MenuCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _MenuCard(
      {required this.icon,
      required this.title,
      required this.subtitle,
      required this.onTap});

  @override
  Widget build(BuildContext context) => Card(
        margin: EdgeInsets.zero,
        child: InkWell(
          borderRadius: AppRadius.borderRadiusMd,
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(icon, color: const Color(0xFF8B5E34)),
                const SizedBox(height: 8),
                Text(title,
                    style: AppTypography.bodyMd
                        .copyWith(fontWeight: FontWeight.w800)),
                Text(subtitle,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: AppTypography.captionSm),
              ],
            ),
          ),
        ),
      );
}

class _DetailList extends StatelessWidget {
  final String title;
  final String description;
  final List<String> items;

  const _DetailList(
      {required this.title, required this.description, required this.items});

  @override
  Widget build(BuildContext context) => ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text(title, style: AppTypography.displayLg),
          const SizedBox(height: 10),
          Text(description,
              style:
                  AppTypography.bodyMd.copyWith(color: AppColors.neutral700)),
          const SizedBox(height: 18),
          Card(
            child: Column(
              children: [
                for (var index = 0; index < items.length; index++) ...[
                  ListTile(
                    leading: const Icon(Icons.check_circle_rounded,
                        color: AppColors.primary500),
                    title: Text(items[index]),
                  ),
                  if (index != items.length - 1) const Divider(height: 1),
                ],
              ],
            ),
          ),
        ],
      );
}

class _HeroDetail extends StatelessWidget {
  final List<(String, String, IconData)> heroes;

  const _HeroDetail({required this.heroes});

  @override
  Widget build(BuildContext context) => ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text('용사 6인 전직', style: AppTypography.displayLg),
          const SizedBox(height: 8),
          Text('첫 용사 1명은 무료 선택하고, 나머지는 0계층 대형 노드로 영입한 뒤 개별 전직합니다.',
              style: AppTypography.bodyMd),
          const SizedBox(height: 16),
          for (final hero in heroes)
            Card(
              child: ListTile(
                leading: CircleAvatar(child: Icon(hero.$3)),
                title: Text(hero.$2),
                subtitle: const Text('전직 단계와 전직 전용 장비 외형 영구 보존'),
              ),
            ),
        ],
      );
}

class _ConstellationDetail extends StatefulWidget {
  final CanonicalGameState? state;

  const _ConstellationDetail({required this.state});

  @override
  State<_ConstellationDetail> createState() => _ConstellationDetailState();
}

class _ConstellationDetailState extends State<_ConstellationDetail> {
  int _selectedLayer = 0;

  @override
  Widget build(BuildContext context) {
    final state = widget.state;
    final layers = state?.constellationLayers ?? const [];
    ConstellationLayerState? selected;
    for (final layer in layers) {
      if (layer.layer == _selectedLayer) selected = layer;
    }

    return ListView(
      key: const Key('constellation-detail'),
      padding: const EdgeInsets.fromLTRB(16, 20, 16, 32),
      children: [
        Text('360° 별자리 성장판', style: AppTypography.displayLg),
        const SizedBox(height: 8),
        Text(
          '중앙 0계층에서 5명을 영입하고, 바깥 1~6계층에서 여섯 용사를 개별 전직합니다.',
          style: AppTypography.bodyMd,
        ),
        const SizedBox(height: 12),
        if (state == null || !state.initialHeroSelected)
          const _GameNotice(
            message: '첫 무료 용사를 선택하면 중앙 0계층의 영입 노드 5개가 열립니다.',
          )
        else
          _StarterHeroCard(
            roleName: _roleNameForCode(state.starterHeroCode),
          ),
        const SizedBox(height: 12),
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Row(
            children: [
              for (var layer = 0; layer <= 6; layer++) ...[
                ChoiceChip(
                  key: Key('constellation-layer-$layer'),
                  label: Text(layer == 0 ? '0계층 · 영입' : '$layer계층'),
                  selected: _selectedLayer == layer,
                  onSelected: state?.initialHeroSelected == true
                      ? (_) => setState(() => _selectedLayer = layer)
                      : null,
                ),
                if (layer != 6) const SizedBox(width: 7),
              ],
            ],
          ),
        ),
        const SizedBox(height: 12),
        _ConstellationBoard(
          layer: _selectedLayer,
          nodes: selected?.nodes ?? const [],
        ),
        const SizedBox(height: 12),
        _ConstellationLayerSummary(
          layer: _selectedLayer,
          nodes: selected?.nodes ?? const [],
          starterSelected: state?.initialHeroSelected ?? false,
        ),
        const SizedBox(height: 12),
        const _DetailRuleCard(),
      ],
    );
  }
}

class _StarterHeroCard extends StatelessWidget {
  final String roleName;

  const _StarterHeroCard({required this.roleName});

  @override
  Widget build(BuildContext context) => Card(
        color: const Color(0xFFFFF3D6),
        child: ListTile(
          leading: const CircleAvatar(
            backgroundColor: Color(0xFFFFD36E),
            child: Icon(Icons.star_rounded, color: Color(0xFF6A451F)),
          ),
          title: Text('무료 첫 용사 · $roleName'),
          subtitle: const Text('0계층 영입 노드를 사용하지 않으며 환생 후에도 영구 보존됩니다.'),
        ),
      );
}

class _ConstellationBoard extends StatelessWidget {
  final int layer;
  final List<ConstellationNodeState> nodes;

  const _ConstellationBoard({required this.layer, required this.nodes});

  static const _radiusByLayer = [0.09, 0.16, 0.245, 0.325, 0.39, 0.445, 0.475];

  @override
  Widget build(BuildContext context) => Align(
        alignment: Alignment.topCenter,
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 620),
          child: Card(
            color: const Color(0xFF071426),
            clipBehavior: Clip.antiAlias,
            child: InteractiveViewer(
              minScale: 1,
              maxScale: 3,
              child: AspectRatio(
                aspectRatio: 1,
                child: Padding(
                  padding: const EdgeInsets.all(10),
                  child: LayoutBuilder(
                    builder: (context, constraints) {
                      final side = math.min(
                        constraints.maxWidth,
                        constraints.maxHeight,
                      );
                      final center = side / 2;
                      final radius = side * _radiusByLayer[layer];
                      return Stack(
                        key: const Key('constellation-board'),
                        children: [
                          Positioned.fill(
                            child: Image.asset(
                              'assets/images/game/constellation_board_base.png',
                              fit: BoxFit.contain,
                              filterQuality: FilterQuality.high,
                            ),
                          ),
                          for (var index = 0; index < nodes.length; index++)
                            _positionedNode(
                              node: nodes[index],
                              index: index,
                              count: nodes.length,
                              center: center,
                              radius: radius,
                            ),
                        ],
                      );
                    },
                  ),
                ),
              ),
            ),
          ),
        ),
      );

  Widget _positionedNode({
    required ConstellationNodeState node,
    required int index,
    required int count,
    required double center,
    required double radius,
  }) {
    final angle = -math.pi / 2 + (2 * math.pi * index / math.max(count, 1));
    const markerSize = 38.0;
    return Positioned(
      left: center + radius * math.cos(angle) - markerSize / 2,
      top: center + radius * math.sin(angle) - markerSize / 2,
      width: markerSize,
      height: markerSize,
      child: _ConstellationNodeMarker(node: node),
    );
  }
}

class _ConstellationNodeMarker extends StatelessWidget {
  final ConstellationNodeState node;

  const _ConstellationNodeMarker({required this.node});

  @override
  Widget build(BuildContext context) {
    final unlocked = node.state == 'UNLOCKED';
    final next = node.state == 'NEXT';
    final background = unlocked
        ? const Color(0xFFFFD36E)
        : next
            ? const Color(0xFF6ED4B2)
            : const Color(0xFF34435D);
    final foreground = unlocked
        ? const Color(0xFF5C3B16)
        : next
            ? const Color(0xFF123D35)
            : const Color(0xFFB8C0D2);
    return Tooltip(
      message: '${node.roleName} · ${_nodeStateLabel(node)}',
      child: Container(
        key: Key('constellation-node-${node.layer}-${node.heroCode}'),
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: background,
          border:
              Border.all(color: Colors.white.withValues(alpha: 0.75), width: 2),
          boxShadow: const [
            BoxShadow(
                color: Colors.black38, blurRadius: 5, offset: Offset(0, 2)),
          ],
        ),
        child: Icon(
          unlocked
              ? Icons.check_rounded
              : next
                  ? _roleIcon(node.heroCode)
                  : Icons.lock_rounded,
          size: 20,
          color: foreground,
        ),
      ),
    );
  }
}

class _ConstellationLayerSummary extends StatelessWidget {
  final int layer;
  final List<ConstellationNodeState> nodes;
  final bool starterSelected;

  const _ConstellationLayerSummary({
    required this.layer,
    required this.nodes,
    required this.starterSelected,
  });

  @override
  Widget build(BuildContext context) {
    if (!starterSelected) {
      return const _GameNotice(message: '첫 용사 선택 전에는 별자리 노드를 표시하지 않습니다.');
    }
    final unlocked = nodes.where((node) => node.state == 'UNLOCKED').length;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              layer == 0 ? '0계층 · 남은 용사 영입' : '$layer계층 · $layer차 전직',
              style: AppTypography.titleMd,
            ),
            const SizedBox(height: 4),
            Text(
              '${nodes.length}개 중 $unlocked개 해금',
              style: AppTypography.captionSm,
            ),
            const SizedBox(height: 10),
            for (final node in nodes)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 3),
                child: Row(
                  children: [
                    Icon(_roleIcon(node.heroCode), size: 18),
                    const SizedBox(width: 8),
                    Expanded(child: Text(node.roleName)),
                    Text(_nodeStateLabel(node), style: AppTypography.captionSm),
                  ],
                ),
              ),
            if (nodes.any((node) => node.state != 'UNLOCKED')) ...[
              const SizedBox(height: 10),
              Text(
                layer == 0
                    ? '영입 비용은 밸런스 확정 후 활성화됩니다.'
                    : '전직 비용은 밸런스 확정 후 활성화됩니다.',
                style: AppTypography.captionSm,
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _DetailRuleCard extends StatelessWidget {
  const _DetailRuleCard();

  @override
  Widget build(BuildContext context) {
    const items = [
      '0계층: 무료 첫 용사를 제외한 영입 노드 5개',
      '1~6계층: 용사별 전직 노드 각 6개',
      '소형·중형 노드: 회차 성장, 환생 시 초기화',
      '대형 노드·전직·전직 외형: 영구 보존',
    ];
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('보존 규칙', style: AppTypography.titleMd),
            const SizedBox(height: 4),
            Text(
              '대형 노드와 전직은 수집 성과이므로 환생해도 사라지지 않습니다.',
              style: AppTypography.captionSm,
            ),
            const SizedBox(height: 10),
            for (final item in items)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 3),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.check_circle_rounded,
                        size: 18, color: AppColors.primary500),
                    const SizedBox(width: 7),
                    Expanded(child: Text(item)),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}

String _nodeStateLabel(ConstellationNodeState node) => switch (node.state) {
      'UNLOCKED' => node.nodeKind == 'RECRUIT' ? '영입 완료' : '전직 완료',
      'NEXT' => '다음 전직',
      _ => '잠김',
    };

String _roleNameForCode(String? heroCode) => switch (heroCode) {
      'TANKER' => '탱커',
      'WARRIOR' => '전사',
      'MAGE' => '마법사',
      'ARCHER' => '궁수',
      'ROGUE' => '도적',
      'HEALER' => '치유사',
      _ => '선택 전',
    };

IconData _roleIcon(String heroCode) => switch (heroCode) {
      'TANKER' => Icons.shield_rounded,
      'WARRIOR' => Icons.sports_martial_arts_rounded,
      'MAGE' => Icons.auto_fix_high_rounded,
      'ARCHER' => Icons.gps_fixed_rounded,
      'ROGUE' => Icons.bolt_rounded,
      'HEALER' => Icons.healing_rounded,
      _ => Icons.star_outline_rounded,
    };

class _RebirthDetail extends StatelessWidget {
  final RebirthPreview? preview;

  const _RebirthDetail({required this.preview});

  @override
  Widget build(BuildContext context) {
    final reset = preview?.reset ?? const <String, int>{};
    final retain = preview?.retain ?? const <String, dynamic>{};
    return ListView(
      key: const Key('rebirth-rules'),
      padding: const EdgeInsets.all(20),
      children: [
        Text('환생 규칙', style: AppTypography.displayLg),
        const SizedBox(height: 8),
        Text('반복 성장의 재미는 되살리되, 어렵게 얻은 용사와 전직은 빼앗지 않습니다.',
            style: AppTypography.bodyMd),
        const SizedBox(height: 12),
        _GameNotice(
          message: preview == null
              ? '서버 미리보기를 불러오기 전입니다. 환생 실행 버튼은 제공하지 않습니다.'
              : preview!.canRebirth
                  ? '다음 환생은 ${preview!.nextRunNumber}회차입니다. 아래 수량을 확인한 뒤에만 실행할 수 있습니다.'
                  : '아직 초기화할 회차 진행이 없어 환생할 수 없습니다.',
        ),
        const SizedBox(height: 12),
        _RuleCard(
          color: const Color(0xFFFFEEE7),
          icon: Icons.restart_alt_rounded,
          title: '회차마다 초기화',
          items: [
            '탑 ${reset['tower_floor'] ?? 1}층 · ${reset['room_position'] ?? 1}번 방',
            '골드 ${reset['gold'] ?? 0}',
            '소형 노드 ${reset['small_nodes'] ?? 0}개 · 중형 노드 ${reset['medium_nodes'] ?? 0}개',
          ],
        ),
        const SizedBox(height: 12),
        _RuleCard(
          color: const Color(0xFFE8F7ED),
          icon: Icons.lock_rounded,
          title: '영구 보존',
          items: [
            '영입 상태와 최고 전직 차수·전직 외형',
            '대형 노드 ${retain['large_nodes'] ?? 0}개',
            '스킬·아바타·정령',
            '건강 정수 ${retain['health_essence'] ?? 0} · 별 조각 ${retain['star_shards'] ?? 0} · 초월 ${retain['transcendence_points'] ?? 0}',
          ],
        ),
      ],
    );
  }
}

class _RuleCard extends StatelessWidget {
  final Color color;
  final IconData icon;
  final String title;
  final List<String> items;

  const _RuleCard(
      {required this.color,
      required this.icon,
      required this.title,
      required this.items});

  @override
  Widget build(BuildContext context) => Card(
        color: color,
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(children: [
                Icon(icon),
                const SizedBox(width: 8),
                Text(title, style: AppTypography.titleMd)
              ]),
              const SizedBox(height: 10),
              for (final item in items)
                Padding(
                    padding: const EdgeInsets.only(top: 6),
                    child: Text('• $item')),
            ],
          ),
        ),
      );
}
