# WP-0001 — Repository Security & Hygiene Bootstrap
Version: v1.0 FINAL
Project: HEALTH_IS_ALL
Repository: `ikpkgood1010-cell/HEALTH_IS_ALL`
Baseline branch: `main`

---

## 1. 작업 목적

Public Repository를 실제 개발에 사용하기 전에 보안 정보와 생성물의 상태를 점검하고,
이후 Codex가 안전하게 작업할 수 있는 최소 Repository 규칙을 확정한다.

이 WP는 기능 개발 WP가 아니다.

**기존 기능 코드, DB migration, 기획 문서를 임의로 삭제하거나 재구성하지 않는다.**

---

## 2. 작업 범위

### 포함

1. Secret / Credential 검사
2. `.env` 및 환경설정 파일 검사
3. Generated Artifact 검사
4. `.gitignore` 검사 및 필요한 최소 보완
5. Git tracked file 상태 점검
6. Repository 작업 규칙 문서화
7. Bootstrap 완료 판정

### 제외

- Flutter 기능 수정
- FastAPI 기능 수정
- DB schema 변경
- API contract 변경
- Navigation 변경
- 기존 legacy 폴더 삭제
- 대규모 directory migration
- dependency upgrade

---

## 3. 기준 Repository 구조

현재 실제 runtime을 기준으로 한다.

```text
/lib                 Flutter runtime
/backend             FastAPI runtime
/02_DATABASE         DB migration / schema evidence
/test                Flutter/Dart tests
/tests               backend/other tests
/scripts              validation/automation
/00_PROJECT          project planning evidence
/01_ARCHITECTURE     architecture evidence
/07_PRODUCT          product evidence
```

`apps/mobile/`, `packages/domain/` 등 RTM v0.3의 목표 경로를 이 WP에서 생성하지 않는다.

---

# 4. 작업 순서

## Step 1 — Secret Scan

다음 패턴을 검사한다.

```text
.env
.env.*
*.pem
*.key
*.p12
credentials
credential
secret
api_key
apikey
access_token
refresh_token
private_key
password
```

### 판정

- 실제 비밀값 발견 → **FAIL**
- 문서 예시/placeholder만 존재 → PASS
- 판단 불가 → REVIEW

### 절대 하지 말 것

발견된 secret을 Codex 작업 로그, README, Issue, commit message에 복사하지 않는다.

---

## Step 2 — Git History Scan

현재 working tree뿐 아니라 Git history에도 민감정보가 있었는지 확인한다.

### 판정

- 현재 파일에 secret → FAIL
- 과거 commit에 실제 secret → SECURITY REVIEW 필요
- placeholder/example만 존재 → PASS

실제 secret이 과거 history에 있었다면 단순 파일 삭제로 완료 처리하지 않는다.

---

## Step 3 — Generated Artifact 검사

다음 유형을 확인한다.

```text
.dart_tool/
build/
.pytest_cache/
__pycache__/
*.pyc
coverage/
.DS_Store
*.log
```

특히 현재 Repository에서 확인된 `.dart_tool` 및 Python `__pycache__`는
generated artifact 후보로 취급한다.

### 원칙

- 즉시 삭제하지 않는다.
- 현재 Git tracked 상태를 먼저 확인한다.
- source와 generated artifact를 구분한다.
- 제거가 필요한 경우 별도의 hygiene 변경으로 처리한다.

---

## Step 4 — `.gitignore`

현재 `.gitignore`를 먼저 확인한다.

필요한 경우 최소한 다음 범주를 차단한다.

```text
.env
.env.*
!.env.example

.dart_tool/
build/
.pytest_cache/
__pycache__/
*.pyc
coverage/
.DS_Store
```

단, 기존 프로젝트의 의도적인 예외 규칙은 덮어쓰지 않는다.

---

## Step 5 — Repository 변경 제한

WP-0001에서 허용되는 변경:

```text
.gitignore
docs/REPOSITORY_SECURITY.md
docs/REPOSITORY_RULES.md
```

보안 문제 해결에 직접 필요한 파일 외에는 수정하지 않는다.

