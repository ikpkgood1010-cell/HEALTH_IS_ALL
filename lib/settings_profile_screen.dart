import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app_theme.dart';

/// ============================================================================
/// Settings & Profile Screen Implementation (v1.0)
/// Based on: Component_Catalog.md & Screen_Specification_Master.md
/// ============================================================================

class UserProfileModel {
final String nickname;
final String email;
final int targetCalories;
final int targetWaterMl;
final int targetExerciseMinutes;
final bool pushNotificationsEnabled;
final bool autoSyncEnabled;
final DateTime? lastSyncedAt;

UserProfileModel({
required this.nickname,
required this.email,
required this.targetCalories,
required this.targetWaterMl,
required this.targetExerciseMinutes,
this.pushNotificationsEnabled = true,
this.autoSyncEnabled = true,
this.lastSyncedAt,
});

UserProfileModel copyWith({
String? nickname,
String? email,
int? targetCalories,
int? targetWaterMl,
int? targetExerciseMinutes,
bool? pushNotificationsEnabled,
bool? autoSyncEnabled,
DateTime? lastSyncedAt,
}) {
return UserProfileModel(
nickname: nickname ?? this.nickname,
email: email ?? this.email,
targetCalories: targetCalories ?? this.targetCalories,
targetWaterMl: targetWaterMl ?? this.targetWaterMl,
targetExerciseMinutes: targetExerciseMinutes ?? this.targetExerciseMinutes,
pushNotificationsEnabled: pushNotificationsEnabled ?? this.pushNotificationsEnabled,
autoSyncEnabled: autoSyncEnabled ?? this.autoSyncEnabled,
lastSyncedAt: lastSyncedAt ?? this.lastSyncedAt,
);
}
}

class UserProfileNotifier extends StateNotifier<UserProfileModel> {
UserProfileNotifier()
: super(
UserProfileModel(
nickname: '러너킴',
email: 'runner.kim@example.com',
targetCalories: 2000,
targetWaterMl: 2000,
targetExerciseMinutes: 45,
lastSyncedAt: DateTime.now().subtract(const Duration(minutes: 15)),
),
);

void updateTargets({int? calories, int? water, int? exercise}) {
state = state.copyWith(
targetCalories: calories,
targetWaterMl: water,
targetExerciseMinutes: exercise,
);
}

void toggleNotifications(bool value) {
state = state.copyWith(pushNotificationsEnabled: value);
}

void toggleAutoSync(bool value) {
state = state.copyWith(autoSyncEnabled: value);
}

void triggerManualSync() {
state = state.copyWith(lastSyncedAt: DateTime.now());
}
}

final userProfileProvider =
StateNotifierProvider<UserProfileNotifier, UserProfileModel>((ref) {
return UserProfileNotifier();
});

class SettingsProfileScreen extends ConsumerWidget {
const SettingsProfileScreen({Key? key}) : super(key: key);

@override
Widget build(BuildContext context, WidgetRef ref) {
final profile = ref.watch(userProfileProvider);

return Scaffold(
appBar: AppBar(
title: const Text('마이페이지 & 설정'),
),
body: SingleChildScrollView(
physics: const BouncingScrollPhysics(),
padding: const EdgeInsets.all(AppSpacing.md),
child: Column(
crossAxisAlignment: CrossAxisAlignment.start,
children: [
// User Profile Header Card
_buildProfileHeader(profile),
const SizedBox(height: AppSpacing.lg),

// Daily Target Management
_buildSectionTitle('🎯 일일 목표 설정'),
const SizedBox(height: AppSpacing.xs),
_buildTargetTile(
context,
ref,
icon: Icons.water_drop,
iconColor: Colors.cyan,
title: '목표 수분량',
valueText: '${profile.targetWaterMl} ml',
onTap: () => _showEditTargetDialog(
context,
ref,
title: '목표 수분량 변경',
currentValue: profile.targetWaterMl,
unit: 'ml',
onSave: (val) => ref
.read(userProfileProvider.notifier)
.updateTargets(water: val),
),
),
_buildTargetTile(
context,
ref,
icon: Icons.timer,
iconColor: Colors.green,
title: '목표 운동 시간',
valueText: '${profile.targetExerciseMinutes} 분',
onTap: () => _showEditTargetDialog(
context,
ref,
title: '목표 운동시간 변경',
currentValue: profile.targetExerciseMinutes,
unit: '분',
onSave: (val) => ref
.read(userProfileProvider.notifier)
.updateTargets(exercise: val),
),
),
const SizedBox(height: AppSpacing.lg),

// Notifications & Sync Controls
_buildSectionTitle('🔔 알림 및 동기화'),
const SizedBox(height: AppSpacing.xs),
Card(
child: Column(
children: [
SwitchListTile(
title: const Text('루틴 알림 받기', style: AppTypography.bodyMd),
subtitle: const Text('설정한 루틴 시간에 맞추어 푸시 알림을 전송합니다.',
style: AppTypography.captionSm),
activeColor: AppColors.primary500,
value: profile.pushNotificationsEnabled,
onChanged: (val) {
ref
.read(userProfileProvider.notifier)
.toggleNotifications(val);
},
),
const Divider(height: 1),
SwitchListTile(
title: const Text('네트워크 자동 동기화', style: AppTypography.bodyMd),
subtitle: const Text('와이파이 연결 시 오프라인 기록을 자동 업로드합니다.',
style: AppTypography.captionSm),
activeColor: AppColors.primary500,
value: profile.autoSyncEnabled,
onChanged: (val) {
ref.read(userProfileProvider.notifier).toggleAutoSync(val);
},
),
const Divider(height: 1),
ListTile(
leading: const Icon(Icons.sync, color: AppColors.primary500),
title: const Text('지금 즉시 동기화', style: AppTypography.bodyMd),
subtitle: Text(
profile.lastSyncedAt != null
? '최종 동기화: ${_formatTime(profile.lastSyncedAt!)}'
: '동기화 기록 없음',
style: AppTypography.captionSm,
),
trailing: TextButton(
onPressed: () {
ref.read(userProfileProvider.notifier).triggerManualSync();
ScaffoldMessenger.of(context).showSnackBar(
const SnackBar(content: Text('동기화가 완료되었습니다.')),
);
},
child: const Text('동기화'),
),
),
 ],
),
),
const SizedBox(height: AppSpacing.lg),

// App Meta & Account
_buildSectionTitle('ℹ️ 앱 정보 및 계정'),
const SizedBox(height: AppSpacing.xs),
Card(
child: Column(
children: [
const ListTile(
title: Text('앱 버전', style: AppTypography.bodyMd),
trailing: Text('v1.0.0 (Build 102)', style: AppTypography.captionSm),
),
const Divider(height: 1),
ListTile(
title: const Text('로그아웃',
style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold)),
onTap: () => _showLogoutDialog(context),
),
 ],
),
),
],
),
),
);
}

