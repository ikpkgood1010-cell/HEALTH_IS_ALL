import 'package:flutter/material.dart';
import 'app_theme.dart';

/// ============================================================================
/// Spirit Interactive Widget (v1.0)
/// Based on: Spirit_Relationship_Progression.md & Component_Catalog.md
/// ============================================================================

enum SpiritMood { energetic, comfort, gentlePush, rest }

class SpiritInteractiveWidget extends StatefulWidget {
final int spiritLevel;
final SpiritMood mood;
final String dialogue;
final Function(int gainedBp)? onTapInteraction;

const SpiritInteractiveWidget({
Key? key,
required this.spiritLevel,
required this.mood,
required this.dialogue,
this.onTapInteraction,
}) : super(key: key);

@override
State<SpiritInteractiveWidget> createState() => _SpiritInteractiveWidgetState();
}

class _SpiritInteractiveWidgetState extends State<SpiritInteractiveWidget>
with SingleTickerProviderStateMixin {
late AnimationController _controller;
late Animation<double> _scaleAnimation;
late String _currentDialogue;
bool _isInteracting = false;

@override
void initState() {
super.initState();
_currentDialogue = widget.dialogue;
_controller = AnimationController(
duration: const Duration(milliseconds: 250),
vsync: this,
);
_scaleAnimation = Tween<double>(begin: 1.0, end: 1.15).animate(
CurvedAnimation(parent: _controller, curve: Curves.easeOutBack),
);
}

@override
void didUpdateWidget(covariant SpiritInteractiveWidget oldWidget) {
super.didUpdateWidget(oldWidget);
if (oldWidget.dialogue != widget.dialogue) {
setState(() {
_currentDialogue = widget.dialogue;
});
}
}

@override
void dispose() {
_controller.dispose();
super.dispose();
}

void _handleTap() async {
if (_isInteracting) return;
setState(() {
_isInteracting = true;
});

// Bounce Scale Animation
await _controller.forward();
await _controller.reverse();

// Interaction Dialogue Feedback
setState(() {
_currentDialogue = _getInteractionDialogue(widget.mood);
_isInteracting = false;
});

// BP (Bond Points) Callback
if (widget.onTapInteraction != null) {
widget.onTapInteraction!(5); // Daily Interaction +5 BP
}
}

String _getInteractionDialogue(SpiritMood mood) {
switch (mood) {
case SpiritMood.energetic:
return "당신과 함께라면 힘이 더 솟아나요! 반짝반짝 ✨";
case SpiritMood.comfort:
return "오늘도 당신 옆에 있을게요. 편안한 마음으로 함께해요 🌿";
case SpiritMood.gentlePush:
return "작은 한 걸음이라도 충분해요! 언제나 당신 편이에요 💪";
case SpiritMood.rest:
return "오늘 밤은 푹 쉬어요. 휴식도 멋진 성장이에요 🌙";
}
}

Color _getMoodAuraColor(SpiritMood mood) {
switch (mood) {
case SpiritMood.energetic:
return AppColors.accentEnergy;
case SpiritMood.comfort:
return AppColors.primary500;
case SpiritMood.gentlePush:
return AppColors.secondary500;
case SpiritMood.rest:
return const Color(0xFF9B59B6);
}
}

IconData _getMoodIcon(SpiritMood mood) {
switch (mood) {
case SpiritMood.energetic:
return Icons.bolt;
case SpiritMood.comfort:
return Icons.favorite;
case SpiritMood.gentlePush:
return Icons.directions_run;
case SpiritMood.rest:
return Icons.bedtime;
}
}

@override
Widget build(BuildContext context) {
final auraColor = _getMoodAuraColor(widget.mood);

return Card(
color: AppColors.primary100,
elevation: 0,
shape: RoundedRectangleBorder(
borderRadius: AppRadius.borderRadiusMd,
),
child: Padding(
padding: const EdgeInsets.all(AppSpacing.md),
child: Column(
children: [
// Top Status Header
Row(
mainAxisAlignment: MainAxisAlignment.spaceBetween,
children: [
Row(
children: [
Icon(_getMoodIcon(widget.mood), color: auraColor, size: 18),
const SizedBox(width: AppSpacing.xs),
Text(
'Lv. ${widget.spiritLevel} 수호 정령',
style: AppTypography.captionSm.copyWith(
fontWeight: FontWeight.bold,
color: AppColors.neutral900,
),
),
 ],
),
Container(
padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
decoration: BoxDecoration(
color: Colors.white,
borderRadius: AppRadius.borderRadiusFull,
),
child: Text(
widget.mood.name.toUpperCase(),
style: AppTypography.captionSm.copyWith(
color: auraColor,
fontWeight: FontWeight.w700,
),
),
),
],
),
const SizedBox(height: AppSpacing.md),

// Interactive Spirit Body Area
GestureDetector(
onTap: _handleTap,
child: ScaleTransition(
scale: _scaleAnimation,
child: Stack(
alignment: Alignment.center,
children: [
// Spirit Glow Effect
AnimatedContainer(
duration: const Duration(milliseconds: 300),
width: 110,
height: 110,
decoration: BoxDecoration(
shape: BoxShape.circle,
color: auraColor.withOpacity(0.25),
boxShadow: [
BoxShadow(
color: auraColor.withOpacity(0.3),
blurRadius: 20,
spreadRadius: 5,
),
 ],
),
),
// Spirit Avatar Center
Container(
width: 85,
height: 85,
decoration: BoxDecoration(
shape: BoxShape.circle,
color: auraColor,
),
child: const Icon(
Icons.auto_awesome,
color: Colors.white,
size: 48,
),
),
],
),
),
),
const SizedBox(height: AppSpacing.md),

// Dynamic Dialogue Bubble
AnimatedSwitcher(
duration: const Duration(milliseconds: 200),
child: Container(
key: ValueKey<String>(_currentDialogue),
width: double.infinity,
padding: const EdgeInsets.all(AppSpacing.md),
decoration: BoxDecoration(
color: Colors.white,
borderRadius: AppRadius.borderRadiusMd,
boxShadow: [
BoxShadow(
color: Colors.black.withOpacity(0.04),
blurRadius: 8,
offset: const Offset(0, 2),
),
 ],
),
child: Text(
'"$_currentDialogue"',
textAlign: TextAlign.center,
style: AppTypography.bodyMd.copyWith(
fontWeight: FontWeight.w600,
color: AppColors.neutral900,
),
),
),
),
],
),
),
);
}
}