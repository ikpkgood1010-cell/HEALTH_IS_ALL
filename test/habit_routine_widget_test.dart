import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

class HabitTileWidget extends StatefulWidget {
  final String title;
  final bool initialCompleted;

  const HabitTileWidget({
    Key? key,
    required this.title,
    this.initialCompleted = false,
  }) : super(key: key);

  @override
  State<HabitTileWidget> createState() => _HabitTileWidgetState();
}

class _HabitTileWidgetState extends State<HabitTileWidget> {
  late bool _isCompleted;

  @override
  void initState() {
    super.initState();
    _isCompleted = widget.initialCompleted;
  }

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(widget.title),
      trailing: Checkbox(
        value: _isCompleted,
        onChanged: (val) {
          setState(() {
            _isCompleted = val ?? false;
          });
        },
      ),
    );
  }
}

void main() {
  group('HabitTileWidget 위젯 테스트', () {
    testWidgets('체크박스 클릭 시 습관 완료 상태가 전환된다', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: HabitTileWidget(title: '기상 후 물 1컵 마시기'),
          ),
        ),
      );

      expect(find.text('기상 후 물 1컵 마시기'), findsOneWidget);

      final checkboxFinder = find.byType(Checkbox);
      expect(checkboxFinder, findsOneWidget);

      Checkbox checkbox = tester.widget(checkboxFinder);
      expect(checkbox.value, isFalse);

      await tester.tap(checkboxFinder);
      await tester.pump();

      checkbox = tester.widget(checkboxFinder);
      expect(checkbox.value, isTrue);
    });
  });
}