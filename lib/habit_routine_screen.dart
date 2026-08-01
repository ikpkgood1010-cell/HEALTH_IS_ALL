import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app_theme.dart';

/// ============================================================================
/// Habit Routine Screen Implementation (v1.0)
/// Based on: Component_Catalog.md & Screen_Specification_Master.md
/// ============================================================================

enum HabitCategory { morning, afternoon, evening, all }

class HabitRoutineModel {
final String id;
final String title;
final String category; // 'morning', 'afternoon', 'evening'
final bool isCompleted;
final int streakCount;

HabitRoutineModel({
required this.id,
required this.title,
required this.category,
this.isCompleted = false,
this.streakCount = 0,
});

HabitRoutineModel copyWith({
String? id,
String? title,
String? category,
bool? isCompleted,
int? streakCount,
}) {
return HabitRoutineModel(
id: id ?? this.id,
title: title ?? this.title,
category: category ?? this.category,
isCompleted: isCompleted ?? this.isCompleted,
streakCount: streakCount ?? this.streakCount,
);
}
}

// State Notifier for Habits
class HabitRoutineNotifier extends StateNotifier<List<HabitRoutineModel>> {
HabitRoutineNotifier()
: super([
HabitRoutineModel(
id: '1',
title: '아침 미온수 500ml 마시기',
category: 'morning',
isCompleted: true,
streakCount: 12,
),
HabitRoutineModel(
id: '2',
title: '비타민 및 영양제 섭취',
category: 'morning',
isCompleted: true,
streakCount: 5,
),
HabitRoutineModel(
id: '3',
title: '점심 식사 후 10분 산책',
category: 'afternoon',
isCompleted: false,
streakCount: 3,
),
HabitRoutineModel(
id: '4',
title: '저녁 폼롤러 스트레칭 15분',
category: 'evening',
isCompleted: false,
streakCount: 8,
),
 ]);

void toggleHabit(String id) {
state = state.map((habit) {
if (habit.id == id) {
final nextStatus = !habit.isCompleted;
return habit.copyWith(
isCompleted: nextStatus,
streakCount: nextStatus ? habit.streakCount + 1 : (habit.streakCount > 0 ? habit.streakCount - 1 : 0),
);
}
return habit;
}).toList();
}

void addHabit(String title, String category) {
final newHabit = HabitRoutineModel(
id: DateTime.now().millisecondsSinceEpoch.toString(),
title: title,
category: category,
isCompleted: false,
streakCount: 0,
);
state = [...state, newHabit];
}
}

final habitRoutineProvider =
StateNotifierProvider<HabitRoutineNotifier, List<HabitRoutineModel>>((ref) {
return HabitRoutineNotifier();
});

final habitFilterProvider = StateProvider<HabitCategory>((ref) => HabitCategory.all);

class HabitRoutineScreen extends ConsumerWidget {
const HabitRoutineScreen({Key? key}) : super(key: key);

@override
Widget build(BuildContext context, WidgetRef ref) {
final habits = ref.watch(habitRoutineProvider);
final currentFilter = ref.watch(habitFilterProvider);

final filteredHabits = habits.where((habit) {
if (currentFilter == HabitCategory.morning) return habit.category == 'morning';
if (currentFilter == HabitCategory.afternoon) return habit.category == 'afternoon';
if (currentFilter == HabitCategory.evening) return habit.category == 'evening';
return true;
}).toList();

final completedCount = habits.where((h) => h.isCompleted).length;
final totalCount = habits.length;
final progressRatio = totalCount == 0 ? 0.0 : completedCount / totalCount;

return Scaffold(
appBar: AppBar(
title: const Text('습관 루틴 관리'),
actions: [
IconButton(
icon: const Icon(Icons.add),
onPressed: () => _showAddHabitBottomSheet(context, ref),
),
 ],
),
body: Padding(
padding: const EdgeInsets.all(AppSpacing.md),
child: Column(
crossAxisAlignment: CrossAxisAlignment.start,
children: [
// Daily Progress Card
_buildProgressCard(completedCount, totalCount, progressRatio),
const SizedBox(height: AppSpacing.md),

// Category Filter Chips
_buildFilterChips(ref, currentFilter),
const SizedBox(height: AppSpacing.md),

// Habit List
Expanded(
child: filteredHabits.isEmpty
? const Center(
child: Text('등록된 습관이 없습니다.', style: AppTypography.captionSm),
)
: ListView.separated(
physics: const BouncingScrollPhysics(),
itemCount: filteredHabits.length,
separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.sm),
itemBuilder: (context, index) {
final habit = filteredHabits[index];
return _buildHabitCard(ref, habit);
},
),
),
],
),
),
floatingActionButton: FloatingActionButton.extended(
onPressed: () => _showAddHabitBottomSheet(context, ref),
backgroundColor: AppColors.primary500,
icon: const Icon(Icons.add, color: Colors.white),
label: Text(
'습관 추가',
style: AppTypography.bodyMd.copyWith(
color: Colors.white,
fontWeight: FontWeight.bold,
),
),
),
);
}