---

# 5. Codex 실행 명령서

Codex에게 다음 작업 원칙을 전달한다.

```text
You are working on the existing HEALTH_IS_ALL repository.

DO NOT rewrite the repository.

DO NOT delete existing source code.
DO NOT delete database migrations.
DO NOT rename unrelated directories.
DO NOT create apps/mobile or packages/*.
DO NOT modify Flutter screens, FastAPI endpoints, or DB schema in WP-0001.

First inspect the repository and report:
1. tracked secrets
2. suspicious credential files
3. generated artifacts
4. current .gitignore
5. relevant Git history findings

Only after inspection, make the minimum hygiene changes required by this WP.

Every changed file must be listed.
Every deletion must be explicitly justified.

Do not expose secret values in output.
```

---

# 6. 산출물

WP-0001 완료 후 반드시 다음이 존재해야 한다.

```text
docs/
├── REPOSITORY_SECURITY.md
└── REPOSITORY_RULES.md
```

## REPOSITORY_SECURITY.md

반드시 기록:

```text
검사일
검사 대상
Secret scan 결과
Git history 결과
Generated artifact 결과
.gitignore 결과
조치 사항
잔여 위험
최종 판정
```

Secret의 실제 값은 기록하지 않는다.

## REPOSITORY_RULES.md

반드시 기록:

```text
Canonical runtime
허용 변경 범위
금지 변경
DB migration 보호 규칙
API contract 보호 규칙
Codex 작업 규칙
Branch/PR 규칙
Test 규칙
```

---

# 7. Acceptance Criteria

### AC-001 Secret

실제 credential/API key/private key가 working tree에 남아 있지 않다.

### AC-002 History

Git history에서 실제 secret 노출 여부를 확인했다.

### AC-003 Generated

`.dart_tool`, `__pycache__` 등 generated artifact의 tracked 여부가 확인됐다.

### AC-004 Gitignore

필요한 generated/secret 패턴이 `.gitignore`에 정의되어 있다.

### AC-005 Source Protection

기존 `/lib`, `/backend`, `/02_DATABASE` 기능 코드가 WP-0001 때문에 변경되지 않았다.

### AC-006 Documentation

`REPOSITORY_SECURITY.md`와 `REPOSITORY_RULES.md`가 생성되었다.

### AC-007 Auditability

변경 파일 목록과 변경 이유가 확인 가능하다.

### AC-008 No Greenfield Rewrite

`apps/mobile/`, `packages/domain/` 등의 신규 구조가 WP-0001 때문에 생성되지 않았다.

### AC-009 Test

WP-0001의 변경은 Repository hygiene/security 범위에 한정된다.

### AC-010 Gate

AC-001~AC-009가 모두 PASS여야 WP-0001을 완료 처리한다.

---

# 8. 완료 상태

```text
WP-0001
Status: READY FOR CODEX

Prerequisite:
- RTM v0.4 completed
- Bootstrap design completed

Next:
- Codex execution
- Security/Hygiene report
- Review
- WP-0002
```

---

# 9. 실패 처리

다음 중 하나라도 발생하면 WP-0001을 완료 처리하지 않는다.

```text
FAIL
├─ 실제 secret 발견
├─ Git history의 실제 secret 노출 확인
├─ .gitignore 불명확
├─ 기존 source가 hygiene 작업으로 변경됨
├─ DB migration 변경 발생
└─ unrelated file 대량 변경
```

이 경우:

```text
WP-0001
→ BLOCKED / SECURITY REVIEW
→ 원인 수정
→ 재검증
```

순서로 진행한다.

---

# 10. Definition of Done

다음 조건을 모두 만족하면 WP-0001 완료다.

```text
[PASS] Secret scan
[PASS] Git history scan
[PASS] Generated artifact audit
[PASS] .gitignore review
[PASS] Security report
[PASS] Repository rules
[PASS] No unrelated source changes
[PASS] No DB migration changes
[PASS] No API changes
[PASS] No feature changes
```

그 다음에만 WP-0002를 시작한다.
