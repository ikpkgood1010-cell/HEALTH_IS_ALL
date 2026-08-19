import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart' as riverpod;
import 'mock_data_provider.dart';
import 'api_data_provider.dart';
import 'main_navigation_screen.dart';
import 'anonymous_user_repository.dart';
import 'app_theme.dart';

/// HEALTH IS ALL - Application Entrypoint
///
/// MockDataProvider(로컬 목업, 오프라인/개발용)와 ApiDataProvider(실제
/// 백엔드 서버 연동)를 함께 등록해 둔다. 화면은 필요에 따라 둘 중 하나를
/// Provider.of<...>()로 선택해서 쓰면 되며, main.dart를 다시 건드리지
/// 않아도 화면 단위로 점진적 전환이 가능하다.
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final userId = await AnonymousUserRepository().loadOrCreateUserId();
  runApp(
    riverpod.ProviderScope(
      child: MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => MockDataProvider()),
          ChangeNotifierProvider(
              create: (_) => ApiDataProvider(userId: userId)),
        ],
        child: const HealthIsAllApp(),
      ),
    ),
  );
}

class HealthIsAllApp extends StatelessWidget {
  const HealthIsAllApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'HEALTH IS ALL : 건강이 전부다 !!',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const MainNavigationScreen(),
    );
  }
}