Widget _buildProgressCard(int completed, int total, double ratio) {
return Card(
color: AppColors.primary100,
child: Padding(
padding: const EdgeInsets.all(AppSpacing.md),
child: Column(
crossAxisAlignment: CrossAxisAlignment.start,
children: [
Row(
mainAxisAlignment: MainAxisAlignment.spaceBetween,
children: [
Text('오늘의 달성률', style: AppTypography.titleMd),
Text(
'$completed / $total 완료',
style: AppTypography.bodyMd.copyWith(
color: AppColors.primary500,
fontWeight: FontWeight.bold,
),
),
 ],
),
const SizedBox(height: AppSpacing.sm),
ClipRRect(
borderRadius: AppRadius.borderRadiusFull,
child: LinearProgressIndicator(
value: ratio,
minHeight: 10,
backgroundColor: Colors.white,
color: AppColors.primary500,
),
),
],
),
),
);
}

Widget _buildFilterChips(WidgetRef ref, HabitCategory selectedCategory) {
return SingleChildScrollView(
scrollDirection: Axis.horizontal,
child: Row(
children: [
_chipItem(ref, '전체', HabitCategory.all, selectedCategory),
const SizedBox(width: AppSpacing.xs),
_chipItem(ref, '🌅 아침', HabitCategory.morning, selectedCategory),
const SizedBox(width: AppSpacing.xs),
_chipItem(ref, '☀️ 오후', HabitCategory.afternoon, selectedCategory),
const SizedBox(width: AppSpacing.xs),
_chipItem(ref, '🌙 저녁', HabitCategory.evening, selectedCategory),
 ],
),
);
}

Widget _chipItem(
WidgetRef ref, String label, HabitCategory category, HabitCategory selectedCategory) {
final isSelected = category == selectedCategory;
return ChoiceChip(
label: Text(label),
selected: isSelected,
selectedColor: AppColors.primary500,
backgroundColor: Colors.white,
labelStyle: TextStyle(
color: isSelected ? Colors.white : AppColors.neutral900,
fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
),
onSelected: (_) {
ref.read(habitFilterProvider.notifier).state = category;
},
);
}

Widget _buildHabitCard(WidgetRef ref, HabitRoutineModel habit) {
return Card(
child: ListTile(
contentPadding: const EdgeInsets.symmetric(
horizontal: AppSpacing.md,
vertical: AppSpacing.xs,
),
leading: Checkbox(
value: habit.isCompleted,
activeColor: AppColors.primary500,
shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
onChanged: (_) {
ref.read(habitRoutineProvider.notifier).toggleHabit(habit.id);
},
),
title: Text(
habit.title,
style: AppTypography.bodyMd.copyWith(
decoration: habit.isCompleted ? TextDecoration.lineThrough : null,
color: habit.isCompleted ? AppColors.neutral500 : AppColors.neutral900,
),
),
subtitle: Text(
'🔥 ${habit.streakCount}일 연속 달성 중',
style: AppTypography.captionSm.copyWith(color: AppColors.primary500),
),
),
);
}

void _showAddHabitBottomSheet(BuildContext context, WidgetRef ref) {
final controller = TextEditingController();
String selectedCategory = 'morning';

showModalBottomSheet(
context: context,
isScrollControlled: true,
shape: const RoundedRectangleBorder(
borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
),
builder: (context) {
return StatefulBuilder(
builder: (context, setStateModal) {
return Padding(
padding: EdgeInsets.only(
bottom: MediaQuery.of(context).viewInsets.bottom + AppSpacing.md,
top: AppSpacing.md,
left: AppSpacing.md,
right: AppSpacing.md,
),
child: Column(
mainAxisSize: MainAxisSize.min,
crossAxisAlignment: CrossAxisAlignment.start,
children: [
Text('새 습관 루틴 추가', style: AppTypography.titleMd),
const SizedBox(height: AppSpacing.md),
TextField(
controller: controller,
decoration: const InputDecoration(
hintText: '예: 하루 물 2리터 마시기',
border: OutlineInputBorder(),
),
),
const SizedBox(height: AppSpacing.md),
DropdownButtonFormField<String>(
value: selectedCategory,
items: const [
DropdownMenuItem(value: 'morning', child: Text('🌅 아침 루틴')),
DropdownMenuItem(value: 'afternoon', child: Text('☀️ 오후 루틴')),
DropdownMenuItem(value: 'evening', child: Text('🌙 저녁 루틴')),
 ],
onChanged: (val) {
if (val != null) setStateModal(() => selectedCategory = val);
},
decoration: const InputDecoration(border: OutlineInputBorder()),
),
const SizedBox(height: AppSpacing.lg),
ElevatedButton(
onPressed: () {
if (controller.text.trim().isNotEmpty) {
ref
.read(habitRoutineProvider.notifier)
.addHabit(controller.text.trim(), selectedCategory);
Navigator.pop(context);
}
},
child: const Text('등록하기'),
),
],
),
);
},
);
}
);
}
}