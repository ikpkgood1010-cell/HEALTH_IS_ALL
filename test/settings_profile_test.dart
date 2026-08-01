import 'package:flutter_test/flutter_test.dart';

class UserProfileModel {
  String nickname;
  int targetCalories;
  int targetWaterMl;
  bool pushNotificationsEnabled;

  UserProfileModel({
    required this.nickname,
    required this.targetCalories,
    required this.targetWaterMl,
    this.pushNotificationsEnabled = true,
  });

  void updateTargetCalories(int newTarget) {
    if (newTarget <= 0) {
      throw ArgumentError('목표 칼로리는 0보다 커야 합니다.');
    }
    targetCalories = newTarget;
  }

  void toggleNotifications() {
    pushNotificationsEnabled = !pushNotificationsEnabled;
  }
}

void main() {
  group('UserProfileModel 단위 테스트', () {
    test('목표 칼로리 변경 기능 검증', () {
      final profile = UserProfileModel(
        nickname: '건강이',
        targetCalories: 2000,
        targetWaterMl: 2000,
      );

      profile.updateTargetCalories(2200);

      expect(profile.targetCalories, equals(2200));
    });

    test('목표 칼로리에 유효하지 않은 값 입력 시 예외가 발생한다', () {
      final profile = UserProfileModel(
        nickname: '건강이',
        targetCalories: 2000,
        targetWaterMl: 2000,
      );

      expect(() => profile.updateTargetCalories(0), throwsArgumentError);
    });

    test('푸시 알림 토글 전환 테스트', () {
      final profile = UserProfileModel(
        nickname: '건강이',
        targetCalories: 2000,
        targetWaterMl: 2000,
        pushNotificationsEnabled: true,
      );

      profile.toggleNotifications();

      expect(profile.pushNotificationsEnabled, isFalse);
    });
  });
}