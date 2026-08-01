import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app_theme.dart';

/// ============================================================================
/// Meal & Exercise Logger Screen Implementation (v1.0)
/// Based on: Component_Catalog.md & Screen_Specification_Master.md
/// ============================================================================

enum LogCategory { meal, exercise }

enum MealTimeType { breakfast, lunch, dinner, snack }

class MealRecord {
final String id;
final MealTimeType timeType;
final String foodName;
final int calories;
final DateTime time;

MealRecord({
required this.id,
required this.timeType,
required this.foodName,
required this.calories,
required this.time,
});
}

class ExerciseRecord {
final String id;
final String exerciseName;
final int durationMinutes;
final int caloriesBurned;
final DateTime time;

ExerciseRecord({
required this.id,
required this.exerciseName,
required this.durationMinutes,
required this.caloriesBurned,
required this.time,
});
}

// Log State Notifiers
class MealLogNotifier extends StateNotifier<List<MealRecord>> {
MealLogNotifier()
: super([
MealRecord(
id: 'm1',
timeType: MealTimeType.breakfast,
foodName: '훈제오리 구이 & 야채 찜',
calories: 420,
time: DateTime.now().subtract(const Duration(hours: 4)),
),
 ]);

void addRecord(MealTimeType type, String foodName, int calories) {
final record = MealRecord(
id: DateTime.now().millisecondsSinceEpoch.toString(),
timeType: type,
foodName: foodName,
calories: calories,
time: DateTime.now(),
);
state = [record, ...state];
}
}

class ExerciseLogNotifier extends StateNotifier<List<ExerciseRecord>> {
ExerciseLogNotifier()
: super([
ExerciseRecord(
id: 'e1',
exerciseName: '실내 사이클',
durationMinutes: 30,
caloriesBurned: 210,
time: DateTime.now().subtract(const Duration(hours: 2)),
),
 ]);

void addRecord(String name, int minutes, int calories) {
final record = ExerciseRecord(
id: DateTime.now().millisecondsSinceEpoch.toString(),
exerciseName: name,
durationMinutes: minutes,
caloriesBurned: calories,
time: DateTime.now(),
);
state = [record, ...state];
}
}

final mealLogProvider =
StateNotifierProvider<MealLogNotifier, List<MealRecord>>((ref) => MealLogNotifier());

final exerciseLogProvider =
StateNotifierProvider<ExerciseLogNotifier, List<ExerciseRecord>>((ref) => ExerciseLogNotifier());

class MealExerciseLoggerScreen extends ConsumerStatefulWidget {
const MealExerciseLoggerScreen({Key? key}) : super(key: key);

@override
ConsumerState<MealExerciseLoggerScreen> createState() => _MealExerciseLoggerScreenState();
}

