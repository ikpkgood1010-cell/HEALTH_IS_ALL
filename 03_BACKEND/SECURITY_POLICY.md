# SECURITY_POLICY

## Purpose
본 문서는 인증/인가, 데이터 암호화, API 보안, SQL Injection, XSS, CSRF 예방 및 시크릿 관리 등 백엔드와 앱 전반의 보안 표준을 규정하는 SSOT이다.

## Scope
백엔드 API Gateway, DB 영속성 레이어, 토큰 관리자, Flutter 클라이언트 세션 관리에 적용된다.

## SSOT
시스템 전체 정보보안 및 암호화 알고리즘 규격의 단일 진실 출처이다.

## Security Architecture Standards

### 1. Authentication & Session Management
- **Algorithm**: JWT with RS256 (Private/Public Key Pair).
- **Access Token TTL**: 30분.
- **Refresh Token TTL**: 14일 (DB 내 JTI 단방향 해시 저장 + Refresh Token Rotation 필수).

### 2. Encryption Standards
- **Data at Rest (저장 데이터)**: DB 민감 생체/개인정보는 `AES-256-GCM`으로 암호화.
- **Data in Transit (전송 데이터)**: 모든 HTTP 통신은 `TLS 1.3` 전용 강제.

### 3. API Protection & Rate Limiting
- **Rate Limit Formula**: Token Bucket 알고리즘 적용 (사용자당 분당 최대 120회 요청 제한).
  $$\text{Tokens}_{\text{current}} = \min\left( \text{Capacity}, \; \text{Tokens}_{\text{last}} + \Delta t \times \text{RefillRate} \right)$$
- **Injection Defense**: Spring Data JPA Prepared Statement 사용으로 SQL Injection 완벽 차단.
- **XSS & CSRF**: REST API Stateless 구조 + Content-Security-Policy(CSP) 헤더 적용.

## Runtime Impact
- 외부 공격 및 토큰 탈취 시도 시 피해 범위를 격리하고 데이터 유출 리스크를 근본적으로 차단한다.

## Related Documents
- `03_BACKEND/PRIVACY_DATA_POLICY.md`
- `03_BACKEND/ERROR_HANDLING_STANDARD.md`

## Change History
- v1.0.0 (2026-07-31): Security Policy established.