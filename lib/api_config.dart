// 조건부 import: 기본값(io)을 먼저 쓰고, dart.library.js_interop이
// 감지되면(즉 웹/Wasm 컴파일 시) web 버전으로 자동 교체된다.
// (js_interop은 package:web이 쓰는 라이브러리로, 구버전에서 흔히 쓰던
// dart.library.html 조건보다 Wasm 컴파일 타깃까지 정확히 포괄한다.)
// 참고: Dart 조건부 import 문법은 "기본 파일을 먼저, 조건 파일을 뒤에"
// 쓰는 순서를 따른다.
import 'api_config_io.dart'
    if (dart.library.js_interop) 'api_config_web.dart' as platform;

/// 앱 전체에서 사용할 기본 API 서버 baseUrl을 결정한다.
///
/// 우선순위:
/// 1. `--dart-define=API_BASE_URL=...` 로 빌드/실행 시점에 명시적으로 준
///    값이 있으면 그것을 최우선으로 사용한다 (로컬 개발, 커스텀 배포 등
///    자동 감지가 맞지 않는 모든 경우의 탈출구).
/// 2. 없으면 플랫폼별 자동 감지 로직(api_config_io.dart / api_config_web.dart)
///    을 사용한다.
String resolveApiBaseUrl() {
  const override = String.fromEnvironment('API_BASE_URL', defaultValue: '');
  if (override.isNotEmpty) {
    return override;
  }
  return platform.resolveDefaultBaseUrl();
}