class _MealExerciseLoggerScreenState extends ConsumerState<MealExerciseLoggerScreen> {
LogCategory _selectedCategory = LogCategory.meal;

// Meal Form Controllers
MealTimeType _selectedMealTime = MealTimeType.lunch;
final _foodNameController = TextEditingController();
final _mealCalorieController = TextEditingController();

// Exercise Form Controllers
final _exerciseNameController = TextEditingController();
final _durationController = TextEditingController();
final _exerciseCalorieController = TextEditingController();

@override
void dispose() {
_foodNameController.dispose();
_mealCalorieController.dispose();
_exerciseNameController.dispose();
_durationController.dispose();
_exerciseCalorieController.dispose();
super.dispose();
}

void _submitMealLog() {
final foodName = _foodNameController.text.trim();
final calories = int.tryParse(_mealCalorieController.text.trim()) ?? 0;

if (foodName.isEmpty) {
_showSnackBar('음식명을 입력해 주세요.');
return;
}

ref.read(mealLogProvider.notifier).addRecord(_selectedMealTime, foodName, calories);
_foodNameController.clear();
_mealCalorieController.clear();
_showSnackBar('식단 기록이 등록되었습니다!');
}

void _submitExerciseLog() {
final exName = _exerciseNameController.text.trim();
final minutes = int.tryParse(_durationController.text.trim()) ?? 0;
final calories = int.tryParse(_exerciseCalorieController.text.trim()) ?? 0;

if (exName.isEmpty || minutes <= 0) {
_showSnackBar('운동 이름과 시간을 올바르게 입력해 주세요.');
return;
}

ref.read(exerciseLogProvider.notifier).addRecord(exName, minutes, calories);
_exerciseNameController.clear();
_durationController.clear();
_exerciseCalorieController.clear();
_showSnackBar('운동 기록이 등록되었습니다!');
}

void _showSnackBar(String text) {
ScaffoldMessenger.of(context).showSnackBar(
SnackBar(
content: Text(text),
duration: const Duration(seconds: 2),
),
);
}

@override
Widget build(BuildContext context) {
final mealLogs = ref.watch(mealLogProvider);
final exerciseLogs = ref.watch(exerciseLogProvider);

return Scaffold(
appBar: AppBar(
title: const Text('식단 & 운동 기록하기'),
),
body: SingleChildScrollView(
physics: const BouncingScrollPhysics(),
padding: const EdgeInsets.all(AppSpacing.md),
child: Column(
crossAxisAlignment: CrossAxisAlignment.start,
children: [
// Segmented Control Switcher
Row(
children: [
Expanded(
child: _buildCategoryTab('🥗 식단 기록', LogCategory.meal),
),
const SizedBox(width: AppSpacing.sm),
Expanded(
child: _buildCategoryTab('🏃‍♂️ 운동 기록', LogCategory.exercise),
),
 ],
),
const SizedBox(height: AppSpacing.lg),

// Input Form Block
_selectedCategory == LogCategory.meal
? _buildMealInputForm()
: _buildExerciseInputForm(),

const SizedBox(height: AppSpacing.xl),

// Timeline Records Display
Text(
_selectedCategory == LogCategory.meal ? '오늘 기록된 식단' : '오늘 기록된 운동',
style: AppTypography.titleMd,
),
const SizedBox(height: AppSpacing.sm),

_selectedCategory == LogCategory.meal
? _buildMealList(mealLogs)
: _buildExerciseList(exerciseLogs),
],
),
),
);
}

Widget _buildCategoryTab(String title, LogCategory category) {
final isSelected = _selectedCategory == category;
return GestureDetector(
onTap: () => setState(() => _selectedCategory = category),
child: AnimatedContainer(
duration: const Duration(milliseconds: 200),
padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
alignment: Alignment.center,
decoration: BoxDecoration(
color: isSelected ? AppColors.primary500 : Colors.white,
borderRadius: AppRadius.borderRadiusMd,
border: Border.all(
color: isSelected ? AppColors.primary500 : AppColors.neutral500,
),
),
child: Text(
title,
style: AppTypography.bodyMd.copyWith(
color: isSelected ? Colors.white : AppColors.neutral900,
fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
),
),
),
);
}

Widget _buildMealInputForm() {
return Card(
child: Padding(
padding: const EdgeInsets.all(AppSpacing.md),
child: Column(
crossAxisAlignment: CrossAxisAlignment.start,
children: [
DropdownButtonFormField<MealTimeType>(
value: _selectedMealTime,
items: const [
DropdownMenuItem(value: MealTimeType.breakfast, child: Text('🌅 아침')),
DropdownMenuItem(value: MealTimeType.lunch, child: Text('☀️ 점심')),
DropdownMenuItem(value: MealTimeType.dinner, child: Text('🌙 저녁')),
DropdownMenuItem(value: MealTimeType.snack, child: Text('🥨 간식')),
 ],
onChanged: (val) {
if (val != null) setState(() => _selectedMealTime = val);
},
decoration: const InputDecoration(
labelText: '식사 시간대',
border: OutlineInputBorder(),
),
),
const SizedBox(height: AppSpacing.md),
TextField(
controller: _foodNameController,
decoration: const InputDecoration(
labelText: '음식명',
hintText: '예: 닭가슴살 샐러드, 현미밥',
border: OutlineInputBorder(),
),
),
const SizedBox(height: AppSpacing.md),
TextField(
controller: _mealCalorieController,
keyboardType: TextInputType.number,
decoration: const InputDecoration(
labelText: '추정 칼로리 (kcal)',
hintText: '예: 350',
border: OutlineInputBorder(),
),
),
const SizedBox(height: AppSpacing.lg),
ElevatedButton.icon(
onPressed: _submitMealLog,
icon: const Icon(Icons.check),
label: const Text('식단 기록 추가하기'),
),
],
),
),
);
}

Widget _buildExerciseInputForm() {
return Card(
child: Padding(
padding: const EdgeInsets.all(AppSpacing.md),
child: Column(
crossAxisAlignment: CrossAxisAlignment.start,
children: [
TextField(
controller: _exerciseNameController,
decoration: const InputDecoration(
labelText: '운동 종목',
hintText: '예: 인터벌 러닝, 하체 웨이트',
border: OutlineInputBorder(),
),
),
const SizedBox(height: AppSpacing.md),
Row(
children: [
Expanded(
child: TextField(
controller: _durationController,
keyboardType: TextInputType.number,
decoration: const InputDecoration(
labelText: '운동 시간 (분)',
hintText: '30',
border: OutlineInputBorder(),
),
),
),
const SizedBox(width: AppSpacing.md),
Expanded(
child: TextField(
controller: _exerciseCalorieController,
keyboardType: TextInputType.number,
decoration: const InputDecoration(
labelText: '소모 칼로리 (kcal)',
hintText: '200',
border: OutlineInputBorder(),
),
),
),
 ],
),
const SizedBox(height: AppSpacing.lg),
ElevatedButton.icon(
onPressed: _submitExerciseLog,
icon: const Icon(Icons.fitness_center),
label: const Text('운동 기록 추가하기'),
),
],
),
),
);
}

Widget _buildMealList(List<MealRecord> records) {
if (records.isEmpty) {
return const Padding(
padding: EdgeInsets.all(AppSpacing.lg),
child: Center(child: Text('오늘 기록된 식단이 없습니다.')),
);
}
return Column(
children: records.map((record) {
String label = '식사';
if (record.timeType == MealTimeType.breakfast) label = '아침';
if (record.timeType == MealTimeType.lunch) label = '점심';
if (record.timeType == MealTimeType.dinner) label = '저녁';
if (record.timeType == MealTimeType.snack) label = '간식';

return Card(
child: ListTile(
leading: CircleAvatar(
backgroundColor: AppColors.primary100,
child: Text(
label[0],
style: const TextStyle(
color: AppColors.primary500,
fontWeight: FontWeight.bold,
),
),
),
title: Text(record.foodName, style: AppTypography.bodyMd),
subtitle: Text('${record.calories} kcal'),
),
);
}).toList(),
);
}

Widget _buildExerciseList(List<ExerciseRecord> records) {
if (records.isEmpty) {
return const Padding(
padding: EdgeInsets.all(AppSpacing.lg),
child: Center(child: Text('오늘 기록된 운동이 없습니다.')),
);
}
return Column(
children: records.map((record) {
return Card(
child: ListTile(
leading: const CircleAvatar(
backgroundColor: AppColors.primary100,
child: Icon(Icons.directions_run, color: AppColors.secondary500),
),
title: Text(record.exerciseName, style: AppTypography.bodyMd),
subtitle: Text('${record.caloriesBurned} kcal 소모'),
),
);
}).toList(),
);
}
}