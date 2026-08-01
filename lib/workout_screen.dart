import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'api_data_provider.dart';

/// HEALTH IS ALL - Workout Record & Real-time METs Analytics Screen
/// Dual-Excellence: 운동 소모 칼로리 정밀 시각화 + '건강이' 피드백 연동
///
/// PATCH_009: ApiDataProvider(실제 백엔드 연동)로 전환. home_screen.dart의
/// 레퍼런스 패턴(async/await + lastError 확인)을 그대로 따랐다.
class WorkoutScreen extends StatefulWidget {
  const WorkoutScreen({Key? key}) : super(key: key);

  @override
  State<WorkoutScreen> createState() => _WorkoutScreenState();
}

class _WorkoutScreenState extends State<WorkoutScreen> {
  final _formKey = GlobalKey<FormState>();
  String _workoutType = '러닝';
  int _durationMinutes = 30;
  String _intensity = '보통';

  double get _estimatedCalories {
    double met = 4.0;
    if (_workoutType == '러닝') met = 8.0;
    if (_workoutType == '등산') met = 6.5;
    if (_workoutType == '사이클') met = 6.8;
    if (_workoutType == '근력운동') met = 5.0;

    final double intensityFactor = _intensity == '강함' ? 1.25 : (_intensity == '가볍게' ? 0.85 : 1.0);
    return met * 70.0 * (_durationMinutes / 60.0) * intensityFactor;
  }

  Future<void> _submitWorkoutLog() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      final provider = Provider.of<ApiDataProvider>(context, listen: false);
      await provider.logWorkout(_durationMinutes, _estimatedCalories.toInt());

      if (!mounted) return;

      if (provider.lastError != null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(provider.lastError!),
            backgroundColor: Colors.red.shade400,
          ),
        );
        return;
      }

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('$_durationMinutes분 완수! 50 Exp 획득 및 건강이 활력 상승!'),
          backgroundColor: Colors.deepOrange.shade600,
        ),
      );

      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('운동 기록하기', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 1,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(18.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20.0),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [Colors.deepOrange.shade400, Colors.orange.shade300],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(color: Colors.orange.withOpacity(0.3), blurRadius: 10, offset: const Offset(0, 4)),
                  ],
                ),
                child: Column(
                  children: [
                    const Text('예상 운동 소모 칼로리', style: TextStyle(color: Colors.white, fontSize: 14)),
                    const SizedBox(height: 8),
                    Text(
                      '${_estimatedCalories.toStringAsFixed(0)} kcal',
                      style: const TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      '$_workoutType · $_intensity · METs 기반 자동 연산',
                      style: const TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              const Text('운동 세부 정보', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                value: _workoutType,
                decoration: InputDecoration(
                  labelText: '운동 종목',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
                items: ['러닝', '걷기', '등산', '사이클', '근력운동'].map((type) {
                  return DropdownMenuItem(value: type, child: Text(type));
                }).toList(),
                onChanged: (val) => setState(() => _workoutType = val!),
              ),
              const SizedBox(height: 16),
              Text('운동 시간: $_durationMinutes분', style: const TextStyle(fontWeight: FontWeight.bold)),
              Slider(
                value: _durationMinutes.toDouble(),
                min: 10,
                max: 120,
                divisions: 22,
                label: '$_durationMinutes분',
                onChanged: (val) => setState(() => _durationMinutes = val.round()),
              ),
              const SizedBox(height: 12),
              const Text('수행 강도', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: ['가볍게', '보통', '강함'].map((level) {
                  final isSelected = _intensity == level;
                  return ChoiceChip(
                    label: Text(level),
                    selected: isSelected,
                    selectedColor: Colors.deepOrange.shade100,
                    onSelected: (selected) {
                      if (selected) setState(() => _intensity = level);
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 32),
              SizedBox(
                width: double.infinity,
                height: 52,
                child: ElevatedButton.icon(
                  onPressed: _submitWorkoutLog,
                  icon: const Icon(Icons.directions_run, color: Colors.white),
                  label: const Text('운동 기록 완료 및 50 Exp 받기', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepOrange,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
