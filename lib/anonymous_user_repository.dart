import 'dart:math';

import 'package:hive_flutter/hive_flutter.dart';

/// Keeps one anonymous MVP identity on this device without requiring login.
class AnonymousUserRepository {
  static const _boxName = 'anonymous_user';
  static const _userIdKey = 'user_id';
  static const maxUserIdLength = 36;

  Future<String> loadOrCreateUserId() async {
    await Hive.initFlutter();
    final box = await Hive.openBox<String>(_boxName);
    final existing = box.get(_userIdKey);
    if (existing != null && existing.startsWith('anon_')) {
      if (existing.length <= maxUserIdLength) return existing;
      final normalized = existing.substring(0, maxUserIdLength);
      await box.put(_userIdKey, normalized);
      return normalized;
    }

    final id = createAnonymousUserId(Random.secure());
    await box.put(_userIdKey, id);
    return id;
  }
}

String createAnonymousUserId(Random random) {
  const prefix = 'anon_';
  final randomLength = AnonymousUserRepository.maxUserIdLength - prefix.length;
  return '$prefix${List.generate(randomLength, (_) => random.nextInt(16).toRadixString(16)).join()}';
}
