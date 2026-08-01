import 'package:web/web.dart' as web;

/// 웹 환경의 기본 API 서버 주소를 결정한다.
///
/// package:web(dart:js_interop 기반, Wasm 컴파일 호환)을 사용해 사용자가
/// 접속한 브라우저 주소(origin)를 그대로 API 서버 주소로 삼는다. deploy/
/// 아래 nginx 설정이 프론트엔드와 백엔드를 같은 오리진에서 `/api` 경로로
/// 프록시하도록 구성되어 있으므로, 배포 후 코드 수정 없이 그대로 동작한다.
/// (구버전 dart:html은 deprecated이며 Wasm 컴파일을 지원하지 않아 사용하지
/// 않았다.)
///
/// - 로컬 개발(flutter run -d chrome 등)에서는 보통 프론트가
///   http://localhost:PORT 로 뜨고 백엔드는 http://localhost:8000 이므로
///   포트가 다르면 origin을 그대로 쓰면 안 된다. 이 경우
///   --dart-define=API_BASE_URL=http://localhost:8000 로 오버라이드해서
///   실행하는 것을 권장한다 (api_config.dart 참고).
/// - 실제 배포(같은 오리진 + /api 프록시) 환경에서는 origin 그대로 사용하고
///   api_client.dart가 자동으로 경로 앞에 baseUrl을 붙인다.
String resolveDefaultBaseUrl() {
  final origin = web.window.location.origin;
  if (origin.isEmpty) {
    return 'http://localhost:8000';
  }
  return origin;
}
