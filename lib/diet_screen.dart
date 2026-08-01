import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'api_data_provider.dart';

/// HEALTH IS ALL - Diet Record & Dynamic Nutrition Analytics Screen
/// Dual-Excellence: 영양 지표의 명확한 전달 + 실시간 Exp 연동
///
/// PATCH_009: ApiDataProvider(실제 백엔드 연동)로 전환. home_screen.dart의
/// 레퍼런스 패턴(async/await + lastError 확인)을 그대로 따랐다.
class DietScreen extends StatefulWidget {
  const DietScreen({Key? key}) : super(key: key);

  @override
  State<DietScreen> createState() => _DietScreenState();
}

class _DietScreenState extends State<DietScreen> {
  final _formKey = GlobalKey<FormState>();
  String _mealType = '점심';
  double _calories = 550.0;
  double _carbs = 65.0;
  double _protein = 30.0;
  double _fat = 15.0;
  double _fiber = 6.0;

  Future<void> _submitDietLog() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      final provider = Provider.of<ApiDataProvider>(context, listen: false);
      await provider.logMeal(_calories.toInt(), _mealType);

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
          content: Text("$_mealType 식단 기록 완료! '건강이'가 기뻐하며 Exp가 충전되었습니다."),
          backgroundColor: Colors.green.shade700,
        ),
      );

      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('식단 기록하기', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold)),
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
                padding: const EdgeInsets.all(16.0),
                decoration: BoxDecoration(
                  color: Colors.green.shade50,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.green.shade200),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('실시간 영양 균형 분석', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.green)),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _buildNutrientInfo('탄수화물', '$_carbs g', Colors.orange),
                        _buildNutrientInfo('단백질', '$_protein g', Colors.blue),
                        _buildNutrientInfo('지방', '$_fat g', Colors.redAccent),
                        _buildNutrientInfo('식이섬유', '$_fiber g', Colors.teal),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              const Text('식사 정보 입력', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                value: _mealType,
                decoration: InputDecoration(
                  labelText: '식사 종류',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
                items: ['아침', '점심', '저녁', '간식'].map((type) {
                  return DropdownMenuItem(value: type, child: Text(type));
                }).toList(),
                onChanged: (val) => setState(() => _mealType = val!),
              ),
              const SizedBox(height: 14),
              TextFormField(
                initialValue: _calories.toString(),
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: '총 칼로리 (kcal)',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  suffixText: 'kcal',
                ),
                onSaved: (val) => _calories = double.tryParse(val ?? '0') ?? 0,
              ),
              const SizedBox(height: 14),
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      initialValue: _protein.toString(),
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: '단백질 (g)',
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      onSaved: (val) => _protein = double.tryParse(val ?? '0') ?? 0,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: TextFormField(
                      initialValue: _fiber.toString(),
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: '식이섬유 (g)',
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      onSaved: (val) => _fiber = double.tryParse(val ?? '0') ?? 0,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 28),
              SizedBox(
                width: double.infinity,
                height: 52,
                child: ElevatedButton.icon(
                  onPressed: _submitDietLog,
                  icon: const Icon(Icons.check_circle_outline, color: Colors.white),
                  label: const Text('식단 저장 및 30 Exp 받기', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green.shade600,
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

  Widget _buildNutrientInfo(String label, String value, Color color) {
    return Column(
      children: [
        Text(label, style: TextStyle(fontSize: 12, color: Colors.grey.shade700)),
        const SizedBox(height: 4),
        Text(value, style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: color)),
      ],
    );
  }
}
