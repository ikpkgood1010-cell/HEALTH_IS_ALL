import 'package:flutter/material.dart';

import 'detailed_health_record_screen.dart';

class WorkoutScreen extends StatelessWidget {
  const WorkoutScreen({super.key});

  @override
  Widget build(BuildContext context) =>
      const DetailedHealthRecordScreen(isMeal: false);
}