Widget _buildProfileHeader(UserProfileModel profile) {
return Card(
color: AppColors.primary100,
child: Padding(
padding: const EdgeInsets.all(AppSpacing.md),
child: Row(
children: [
CircleAvatar(
radius: 32,
backgroundColor: AppColors.primary500,
child: Text(
profile.nickname[0],
style: const TextStyle(
fontSize: 24,
color: Colors.white,
fontWeight: FontWeight.bold,
),
),
),
const SizedBox(width: AppSpacing.md),
Expanded(
child: Column(
crossAxisAlignment: CrossAxisAlignment.start,
children: [
Text(profile.nickname, style: AppTypography.titleMd),
const SizedBox(height: 4),
Text(profile.email, style: AppTypography.captionSm),
 ],
),
),
IconButton(
icon: const Icon(Icons.edit_outlined, color: AppColors.primary500),
onPressed: () {},
),
],
),
),
);
}

Widget _buildSectionTitle(String title) {
return Text(title, style: AppTypography.titleMd);
}

Widget _buildTargetTile(
BuildContext context,
WidgetRef ref, {
required IconData icon,
required Color iconColor,
required String title,
required String valueText,
required VoidCallback onTap,
}) {
return Card(
child: ListTile(
leading: CircleAvatar(
backgroundColor: iconColor.withOpacity(0.15),
child: Icon(icon, color: iconColor),
),
title: Text(title, style: AppTypography.bodyMd),
trailing: Row(
mainAxisSize: MainAxisSize.min,
children: [
Text(
valueText,
style: AppTypography.bodyMd.copyWith(
fontWeight: FontWeight.bold,
color: AppColors.primary500,
),
),
const Icon(Icons.chevron_right, color: AppColors.neutral500),
 ],
),
onTap: onTap,
),
);
}

void _showEditTargetDialog(
BuildContext context,
WidgetRef ref, {
required String title,
required int currentValue,
required String unit,
required Function(int) onSave,
}) {
final controller = TextEditingController(text: currentValue.toString());

showDialog(
context: context,
builder: (context) {
return AlertDialog(
title: Text(title),
content: TextField(
controller: controller,
keyboardType: TextInputType.number,
decoration: InputDecoration(
suffixText: unit,
border: const OutlineInputBorder(),
),
),
actions: [
TextButton(
onPressed: () => Navigator.pop(context),
child: const Text('취소'),
),
ElevatedButton(
onPressed: () {
final newValue = int.tryParse(controller.text.trim());
if (newValue != null && newValue > 0) {
onSave(newValue);
Navigator.pop(context);
}
},
child: const Text('저장'),
),
 ],
);
},
);
}

void _showLogoutDialog(BuildContext context) {
showDialog(
context: context,
builder: (context) {
return AlertDialog(
title: const Text('로그아웃'),
content: const Text('정말 로그아웃 하시겠습니까?\n오프라인에 남아있는 기록은 저장됩니다.'),
actions: [
TextButton(
onPressed: () => Navigator.pop(context),
child: const Text('취소'),
),
ElevatedButton(
style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
onPressed: () => Navigator.pop(context),
child: const Text('로그아웃'),
),
 ],
);
},
);
}

String _formatTime(DateTime dt) {
return '${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
}
}