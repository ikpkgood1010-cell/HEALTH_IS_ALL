import 'package:flutter/material.dart';

import 'detailed_health_record_screen.dart';

class DietScreen extends StatelessWidget {
  const DietScreen({super.key});

  @override
  Widget build(BuildContext context) =>
      const DetailedHealthRecordScreen(isMeal: true);
}
