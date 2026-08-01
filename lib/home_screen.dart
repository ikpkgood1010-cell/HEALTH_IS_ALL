import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'widgets/health_i_widget.dart';
import 'api_data_provider.dart';
import 'spirit_screen.dart';
import 'workout_screen.dart';
import 'diet_screen.dart';

/// HEALTH IS ALL - Main Home Screen
/// Dual-Excellence: 건강 정보의 명확한 전달 + '건강이' 게임성 조화
///
/// [레퍼런스 구현] 이 화면은 ApiDataProvider(실제 백엔드 연동)를 사용하는
/// 예시다.
///
/// 화면 순서(사용자 요청 반영):
///   1. 상단 - 정령(미니게임) 섹션
///   2. 중간 - 운동 섹션
///   3. 하단 - 식단/칼로리 섹션
/// 각 섹션 끝에는 그동안 화면은 있었지만 진입 경로가 없어 "고아 화면"으로
/// 남아있던 SpiritScreen/WorkoutScreen/DietScreen으로 가는 카드형 버튼을
/// 추가했다.
class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ApiDataProvider>().refreshStatus();
    });
  }

  void _onTapHealthI() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text("'건강이'가 기분 좋게 춤을 춥니다! (+5 마음 반응)"),
        duration: Duration(seconds: 1),
      ),
    );
  }

  Future<void> _quickLog({
    required Future<void> Function() action,
    required String successMessage,
    required Color color,
  }) async {
    await action();
    if (!mounted) return;
    final provider = context.read<ApiDataProvider>();
    if (provider.lastError != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(provider.lastError!), backgroundColor: Colors.red.shade400),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(successMessage), backgroundColor: color),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<ApiDataProvider>();

    return Scaffold(
      backgroundColor: const Color(0xFFF7F9FC),
      appBar: AppBar(
        title: const Text(
          'HEALTH IS ALL',
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.black87),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          if (provider.isLoading)
            const Padding(
              padding: EdgeInsets.only(right: 16),
              child: Center(
                child: SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                ),
              ),
            )
          else
            IconButton(
              icon: const Icon(Icons.refresh, color: Colors.black87),
              onPressed: () => provider.refreshStatus(),
            ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () => provider.refreshStatus(),
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 18.0, vertical: 10.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (provider.lastError != null) ...[
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.red.shade200),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.wifi_off, color: Colors.red.shade400, size: 18),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          provider.lastError!,
                          style: TextStyle(color: Colors.red.shade700, fontSize: 12),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
              ],

              // ============== 1. 상단: 정령 / 미니게임 섹션 ==============
              const Text(
                '나의 정령',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(
                    child: _buildHealthCard(
                      title: '일일 Exp',
                      value: '${provider.todayExpGained}',
                      unit: '/ ${provider.dailyExpCap} Exp',
                      icon: Icons.stars,
                      color: Colors.purple,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _buildHealthCard(
                      title: '연속 기록',
                      value: '${provider.streakDays}',
                      unit: '일째',
                      icon: Icons.local_fire_department_outlined,
                      color: Colors.teal,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              HealthIWidget(
                currentExp: provider.currentExp,
                level: provider.level,
                emotionState: provider.emotionState,
                dialogue: provider.dialogue,
                onTapHealthI: _onTapHealthI,
              ),
              const SizedBox(height: 12),
              _buildNavCard(
                icon: Icons.auto_awesome,
                title: '정령이랑 더 놀아주기',
                subtitle: '교감하고 정령의 속성 균형을 확인해요',
                color: Colors.purple,
                onTap: () => Navigator.of(context).push(
                  MaterialPageRoute(builder: (_) => const SpiritScreen()),
                ),
              ),

              const SizedBox(height: 28),

              // ============== 2. 중간: 운동 섹션 ==============
              const Text(
                '오늘 운동',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              _buildHealthCard(
                title: '오늘 운동',
                value: '${provider.workoutMinutes}',
                unit: '분',
                icon: Icons.fitness_center,
                color: Colors.deepOrange,
              ),
              const SizedBox(height: 12),
              Center(
                child: _buildActionButton(
                  icon: Icons.fitness_center,
                  label: '운동 +30분',
                  color: Colors.deepOrange,
                  onTap: () => _quickLog(
                    action: () => provider.logWorkout(30, 200),
                    successMessage: '운동 30분 기록 완료! 50 Exp 획득',
                    color: Colors.deepOrange.shade600,
                  ),
                ),
              ),
              const SizedBox(height: 12),
              _buildNavCard(
                icon: Icons.edit_note,
                title: '운동 상세 기록하기',
                subtitle: '운동 종목/강도까지 직접 입력해요',
                color: Colors.deepOrange,
                onTap: () => Navigator.of(context).push(
                  MaterialPageRoute(builder: (_) => const WorkoutScreen()),
                ),
              ),

              const SizedBox(height: 28),

              // ============== 3. 하단: 식단 / 칼로리 섹션 ==============
              const Text(
                '식단과 칼로리',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(
                    child: _buildHealthCard(
                      title: '칼로리',
                      value: '${provider.consumedCalories}',
                      unit: '/ ${provider.targetCalories} kcal',
                      icon: Icons.local_fire_department,
                      color: Colors.orange,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _buildHealthCard(
                      title: '수분',
                      value: provider.waterLiters.toStringAsFixed(1),
                      unit: 'L / ${provider.targetWaterLiters.toStringAsFixed(1)}L',
                      icon: Icons.water_drop,
                      color: Colors.cyan,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _buildActionButton(
                    icon: Icons.restaurant,
                    label: '식단 +550kcal',
                    color: Colors.green,
                    onTap: () => _quickLog(
                      action: () => provider.logMeal(550, '간편 기록'),
                      successMessage: '식단 550kcal 기록 완료! 30 Exp 획득',
                      color: Colors.green.shade700,
                    ),
                  ),
                  _buildActionButton(
                    icon: Icons.water_drop,
                    label: '물 250ml',
                    color: Colors.cyan,
                    onTap: () => _quickLog(
                      action: () => provider.addWater(0.25),
                      successMessage: '물 250ml 기록 완료! 10 Exp 획득',
                      color: Colors.cyan.shade700,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              _buildNavCard(
                icon: Icons.edit_note,
                title: '식단 상세 기록하기',
                subtitle: '식사 종류/탄단지까지 직접 입력해요',
                color: Colors.green,
                onTap: () => Navigator.of(context).push(
                  MaterialPageRoute(builder: (_) => const DietScreen()),
                ),
              ),
              const SizedBox(height: 12),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHealthCard({
    required String title,
    required String value,
    required String unit,
    required IconData icon,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.03),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, size: 20, color: color),
              const SizedBox(width: 6),
              Text(title, style: TextStyle(color: Colors.grey.shade600, fontSize: 13)),
            ],
          ),
          const SizedBox(height: 8),
          RichText(
            text: TextSpan(
              children: [
                TextSpan(
                  text: value,
                  style: const TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.bold,
                    color: Colors.black87,
                  ),
                ),
                TextSpan(
                  text: ' $unit',
                  style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionButton({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        width: 100,
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 6),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 8),
            Text(
              label,
              textAlign: TextAlign.center,
              style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 11),
            ),
          ],
        ),
      ),
    );
  }

  /// 그동안 진입 경로가 없어 "고아 화면"으로 남아있던 상세 화면들
  /// (정령/운동/식단)로 이동하는 카드형 버튼.
  Widget _buildNavCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required Color color,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: color.withOpacity(0.08),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: color.withOpacity(0.25)),
        ),
        child: Row(
          children: [
            Icon(icon, color: color, size: 22),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      color: color,
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    subtitle,
                    style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                  ),
                ],
              ),
            ),
            Icon(Icons.chevron_right, color: color),
          ],
        ),
      ),
    );
  }
}
