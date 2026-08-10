import 'dart:math';

import 'package:hive_flutter/hive_flutter.dart';

/// Keeps one anonymous MVP identity on this device without requiring login.
class AnonymousUserRepository {
  static const _boxName = 'anonymous_user';
  static const _userIdKey = 'user_id';

  Future<String> loadOrCreateUserId() async {
    await Hive.initFlutter();
    final box = await Hive.openBox<String>(_boxName);
    final existing = box.get(_userIdKey);
    if (existing != null && existing.startsWith('anon_')) {
      return existing;
    }

    final random = Random.secure();
    final id =
        'anon_${List.generate(32, (_) => random.nextInt(16).toRadixString(16)).join()}';
    await box.put(_userIdKey, id);
    return id;
  }
}
