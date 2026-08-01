# 웹 앱 배포 가이드 (PWA)

> 이 문서는 "스토어 심사 없이, 브라우저로 접속해서 앱처럼 쓸 수 있게
> 배포"하는 것이 목표인 경우를 위한 가이드다. APK를 만들어 웹사이트에서
> 다운로드하게 하는 방식이 아니라, **진짜 웹앱(PWA)**으로 만드는 것을
> 전제로 한다. 이유는 아래 "왜 APK 직접배포 대신 PWA인가" 참고.

## 왜 APK 직접배포 대신 PWA인가

| | 스토어 배포 | APK 직접배포 (웹에 올려서 다운로드) | 웹앱/PWA (이 가이드) |
|---|---|---|---|
| 설치 과정 | 스토어 앱 원클릭 | "출처를 알 수 없는 앱" 허용 필요, 보안 경고 노출 | 브라우저 접속만 하면 됨, "홈 화면에 추가"로 앱처럼 사용 가능 |
| 업데이트 | 자동 | **자동 안 됨** — 새 APK를 사용자가 매번 재다운로드/재설치해야 함 | **자동** — 서버 배포만 하면 사용자는 새로고침만으로 최신 버전 |
| 신뢰도 | 높음 | 낮음(설치 시 경고) | 브라우저 정상 사이트와 동일 |
| iOS 대응 | 별도 App Store 심사 필요 | 사실상 불가 (iOS는 APK 설치 자체가 안 됨) | 가능 (Safari에서도 PWA 동작) |

즉 "업데이트가 자동으로 적용되는, 스토어 없는 배포"가 목표라면 PWA가
정답에 가깝다. 이 프로젝트는 이미 Flutter로 작성되어 있고 Flutter는
web 빌드를 공식 지원하므로, 코드를 거의 새로 짤 필요 없이 같은
코드베이스로 웹 버전을 만들 수 있다.

## 배포 아키텍처

```
사용자 브라우저
      │
      ▼
[nginx : 80/443]  ← Flutter web 빌드 결과(정적 파일) 서빙
      │
      ├── "/"       → index.html 등 정적 파일
      └── "/api/*"  → 프록시 → [FastAPI : 8000] → [Postgres]
```

프론트엔드와 백엔드가 **같은 도메인(같은 오리진)** 에서 서빙되므로
브라우저의 CORS 제약을 아예 신경 쓸 필요가 없고, 앱 코드에서 서버
주소를 하드코딩할 필요도 없다 (`lib/api_config_web.dart`가 현재 접속
주소를 그대로 API 주소로 사용한다).

## 로컬에서 미리 확인하기

Flutter SDK가 설치된 PC에서:

```bash
# 프로젝트 루트에서
flutter pub get
flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000
```

이때 백엔드도 별도 터미널에서 함께 띄워야 한다:

```bash
uvicorn backend.main:app --reload
```

`--dart-define=API_BASE_URL=...`을 준 이유: 로컬 개발 시 프론트(예:
`localhost:5000`)와 백엔드(`localhost:8000`) 포트가 다르기 때문에,
자동 감지(origin 그대로 사용)가 아니라 명시적으로 백엔드 주소를
지정해줘야 한다. 실제 배포(같은 오리진) 환경에서는 이 옵션이 필요 없다.

## 실제 서버에 배포하기 (Docker)

서버(클라우드 VM 등)에 Docker와 Docker Compose가 설치되어 있어야 한다.

```bash
git clone <이 저장소>
cd HEALTH_IS_ALL_PATCH_008_COMPLETED_FINAL
docker compose -f deploy/docker-compose.web.yml up --build -d
```

- 접속: `http://<서버 IP 또는 도메인>`
- 내부적으로 `web`(nginx+Flutter), `backend`(FastAPI), `db`(Postgres)
  3개 컨테이너가 뜬다.
- HTTPS가 필요하면(실제 서비스라면 필수) `deploy/nginx.conf` 앞단에
  Let's Encrypt 인증서를 붙인 별도 nginx/Caddy를 두거나, Cloudflare
  같은 서비스의 프록시를 이용하는 것을 권장한다 (이 저장소는 HTTP까지만
  기본 제공).

## 사용자에게 "앱처럼" 쓰게 하려면 — 홈 화면에 추가

스토어 없이도 아래 방법으로 사용자 폰 화면에 아이콘을 만들 수 있고,
이후 실행하면 주소창 없이 앱처럼 뜬다 (PWA의 "홈 화면에 추가" 기능).

- **안드로이드(크롬)**: 사이트 접속 → 우측 상단 메뉴 → "홈 화면에 추가"
- **iOS(사파리)**: 사이트 접속 → 공유 버튼 → "홈 화면에 추가"

이 기능이 제대로 동작하려면 `web/manifest.json`과 아이콘 파일들이
채워져 있어야 한다 (`web/icons/README.md` 참고 — 현재 아이콘 실제
이미지 파일은 비어 있어 채워 넣는 작업이 필요하다).

## 업데이트 배포 방법

새 기능을 추가하고 서버에서 아래만 다시 실행하면, 사용자는 **아무것도
설치하지 않아도** 다음 접속(또는 새로고침) 시 최신 버전을 받는다.

```bash
git pull
docker compose -f deploy/docker-compose.web.yml up --build -d
```

## 남은 작업 (다음 세션에서 처리 필요)

1. `web/icons/` 안의 실제 PNG 아이콘 4종 + `web/favicon.png` 채우기
   (README 참고).
2. 실제 서버/도메인 확보 후 HTTPS 적용.
3. Flutter SDK가 설치된 환경에서 `flutter pub get` / `flutter analyze` /
   `flutter build web` 실제 실행 검증 (이 작업 환경은 Flutter SDK와
   네트워크가 없어 정적 검증까지만 수행했다).
