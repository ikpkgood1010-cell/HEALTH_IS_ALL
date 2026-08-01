import 'package:flutter/material.dart';

/// HEALTH IS ALL - '건강이' Interactive Character & Exp Bar Widget
/// Dual-Excellence: 생동감 있는 게임적 애니메이션 + 정밀한 Exp 진행도 시각화
class HealthIWidget extends StatefulWidget {
  final int currentExp;
  final int level;
  final String emotionState;
  final String dialogue;
  final VoidCallback onTapHealthI;

  const HealthIWidget({
    Key? key,
    required this.currentExp,
    required this.level,
    required this.emotionState,
    required this.dialogue,
    required this.onTapHealthI,
  }) : super(key: key);

  @override
  State<HealthIWidget> createState() => _HealthIWidgetState();
}

class _HealthIWidgetState extends State<HealthIWidget> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);

    _scaleAnimation = Tween<double>(begin: 0.96, end: 1.04).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final int maxExpForLevel = widget.level * 300;
    final double expRatio = (widget.currentExp / maxExpForLevel).clamp(0.0, 1.0);

    return Container(
      padding: const EdgeInsets.all(20.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.purple.withOpacity(0.08),
            blurRadius: 16,
            offset: const Offset(0, 4),
          ),
        ],
        border: Border.all(color: Colors.purple.shade100, width: 1.5),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.purple.shade600,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  'Lv. ${widget.level}',
                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.green.shade50,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  widget.emotionState,
                  style: TextStyle(color: Colors.green.shade800, fontWeight: FontWeight.bold, fontSize: 12),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          GestureDetector(
            onTap: widget.onTapHealthI,
            child: ScaleTransition(
              scale: _scaleAnimation,
              child: Container(
                width: 110,
                height: 110,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: LinearGradient(
                    colors: [Colors.lightGreen.shade300, Colors.teal.shade300],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.green.withOpacity(0.25),
                      blurRadius: 12,
                      offset: const Offset(0, 6),
                    ),
                  ],
                ),
                child: const Icon(
                  Icons.sentiment_very_satisfied_rounded,
                  size: 70,
                  color: Colors.white,
                ),
              ),
            ),
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            decoration: BoxDecoration(
              color: Colors.grey.shade100,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Text(
              '"${widget.dialogue}"',
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.black87, fontSize: 13, fontStyle: FontStyle.italic),
            ),
          ),
          const SizedBox(height: 18),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    '성장 Exp',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.purple),
                  ),
                  Text(
                    '${widget.currentExp} / $maxExpForLevel Exp',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey.shade700),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: LinearProgressIndicator(
                  value: expRatio,
                  minHeight: 10,
                  backgroundColor: Colors.purple.shade50,
                  valueColor: AlwaysStoppedAnimation<Color>(Colors.purple.shade400),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
