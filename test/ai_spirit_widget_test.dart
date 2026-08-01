import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

class AISpiritCardWidget extends StatelessWidget {
  final String spiritName;
  final String dialogue;
  final String mood;

  const AISpiritCardWidget({
    Key? key,
    required this.spiritName,
    required this.dialogue,
    required this.mood,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.all(16.0),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                const Icon(Icons.auto_awesome, color: Colors.amber),
                const SizedBox(width: 8),
                Text(
                  spiritName,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                const Spacer(),
                Chip(label: Text(mood)),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              dialogue,
              style: const TextStyle(fontSize: 14),
            ),
          ],
        ),
      ),
    );
  }
}

void main() {
  group('AISpiritCardWidget 테스트', () {
    testWidgets('정령 이름, 대사, 기분 태그가 정확히 화면에 표시된다', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: AISpiritCardWidget(
              spiritName: '다정한 절친 정령',
              dialogue: '오늘도 멋지게 시작해 볼까요?',
              mood: 'Energetic',
            ),
          ),
        ),
      );

      expect(find.text('다정한 절친 정령'), findsOneWidget);
      expect(find.text('오늘도 멋지게 시작해 볼까요?'), findsOneWidget);
      expect(find.text('Energetic'), findsOneWidget);
    });
  });
}