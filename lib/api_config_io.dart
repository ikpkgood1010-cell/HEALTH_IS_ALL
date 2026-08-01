import 'dart:io' show Platform;

/// 비웹(모바일/데스크톱) 환경의 기본 API 서버 주소를 결정한다.
///
/// - Android 에뮬레이터: 10.0.2.2 가 호스트 PC의 localhost를 가리킨다.
/// - iOS 시뮬레이터 / 데스크톱(Windows/macOS/Linux): localhost 사용 가능.
/// - 실기기(Android/iOS) 테스트 시: 같은 네트워크의 PC IP로 직접 교체 필요
///   (기기에서는 자기 자신의 localhost를 가리키게 되어 PC의 localhost에
///   닿을 수 없기 때문. 이 경우 --dart-define=API_BASE_URL=http://<PC IP>:8000
///   형태로 실행 시점에 오버라이드하는 것을 권장한다).
String resolveDefaultBaseUrl() {
  try {
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000';
    }
  } catch (_) {
    // Platform 사용이 불가능한 특수 환경(테스트 등)에서는 무시하고 폴백한다.
  }
  return 'http://localhost:8000';
}
