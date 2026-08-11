import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:health_is_all/anonymous_user_repository.dart';

void main() {
  test('익명 사용자 ID는 DB 계약인 36자를 넘지 않는다', () {
    final userId = createAnonymousUserId(Random(20260811));

    expect(userId, startsWith('anon_'));
    expect(userId.length, AnonymousUserRepository.maxUserIdLength);
    expect(userId, matches(RegExp(r'^anon_[0-9a-f]{31}$')));
  });
}
