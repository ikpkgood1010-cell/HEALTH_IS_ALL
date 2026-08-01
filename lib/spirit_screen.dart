import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'api_data_provider.dart';
import 'spirit_evolution_widget.dart';
import 'spirit_interactive_widget.dart';

/// HEALTH IS ALL - 정령(스피릿) 화면
///
/// 이전 세션들에서 만들어졌지만 어디에도 연결되지 않고 있던
/// `SpiritEvolutionWidget`(4대 속성/진화 단계 표시)과
/// `SpiritInteractiveWidget`(터치 미니게임형 교감 위젯)을
/// 하나의 화면으로 묶어 홈 화면에서 진입할 수 있도록 연결했다.
///
/// 교감 포인트(BP)는 현재 서버 API가 없어 화면 안에서만 누적되는
/// 로컬 상태다. 추후 백엔드에 `/spirit/bond` 같은 엔드포인트가 생기면
/// ApiDataProvider를 통해 실제 저장하도록 교체하면 된다.
class SpiritScreen extends StatefulWidget {
  const SpiritScreen({Key? key}) : super(key: key);

  @override
  State<SpiritScreen> createState() => _SpiritScreenState();
}

class _SpiritScreenState extends State<SpiritScreen> {
  int _bondPoints = 0;

  SpiritMood get _mood {
    // 아주 단순한 규칙: 연속 기록일이 있으면 활기차게, 없으면 다정하게 응원.
    final streak = context.read<ApiDataProvider>().streakDays;
    if (streak >= 3) return SpiritMood.energetic;
    if (streak >= 1) return SpiritMood.comfort;
    return SpiritMood.gentlePush;
  }

  void _onBondGained(int gained) {
    setState(() {
      _bondPoints += gained;
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<ApiDataProvider>();

    return Scaffold(
      backgroundColor: const Color(0xFFF7F9FC),
      appBar: AppBar(
        title: const Text(
          '나의 정령',
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.black87),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black87),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(18.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(14),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.03),
                    blurRadius: 8,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Row(
                children: [
                  const Icon(Icons.favorite, color: Colors.pinkAccent, size: 18),
                  const SizedBox(width: 8),
                  Text(
                    '오늘 교감 포인트: $_bondPoints BP',
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            SpiritInteractiveWidget(
              spiritLevel: provider.level,
              mood: _mood,
              dialogue: provider.dialogue.isNotEmpty
                  ? provider.dialogue
                  : '오늘도 함께해줘서 고마워요!',
              onTapInteraction: _onBondGained,
            ),
            const SizedBox(height: 20),
            const Text(
              '정령의 속성 균형',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            const SpiritEvolutionWidget(),
          ],
        ),
      ),
    );
  }
}
