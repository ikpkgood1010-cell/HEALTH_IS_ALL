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
    ('탱커', Icons.shield_rounded),
    ('전사', Icons.sports_martial_arts_rounded),
    ('마법사', Icons.auto_fix_high_rounded),
    ('궁수', Icons.gps_fixed_rounded),
    ('도적', Icons.bolt_rounded),
    ('치유사', Icons.healing_rounded),
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
              ? '0층 대형 노드에서 영입할 용사를 선택하면 자동 전투가 시작됩니다.'
              : '6명의 용사가 다음 적을 향해 이동합니다.',
        ),
        if (data.gameError != null) ...[
          const SizedBox(height: 10),
          _GameNotice(message: data.gameError!),
        ],
        if (state != null) ...[
          const SizedBox(height: 10),
          _RunStatusCard(state: state),
        ],
        const SizedBox(height: 18),
        Text('나의 6인 파티', style: AppTypography.titleMd),
        const SizedBox(height: 4),
        Text(
          '각 용사는 0층 대형 노드에서 확정 영입합니다.',
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
    (String, IconData) hero,
    CanonicalGameState? state,
  ) {
    CanonicalGameHero? saved;
    for (final item in state?.heroes ?? const <CanonicalGameHero>[]) {
      if (item.roleName == hero.$1) {
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
            child: Icon(recruited ? hero.$2 : Icons.lock_outline_rounded),
          ),
          const SizedBox(height: 6),
          Text(hero.$1, style: AppTypography.captionSm),
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
        return _DetailList(
          title: '완전 자동 탑 전투',
          description:
              '용사 6명이 앞으로 이동하며 방을 차례로 공략합니다. 수동 회피·강제 협동 없이 스킬도 자동으로 사용합니다.',
          items: const ['1~5번 방: 일반 전투', '6번 방: 층 보스', '활성 스킬: 최대 6개 · 자동 사용'],
        );
      case _GameSection.village:
        return const _DetailList(
          title: '마을과 길드',
          description: '길드는 건강 앱의 하단 탭이 아니라 게임 세계 안의 거점입니다.',
          items: ['시설·NPC·교류 기능은 경제 검증 뒤 순차 개방', '현재 단계에서는 위치와 진입 구조만 확정'],
        );
      case _GameSection.heroes:
        return _HeroDetail(heroes: _heroes);
      case _GameSection.constellation:
        return const _DetailList(
          title: '360° 별자리 성장판',
          description: '0층부터 6층까지, 각 층에 용사별 대형 노드 6개가 있습니다.',
          items: [
            '0층 대형 노드: 용사별 확정 영입',
            '1~6층 대형 노드: 용사별 개별 전직',
            '소형·중형 노드: 회차 성장, 환생 시 초기화',
            '대형 노드·전직·전직 외형: 영구 보존',
          ],
        );
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

  void _open(_GameSection section) => setState(() => _section = section);

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
  final List<(String, IconData)> heroes;

  const _HeroDetail({required this.heroes});

  @override
  Widget build(BuildContext context) => ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text('용사 6인 전직', style: AppTypography.displayLg),
          const SizedBox(height: 8),
          Text('각 용사는 별자리 대형 노드를 통해 확정 영입되고 개별 전직합니다.',
              style: AppTypography.bodyMd),
          const SizedBox(height: 16),
          for (final hero in heroes)
            Card(
              child: ListTile(
                leading: CircleAvatar(child: Icon(hero.$2)),
                title: Text(hero.$1),
                subtitle: const Text('전직 단계와 전직 전용 장비 외형 영구 보존'),
              ),
            ),
        ],
      );
}

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
