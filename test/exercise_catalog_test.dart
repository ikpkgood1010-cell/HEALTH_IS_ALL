import 'package:flutter_test/flutter_test.dart';
import 'package:health_is_all/exercise_catalog.dart';

void main() {
  test('운동 카탈로그는 중복 없는 27개 표준 코드를 제공한다', () {
    expect(exerciseCatalog, hasLength(27));
    expect(exerciseCatalog.map((item) => item.code).toSet(), hasLength(27));
  });

  test('운동마다 권장 강도와 대분류가 있다', () {
    for (final exercise in exerciseCatalog) {
      expect(ExerciseCategoryGroup.values, contains(exercise.group));
      expect(IntensityLevel.values, contains(exercise.recommendedIntensity));
    }
  });
}
