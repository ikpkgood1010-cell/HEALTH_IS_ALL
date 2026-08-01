# PATCH_010_SANDBOX_REPORT

## 실제 확인 결과
- 업로드된 프로젝트는 문서/설계 대비 실제 런타임 연결이 불완전한 상태였음.
- `README.md`에도 백엔드와 Flutter 앱이 아직 연결되지 않았고 일부는 목업 기반이라고 명시되어 있었음.
- 다만 코드 기준으로는 `HomeScreen`, `DietScreen`, `WorkoutScreen`, `SpiritScreen`은 `ApiDataProvider`를 통해 FastAPI 백엔드와 연결되어 있었음.
- 반면 `ShopScreen`은 `currentExp: 120` 하드코딩을 사용하고 있었고, `HabitRoutineScreen`은 실제로 Dart 문법이 깨져 있어 앱 컴파일을 막을 가능성이 높았음.

## 이번 수정 사항
1. `lib/habit_routine_screen.dart`
   - 깨진 문자열(`'$completed / $total 완료'` 부분) 복구
   - `_chipItem`, `_buildHabitCard` 이름 불일치 수정
   - `ChoiceChip.onSelected`, `Checkbox.onChanged` 콜백 시그니처 수정
2. `lib/shop_screen.dart`
   - 하드코딩된 Exp 주입 제거
   - `ApiDataProvider`의 실제 `currentExp`를 구독하도록 수정
3. `lib/main_navigation_screen.dart`
   - 변경된 `ShopScreen()` 생성자에 맞게 연결 수정

## 이 환경에서 실제 검증한 것
- Python 의존성 설치 완료
- `uvicorn backend.main:app` 기동 및 `/healthz` 200 OK 확인
- `pytest -q` 실행 결과: `9 passed`

## 이 환경에서 검증 불가한 것
- Flutter SDK가 없어 `flutter pub get`, `flutter analyze`, `flutter run -d chrome`, `flutter build web`은 실행하지 못함.
- 따라서 최종 Flutter 런타임 검증은 사용자 로컬 Flutter 환경에서 반드시 다시 확인해야 함.

## 로컬에서 바로 확인할 것
1. 백엔드
   - `python -m venv venv`
   - `venv\\Scripts\\activate` (Windows)
   - `pip install -r requirements.txt`
   - `uvicorn backend.main:app --reload`
2. Flutter
   - `flutter pub get`
   - `flutter analyze`
   - `flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000`

## 참고
- 사용자가 겪은 기존 `flutter run -d chrome`의 shader compiler 오류는 로컬 Windows Flutter/셰이더 컴파일 환경 이슈일 가능성이 있어, 이번 코드 패치와 별개로 재확인이 필요함.
