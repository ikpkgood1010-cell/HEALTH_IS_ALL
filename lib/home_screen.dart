import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'widgets/health_i_widget.dart';
import 'api_data_provider.dart';

/// HEALTH IS ALL - Main Home Screen
/// Dual-Excellence: 건강 정보의 명확한 전달 + '건강이' 게임성 조화
///
/// [레퍼런스 구현] 이 화면은 ApiDataProvider(실제 백엔드 연동)를 사용하는
/// 예시다. 다른 화면(diet_screen, workout_screen 등)도 동일한 패턴을
/// 따르면 된다:
///   1. initState에서 context.read<ApiDataProvider>().refreshStatus() 호출
///   2. build에서 context.watch<ApiDataProvider>()로 값을 구독
///   3. 기록 버튼에서 provider의 async 메서드(logMeal 등) 호출
///   4. isLoading / lastError를 살펴 로딩 인디케이터·에러 스낵바 표시
class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    // 화면 진입 시 서버에서 최신 상태를 가져온다.
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
              const Text(
                '오늘의 건강 요약',
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
                      title: '오늘 운동',
                      value: '${provider.workoutMinutes}',
                      unit: '분',
                      icon: Icons.fitness_center,
                      color: Colors.deepOrange,
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
              const SizedBox(height: 16),
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
              const SizedBox(height: 24),
              HealthIWidget(
                currentExp: provider.currentExp,
                level: provider.level,
                emotionState: provider.emotionState,
                dialogue: provider.dialogue,
                onTapHealthI: _onTapHealthI,
              ),
              const SizedBox(height: 24),
              const Text(
                '빠른 기록하기',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
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
                    icon: Icons.fitness_center,
                    label: '운동 +30분',
                    color: Colors.deepOrange,
                    onTap: () => _quickLog(
                      action: () => provider.logWorkout(30, 200),
                      successMessage: '운동 30분 기록 완료! 50 Exp 획득',
                      color: Colors.deepOrange.shade600,
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
}
